#Abstract Device Methods
def get_power_consumption(thing, weight):
    pass

def describe_device():
    print("no description func yet")

def toggle_status(thing):
    pass


#Device Constructor
def device_new(name: str, location: str, base_power: float, status: str):
    return {
        "name": name,
        "loctation": location,
        "base_power": base_power,
        "status": status
    }


#Parent Class Device
Device = {
    "_classname": "Device",
    "_parent": None,
    "_new": device_new,
    "power_consumption": get_power_consumption,
    "description": describe_device,
    "toggle_status": toggle_status,
}


def light(brightness: int, base_power: int, name: str, location: str):

    def get_power_consumption():
        return round(base_power * brightness/ 100)
    
    def describe_device():
        return f" My name is {name}. I am a light. My location is {location}. My brightness is {brightness}%."