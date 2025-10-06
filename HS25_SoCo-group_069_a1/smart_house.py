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
