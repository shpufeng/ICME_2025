import pickle,json,os
from networkx.algorithms.shortest_paths.weighted import multi_source_dijkstra as multi_dij
from networkx.algorithms.shortest_paths import shortest_path
from networkx.exception import NetworkXNoPath
from networkx.algorithms.components import number_strongly_connected_components,is_strongly_connected
import networkx
os.environ['CUDA_VISIBLE_DEVICES']='9'
from ai2thor.controller import Controller
kitchens = [f"FloorPlan{i}" for i in range(1, 31)]
living_rooms = [f"FloorPlan{200 + i}" for i in range(1, 31)]
bedrooms = [f"FloorPlan{300 + i}" for i in range(1, 31)]
bathrooms = [f"FloorPlan{400 + i}" for i in range(1, 31)]
scenes=kitchens+living_rooms+bedrooms+bathrooms
task_type='test'
data_dir='/home/fengsp/i-THORdata/'
controller = Controller(scene="FloorPlan26",platform="CloudRendering")
TARGET_CLASSES = [
        'AlarmClock', 'Book', 'Bowl', 'CellPhone', 'Chair', 'CoffeeMachine', 'DeskLamp', 'FloorLamp',
        'Fridge', 'GarbageCan', 'Kettle', 'Laptop', 'LightSwitch', 'Microwave', 'Pan', 'Plate', 'Pot',
        'RemoteControl', 'Sink', 'StoveBurner', 'Television', 'Toaster',
]

# scenes=['FloorPlan325']
all_objects={classes:[] for classes in TARGET_CLASSES}
for room in scenes:
    print(room)
    last_event=controller.reset(scene=room)
    object_metadatas=last_event.metadata["objects"]
    for object_info in object_metadatas:
        object_id=object_info['objectId']
        object_type=object_id.split("|")[0]
        if object_type in TARGET_CLASSES:
            all_objects[object_type].append(object_info['axisAlignedBoundingBox']['size'])

def get_size(goal_obj):
    x=goal_obj['x']
    y=goal_obj['y']
    z=goal_obj['z']
    return x*y+x*z+y*z
def average_size(goals):
    cum=0
    for obj in goals:
        cum+=get_size(obj)
    return cum/len(goals)
goal_avg_size={}
for goal_type in TARGET_CLASSES:
    goal_avg_size[goal_type]=average_size(all_objects[goal_type])

with open('goal_sizes.json','w') as f:
    json.dump(goal_avg_size,f)

cum=0
for goal_type in TARGET_CLASSES:
    cum+=goal_avg_size[goal_type]
print(cum/22)#0.6198013498575854