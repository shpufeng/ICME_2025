
Trainning and testing Command For reproducing experiment results:
Basemodel:
nohup python main.py --title BaseModel --model BaseModel --workers 16 --gpu-ids 5 --max-ep 2000000 --images-file-name res_global_feature.hdf5  --test-after-train

DAT:
nohup python main.py --title DAT --model DAT --workers 16 --gpu-ids 6 --max-ep 2000000 --log-dir runs/RL_train --save-model-dir trained_models/RL_train --pretrained-trans trained_models/pretrain/checkpoint0004.pth --images-file-name res_global_feature.hdf5 --test-after-train 

IOM:
python main.py --title IOM --model IOM --workers 1 --gpu-ids 0  --max-ep 2000000 --log-dir runs/RL_train --save-model-dir trained_models/RL_train --pretrained-trans trained_models/pretrain/checkpointIOM.pth --images-file-name res_global_feature.hdf5 


Our Method:
python main.py --title TSRM --model TSRM --workers 14 --gpu-id 0 --max-ep 1500000 --test-after-train