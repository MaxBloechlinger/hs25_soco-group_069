
#---------------------[CALL & CONSTRUCTOR FUNCTIONS]---------------------
def find(cls, method_name):
    if cls is None:
        raise NotImplementedError(method_name)
    if method_name in cls:
        return cls[method_name]

    #no parent
    if cls["_parent"] == None:
        raise NotImplementedError(f"{method_name} not implemented by {cls}")

    #multiple parents
    if isinstance(cls["_parent"],list) and len(cls["_parent"]) >= 2:
        for parent in cls["_parent"]:
            try: 
                return find(parent, method_name)
            except NotImplementedError: 
                continue
        raise NotImplementedError(method_name)
        
    #single parent
    return find(cls["_parent"], method_name)

def call(thing, method_name, *args, **kwargs):
    method = find(thing["_class"], method_name)
    return method(thing, *args, **kwargs)

def make(cls, *args, **kwargs):
    obj = cls["_new"](*args, **kwargs)
    if cls["_classname"] in ["Light", "Camera", "Thermostat"]:
        ALL_DEVICES.append(obj)
    return obj


#---------------------[DEVICE PARENT CLASS]---------------------

#Abstract "Device" Methods
def get_power_consumption(thing):
    raise NotImplementedError("get_power_consumption not implemented")


def describe_device(thing):
    raise NotImplementedError("describe_device not implemented")

def toggle_status(thing):
    if thing["status"] == "on":
        thing["status"] = "off"
    else:
        thing["status"] = "on"

#"Device" Constructor
def device_new(name: str, location: str, base_power: float, status: str):
    return {
        "name": name,
        "location": location,
        "base_power": base_power,
        "status": status,
        "_class": Device
    }

#Parent Class "Device"
Device = {
    "_classname": "Device",
    "_parent": None,
    "_new": device_new,
    "get_power_consumption": get_power_consumption,
    "describe_device": describe_device,
    "toggle_status": toggle_status,
}


#---------------------[CONNECTABLE PARENT CLASS]---------------------

#Abstract "Connectable" Methods
def connect(thing, ip):
    thing["ip"]  = ip
    thing["connected"] = True

def disconnect(thing):
    thing["connected"] = False

def is_connected(thing):
    return thing["connected"]

#"Connectable" Constructor
def connectable_new(connected: bool = False, ip: str= None):
    return {
        "connected": connected,
        "ip": ip,
        "_class": Connectable
    }
    
#Parent Class "Connectable"
Connectable = {
    "_classname": "Connectable",
    "_parent": None,
    "_new": connectable_new,
    "connect": connect,
    "disconnect": disconnect,
    "is_connected": is_connected,
}

#---------------------[LIGHT CLASS]---------------------

#"Light" Constructor
def light_new(
    name: str, location: str, base_power: float, status: str,
    brightness: int,):
    return make(Device, name, location, base_power, status) | {
        "brightness": brightness,
        "_class": Light
    }
    

    
#Abstract Methods for "Light"
def light_describe_device(thing):
    name = thing["name"]
    location = thing["location"]
    brightness = thing["brightness"]
    status = thing["status"]
    type = thing["_class"]["_classname"]
    return f"The {name} [{type}] is located in the {location}, is currently {status}, and is currently set to {brightness}% brightness."

def light_get_power_consumption(thing):
    if thing["status"] != "on":
        return "Device is currently turned off, thus not consuming any power."

    return round(thing["base_power"] * (thing["brightness"] / 100))


#light Inheritance
Light = {
    "_classname": "Light",
    "_parent": Device,
    "_new": light_new,
    "describe_device": light_describe_device,
    "get_power_consumption": light_get_power_consumption
}

#---------------------[THERMOSTAT CLASS]---------------------

#Abstract Methods for "Thermostat"
def thermostat_get_power_consumption(thing):
    if thing["status"] != "on":
        return "Device is currently turned off, thus not consuming any power."
    
    return round(thing["base_power"] * abs(thing["target_temperature"] - thing["room_temperature"]))

