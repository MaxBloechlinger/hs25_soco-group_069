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

## Design Decisions for Step 1 & 2

### Only Dictionaries

- We implemented a *class* system without actually using classes, only plain dictionaries as this was a given requirement for the assignment. 

**The Class Dictionaries**
- They define the methods of the object and have attribute: "_new" which references the constructor for new instances
- Can have a "_parent" (or multiple)

**Instance Dictionaries**
- Stores the given information/ state of the object and has a "_class" attribute which points to the  "_class" dictionary.

### Methods Calls

- **constructor: make(cls, \*args, \*\*kwargs)**
  Calls the '\_new' method defined in the class dictionary of 'cls' to create an object instance. If called, it also adds the instances to the global *ALL_THINGS* list.
- **call function: call(thing, method_name, \*args, \*\*kwargs)**
  Uses find() function to locate correct method in current or parent class dictionary
- **find function: find(cls, method_name)**
  Recursively searches for the method provided by call().
  If the current class dictionary did not implement the method find() searches in the parent class dictionary

  **Why we chose this design** - We tried to adhere as closely to the given format and outline defined in the book: *Software Design by Example, Chapter 2*

### Multiple Inheritance Implementation
- We achieved this in our find() functions by checking whether *"_parent"* has len >= 2 which then iterates through the list with a try, except block 
- Will raise NotImplementedError if no *"_parent"* can be found
- Is relatively simple and allows for Camera & Thermostat to inherit from both Device and Connectable

### Smart House Manager
- The approach we took here is that the Smart House Manager will scan the globally instantiated ALL_THINGS list where all devices should be stored.
- This allows us to track all instantiated devices and creates a broader scope for the project if more devices would want to be added.
- It can also be filtered with search_type and search_room if a user wants to only look up specific rooms and/or devices

### Error Handling
- In case the abstract "Device" methods were not to be implemented or missing we created a *raise NotImplementedError* block
- The same goes for the *find()* function, if no parent or method can't be found we raise a *NotImplementedError*
- The Management Methods, *(defined below)*, ignores attributes like status, which stem from non-device objects - Smart House Management instances - as to not call Smart House Management methods on itself.
- When devices are off we wanted to return a string message - seen in the *get_power_consumption* methods, to create a more friendly and clear message, instead of a 0.


## STEP 01

### Dictionary Classes

As requested in the assignment we implemented our own Dictionary-Based Object Classes instead of standard Python Classes


### Device Parent Class

Attributes:

- Name, location, base_power, status

Methods:

- toggle_status() - Switches the status of the instance being sent into the function to either "on" or "off"
- get_power_consumption() - [**abstract**]
- describe_device() - [**abstract**]
- device_new(...) - Constructs a new dictionary, an instance of Device. "_class" is Device

### Connectable Parent Class

Attributes:

- Connected, ip

Methods:

- connect(ip) Sets the status of connected to **True** and stores the ip address
- disconnect() Sets the status of connected to **False**
- is_connected() - Returns the status of the connection
- connectable_new(...) Constructs a new dictionary, an instance of Connectable. "_class" is Connectable

### Light Subclass

Attributes:

- Inherits all Attributes from Device and has additional attribute brightness

Methods:

- light_new(...) - Constructs a new instance with its "_class" set to Light and "_parent" set to **Device**
- light_describe_device() - Returns all relevant information stored in the Light instance formatted for human readability.
- light_get_power_consumption() -  If on, returns the power consumption with formula: round(base_power*(brightness / 100)). Otherwise returns a string indicating the device is off.

### Thermostat Subclass

Attributes:

- Inherits both from Device and Connectable and has additional attributes room_temperature & target_temperature

Methods:

- thermostat_get_power_consumption() - If on, returns the power consumption with formula: round(base_power * abs(target_temperature - room_temperature))
- thermostat_describe_device() - Returns all relevant information stored in the Thermostat instance formatted for human readability.
- set_target_temperature(new_temperature) - Sets the temperature the instance should adopt
- get_target_temperature() - Returns the set target temperature of the instance
- thermostat_new(...) -  Constructs a new instance with its "_class" set to Thermostat and "_parent" set to [**Device**, **Connectable**]

### Camera Subclass

Attributes: 

- Inherits both from Device and Connectable and has additional attribute resolution_factor which can be low, medium or high after computation.

Methods:

- camera_new(...) - Constructs a new instance with its "_class" set to Camera and "_parent" set to [**Device**, **Connectable**]
- camera_get_power_consumption() - If on, returns the power consumption with formula: consumption = base power ∗ resolution_factor
- camera_describe_device() - Returns all relevant information stored in the Camera instance formatted for human readability.

## STEP 02

### Management of the Smart House

