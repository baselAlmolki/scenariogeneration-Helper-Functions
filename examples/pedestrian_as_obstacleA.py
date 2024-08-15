from scenariogeneration import esmini, xosc, prettyprint, ScenarioGenerator
import os
from scenariogeneration import ScenarioGenerator
from scenariogeneration_helper_functions import *


for i in range(15, 33, 5): #vary ego speed

    class Scenario(ScenarioGenerator):
        def __init__(self):
            super().__init__()
        
        def scenario(self, **kwargs): 
            
            catalog = xosc.Catalog()
            catalog.add_catalog("VehicleCatalog", "../xosc/Catalogs/Vehicles")

            road = xosc.RoadNetwork( 
                roadfile="../xodr/straight_500m_signs.xodr", scenegraph="../models/straight_500m_signs.osgb"
            )

            paramdec = xosc.ParameterDeclarations()
            entities = xosc.Entities()

            bb = xosc.BoundingBox(2, 5, 1.8, 2.0, 0, 0.9)
            fa = xosc.Axle(0.523598775598, 0.8, 1.68, 2.98, 0.4)
            ba = xosc.Axle(0.523598775598, 0.8, 1.68, 0, 0.4)

            #add ego vehicle
            create_car(entities,"car_white",bb,fa,ba,69, 10, 10,"white",True)
            egoname = "Ego"
            test_speed = i

            s_long = test_speed*(4/2.2) + 1  #distance of pedestrian from ego

            orientation = xosc.Orientation(3 * 3.14159 / 2, 0, 0)  
            
            #add pedestrian
            create_pedestrian(entities,"pedestrian1",70,xosc.BoundingBox(0.5, 0.5, 1.7, 0, 0, 0),"walkman")

            #create pedestrian trajectory
            positionlist = []
            positionlist.append(xosc.RelativeWorldPosition(egoname, s_long+2.5, 4, 0, orientation))
            positionlist.append(xosc.RelativeWorldPosition(egoname, s_long+2.5, 0, 0, orientation))
            positionlist.append(xosc.RelativeWorldPosition(egoname, s_long+2.5, -4, 0, orientation))
            polyline = xosc.Polyline([0, 2.0, 4.0],positionlist)
            traj = xosc.Trajectory("my_trajectory", True)
            traj.add_shape(polyline)

            init = xosc.Init()
            
            # define transition_dynamics
            step_time = xosc.TransitionDynamics(
                xosc.DynamicsShapes.step, xosc.DynamicsDimension.time, 1
            )
            lin_time = xosc.TransitionDynamics(
                xosc.DynamicsShapes.sinusoidal, xosc.DynamicsDimension.rate, 3
            )  

            #initialize ego vehicle
            egostart = xosc.TeleportAction(xosc.LanePosition(3, 0, -1, 1,))
            init_speed(init, test_speed, step_time,egoname)
            init_actions(init, egoname, egostart)

            #initialize pedestrian
            pedestrian_start = xosc.TeleportAction(xosc.RelativeWorldPosition(egoname, s_long+2.5, 4, 0, orientation))
            pedestrian_behaviour = xosc.FollowTrajectoryAction(traj,'follow',)
            pedestrian_speed = xosc.AbsoluteSpeedAction(2.2,step_time)
            init_actions(init, "pedestrian1", pedestrian_start,pedestrian_behaviour,pedestrian_speed)

            #create event such that ego stops on collision
            collision_cond = xosc.CollisionCondition("pedestrian1")
            collision_action = xosc.AbsoluteSpeedAction(0,step_time)
            trigger1 = creat_trigger("trigger1",collision_cond,egoname)
            event1 = create_event("event1",egoname,collision_action,trigger1)

            man = xosc.Maneuver("my_maneuver")
            man.add_event(event1)
            mangr = xosc.ManeuverGroup("mangroup")
            mangr.add_actor("$owner")
            mangr.add_maneuver(man)
            starttrigger = xosc.ValueTrigger(
                "starttrigger",
                0,
                xosc.ConditionEdge.rising,
                xosc.SimulationTimeCondition(0, xosc.Rule.greaterThan),
                )
            act = xosc.Act("my_act", starttrigger)
            act.add_maneuver_group(mangr)

            # create the story
            storyparam = xosc.ParameterDeclarations()
            storyparam.add_parameter(
                xosc.Parameter("$owner", xosc.ParameterType.string,egoname)
            )
            story = xosc.Story("mystory", storyparam)
            story.add_act(act)

            # create the storyboard
            stoptrigger = xosc.EntityTrigger(
                "stop_simulation", 
                0.5, 
                xosc.ConditionEdge.rising, 
                xosc.EndOfRoadCondition(0.5), 
                egoname, 
                triggeringpoint="stop")

            sb = xosc.StoryBoard(init,stoptrigger)
            sb.add_story(story)

            sce = xosc.Scenario(
                "pedestrian_as_obstacle",
                "Basel",
                paramdec,
                entities=entities,
                storyboard=sb,
                roadnetwork=road,
                catalog=catalog,
            )
            return sce
        
    
    if __name__ == "__main__":
        sce = Scenario()

        prettyprint(sce.scenario().get_element())

        # Define the path to the esmini resources directory
        esmini_resources_dir = "path/to/esmini/resources/directory"

        sce.generate(esmini_resources_dir)

        # Specify the path to esmini
        esmini_path = "path/to/esmini"
        
        # Run esmini to visualize the scenario
        esmini(sce, esminipath=esmini_path, index_to_run='first')
