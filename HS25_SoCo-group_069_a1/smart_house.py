#---------------------[CALL & CONSTRUCTOR FUNCTIONS]---------------------
def find(cls, method_name):
    while cls is not None:
        if method_name in cls:
            return cls[method_name]
        cls = cls["_parent"]
    raise NotImplementedError("method_name")

def call(thing, method_name, *args):
    method = find(thing["_class"], method_name)
    return method(thing, *args)

def make(cls, *args):
    return cls["_new"](*args)


#---------------------[DEVICE PARENT CLASS]---------------------

#Abstract "Device" Methods
def get_power_consumption(thing):
    if thing["status"] == "off":
        return "0.0, device is turned off"
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
    "get_power_consumption": get_power_consumption,
    "describe_device": describe_device,
    "toggle_status": toggle_status,
}

device = device_new("Device1", "Garage", 50.0, "off")
result = get_power_consumption(device)
print(result)

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

#Light test
print("======================[Light test]======================")
bedroom_light = make(Light, "Bedtable", "Bedroom", 300, "off", 70)
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

#Thermostat test
print("======================[Thermostat test]======================")
bathroom_thermostat = make(Thermostat, "Towel", "Bathroom", 1200, "on", 18, 24, True, "127.0.0.1")

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


#Camera test
print("======================[Camera test]======================")
living_room_camera = make(Camera, "New RGB", "Living Room", 500, "on", 8, True, "127.0.0.1")
#print(camera_describe_device(living_room_camera))
camera_describe = call(living_room_camera, "describe_device")
camera_power = call(living_room_camera, "get_power_consumption")

print(camera_describe)
print(camera_power)
camera_power = call(living_room_camera, "get_power_consumption")

#call(living_room_camera, "toggle_status")
camera_power = call(living_room_camera, "get_power_consumption")
print(f"POWER: {camera_power}")



#---------------------[Step 2]---------------------


print("======================[Smart House Management test]======================\n")

ALL_THINGS = [bedroom_light, bathroom_thermostat, living_room_camera]

def calculate_total_power_consumption(search_type=None, search_room=None):
    res = 0
    for thing in ALL_THINGS:
        if thing["status"] != "on":
            continue
        if ((search_type is not None and thing["_class"] != search_type) or 
            (search_room is not None and thing["location"] != search_room)):
            continue
        res += call(thing, "get_power_consumption")
    return res

def get_all_device_description(search_type=None, search_room=None):
    descriptions = []
    for thing in ALL_THINGS:
        if ((search_type is not None and thing["_class"] != search_type) or 
            (search_room is not None and thing["location"] != search_room)):
            continue
        descriptions.append(call(thing,"describe_device"))
    return descriptions

def get_all_connected_devices(ip=None):
    results = []
    for thing in ALL_THINGS:
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
    "calculate_total_power_consumption": calculate_total_power_consumption,
    "get_all_device_description": get_all_device_description,
    "get_all_connected_devices": get_all_connected_devices,
}

print("Device Description Test:\n")
print(get_all_device_description(search_type=None, search_room="Bedroom"))
print(get_all_device_description(search_type=Light, search_room=None))
print(get_all_device_description(search_type=None, search_room="Living Room"))
print(get_all_device_description(search_type=Thermostat, search_room="Bathroom"))
print("\n")

print("Power Consumption Test\n")
print("The total power consumption is:", calculate_total_power_consumption())
print("The total power consumption in the bedroom is:", calculate_total_power_consumption(search_room="Bedroom"))
print("The total power consumption of all Lights are:", calculate_total_power_consumption(search_type=Light)) #Value is correct according to the input variables and formula
print("\n")

print("All connected devices are:\n", get_all_connected_devices())
print("All connected devices with correct IP input are:\n", get_all_connected_devices("127.0.0.1"))
print("All connected devices with wrong IP input are:\n", get_all_connected_devices("123.345.1.100"))