**Objective:** Using Python dictionaries to create the object system and use it to create the required classes and objects.

### The Smart House Manager

- smart_house_management_new() - Constructs a new SmartHouseManagement Dictionary with its "_class" set to **SmartHouseManagement** 
- calculate_total_power_consumption(...) - Returns the sum of all power currently being consumed with instances Status = on. Can furthermore also discriminate by room or type:
  - search_type: Restricts output by subclass
  - search_room: Restricts output by matching string location
- get_all_device_description(...) - Returns the *describe_device* output for each subclass. Also can be filtered with *search_type* and *search_room*
- get_all_connected_devices(...) - Returns the connected *Thermostat* and *Camera* instances's *describe_device*. If no ip is provided all devices with ip attribute are called, otherwise only those with matching ip.

## STEP 03

### Testing Framework Design

We implemented our own testing framework without using external librarys as required in the assignment. It validates all methods and functionalities.

Automatic Test Discovery:

- Functions starting with 'test_' at the beginning are automatically detected using introspection.
- Only functions are executed, all not callable variables starting with 'test_' are ignored.
- Uses 'globals()' to find all test functions

Test execution flow:

1. Loop through all 'test_' functions
2. Run 'setUp()' before each test to create new device instances
3. Execute test function for each device in ALL_THINGS
4. Run 'tearDown()' after every test to clean up
5. Measure and report exection time

### Test States

There are three possible test states in the framework:
- Pass: Test executed successfully
- Fail: Test failed an assertion (AssertionError)
- Error: Test crashed with an exeption (Any other Exception)

### setUp() and tearDown()

**setUp()**
- Creates fresh instances of all device types
- Creates a SmartHouseManagement instance
- Appends ALL_THINGS list with the test devices
- Syncs ALL_THINGS locally and also with the smart_house file 

**tearDown()**
- Clears ALL_THINGS list in the test module and in the smart_house module
- Ensures a clean state for the next test

### Command Line Parameters

**--select <pattern>**
- Runs only tests that mach the specified pattern
- Example: 'python test_smart_house.py --select light' runs only ligth tests.

**--verbose-**
- Lists all variables starting with 'test_' and their types as well as the result of the test suite
- Demonstrates that only functions are executed, not variables

### Test Categories

**Device Tests:**
- test_toggle_status - Verifies on/off status switching

**Connectable Tests:**
- test_connect_ip - Verifies IP address storage
- test_connect_status - Verifies connection status update
- test_disconnect - Verifies disconnection functionality
- test_connected - Verifies is_connected() returns correct value

**Light Tests:**
- test_describe_light - Verifies correct description format
- test_get_power_consumption_light - Verifies power calculation formula
- test_toggle_status_light - Verifies toggle functionality

**Thermostat Tests:**
- test_describe_thermostat - Verifies description includes temperature info
- test_get_power_consumption_thermostat - Verifies power calculation based on temperature difference
- test_toggle_status_thermostat - Verifies toggle functionality
- test_set_target_temperature_thermostat - Verifies temperature can be set
- test_get_target_temperature_thermostat - Verifies temperature can be read

**Camera Tests:**
- test_describe_camera - Verifies description includes resolution
- test_get_power_consumption_camera - Verifies power calculation formula
- test_camera_resolution - Verifies resolution categorization (low/medium/high)
- test_toggle_status_camera - Verifies toggle functionality

**Management Tests:**
- test_total_power_consumption_management - Verifies total power calculation with and without filters (room, type)
- test_get_all_device_description_management - Verifies description retrieval with filtering
- test_get_all_connected_devices_management - Verifies connected device filtering (with/without IP)

### Why We Chose These Tests

**Coverage Strategy:**
- **Method Coverage** - Every method is tested
- **State Coverage** - Tests verify both "on" and "off" states
- **Inheritance Coverage** - Tests confirm inherited methods work correctly
- **Filter Coverage** - Tests validate all filter combinations (search_type, search_room, ip)
- **Edge Cases** - Tests also handle off devices, disconnected devices, and empty filters

**Example Reasoning:**
- test_get_power_consumption_light verifies the brightness formula and ensures off devices return string messages
- test_get_all_connected_devices_management validates that only on and connected devices are returned

### Test Output Format

```
toggle_status passed, ran in 0.000116s
connect_ip passed, ran in 0.000163s
...
Total Runtime: 0.002185s

99 PASSED:
['Bedtable Light passed toggle_status', ...]
0 FAILED:
[]
0 ERRORS:
[]
```

### Running the Tests
```bash
# Run all tests
python test_smart_house.py

# Run only light tests
python test_smart_house.py --select light

# Run only management tests
python test_smart_house.py --select management

# Verbose test mode (show all test_ variables)
python test_smart_house.py --verbose
```
