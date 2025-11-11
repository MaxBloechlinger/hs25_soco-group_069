# HS25 SoCo Assignment 2 Group 69: LGL Interpreter

**Members:** Max Blöchlinger, Abraham Herzog, Luiz Hablützel

## Content

- **interpreter.py**
  [Step01-Step04]
  Implementations of Mathematical Operations, Data Structures, programming elements & tracing
- **extensions.lgl**
  [Step01]
  Implementations of 3 algorithms to test the Mathematical Operations of the Interpreter, with added output verification.
- **data_structures.lgl**
  [Step02]
  Checks whether arrays & sets behave correctly in the interpreter.
- **functional.lgl**
  [Step03]
  Implementations of algorithms to verify functional programming operations (map, reduce, filter) with output verification
- **tracing.lgl**
  [Step04]
  Implementation of tracing in the interpreter, enabling visual tracing functionality

## Usage Examples

_Run one of the following lines in your terminal:_

`python interpreter.py extensions.lgl`

`python interpreter.py data_structures.lgl`

`python interpreter.py functional.lgl`

```
Example:
run 'python interpreter.py extensions.lgl'

Output:
0       # 2 % 2
2       # subtrahieren loop
10      # addieren loop
8       # double loop
2.5     # half loop
10      # x
False   # 10 < 3
True    # 10 > 3
False   # 10 <= 3
True    # 10 >= 3
False   # 10 == 3
True    # 10 != 3
1       # 10 and 3
1       # 10 or 3
0       # not 10
5.0     # 10 / 2
0.0     # 10 to power of -2
0       # 10 % 2
False   # 4 <= 3
#block appears twice
>>> None
[{'i': 8, 'j': 2.5, 'x': 10, 'y': 55}]
>>> None
[{'i': 8, 'j': 2.5, 'x': 10, 'y': 55}]

```

## Design Decisions for the Interpreter

### args & envs

As you will see, every function in the interpreter will take `args` & `envs` as arguments with the structure of \_do\_\_ operation(args, envs).

We felt this was necessary due to previous implementations already using this scheme and, therefore, allowed us to implement new data structures and operations in a concise and consistent manner.

The `args` argument in every function usually contains what the user wants to do. If you want to multiply two numbers, that is where they are being sent into the function, e.g.,

```
def do_addieren(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left + right
```

As you can see, if we want to add two numbers, `args` are where these numbers are sent into and checked for their validity: `assert len(args) == 2`

As for why `envs` can be found in every functions arguments is because, it is a list of dictionaries which allows for variable lookup and allowing a function to be limited to its scope.

In the **extensions.lgl** file we can see us setting a variable x: `["set", "x", 10]` which stores the variable as **envs = {"x": 10}**.

We could then call `["get", "x"]`, which will lead to the interpreter to look up **x** in `envs`.

### Structure of function **do\_** prefix

Every function in the interpreter starts with the **do\_** prefix to create a less labour intensive alternative than manually registering every function.

The interpreter finds all functions starting with **do\_**, registers them automatically, removes the **do\_** part of the function name and stores them in a dictionary.

So `do_addieren` is stored as `addieren` and can be called anytime as a function to add two numbers.

### Design Decisions for Step01 - Mathematical operations and Loops

Given the previous arithmetic operations already in the interpreter, we decided it would be best to keep the coherent design pattern. As such, we implemented the Arithmetic operations, Comparison operations & Boolean operations with the previous scheme in mind.

**Arithmetic Operations**

**Multiplication: do_multiplication(args,env):**

- Takes two arguments and checks if the input is valid
- Returns the left argument multiplied by the right argument

**Division: do_division(args,env):**

- Takes two arguments and checks if the input is valid
- Returns the left argument divided by the right argument
- To handle _ZeroDivisionError_ we implemented a try-except block which returns a tuple: (0, "Can't divide by zero") to warn the user

**Pow: do_pow(args,env):**

- Returns the left argument to the power of the right argument
- Also supports negative exponents

