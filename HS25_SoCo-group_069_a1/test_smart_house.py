import time
import argparse
from smart_house import *

#====================================[DEVICE METHOD TESTS]====================================

def test_toggle_status(thing):
    if thing["status"] == "off":
        call(thing, "toggle_status")
        assert thing["status"] == "on"
    else:
        call(thing, "toggle_status")
        assert thing["status"] == "off"
        
test_variables = "This is a variable which should not run"
test_variables_list = [1,2,3,4]
test_string = "not a function"
test_number = 42

#====================================[CONNECTABLE METHOD TESTS]====================================
def test_connect_ip(thing):
    if isinstance(thing["_class"]["_parent"], list):
        ip = "8.8.8.8"
        call(thing, "connect", ip)
        assert thing["ip"] == ip
        assert thing["connected"] == True

def test_connect_status(thing):
    if isinstance(thing["_class"]["_parent"], list):
        ip = "8.8.8.8"
        call(thing, "connect", ip)
        assert thing["connected"] == True
        assert thing["ip"] == ip

def test_disconnect(thing):
    if isinstance(thing["_class"]["_parent"], list):
        call(thing, "disconnect")
        assert thing["connected"] == False
        
def test_connected(thing):
    if isinstance(thing["_class"]["_parent"], list):
        call(thing, "connect", "1.2.3.4")
        assert call(thing, "is_connected") == True
        call(thing, "disconnect")
        assert call(thing, "is_connected") == False


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

def test_get_power_consumption_light(thing):
    result = call(thing, "get_power_consumption")
    if thing["status"] == "off":
        assert result == "Device is currently turned off, thus not consuming any power."

    elif thing["_class"]["_classname"] == "Light":
        assert result == round(thing["base_power"] * (thing["brightness"] / 100))

def test_toggle_status_light(thing):
    if thing["status"] == "off":
        call(thing, "toggle_status")
        assert thing["status"] == "on"
    else:
        call(thing, "toggle_status")
        assert thing["status"] == "off"

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

def test_get_power_consumption_thermostat(thing):
    result = call(thing, "get_power_consumption")
    if thing["status"] == "off":
        assert result == "Device is currently turned off, thus not consuming any power."

    elif thing["_class"]["_classname"] == "Thermostat":
        assert result == round(thing["base_power"] * abs(thing["target_temperature"] - thing["room_temperature"]))

def test_toggle_status_thermostat(thing):
    if thing["status"] == "off":
        call(thing, "toggle_status")
        assert thing["status"] == "on"
    else:
        call(thing, "toggle_status")
        assert thing["status"] == "off"

def test_set_target_temperature_thermostat(thing):
    if thing["_class"]["_classname"] != "Thermostat":
        return
    call(thing, "set_target_temperature", 20)
    assert thing["target_temperature"] == 20
    
def test_get_target_temperature_thermostat(thing):
    if thing["_class"]["_classname"] != "Thermostat":
        return
    res = call(thing, "get_target_temperature")
    assert thing["target_temperature"] == res


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

def test_get_power_consumption_camera(thing):
    if thing["_class"]["_classname"] != "Camera":
        return
    result = call(thing, "get_power_consumption")
    if thing["status"] == "off":
        assert result == "Device is currently turned off, thus not consuming any power."
 
    elif thing["_class"]["_classname"] == "Camera":
        assert result == round(thing["base_power"] * thing["resolution_factor"])


def test_camera_resolution(thing):
    if thing["_class"]["_classname"] != "Camera":
        return
    if thing["resolution_factor"] < 5:
        assert thing["resolution"] == "low"
    elif thing["resolution_factor"] < 10:
        assert thing["resolution"] == "medium"
    else:
        assert thing["resolution"] == "high"

def test_toggle_status_camera(thing):
    if thing["_class"]["_classname"] != "Camera":
        return
    if thing["status"] == "off":
        call(thing, "toggle_status")
        assert thing["status"] == "on"
    else:
        call(thing, "toggle_status")
        assert thing["status"] == "off"

#====================================[MANAGEMENT METHOD TESTS]====================================

def test_total_power_consumption(manager):
    expected = 0
    for dev in ALL_THINGS:
        if dev["status"] == "on":
            expected += call(dev, "get_power_consumption")
    result = call(manager, "calculate_total_power_consumption")
    print(result)
    print(expected)
    assert result == expected
#"find/call" Methods tests

def test_find_unknown_method(thing):
    try:
        call(thing, "unknown_method")
        assert False, "Expected NotImplementedError for unknown method"
    except NotImplementedError:
        pass
    


#----------------------------[TEST SET]----------------------------

def setUp():
    global ALL_THINGS
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
    

def tearDown():
    global ALL_THINGS
    ALL_THINGS = []


def run_tests(select=None):
    results = {"pass": 0, "fail": 0, "error": 0}
    total_time = 0
    objects = {"PASS": [], "FAIL": [], "ERROR": []}

    for (name, test) in list(globals().items()):
        if not name.startswith("test_"):
            continue
        
        if not callable(test):
            continue

        start_time = time.perf_counter()

        setUp()

        test_passed = True
        test_status = "passed"
        
        for thing in ALL_THINGS:
            if select:
                #skip tests that don't match selection
                if select.lower() not in name.lower():
                    continue
                #skip tests that don't match thing
                if select.lower() == "light" and thing["_class"]["_classname"] != "Light":
                    continue
                if select.lower() == "thermostat" and thing["_class"]["_classname"] != "Thermostat":
                    continue
                if select.lower() == "camera" and thing["_class"]["_classname"] != "Camera":
                    continue
            try:
                test(thing)
                results["pass"] += 1
                objects["PASS"].append(f'{thing["name"]} passed {name[5:]}') 
            except AssertionError:
                results["fail"] += 1
                test_passed = False
                test_status = "failed"
                objects["FAIL"].append(f'{thing["name"]} failed {name[5:]}')
                
            except Exception:
                results["error"] += 1
                test_passed = False
                test_status = "crashed"
                objects["ERROR"].append(f'{thing["name"]} crashed {name[5:]}')

        tearDown()

        end_time = time.perf_counter()
        duration = end_time - start_time
        total_time += duration
        
        print(f"{name[5:]} {test_status}, ran in {duration:.6f}s\n")
        

    print(f"Total Runtime: {total_time:.6f}s\n")

    print(f"{results['pass']} PASSED: \n{objects['PASS']}")
    print(f"{results['fail']} FAILED: \n{objects['FAIL']}")
    print(f"{results['error']} ERRORS: \n{objects['ERROR']}")
 
 
 
if __name__ == "__main__":
    # Example usage in terminal: 
    # python test_smart_house.py --select thermostat --verbose
    p = argparse.ArgumentParser()
    p.add_argument("--select", type=str)
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    if args.verbose:
        print("\n===[Verbose: listing all variables that start with 'test_']===")
        for name, obj in list(globals().items()):
            if name.startswith("test_"):
                t = "function" if callable(obj) else type(obj).__name__
                print(f"{name}, type: {t}")
    run_tests(select=args.select)

