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

The prefix **do_** allows the interpreter to map operations names to their function.


### Design Decision for Step02 - Arrays and Sets in LGL

To implement array & set compatability into the interpreter we decided to utilise built-in python functions to do so. Additionaly, we stuck to the existing interpreter design, i.e., every function takes *args* & *envs* as parameters, thus allowing us to somewhat seamlessly integreate new data strucutes into the interpreter.

### Design Decision for Step03 - Functional Programming Elements

*Insert Here*


### Design Decisions for Step04 - Visualized Tracing

*Insert Here*