**Modulo: do_modulo(args,env):**

- Takes two arguments and checks if the input is valid
- Returns left % right
- To handle _ZeroDivisionError_ we implemented a try-except block which returns a tuple: (0, "Can't divide by zero") to warn the user, same as in the Division Function

**Comparison Operations:**

- The comparison Operations all follow the same structure, take two arguments, evaluate them and return the given comparison which was called:
- **do_lessThan(args,env):** (`<`) - Returns `left < right`
- **do_greaterThan(args,env):** (`>`) - Returns `left > right`
- **do_lessThanEQ(args,env):** (`<=`) - Returns `left <= right`
- **do_greaterThanEQ(args,env):** (`>=`) - Returns `left >= right`
- **do_EQ(args,env):** (`==`) - Returns `left == right`
- **do_notEQ(args,env):** (`!=`) - Returns `left != right`

**Boolean Operations**

- Similarly to the Comparison Operators, most functions follow the same layout, except **do_NOT** which takes only one and evaluates its truthiness.
- **do_AND(args,env):** (`&&`) - Returns `1 if left and right else 0`
- **def do_OR(args,env):** (`||`) - Returns `1 if left or right else 0`
- **do_NOT(args,env):** (`!`) - Returns `0 if x else 1`

**Loop Implementation**

Furthermore, regarding the do... until loop, we intended to create it following natural do... while semantics. The loop will execute a body so long as the loop is untrue. Notably, for our Little German Language interpreter the syntax is distinct as in: instead of _do while_ we used _do until_ to adhere to given specifications.

**Structure:**

```
["do",
    ["operation"],
    ["until", ["condition"]]
]
```

**Implementation**

- Takes two arguments (args, envs) --> do_do(args, envs):
- Uses a `while True` loop and evaluates each iteration, (until condition), and breaks loop if said condition is true
- Implementation supports nested loops and can use any aforementioned operator; comparison, boolean, arithmetic.

**Syntax**

As seen beforehand in the structure of the **do... until** loop, functions usually expect 2 arguments to operate as expected and also checks for such:

`["lessThanEQ",4 , 3]` --> 4 being the left argument and 3 being the right argument, evaluates to 7

`["multiplication",4 , 3]` --> Evaluates to 12

This would be the expected syntax for every functions, except if specified differently, e.g., **do_NOT**.

### Design Decision for Step02 - Arrays and Sets in LGL

To implement array & set compatability into the interpreter we decided to utilise built-in python functions to do so. Additionaly, we stuck to the existing interpreter design, i.e., every function takes _args_ & _envs_ as parameters, thus allowing us to somewhat seamlessly integreate new data strucutes into the interpreter.

**Array Implementation**

**do_Array(args, envs):**

- Creates a new array with length that has been specified by the user
- Takes only one argument, the length of the array

_Example:_

`["Array", 7]` --> `[0, 0, 0, 0, 0, 0, 0]`

**def do_ArrayGet(args, envs):**

- With this function we can retrieve a value, specified index, from an array of our choosing
- Takes two arguments: the array we want to retrieve and the index of said array

_Example:_

`["ArrayGet", ["get","A"], 1]` --> Looks up array **A** and index **1** and fetches its value

_Error handling:_

- In case the the user inputs an invalid number, we return a **Index out of range** exception.
- We also check that the looked up data structure if of type array and return a string to warn the user incase it was not. This is done with `assert isinstance()` and its appropriate error handling.

**def do_ArraySet(args, envs):**

- With this function, we can set the value of an index in the array
- Takes 3 arguments, the array, index and value we want to set

_Example:_

`["ArraySet", ["get","A"], 0, 7]` --> Here we lookup array A, and insert 7 into index 0.

_Error Handling:_

Here we used the same idea like in **do_ArrayGet**. Check proper index value and wether the called array is of type array.

**def do_ArraySize(args, envs):**

- This function returns the length of the called array
- Only argument it takes is which array we want to retrieve

_Example:_

