<<<<<<< HS25_SoCo-group_069_a1/smart_house.py
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

#methods "Connectable"
def connect(thing, ip):
    thing["ip"]  = ip
    thing["connected"] = True

def disconnect(thing):
    thing["connected"] = False

def is_connected(thing):
    return thing["connected"]

def new_connectable(connected: bool, ip: str):
    return {
        connected: connected,
        ip: ip
    }
    
#parent class "Connectable"
Connectable = {
    "_classname": "Connectable",
    "_parent": None,
    "_new": new_connectable,
    "connect": connect,
    "disconnect": disconnect,
    "is_connected": is_connected,
}


def light(brightness: int, base_power: int, name: str, location: str):

    def get_power_consumption():
        return round(base_power * brightness/ 100)
    
    def describe_device():
        return f" My name is {name}. I am a light. My location is {location}. My brightness is {brightness}%."
>>>>>>> HS25_SoCo-group_069_a1/smart_house.py
