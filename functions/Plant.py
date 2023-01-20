from random import randint, sample
from functions.plant import plant

def randomize_plants(plants):
    count = range(1, len(plant["plants"]) + 1)
    # create list of random sequences
    order = sample(count, k=len(count))
    #print(order)
    for x in range(0, len(plant["plants"])):
        plant["plants"][x]["seq"]=order[x]                  
        #print(plant["plants"][x])
    p = plant["plants"]
    p.sort(key=lambda x: x["seq"])
    return plant

def plants_for_trial(trial):
    # stub for current time
    return plant
if __name__=="__main__":
    print(randomize_plants(plant))