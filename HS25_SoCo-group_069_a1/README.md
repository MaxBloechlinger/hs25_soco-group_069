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

- We implemented a _class_ system without actually using classes, only plain dictionaries as this was a given requirement for the assignment.

**The Class Dictionaries**

- They define the methods of the object and have attribute: "\_new" which references the constructor for new instances
- Can have a "\_parent" (or multiple)

**Instance Dictionaries**

- Stores the given information/ state of the object and has a "\_class" attribute which points to the "\_class" dictionary.

### Methods Calls

- **constructor: make(cls, \*args, \*\*kwargs)**
  Calls the '\_new' method defined in the class dictionary of 'cls' to create an object instance. If called, it also adds the instances to the global _ALL_THINGS_ list.
- **call function: call(thing, method_name, \*args, \*\*kwargs)**
  Uses find() function to locate correct method in current or parent class dictionary
- **find function: find(cls, method_name)**
  Recursively searches for the method provided by call().
  If the current class dictionary did not implement the method find() searches in the parent class dictionary

  **Why we chose this design** - We tried to adhere as closely to the given format and outline defined in the book: _Software Design by Example, Chapter 2_

### Multiple Inheritance Implementation

- We achieved this in our find() functions by checking whether _"\_parent"_ has len >= 2 which then iterates through the list with a try, except block
- Will raise NotImplementedError if no _"\_parent"_ can be found
- Is relatively simple and allows for Camera & Thermostat to inherit from both Device and Connectable

### Smart House Manager

- The approach we took here is that the Smart House Manager will scan the globally instantiated ALL_THINGS list where all devices should be stored.
- This allows us to track all instantiated devices and creates a broader scope for the project if more devices would want to be added.
- It can also be filtered with search_type and search_room if a user wants to only look up specific rooms and/or devices
- As per specifications "Use named keyword arguments '\*\*kwargs' to allow for selecting devices of a specific type, or located in a specific room" which we implemented into the call(...) function so if a None argument were sent into the call(...) function, it would still work, or if chosen to discriminate by device/ room a user could also choose such.

### Error Handling

- In case the abstract "Device" methods were not to be implemented or missing we created a _raise NotImplementedError_ block
- The same goes for the _find()_ function, if no parent or method can't be found we raise a _NotImplementedError_
- The Management Methods, _(defined below)_, ignores attributes like status, which stem from non-device objects - Smart House Management instances - as to not call Smart House Management methods on itself.
- When devices are off we wanted to return a string message - seen in the _get_power_consumption_ methods, to create a more friendly and clear message, instead of a 0.

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
- device_new(...) - Constructs a new dictionary, an instance of Device. "\_class" is Device

### Connectable Parent Class

Attributes:

- Connected, ip

Methods:

- connect(ip) Sets the status of connected to **True** and stores the ip address
- disconnect() Sets the status of connected to **False**
- is_connected() - Returns the status of the connection
- connectable_new(...) Constructs a new dictionary, an instance of Connectable. "\_class" is Connectable

### Light Subclass

Attributes:

- Inherits all Attributes from Device and has additional attribute brightness

Methods:

- light_new(...) - Constructs a new instance with its "\_class" set to Light and "\_parent" set to **Device**
- light_describe_device() - Returns all relevant information stored in the Light instance formatted for human readability.
- light_get_power_consumption() - If on, returns the power consumption with formula: round(base_power\*(brightness / 100)). Otherwise returns a string indicating the device is off.

### Thermostat Subclass

Attributes:

- Inherits both from Device and Connectable and has additional attributes room_temperature & target_temperature

Methods:

- thermostat_get_power_consumption() - If on, returns the power consumption with formula: round(base_power \* abs(target_temperature - room_temperature))
- thermostat_describe_device() - Returns all relevant information stored in the Thermostat instance formatted for human readability.
- set_target_temperature(new_temperature) - Sets the temperature the instance should adopt
- get_target_temperature() - Returns the set target temperature of the instance
- thermostat_new(...) - Constructs a new instance with its "\_class" set to Thermostat and "\_parent" set to [**Device**, **Connectable**]

### Camera Subclass

Attributes:

- Inherits both from Device and Connectable and has additional attribute resolution_factor which can be low, medium or high after computation.

Methods:

- camera_new(...) - Constructs a new instance with its "\_class" set to Camera and "\_parent" set to [**Device**, **Connectable**]
- camera_get_power_consumption() - If on, returns the power consumption with formula: consumption = base power ∗ resolution_factor
- camera_describe_device() - Returns all relevant information stored in the Camera instance formatted for human readability.

## STEP 02

### Management of the Smart House

**Objective:** Using Python dictionaries to create the object system and use it to create the required classes and objects.

### The Smart House Manager

- smart_house_management_new() - Constructs a new SmartHouseManagement Dictionary with its "\_class" set to **SmartHouseManagement**
- calculate_total_power_consumption(...) - Returns the sum of all power currently being consumed with instances Status = on. Can furthermore also discriminate by room or type:
  - search_type: Restricts output by subclass
  - search_room: Restricts output by matching string location
- get*all_device_description(...) - Returns the \_describe_device* output for each subclass. Also can be filtered with _search_type_ and _search_room_
- get*all_connected_devices(...) - Returns the connected \_Thermostat* and _Camera_ instances's _describe_device_. If no ip is provided all devices with ip attribute are called, otherwise only those with matching ip.

## STEP 03

### Testing Framework Design

We implemented our own testing framework without using external libraries as required in the assignment. It validates all methods and functionalities.

Automatic Test Discovery:

