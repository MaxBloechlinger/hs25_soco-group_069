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



#light constructor
def new_light(brightness: int,name: str, location: str, base_power: float, status: str):
    light_inheritance = device_new(name, location, base_power, status)
    light_inheritance["__classname"] = "Light"
    
    if brightness > 100:
        light_inheritance["brightness"] = 100
    elif brightness < 0:
        light_inheritance["brightness"] = 0
    else:
        light_inheritance["brightness"] = brightness
   

def light_describe_device(thing):
    name = thing.get("name", "")
    location = thing.get("location", "")
    brightness = thing.get("brightness", 0)
    device_type = thing.get("_classname", "")
    status = thing.get("status", "")
    return f"The {name} {device_type} is located in the {location}, is currently {status}, and is currently set to {brightness}% brightness."
    
    
#Should round to closest integer. Thana
def light_get_power_consumption(thing):
    if thing.get("status", "") is not "on":
        return "Device is currently turned off, thus not consuming any power."
    
    return round( thing.get("base power", 0) * (thing.get("brightness", 0) / 100))

#light Inheritance
Light = {
    "_classname": "Light",
    "_parent": Device,
    "_new": new_light,
    "power_consumtion": light_get_power_consumption,
    "description": light_describe_device,
    "toggle_status": toggle_status
}




