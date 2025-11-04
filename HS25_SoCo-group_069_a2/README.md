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
    
**Design Decisions for Step01 - Mathematical operations, boolean expressions and operations, and
do ... until loop in LGL**

Given the previous arithmetic operations already in the interpreter, we decided it would be best to keep the coherent design pattern. As such, we implemented the Arithmetic operations, Comparison operations & Boolean operations with the previous scheme in mind. 

Furthermore, regarding the do... until loop, we intended to create it following natural do... while semantics. The loop will execute a body so long as the loop is untrue. Notably, for our Little German Language interpreter the syntax is distinct as in: instead of *do while* we used *do until* to adhere to given specifications.

**Design Decision for Step02 - Arrays and Sets in LGL**

To implement array & set compatability into the interpreter we decided to utilise built-in python functions to do so. Additionaly, we stuck to the existing interpreter design, i.e., every function takes *args* & *envs* as parameters, thus allowing us to somewhat seamlessly integreate new data strucutes into the interpreter.

**Design Decision for Step03 - Functional Programming Elements**

*Insert Here*

