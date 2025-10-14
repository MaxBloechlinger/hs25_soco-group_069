import time
import smart_house

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
