# HS25 SoCo Assignment 2 Group 69: LGL Interpreters

**Members:** Max Blöchlinger, Abraham Herzog, Luiz Hablützel

## Content

- **interpreter.py**
    [Step01-Step04]
    Implmentations of Mathematical Operations, Data structures, programming elements & Tracing  
- **extensions.lgl**
    [Step01]
    Implementations of 3 algorithms to test the Mathematical Operations of the Interpreter, with added output verification.
- **data_structures.lgl**
    [Step02]
    Checks wether arrays & sets behave correctly in the interpreter.
- **functional.lgl**
    [Step03]
    Implementation of algorithms to verify functional programming operations (map, reduce, filter) with output verification 
- **tracing.lgl**
    [Step04]



## Design Decisions for the Interpreter

### args & envs

As you will see, every function in the interpreter will take ``args`` & ``envs`` as arguments with the structure of **do_**operation(args, envs).

We felt this was necessary due to previous implementations already using this scheme and, therefore, allowed us to implement new data structures and operations in a concise and fashionable manner.

The ``args`` argument in every function usually contains what the user wants to do. If you want to multiply two numbers, that is where they are being sent into the function, e.g., 

```
def do_addieren(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left + right
```

As you can see, if we want to add two numbers, ``args`` are where these numbers are sent into and checked for their validty: ``assert len(args) == 2``

As for why ``envs`` can be found in every functions arguments is because, it is a list of dictionaries which allows for variable lookup and allowing a function to be limited to its scope.

In the **extensions.lgl** file we can see us setting a variable x: ``["set", "x", 10]`` which stores the variable as **envs = {"x": 10}**.

We could then call ``["get", "x"]``, which will lead to the interpreter to look up **x** in ``envs``.

### Structure of function **do_** prefix 

Every function in the interpreter starts with the **do_** prefix to create a less labour intensive alternative than manualy registering every function.

The interpreter finds all functions starting with **do_**, registers them automatically, removes the **do_** part of the function name and stores them in a dictionary.

So ``do_addieren`` is stored as ``addieren`` and can be called anytime as a function to add two numbers.

    
### Design Decisions for Step01 - Mathematical operations and Loops

Given the previous arithmetic operations already in the interpreter, we decided it would be best to keep the coherent design pattern. As such, we implemented the Arithmetic operations, Comparison operations & Boolean operations with the previous scheme in mind. 

**Arithmetic Operations**

**Multiplication: do_multiplication(args,env):**
- Takes two arguments and checks if the input is valid
- Returns the left argument multiplied by the right argument

**Division: do_division(args,env):**
- Takes two arguments and checks if the input is valid
- Returns the left argument divided by the right argument
- To handle *ZeroDivisionError* we implemented a try-except block which returns a tuple: (0, "Can't divide by zero") to warn the user

**Pow: do_pow(args,env):**
- Returns the left argument to the power of the right argument
- Also supports negative exponents

**Modulo: do_modulo(args,env):**
- Takes two arguments and checks if the input is valid
- Returns left % right
- To handle *ZeroDivisionError* we implemented a try-except block which returns a tuple: (0, "Can't divide by zero") to warn the user, same as in the Division Function

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

Furthermore, regarding the do... until loop, we intended to create it following natural do... while semantics. The loop will execute a body so long as the loop is untrue. Notably, for our Little German Language interpreter the syntax is distinct as in: instead of *do while* we used *do until* to adhere to given specifications.

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
- Implementation supports nested loops and can use any aformentioned operator; comparison, boolean, arithmetic.

**Syntax**

As seen beforehand in the structure of the **do... until** loop, functions usually expect 2 arguments to operate as expected and also checks for such:

``["lessThanEQ",4 , 3]`` --> 4 being the left argument and 3 being the right argument

``["multiplication",4 , 3]`` --> Evaluates to 12

This would be the expected syntax for every functions, except if specified differently, e.g., **do_NOT**.


### Design Decision for Step02 - Arrays and Sets in LGL

To implement array & set compatability into the interpreter we decided to utilise built-in python functions to do so. Additionaly, we stuck to the existing interpreter design, i.e., every function takes *args* & *envs* as parameters, thus allowing us to somewhat seamlessly integreate new data strucutes into the interpreter.

**Array Implementation**

**do_Array(args, envs):**
- Creates a new array with length that has been specified
- Takes only one argument, the length of the array

*Example:*

 ``["Array", 7]`` --> ``[0, 0, 0, 0, 0, 0, 0]``

**def do_ArrayGet(args, envs):**
- With this function we can retrieve a value, specified index, from an array of our choosing
- Takes two arguments: the array we want to retrieve and the index of said array

*Example:*

``["ArrayGet", ["get","A"], 1]`` --> Looks up array **A** and index **1** and fetches its value

*Error handling:*

- In case the the user inputs an invalid number, we return a **Index out of range** exception.
- We also check that the looked up data structure if of type array and return a string to warn the user incase it was not. This is done with ``assert isinstance()`` and its appropriate error handling.

**def do_ArraySet(args, envs):**
- With this function can set the value of an index in the array
- Takes 3 arguments, the array, index and value we want to set

*Example:*

``["ArraySet", ["get","A"], 0, 7]`` --> Here we lookup for array A, and insert 7 into index 0.