- Functions starting with 'test\_' at the beginning are automatically detected using introspection.
- Only functions are executed, non callable variables starting with 'test\_' are ignored.
- Uses 'globals()' to find all test functions

Test execution flow:

1. Loops through all 'test\_' functions
2. Runs 'setUp()' before each test to create a new device instances
3. Executes test functions for each device in ALL_THINGS
4. Runs 'tearDown()' after every test to clean up
5. Measures and reports execution time

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

- Clears ALL_THINGS list in the test file and in the smart_house file
- Ensures a clean state for the next test

### Command Line Parameters

**--select <pattern>**

- Runs only tests that match the specified pattern
- Example: 'python test_smart_house.py --select light' runs only light tests.

**--verbose**

- Lists all variables starting with 'test\_' and their types as well as the result of the test suite
- Demonstrates that only functions are executed and not variables

### Test Categories

**Device Tests:**

- test_toggle_status - Verifies on/off status switching

**Connectable Tests:**

- test_connect_ip - Verifies IP address storage
- test_connect_status - Verifies connection status update
- test_disconnect - Verifies disconnection functionality
- test_connected - Verifies is_connected() returns correct value

_For the Device and Connectable Tests (Camera & Thermostat) we split all tests into the respective subclasses so "--select" would work correctly_

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
-----------------------------------------------------------------
toggle_status passed, ran in 0.000116s
-----------------------------------------------------------------
connect_ip passed, ran in 0.000163s
-----------------------------------------------------------------
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

# Run only thermostat tests + Verbose mode
python test_smart_house.py --select thermostat --verbose
```

## Use of Generative Ai

### Scope and use of Generative Ai

- We restricted our use of LLMs to the extent warranted by the assignments outline.
- LLMs were mostly used as tutors and assistants to understand concepts or clarify specifications. Meaning, we used Claude and ChatGPT to either explain why or how and implementation would work and wether our implementation was functioning as we intended.
- The final code was written and reviewed only by the authors of the Project and no code was taken directly from LLMs.

### Prompts - ChatGPT & Claude

**Prompts Used by Luiz Hablützel:**

- “I get a KeyError when I try to access a device in ALL_THINGS — how can I fix this?”
- “Why does my test fail when I call get_power_consumption on an off device?”
- “How can I refactor SmartHouseManagement so it doesn’t rely on ALL_THINGS but still finds all devices?”
- “How do I avoid merge conflicts when I reset my branch to match remote?”
- “Why is my test not running? It’s named correctly but doesn’t execute.”
- “How can I validate that my introspection with globals() is working correctly?”
- "Check for correct formatting and grammar in the readme testing framework section"

**Prompts Used by Abraham Herzog:**

- Compare the readme.me file with both python files regarding the content and give a descriptive feedback
- Given asg01(Project 1 File), how does our implementation look like - _all files were uploaded to the LLM here_
- Read the asg01 File (Project 1 File) and create bullet points and a step by step guide to approach this project

I also asked ChatGPT: can you check chat history or other histories and show me the prompts I used or might have used regarding this asg01 project

- 2025-10-12 13:00
  “This is the description get_all_connected_devices(ip=None)… [spec text] … Here’s my function …”
  → You asked for alignment of your implementation with the spec and correctness of the filter/return shape.
- 2025-10-11 17:00
  “SyntaxError: f-string: expecting '}' on smart_house.py, line 223.”
  → Classic nested f-string problem you wanted fixed.
- 2025-10-14 13:00
  “I get this output … Is this the expected output?”
  → You wanted confirmation that the test printout was normal.
- 2025-10-14 ~13:00
  “How can I measure the time the test took? perf_counter vs perf_counter_ns.”
- 2025-10-21 ~10:10
  “Does the current README accurately describe smart_house.py behavior?”
- 2025-10-17 ~15:00
  “Given \_parent = [Device, Connectable], does my find search left-to-right and stop at the first implementation?”

  _Disclaimer:_ The given time and dates by ChatGPT might not be very accurate

**Prompts used by Max Blöchlinger**

- "my teammates changed the way the custom dictionary objects are kept track ofagain as u can see in the "new" files. tell me exactly if it works the same way and what they changed"

- “Can you explain how to implement inheritance using Python dictionaries without using class, and how find() and call() should handle multiple parents?”

- "should the \_new function be specific to each subclass?"

- “What’s the cleanest way to keep track of all created smart house devices using a global list like ALL_THINGS, and how do I avoid duplicate entries during tests?”

- “How can I automatically discover and run all functions starting with test\_ without using unittest or pytest, and show pass/fail/error states?”

- “How do I use argparse to add a --select option so that only tests containing a certain word like light are executed?”

- “If my make() function automatically appends objects to ALL_THINGS, do i need to change anything in my test setup so the output matches the old version?”

- “can you explain again if this inheritance works with dictionary objects.”

- "can you check if the calculate_total_power_consumption func fulfills the assignment?"

- “so my teammates changed how ALL_THINGS is tracked, can you tell me if it still works the same and what i may need to look at?”

- “what's typically done in a setup() and teardown function for custom testing?”

- "why do I need to clear both ALL_THINGS lists if they’re referencing the same thing?

- “what ways are there to add a --select argument so i can just run light tests for lights or thermostattest for thermostats in the terminal?”

- “duplicates appear in ALL_THINGS after multiple test runs, how do i properly clear or handle that so the power output stays the same?”

- "i feel we should check for duplicates to be safe in the make() func what do you think?"

- "how can i make the passed tests prints prettier?"

- "do these files (all files) fulfill the assignment (asg01.pdf)?"