def thermostat_describe_device(thing):
    name = thing["name"]
    location = thing["location"]
    status = thing["status"]
    target_temperature = thing["target_temperature"]
    room_temperature = thing["room_temperature"]
    ip = thing["ip"]
    connected = thing["connected"]
    type = thing["_class"]["_classname"]

    connected_string = f"connected to server {ip}" if connected else "disconnected"
    return (
    f"The {name} [{type}] is located in the {location}, is currently {status}, and is currently set to {target_temperature} degrees Celsius in a {room_temperature} degree room. It is currently {connected_string}."
)

#"Thermostat" Methods
def set_target_temperature(thing, new_temperature: int):
    thing["target_temperature"] = new_temperature

def get_target_temperature(thing):
    return thing["target_temperature"]

#"Thermostat" Constructor
def thermostat_new(
        name:str, location:str, base_power:float, status:str,
        room_temperature:int, target_temperature:int,
        connected:bool=False, ip: str=None):
    return make(Device,name,location,base_power,status) | make(Connectable,connected,ip) | {
        "room_temperature": room_temperature,
        "target_temperature": target_temperature,
        "_class": Thermostat
    }


Thermostat = {
    "_classname": "Thermostat",
    "_parent": [Device, Connectable],
    "_new": thermostat_new,
    "describe_device": thermostat_describe_device,
    "get_power_consumption": thermostat_get_power_consumption,
    "set_target_temperature": set_target_temperature,
    "get_target_temperature": get_target_temperature
}


#---------------------[CAMERA CLASS]---------------------


#Camera Constructor
def camera_new(name:str, location:str, base_power:float, status:str,
               resolution_factor: int,
               connected:bool=False, ip: str=None):
    if (resolution_factor < 5):
        resolution = "low"
    elif(5<=resolution_factor<10):
        resolution = "medium"
    else:
        resolution = "high"
    return make(Device,name,location,base_power,status) | make(Connectable,connected,ip) | {
        "resolution_factor": resolution_factor,
        "resolution": resolution,
        "_class": Camera
    }


def camera_get_power_consumption(thing):
    if thing["status"] != "on":
        return "Device is currently turned off, thus not consuming any power."
    
    return round(thing["base_power"] * thing["resolution_factor"])

def camera_describe_device(thing):
    name = thing["name"]
    location = thing["location"]
    connected = thing["connected"]
    status = thing["status"]
    resolution = thing["resolution"]
    ip = thing["ip"]
    type = thing["_class"]["_classname"]

    connected_string = f"connected to server {ip}" if connected else "disconnected"
    return f"The {name} [{type}] is located in the {location}, is currently {status}, and is a {resolution} resolution sensor. It is currently {connected_string}."



Camera = {
    "_classname": "Camera",
    "_parent": [Device, Connectable],
    "_new": camera_new,
    "describe_device": camera_describe_device,
    "get_power_consumption": camera_get_power_consumption
   
}


#---------------------[Step 2]---------------------


ALL_DEVICES = []

def smart_house_management_new():
    return {
        "_class": SmartHouseManagement    
    }
    

def calculate_total_power_consumption(thing, search_type=None, search_room=None):
    res = 0
    for thing in ALL_DEVICES:
        if thing["status"] != "on":
            continue
        if ((search_type is not None and thing["_class"] != search_type) or 
            (search_room is not None and thing["location"] != search_room)):
            continue
        res += call(thing, "get_power_consumption")
    return res

def get_all_device_description(thing, search_type=None, search_room=None):
    descriptions = []
    for thing in ALL_DEVICES:
        if ((search_type is not None and thing["_class"] != search_type) or 
            (search_room is not None and thing["location"] != search_room)):
            continue
        descriptions.append(call(thing,"describe_device"))
    return descriptions

def get_all_connected_devices(thing, ip=None):
    results = []
    for thing in ALL_DEVICES:
        if thing["_class"] in [Thermostat, Camera]:
            if thing["status"] == "on" and thing["connected"]:
                if ip is None or thing["ip"] == ip:
                    results.append({
                        "description": call(thing, "describe_device"),
                        "power": call(thing, "get_power_consumption")
                    })

    return results


SmartHouseManagement = {
    "_classname": "SmartHouseManagement",
    "_parent": None,
    "_new": smart_house_management_new,
    "calculate_total_power_consumption": calculate_total_power_consumption,
    "get_all_device_description": get_all_device_description,
    "get_all_connected_devices": get_all_connected_devices
}

