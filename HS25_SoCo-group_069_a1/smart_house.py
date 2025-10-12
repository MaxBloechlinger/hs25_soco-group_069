
#---------------------[CALL & CONSTRUCTOR FUNCTIONS]---------------------
def find(cls, method_name):
    if cls is None:
        raise NotImplementedError(method_name)
    if method_name in cls:
        return cls[method_name]

    #no parent
    if cls["_parent"] == None:
        raise NotImplementedError(f"{method_name} not implemented by {cls}")

    #double parents
    if isinstance(cls["_parent"],list) and len(cls["_parent"]) == 2:
        for parent in cls["_parent"]:
            try: 
                return find(parent, method_name)
            except NotImplementedError: 
                continue
        raise NotImplementedError(method_name)
        
    #single parent
    return find(cls["_parent"], method_name)

def call(thing, method_name, *args):
    method = find(thing["_class"], method_name)
    return method(thing, *args)

def make(cls, *args):
    return cls["_new"](*args)


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
        "status": status
    }

#Parent Class "Device"
Device = {
    "_classname": "Device",
    "_parent": None,
    "_new": device_new,
    "power_consumption": get_power_consumption,
    "description": describe_device,
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
        "ip": ip
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
    return f"The {name} is located in the {location}, is currently {status}, and is currently set to {brightness}% brightness."

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

#Light test
print("======================[Light test]======================")
bedroom_light = make(Light, "Bedtable Light", "Bedroom", 300, "off", 70)
light_describe = call(bedroom_light, "describe_device")
light_power = call(bedroom_light, "get_power_consumption")
print(f"Description: {light_describe}")
print(f"POWER: {light_power}")
call(bedroom_light, "toggle_status")
light_power = call(bedroom_light, "get_power_consumption")
print(f"POWER: {light_power}")
print("\n")


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

    connected_string = f"connected to server {ip}" if connected else "disconnected"
    return (
    f"The {name} is located in the {location}, is currently {status}, and is currently set to {target_temperature} degrees Celsius in a {room_temperature} degree room. It is currently {connected_string}."
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

#Thermostat test
print("======================[Thermostat test]======================")
bathroom_thermostat = make(Thermostat, "Towel Thermostat", "Bathroom", 1200, "on", 18, 24)

thermostat_describe = call(bathroom_thermostat, "describe_device")
print(thermostat_describe)
thermostat_power = call(bathroom_thermostat, "get_power_consumption")
print(thermostat_power)
thermostat_get = call(bathroom_thermostat, "get_target_temperature")
thermostat_set = call(bathroom_thermostat, "set_target_temperature", 10)
thermostat_describe = call(bathroom_thermostat, "describe_device")
print(thermostat_describe)
thermostat_power = call(bathroom_thermostat, "get_power_consumption")
print(thermostat_power)
print("\n")

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

    connected_string = f"connected to server {ip}" if connected else "disconnected"
    return f"The {name} is located in the {location}, is currently {status}, and is a {resolution} resolution sensor. It is currently {connected_string}."



Camera = {
    "_classname": "Camera",
    "_parent": [Device, Connectable],
    "_new": camera_new,
    "describe_device": camera_describe_device,
    "get_power_consumption": camera_get_power_consumption
   
}


#Camera test
print("======================[Camera test]======================")
living_room_camera = make(Camera, "New RGB Camera", "Living Room", 500, "on", 8)
#print(camera_describe_device(living_room_camera))
camera_describe = call(living_room_camera, "describe_device")
camera_power = call(living_room_camera, "get_power_consumption")

print(camera_describe)
print(camera_power)
camera_power = call(living_room_camera, "get_power_consumption")

call(living_room_camera, "toggle_status")
camera_power = call(living_room_camera, "get_power_consumption")
print(f"POWER: {camera_power}")



#---------------------[Step 2]---------------------

SmartHouseManagement = {
    "_classname": "SmartHouseManagement",
    "_parent": None,
    "calculate_total_power_consumption": calculate_total_power_consumption,
    "get_all_device_description": get_all_device_description,
    "get_all_connected_devices": get_all_connected_devices,

}

def search_type(thing):
    pass