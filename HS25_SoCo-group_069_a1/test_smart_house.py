import time
from smart_house import *

#Abstract "Device" Methods tests
def test_get_power_consumption_off():
    device = smart_house.device_new("Device1", "Garage", 50.0, "off")
    result = smart_house.get_power_consumption(device)
    assert result == "0.0, device is turned off"


def test_toggle_status():
    device = smart_house.device_new("Device1", "Garage", 50.0, "off")
    smart_house.toggle_status(device)
    assert device["status"] == "on"

#Abstract "Connectable" Methods tests

def test_connect_ip():
    connectable = smart_house.connectable_new()
    smart_house.connect(connectable, "8.8.8.8")
    assert connectable["ip"] == "8.8.8.8"

def test_connect_status():
    connectable = smart_house.connectable_new()
    smart_house.connect(connectable, "8.8.8.8")
    assert connectable["connected"] == True

#----------------------------[TEST SET]----------------------------
#Light
bedroom_light = make(Light, "Bedtable Light", "Bedroom", 300, "off", 70)
basement_lava_lamp = make(Light, "Basement Lava Lamp", "Basement", 100, "on", 10)
closet_light = make(Light, "Closet Light", "Closet", 20, "on", 50, True, "192.168.1.1")
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
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        start_time = time.perf_counter()
        try:
            test()
            results["pass"] += 1
        except AssertionError:
            results["fail"] += 1
        except Exception:
            results["error"] += 1
        end_time = time.perf_counter()
        final_time = end_time - start_time

    print(f"All tests were run in: {final_time:.6f}s")
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")

run_tests()
