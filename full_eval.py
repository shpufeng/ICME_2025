from __future__ import print_function, division
import os
import json
import time

from utils import command_parser
from utils.class_finder import model_class, agent_class
from main_eval import main_eval
from tqdm import tqdm
from tabulate import tabulate

from tensorboardX import SummaryWriter

os.environ["OMP_NUM_THREADS"] = "1"
os.environ['CUDA_VISIBLE_DEVICES']="0,1,2,3,4,5,6,7,8,9"

def full_eval(args=None):
    if args is None:
        args = command_parser.parse_arguments()

    create_shared_model = model_class(args.model)
    init_agent = agent_class(args.agent_type)

    args.phase = 'eval'
    args.episode_type = 'TestValEpisode'
    args.test_or_val = 'val'
    file_name=args.model+'_'+str(args.large_K)+'_'+'_'+str(args.dij_K)+'_'+str(args.detect_thresh)
    args.results_json=file_name+'.json'
    start_time = time.time()
    local_start_time_str = time.strftime(
        '%Y_%m_%d_%H_%M_%S', time.localtime(start_time)
    )

    tb_log_dir = args.log_dir + "/" + args.title + '_' + args.phase + '_' + local_start_time_str
    log_writer = SummaryWriter(log_dir=tb_log_dir)

    # Get all valid saved_models for the given title and sort by train_ep.
    checkpoints = [(f, f.split("_")) for f in os.listdir(args.save_model_dir)]
    checkpoints = [
        (f, int(s[-7]))
        for (f, s) in checkpoints
        if len(s) >= 4 and f.startswith(args.title) and int(s[-7]) >= args.test_start_from
    ]
    checkpoints.sort(key=lambda x: x[1])
    
    best_model_on_val = None
    best_performance_on_val = 0.0
    for (f, train_ep) in tqdm(checkpoints, desc="Checkpoints."):
        # break

        model = os.path.join(args.save_model_dir, f)
        print(model)
          
        args.load_model = model
        args.present_model =f
        args.test_or_val = "val"
        
  
        main_eval(args, create_shared_model, init_agent,last=False)

        # check if best on val.
        with open(args.results_json, "r") as f:
            results = json.load(f)

        if results["success"] > best_performance_on_val:
            best_model_on_val = model
            best_performance_on_val = results["success"]

        log_writer.add_scalar("val/success", results["success"], train_ep)
        log_writer.add_scalar("val/spl", results["spl"], train_ep)
    
    args.test_or_val = "test"
    args.load_model = best_model_on_val
   
    main_eval(args, create_shared_model, init_agent,last=True)

    with open(args.results_json, "r") as f:
        results = json.load(f)

    print(
        tabulate(
            [
                ["SPL >= 1:", results["GreaterThan/1/spl"]],
                ["Success >= 1:", results["GreaterThan/1/success"]],
                ["SPL >= 5:", results["GreaterThan/5/spl"]],
                ["Success >= 5:", results["GreaterThan/5/success"]],
            ],
            headers=["Metric", "Result"],
            tablefmt="orgtbl",
        )
    )

    print("Best model:", args.load_model)


if __name__ == "__main__":
    full_eval()