`["ArraySize", ["get","A"]]` --> returns the size of the array.

_Error Handling:_

Here we assert wether the only one argument is sent in, the array, and wether we are looking for an array and not other data structures.

**def do_cat(args, envs):**

- This function concatenates two arrays
- Takes two arguments, _Two arrays_, and appends them with the builtin python operator `+`.

_Example:_

`["cat", ["get","A"], ["get","B"]]` --> Appends the values of B to the right of A

_Error Handling:_

Here we check for both sent in arrays wether they are of type list:

`assert isinstance(Array1, list)`

`assert isinstance(Array2, list)`

**Set Implementation**

Sets use Python's built-in `set()` function, allowing us to maintain uniqueness, no duplicate values.

All set operations follow the pattern as previously seen in the arrays implementation

**do_CreateSet(args, envs):**

- Creates a new empty set
- Takes no arguments

_Example:_

`["CreateSet"]` --> Creates a new set **set()**

**do_SetInsert(args, envs):**

- This function inserts an element into the set
- It takes two arguments, the set we want to lookup, and the value we want to add

_Example:_

`["SetInsert", ["get", "I"], 1]` --> inserts 1 into set I

**do_SetContain(args, envs):**

- Checks wether an element exists in the set
- Again takes two arguments, the sent we want to use and the value to find
- Returns 1 if found, else 0

_Example:_

`["SetContain", ["get", "I"], 3]]` --> returns 1 if 3 is in set I

**do_SetSize(args, envs):**

- Returns the length of the set
- Takes one argument: the set

_Example:_

`["SetSize", ["get", "I"]]` --> returns the size

**do_SetMerge(args, envs):**

- Merges two sets
- Takes two sets as arguments
- The function also makes sure that there are no duplicates in the newly created set

_Example:_

`["SetMerge", ["get", "I"], ["get", "J"]]` --> `{1, 2, 3, 4} | {1, 2, 20}` = `{1, 2, 3, 4, 20}`

_Error Handling:_

- The error handling for the set data structure follows a very similar principle to the one seen in _arrays_. If necessary, we usually check wether the amount of arguments sent into the function are correct:

`assert len(args) == 2`

and wether the correct data structure is referenced:

`assert isinstance(s, set)`

### Design Decision for Step03 - Functional Programming Elements

In order to implement and use _map, reduce & filter_ it calls upon previously implemented functions which the user is free to choose from.

**do_map(args, envs):**

- This function essentially applies a specified function to every value in an array
- Thus it only takes 2 arguments: The Function to be mapped to every value and the array this process should be applied to

**Example:**

```
["set", "sq_func", ["func", ["n"], ["multiplication", ["get","n"], ["get","n"]]]],
["set", "Map_Output", ["map", ["get","A"], "sq_func"]]
```

This squares, `sq_func`, every value in array A

**Error Handling:**

We check wether both sent in arguments are of correct type and return a string if not:

`assert isinstance(a, list), "first arg must be array"`

`assert isinstance(f, str), "second arg must be a func"`

Furthermore, we also validate the amount of arguments to be 2

After checking if the sent in string is actually a string we also must check wether the interpreter can find the associated function:

`assert isinstance(f, list) and f[0] == "func", "{f} is not a function"`

**do_reduce(args, envs):**

- This function, for a given array, reduces it to one value, done with a function set by the user, e.g., if you send in `do_addieren`, it will add the last two values together until the arrays consist of only 1 value.
- Two arguments are accpeted, an array and a string function name

_Example:_

```
["set", "add_func", ["func", ["x", "y"], ["addieren", ["get","x"], ["get","y"]]]],
["set", "Reduce_Output", ["reduce", ["get","A"], "add_func"]]
```

--> For input array `[1, 2, 3, 4, 15, 22, 34]` the result would be `81`

_Error Handling:_

Again, as seen previously we first check wether both arguments sent in are valid and if the string can be assigned to a function:

`assert isinstance(a, list), "first arg must be array"`

