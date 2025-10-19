import time
from smart_house import *

#====================================[DEVICE METHOD TESTS]====================================
def test_get_power_consumption(thing):
    result = call(thing, "get_power_consumption")
    if thing["status"] == "off":
        assert result == "Device is currently turned off, thus not consuming any power."

    elif thing["_class"]["_classname"] == "Light":
        assert result == round(thing["base_power"] * (thing["brightness"] / 100))

    elif thing["_class"]["_classname"] == "Thermostat":
        assert result == round(thing["base_power"] * abs(thing["target_temperature"] - thing["room_temperature"]))
        
    elif thing["_class"]["_classname"] == "Camera":
        assert result == round(thing["base_power"] * thing["resolution_factor"])

def test_toggle_status(thing):
    if thing["status"] == "off":
        call(thing, "toggle_status")
        assert thing["status"] == "on"
    else:
        call(thing, "toggle_status")
        assert thing["status"] == "off"
    
#====================================[CONNECTABLE METHOD TESTS]====================================
def test_connect_ip(thing):
    if isinstance(thing["_class"]["_parent"], list):
        ip = "8.8.8.8"
        connect(thing, ip)
        assert thing["ip"] == ip
        assert thing["connected"] == True

def test_connect_status(thing):
    if isinstance(thing["_class"]["_parent"], list):
        ip = "8.8.8.8"
        call(thing, "connect", ip)
        assert thing["connected"] == True
        assert thing["ip"] == ip


#====================================[LIGHT METHOD TESTS]====================================
def test_describe_light(thing):
    if thing["_class"]["_classname"] != "Light":
        return
    else:
        name = thing["name"]
        location = thing["location"]
        brightness = thing["brightness"]
        status = thing["status"]
        type = thing["_class"]["_classname"]


        assert call(thing, "describe_device") ==  f"The {name} [{type}] is located in the {location}, is currently {status}, and is currently set to {brightness}% brightness."

#====================================[THERMOSTAT METHOD TESTS]====================================

def test_describe_thermostat(thing):
    if thing["_class"]["_classname"] != "Thermostat":
        return
    else:
        name = thing["name"]
        location = thing["location"]
        status = thing["status"]
        target_temperature = thing["target_temperature"]
        room_temperature = thing["room_temperature"]
        type = thing["_class"]["_classname"]

        ip = thing["ip"]
        connected = thing["connected"]  

        connected_string = f"connected to server {ip}" if connected else "disconnected"
        assert call(thing, "describe_device") == f"The {name} [{type}] is located in the {location}, is currently {status}, and is currently set to {target_temperature} degrees Celsius in a {room_temperature} degree room. It is currently {connected_string}."

#====================================[CAMERA METHOD TESTS]====================================
        
def test_describe_camera(thing):
    if thing["_class"]["_classname"] != "Camera":
        return
    else:
        name = thing["name"]
        location = thing["location"]
        connected = thing["connected"]
        status = thing["status"]
        resolution = thing["resolution"]
        ip = thing["ip"]
        type = thing["_class"]["_classname"]

        connected_string = f"connected to server {ip}" if connected else "disconnected"
        assert call(thing, "describe_device") == f"The {name} [{type}] is located in the {location}, is currently {status}, and is a {resolution} resolution sensor. It is currently {connected_string}."


#====================================[MANAGEMENT METHOD TESTS]====================================

def test_calculate_total_power_consumption(thing):
    pass



#"find/call" Methods tests

def test_find_unknown_method(thing):
    try:
        call(thing, "unknown_method")
        assert False, "Expected NotImplementedError for unknown method"
    except NotImplementedError:
        pass

#----------------------------[TEST SET]----------------------------
#Light
bedroom_light = make(Light, "Bedtable Light", "Bedroom", 300, "off", 70)
basement_lava_lamp = make(Light, "Basement Lava Lamp", "Basement", 100, "on", 10)
closet_light = make(Light, "Closet Light", "Closet", 20, "on", 50) #light class inherits only from device, so no ip tests neccessary
#Thermostat
bathroom_thermostat = make(Thermostat, "Towel Thermostat", "Bathroom", 1200, "on", 18, 24)
sauna_thermostat = make(Thermostat, "Sauna Thermostat", "Sauna", 500, "on", 20, 80)
office_thermostat = make(Thermostat, "Office Heater", "Office", 100, "on", 17, 23, True, "192.168.1.1")
#Camera
living_room_camera = make(Camera, "Livingroom Camera", "Living Room", 500, "on", 8)
garage_camera = make(Camera, "Garage Peeker", "Garage", 200, "on", 20)
kitchen_camera = make(Camera, "Scooby Cam", "Living Room", 500, "on", 4, True, "192.168.1.1")

ALL_THINGS = [
    bedroom_light, basement_lava_lamp, closet_light,
    bathroom_thermostat, sauna_thermostat, office_thermostat,
    living_room_camera, garage_camera, kitchen_camera
    ]

#setup func
def run_tests():
    results = {"pass": 0, "fail": 0, "error": 0}
    total_time = 0
    objects = {"PASS": [], "FAIL": [], "ERROR": []}
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        start_time = time.perf_counter()
        res = ""
        for thing in ALL_THINGS:
            try:
                test(thing)
                results["pass"] += 1
                res = "passed"
                objects["PASS"].append(f"{thing["name"]} passed {name[5:]}")
            except AssertionError:
                results["fail"] += 1
                res = "failed"
                objects["FAIL"].append(f"{thing["name"]} failed {name[5:]}")
                
            except Exception:
                results["error"] += 1
                res = "crashed"
                objects["ERROR"].append(f"{thing["name"]} crashed {name[5:]}")

        end_time = time.perf_counter()
        final_time = end_time - start_time
        total_time += final_time
        
        print(f"{name[5:]} {res}, ran in {final_time:.6f}s\n")
        

    print(f"All tests were run in: {final_time:.6f}s\n")

    print(f"{results['pass']} PASSED: \n{objects["PASS"]}")
    print(f"{results['fail']} FAILED: \n{objects["FAIL"]}")
    print(f"{results['error']} ERRORS: \n{objects["ERROR"]}")
    

run_tests()
