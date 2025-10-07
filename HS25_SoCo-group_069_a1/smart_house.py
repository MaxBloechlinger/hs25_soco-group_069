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

def connectable_new(connected: bool, ip: str):
    return {
        connected: connected,
        ip: ip
    }
    
#parent class "Connectable"
Connectable = {
    "_classname": "Connectable",
    "_parent": None,
    "_new": connectable_new,
    "connect": connect,
    "disconnect": disconnect,
    "is_connected": is_connected,
}


def new_light():
    pass


#light Inheritance
Light = {
    "_classname": "Light",
    "_parent": Device,
    "_new": new_light,
    "power_consumtion": "implement",
    "description": "implement",
    "toggle_status": "implement"
}



#camera inheritence

# def camera_new(resolution_factor):
#     d = make(Device, name)
#     c = make(Connectable, name)
#     return d | c | {
#         "resolution_factor": resolution_factor
#     }

def camera_new():
    pass 

Camera = {
    "_classname": "Camera",
    "_parent": [Device, Connectable],
    "_new": camera_new
}