`assert isinstance(f, str), "second arg must be a func"`

`assert isinstance(f, list) and f[0] == "func", "{f} is not a function"`

**do_filter(args, envs):**

- The filter operation accepts an array and a function name, and produces a new array where only elements that satisfy the condition for the function to return true are present.
- Two arguments accepted: an array and a function name as string

_Example:_

```
["set", "larger_ten_func", ["func", ["n"], ["greaterThan", ["get","n"], 10]]],
["set", "Filtered_Array", ["filter", ["get","A"], "larger_ten_func"]]
```

--> For input array `[1,2,3,4,15,16]` this would return `[15,16]`, only values larger than 10: `larger_ten_func`

_Error Handling:_

Same principle as for _reduce_ and _map_: We first check wether both arguments sent in are valid and if the string can be assigned to a function.

### Design Decisions for Step04 - Visualized Tracing

We designed our tracing component with an object-oriented dual system in mind. After things became complex with global variables tracing the runtime across the interpreter, we decided to simplify the process by encapsulating all tracing funcationalities in a `Tracer` class. Everytime a program is executed, the interpreter initializes a `Tracer` object that internally manages two lists: one for function calls and one for the stack.

- The calls list acts as a history of all function invocations. Each entry stores the `function name`, its `depth`, the `start_time` and the measured `duration` in a dictionary. This list ist later used to reconstruct the tree calls for visualization.

- The stack list represents the current runtime state. Functions are pushed onto it when entered and popped off when exited so we can calculate durations precisely.

By splitting these tasks, the `tracer` can be both accurate while running (using the stack) and clear afterwards (using the call list). This mix gives a simple and clean structure and it avoids using global stuff and makes the tracing logic easier to reuse and keep tidy.

To turn `tracing` on, we added a command line flag `--trace`. When the interpreter starts, it checks for this flag and if it’s there, switches from normal mode to tracing mode. In tracing mode it prints the full call tree with indentation and timing info. To make sure it always finds the right file, we used a small list comprehension that filters out the `--trace` flag before loading the file. That way, extra flags don’t confuse the argument parsing.

We also decided that tracing shouldn’t just work for user-made functions, but also for some built-in ones. For example, the built-in `do_print` function now appears in the trace tree too. This helps show the full picture of what happens from calculations to the final output.

Execution times are shown in milliseconds as floating-point numbers with two decimal places. We chose that format because whole milliseconds often looked just like zeros. Floats make even short calls visible and make it easier to spot small timing differences between functions.

_Example_

`python interpreter.py --trace tracing.lgl`

```

```

### LLM Declaration

**Prompts Used by Luiz Hablützel:**

- Why is my trace tree showing the print function at the start instead of at the end? **I inserted a snippet from the do_print function**
- Does this LGL file implement the same functionality as the pseudocode program? **I wanted to make sure that I implemented the same code as in the assignment**
- Check this README snippet for grammar mistakes
  **I wanted to avoid grammar mistakes, because my English is error-prone**

**Prompts Used by Abraham Herzog:**

- Why does this not work? **I inserted a snippet from an lgl file, there was a comma missing**
- Check for grammar mistakes **This I used for the readme to avoid any common spelling mistakes**

**Prompts used by Max Blöchlinger**

- "Why are there silent errors when using json in .lgl files?"
- "is using a built in python for loop allowed for this task? (pasted do while task) explain, no code"
- "what is a code tracer?"
- "can i implement a tracer like testing with setup() and teardown()?"
- "REDUCE array add is just like the sum() func in python right?"
- "do these methods work and adhere to the task? no soluion only feedback"
- "we forgot to change the german funcs before can we just leave it?"
- "is there a way to let my ide show errors in json .lgl files?"
- "please explain what they want in this task (map) in socratic style"
- "here's an overview of the current task can we just use this code (class code) as a blueprint for the other methods?"
- "my friend wants to do a tracer in oop style i think name == main with setup teardown is better help (pasted the task)"
