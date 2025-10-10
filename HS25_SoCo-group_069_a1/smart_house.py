#Abstract Device Methods
def get_power_consumption(thing):
    pass

def describe_device(thing):
    print("no description func yet")

def toggle_status(thing):
    pass


#Device Constructor
def device_new(name: str, location: str, base_power: float, status: str):
    return {
        "name": name,
        "location": location,
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



#light constructor
def new_light(brightness: int,name: str, location: str, base_power: float, status: str):
    light_inheritance = device_new(name, location, base_power, status)
    light_inheritance["_classname"] = "Light"
    
    if brightness > 100:
        light_inheritance["brightness"] = 100
    elif brightness < 0:
        light_inheritance["brightness"] = 0
    else:
        light_inheritance["brightness"] = brightness

    return light_inheritance
   

def light_describe_device(thing):
    name = thing["name"]
    location = thing["location"]
    brightness = thing["brightness"]
    device_type = thing["_classname"]
    status = thing["status"]
    return f"The {name} {device_type} is located in the {location}, is currently {status}, and is currently set to {brightness}% brightness."
    
    
#Should round to closest integer. Thana
def light_get_power_consumption(thing):
    if thing["status"] != "on":
        return "Device is currently turned off, thus not consuming any power."

    return round(thing["base_power"] * (thing["brightness"] / 100))

#light Inheritance
Light = {
    "_classname": "Light",
    "_parent": Device,
    "_new": new_light(),
    "power_consumtion": light_get_power_consumption,
    "description": light_describe_device,
    "toggle_status": toggle_status
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