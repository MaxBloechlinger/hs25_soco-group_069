# HS25 SoCo Assignment 1 Group 69: Smarthouse House Management System

**Members:** Max Blöchlinger, Abraham Herzog, Luiz Hablützel

## Content

- **smart_house.py**
  [STEP 01 - STEP 02]
  Implementation of Device & Connectable parent classes, Light, Thermostat & Camera subclasses and their methods
- **test_smart_house.py**
  [STEP 03]
  selfmade testing framework for all methods of smart_house.py
- **repository.md**
  link to gitlab repository

## STEP 01

### Dictionary Classes

As requested in the assignment we implemented our own Dictionary-Based Object Classes instead of standard Python Classes

### Call & Constructor Functions

- **constructor: make(cls, \*args, \*\*kwargs)**
  calls the '\_new' method defined in the class dictionary of 'cls' to create an object instance.

- **call function: call(thing, method_name, \*args, \*\*kwargs)**
  uses find() function to locate correct method in current or parent class dictionary
- **find function: find(cls, method_name)**
  recursively searches for the method provided by call()
  if the current class dictionary did not implement the method find() searches in the parent class dictionary

### Device Parent Class

Attributes:

- name, location, base_power, status

Methods:

- toggle_status()
- get_power_consumption() [**abstract**], describe_device() [**abstract**]

### Connectable Parent Class

Attributes:

- name, location, base_power, status

Methods:

- toggle_status(): turns device on/off via thing["status"]
- get_power_consumption() [**abstract**], describe_device() [**abstract**]:
  not implemented for parent class since each subclass has their own unique implementation
- device_new(): returns a dictionary with it's attributes, "\_class" entry points to Device dictionary
