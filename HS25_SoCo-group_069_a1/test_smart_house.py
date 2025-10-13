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



def run_tests():
    results = {"pass": 0, "fail": 0, "error": 0}
    for (name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        try:
            test()
            results["pass"] += 1
        except AssertionError:
            results["fail"] += 1
        except Exception:
            results["error"] += 1
    print(f"pass {results['pass']}")
    print(f"fail {results['fail']}")
    print(f"error {results['error']}")

run_tests()
