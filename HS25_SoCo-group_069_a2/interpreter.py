import sys
import json
import pprint

env = dict()

# --------------------[Class Operations] --------------------

def do_set(args,envs):
    assert len(args) == 2
    assert isinstance(args[0],str)
    var_name = args[0]
    var_value = do(args[1],envs)
    env_set(var_name,var_value,envs)
    return var_value

def env_set(name,value,envs):
    assert isinstance(name,str)
    envs[-1][name] = value
    
def do_get(args,envs):
    assert len(args) == 1
    assert isinstance(args[0],str)
    var_name = args[0]
    return env_get(var_name,envs)
    #assert args[0] in env, f"Unknown variable {args[0]}"
    #return env[args[0]]

def env_get(name,envs):
    assert isinstance(name,str)
    # envs = [{"same":["func",...]},{"num":3}]
    # we do dynamic scoping
    for env in reversed(envs):
        if name in env:
            return env[name]
    assert False, f"Unknown variable {name}"

def do_seq(args,env):
    # ["addieren", 2, 3], ["addieren", 4, 5]
    for each_ops in args:
        res = do(each_ops,env)
    return res

def do_addieren(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left + right

def do_absolutewert(args,env):
    assert len(args) == 1
    value = do(args[0],env)
    if value >= 0:
        return value
    return -value

def do_subtrahieren(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left - right

def do_print(args, envs):
    values = [do(a, envs) for a in args]
    print(*values)
    return None

def do_func(args, env):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["func",params,body]

# --------------------[Arithmetic Operations] --------------------

def do_multiplication(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left * right

def do_division(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    try:
        return left / right
    except ZeroDivisionError:
        return 0, "Can't divide by zero"
def do_pow(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left ** right

def do_modulo(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    try:
        return left % right
    except ZeroDivisionError:
        return 0, "Can't divide by zero"

# --------------------[Comparison Operations] --------------------

def do_lessThan(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left < right

def do_greaterThan(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left > right

def do_lessThanEQ(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left <= right

def do_greaterThanEQ(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left >= right

def do_EQ(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left == right

def do_notEQ(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left != right

# --------------------[Boolean Operations] --------------------

def do_AND(args,env):
    assert len(args) == 2
    left = do(args[0], env)
    right = do(args[1], env)
    assert left in [0,1] and right in [0,1]
    return 1 if left and right else 0

def do_OR(args,env):
    assert len(args) == 2
    left = do(args[0], env)
    right = do(args[1], env)
    assert left in [0,1] and right in [0,1]
    return 1 if left or right else 0

def do_NOT(args,env):
    assert len(args) == 1
    x = do(args[0], env)
    assert x in [0,1]
    return 0 if x else 1


# --------------------[Boolean Operations] --------------------

#example:

"""
[
    "seq",
    ["set", "x", 1],
    ["do",
        ["set", "x", ["multiplication", ["get", "x"], 2]],
        ["until", ["greaterThanEQ", ["get", "x"], 8]]
    ],
    ["print", ["get", "x"]]
]
"""

def do_do(args, envs):
    assert len(args)==2, "body and/or until condition missing"
    body = args[0]
    until = args[1]
    assert until[0] == "until", "second arg must contani until"

    while True:
        if isinstance(body,list):
            do(body, envs)
        if do(until[1], envs):
            break

# ["call",
#   "same", 3]
def do_call(args,envs):
    assert len(args) >= 1
    assert isinstance(args[0],str)
    name_func = args[0] #same
    values = [do(a,envs) for a in args[1:]] #[3]

    func = env_get(name_func,envs) # ["func",["num"],["get","num"]]
    assert isinstance(func,list) and (func[0] == "func")
    params = func[1]
    body = func[2]
    assert len(values) == len(params), f"You passed {len(values)} parameters instead of {len(params)}"

    local_env = dict() 
    # params = ["num","num2"]
    # values = [3,4]
    # {"num":3, "num2":4}
    for index,param_name in enumerate(params):
        local_env[param_name] = values[index]
    envs.append(local_env)
    result = do(body,envs) #["get","num"]
    envs.pop()

    return result



# {"addieren":do_addieren,
#  "absolutewert":do_absolutewert, 
#  "set":do_set,
#  ...}
OPS = {
    name.replace("do_",""): func
    for (name,func) in globals().items()
    if name.startswith("do_")
}

# OPS_EASY = {}
# for (name,func) in globals().items():
#     if name.startswith("do_"): #do_addieren
#         operation_name = name.replace("do_","") # addieren
#         OPS_EASY[operation_name] = func # "addieren" : do_addieren


def do(program,envs):  # ["addieren",1,2]
    if isinstance(program,int):
        return program
    assert program[0] in OPS, f"Unkown operation {program[0]}"
    func = OPS[program[0]]
    return func(program[1:],envs)



def main():
    filename = sys.argv[1]
    with open(filename,'r') as f:
        program = json.load(f)
        envs = [dict()] 
        result = do(program,envs)
    print(">>>" , result)
    pprint.pprint(envs)

if __name__ == '__main__':
    main()