*Error Handling:*

Here we used the same idea like in **do_ArrayGet**. Check proper index value and wether the called array is of type array.

**def do_ArraySize(args, envs):**
- This function returns the length of the called array
- Only argument it takes is which array we want to retrieve

*Example:*

``["ArraySize", ["get","A"]]`` --> returns the size of the array.

*Error Handling:*

Here we assert wether the only one argument is sent in, the array, and wether we are looking for an array and not other data structures.

**def do_cat(args, envs):**
- This function concatenates two arrays
- Takes two arguments, *Two arrays* and appends them with the builtin python operator ``+``.

*Example:*

``["cat", ["get","A"], ["get","B"]]`` --> Appends the values of B to the right of A

*Error Handling:*

Here we check for both sent in arrays wether they are of type list:

``assert isinstance(Array1, list)``

``assert isinstance(Array2, list)``

**Set Implementation**

Sets use Python's built-in `set()` function, allowing us to maintain uniqueness, no duplicate values.

All set operations follow the pattern as previously seen in the arrays implementation

**do_CreateSet(args, envs):**
- Creates a new empty set
- Takes no arguments

*Example:* 

``["CreateSet"]`` --> Creates a new set **set()**

**do_SetInsert(args, envs):**
- This function inserts an element into the set
- It takes two arguments, the set we want to lookup, and the value we want to add

*Example:* 

``["SetInsert", ["get", "I"], 1]`` --> inserts 1 into set I

**do_SetContain(args, envs):**
- Checks wether an element exists in the set
- Again takes two arguments, the sent we want to use and the value to find
- Returns 1 if found, else 0

*Example:* 

``["SetContain", ["get", "I"], 3]]`` --> returns 1 if 3 is in set I


**do_SetSize(args, envs):**
- Returns the length of the set
- Takes one argument: the set

*Example:* 

``["SetSize", ["get", "I"]]`` --> returns the size

**do_SetMerge(args, envs):**
- Merges two sets 
- Takes two sets as arguments
- The function also makes sure that there are no duplicates in the newly created set

*Example:* 

``["SetMerge", ["get", "I"], ["get", "J"]]`` --> `{1, 2, 3, 4} | {1, 2, 20}` = `{1, 2, 3, 4, 20}`

*Error Handling:*

- The error handling for the set data structure follows a very similar principle to the one seen in *arrays*. If necessary, we usually check wether the amount of arguments sent into the function are correct:

``assert len(args) == 2``

and wether the correct data structure is referenced:

``assert isinstance(s, set)``


### Design Decision for Step03 - Functional Programming Elements

In order to implement and use *map, reduce & filter* it calls upon previously implemented functions which the user is free to choose from.


**do_map(args, envs):**
- This function essentially applies a specified function to every value in an array
- Thus it only takes 2 arguments: The Function to be mapped to every value and the array this process should be applied to

**Example:**

```
["set", "sq_func", ["func", ["n"], ["multiplication", ["get","n"], ["get","n"]]]],
["set", "Map_Output", ["map", ["get","A"], "sq_func"]]
```

This squares ``sq_func`` every value in array A

**Error Handling:**

We check wether both sent in arguments are of correct type and return a string if not:

``assert isinstance(a, list), "first arg must be array"``

``assert isinstance(f, str), "second arg must be a func"``


Furthermore, we also validate the amount of arguments to be 2

After checking if the sent in string is actually a string we also must check wether the interpreter can find the associated function:

``assert isinstance(f, list) and f[0] == "func", "{f} is not a function"``

**do_reduce(args, envs):**
- This function, for a given array, reduces it to one value, done with a function set by the user, e.g., if you send in ``do_addieren``, it will add the last two values together until the arrays consist of only 1 value. 
- Two arguments are accpeted, an array and a string function name

*Example:*

```
["set", "add_func", ["func", ["x", "y"], ["addieren", ["get","x"], ["get","y"]]]],
["set", "Reduce_Output", ["reduce", ["get","A"], "add_func"]]
```
--> For input array ``[1, 2, 3, 4, 15, 22, 34]`` the result would be ``81``

*Error Handling:*

Again, as seen previously we first check wether both arguments sent in are valid and if the string can be assigned to a function:

``assert isinstance(a, list), "first arg must be array"``

``assert isinstance(f, str), "second arg must be a func"``

``assert isinstance(f, list) and f[0] == "func", "{f} is not a function"``


**do_filter(args, envs):**
- The filter operation accepts an array and a function name, and produces a new array where only elements that satisfy the condition for the function to return true are present. 
- Two arguments accepted: an array and a function name as string

*Example:*
```
["set", "larger_ten_func", ["func", ["n"], ["greaterThan", ["get","n"], 10]]],
["set", "Filtered_Array", ["filter", ["get","A"], "larger_ten_func"]]
```
--> For input array ```[1,2,3,4,15,16]``` this would return ```[15,16]```, only values larger than 10:  ``larger_ten_func``

*Error Handling:*

Same principle as for *reduce* and *map*: We first check wether both arguments sent in are valid and if the string can be assigned to a function.


### Design Decisions for Step04 - Visualized Tracing

*Insert Here*

### LLM Decleration

*Insert Here*