from scenariogeneration import esmini, xosc, prettyprint

def create_car(entities,
            name:str,
            boundingbox,
            frontaxle,
            rearaxle,
            max_speed,
            max_acceleration,
            max_deceleration,
            color:str,
            isEgo:bool = False, 
            egoName:str = "Ego"):
    

    vehicle = xosc.Vehicle(
                name, xosc.VehicleCategory.car, boundingbox, frontaxle, rearaxle, max_speed, max_acceleration, max_deceleration
            )

    vehicle.add_property_file(f"../models/car_{color}.osgb")

    match color.lower():
        case "white":
            vehicle.add_property("model_id", "0")
        case "blue":
            vehicle.add_property("model_id", "1")
        case "red":
            vehicle.add_property("model_id", "2")
        case "yellow":
            vehicle.add_property("model_id", "3")
        case _:
            print("No model ID found")  

    if isEgo:
        egoname = egoName
        entities.add_scenario_object(egoname, vehicle)
    else:
        entities.add_scenario_object(name, vehicle)

    return vehicle

def create_pedestrian(entities, 
                    name: str,
                    mass: int,
                    boundingbox,
                    model,
                    isEgo:bool = False, 
                    egoName:str = "Ego"):
     
    pedestrian = xosc.Pedestrian(name,mass,xosc.PedestrianCategory.pedestrian,boundingbox)

    match model.lower():
        case "walkman":
            pedestrian.add_property_file("../models/walkman.osgb")
            pedestrian.add_property("model_id", "7")
        case "cyclist":
            pedestrian.add_property_file("../models/cyclist.osgb")
            pedestrian.add_property("model_id", "9")
        case _:
            pedestrian.add_property_file(f"../models/{model}.osgb")
            print("No model ID found")  

    if isEgo:
        egoname = egoName
        entities.add_scenario_object(egoname, pedestrian)
    else:
        entities.add_scenario_object(name, pedestrian)
        
    return pedestrian

def add_entity(entities, 
            name: str, 
            entityobj, 
            isEgo:bool = False, 
            egoName:str = "Ego"):
    
    if isEgo:
        egoname = egoName
        entities.add_scenario_object(egoname, entityobj)
    else:
        entities.add_scenario_object(name, entityobj)

def init_speed(init, 
            speed: float,
            transition_dynamics,
            name):
                
    speed_act = xosc.AbsoluteSpeedAction(speed, transition_dynamics)
    init.add_init_action(name, speed_act)

def init_actions(init, 
            name:str,
           *actions):
         
    for action in actions:            
        init.add_init_action(name, action)

def creat_trigger(trigger_name:str,
                 condtion,
                 trigger_entity_name:str, 
                 condition_edge = xosc.ConditionEdge.rising, 
                 trigger_delay:float = 0.0):

    trigger = xosc.EntityTrigger(trigger_name,trigger_delay,condition_edge,condtion,trigger_entity_name)

    return trigger

def create_event(event_name:str, 
                 actor, 
                 action,
                 trigger): 
    
    event = xosc.Event(event_name, xosc.Priority.overwrite)
    event.add_trigger(trigger)
    event.add_action(actor, action)

    return event



