#!/usr/bin/env python3

import doctest
import sys

sys.setrecursionlimit(10_000)

# NO ADDITIONAL IMPORTS!

#############################
# Scheme-related Exceptions #
#############################

class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """
    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """
    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """
    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """
    pass

########################
# ENVIRONMENT DIAGRAMS #
########################
class Frame():
    
    def __init__(self, var_val_mapping={}, parent_frame=None):
        self.mapping = var_val_mapping
        self.parent_frame = parent_frame
    
    def get_value(self, var_name):
  
        # checks if there is a value binded to a variable name
        if var_name in self.mapping:
            return self.mapping[var_name]
        
        # checks if there is a parent frame
        elif self.parent_frame is not None:
            return self.parent_frame.get_value(var_name)
        
        # no parent frame with variable name inside it 
        else:
            raise SchemeNameError
            
    def set_value(self, var_name, var_value):
        self.mapping[var_name] = var_value
        
    def update_value(self, var_name, var_value):
        # checks if there is a value binded to a variable name
        if var_name in self.mapping:
            self.mapping[var_name] = var_value
        
        # checks if there is a parent frame
        elif self.parent_frame is not None:
            self.parent_frame.update_value(var_name, var_value)
        
        # no parent frame with variable name inside it 
        else:
            raise SchemeNameError    

############
# FUNCTION #
############
class Function():
    
    def __init__(self, parameters, parsed_expression, frame):
        """
        Initialize the user defined function
        """
        self.parameters = parameters # list of variable names
        self.expression = parsed_expression # expression to 
        self.enclosing_frame = frame
    
    def __call__(self, arguments):
        """
        Call the user defined function and evaluate it
        """
        # checks if you have more or less arguments 
        # passed in then required for function call
        if len(arguments) != len(self.parameters):
            raise SchemeEvaluationError
        
        #if arguments
        function_frame = Frame(
            {param:arg for param, arg in zip(self.parameters, arguments)},
            self.enclosing_frame)
        
        return evaluate(self.expression, function_frame)

######################
# LINKED LISTS' NODE #
######################
class Pair():
    
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
        
############################
# Tokenization and Parsing #
############################

def number_or_symbol(x):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x

def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    valid_tokens = []
    valid_char = ""   # multi-character valid token
    comment_present = False
    
    # goes through each character in string to see if its a valid token
    for char in source: 
        
        # checks for the end of a comment
        if char == "\n":
            if valid_char != "":
                valid_tokens.append(valid_char)
            valid_char = ""
            comment_present = False
            # skips to next character
            continue
        
        # checks for a comment
        elif char == ";" or comment_present:
            if valid_char != "":
                valid_tokens.append(valid_char)
            valid_char = ""
            comment_present = True
            # skips to next character
            continue
        
        # skips spaces
        elif char == " ":
            if valid_char != "":
                valid_tokens.append(valid_char)
            valid_char = ""
            continue
        
        # checks for valid parentheses token
        elif char == "(":
            valid_tokens.append(char)
        
        elif char == ")":
            if valid_char != "":
                valid_tokens.append(valid_char)
            valid_tokens.append(char)
            valid_char = ""
        
        # assumes you are building up a token
        else:
            valid_char += char
    
    # checks if no spaces present in input string
    if char != ")" and valid_char != "":
        valid_tokens.append(valid_char)
            
    # returns a list of all valid tokens  
    return valid_tokens

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    parentheses = []
    left_paren = 0
    right_paren = 0
    
    # throw scheme syntax error if the tokenized 
    # list does not have valid expression
    for element in tokens:
        if element == "(":
            left_paren +=1
            parentheses.append(element)
        
        # checks for valid closing expression
        # no double right parenth
        elif element == ")" :
            right_paren+=1
            
            if len(parentheses) != 0:
                parentheses.pop()
    
    # no partheses and expression greater than 1
    if not left_paren and len(tokens) > 1:
        raise SchemeSyntaxError
    
    # if there is not a corresponding 
    if len(parentheses) != 0 or right_paren != left_paren:
        raise SchemeSyntaxError
        
    # recurive helper function to parse items in string
    def parse_expression(index):       
        char = tokens[index]
        token = number_or_symbol(char)        
        
        # checks if the token is an operator
        if isinstance(token, str) and token != "(" and token != ")":
            return token, index+1
        
        # checks if the token is a number
        if isinstance(token, (int, float)):
            return token, index+1
            
        # subexpression of tokenized string
        if token == "(":
            
            parsed = []
            # skips the left parenthesis
            index+=1
            char=tokens[index]
            
            # goes until you reach the end of the S-expression
            while char != ")":
                token, index = parse_expression(index)
                parsed.append(token)
                char = tokens[index]
            return parsed, index+1
        
    parsed_expression, next_index = parse_expression(0)
    
    # returns the recursive call
    return parsed_expression
 
######################
# Built-in Functions #
######################

def multiplying(args):
    """
    args- a list of numbers of type float or int
    
    A function to multiply the first element by every othr number in args
    """
    first_num = args[0]
    
    # goes through every other element in args
    for next_num in args[1:]:
        first_num*= next_num
    return first_num

def dividing(args):
    """
    args- a list of numbers of type float or int
    
    A function to divide the first element by every othr number in args
    """
    first_num = args[0]
    
    # goes through every other element in args
    for next_num in args[1:]:
        first_num /= next_num
        
    return first_num

def equal_condition(args):
    """
    args- a list of numbers of type float or int
    
    Checks if all the arguments are equal to each other
    """
    first_arg = args[0]
    
    # goes through the rest of arguments and checks for equivalency
    for arg in args[1:]:
        # checks if argument is not equal
        if first_arg != arg:
            return 0
    # defaults to every value being true
    return 1
    
def great_than_condition(args):
    """
    args- a list of numbers of type float or int
    
    Checks if all the arguments are in strictly increasing order (greater than each other)
    """
    first_arg = args[0]
    
    # goes through rest of args and checks for strictly increasing order
    for arg in args[1:]:
        
        # checks if 
        if first_arg <= arg:
            return 0
        first_arg = arg
        
    # defaults to every value being greater than each other
    return 1
    
def greater_equal_condition(args):
    """
    args- a list of numbers of type float or int
    
    Checks if all the arguments are in weakly increasing order 
    (greater than or equal to each other)
    """
    first_arg = args[0]
    
    # goes through rest of args and checks for weakly increasing order
    for arg in args[1:]:
        
        # checks if 
        if first_arg < arg:
            return 0
        
        first_arg = arg
        
    # defaults to every value being greater than or equal to each other
    return 1
    
def less_than_condition(args):
    """
    args- a list of numbers of type float or int
    
    Checks if all the arguments are in strictly decreasing order (less than each other)
    """
    first_arg = args[0]
    
    # goes through rest of args and checks for strictly decreasing order
    for arg in args[1:]:
        
        # checks for first instance of element that is not decreasing
        if first_arg >= arg:
            return 0
        first_arg = arg
        
    # defaults to every value being less than each other
    return 1

def less_equal_condition(args):
    """
    args- a list of numbers of type float or int
    
    Checks if all the arguments are in weakly increasing order 
    (less than or equal to each other)
    """
    
    first_arg = args[0]
    
    # goes through rest of args and checks for strictly increasing order
    for arg in args[1:]:
        
        # checks for first instance of element that is not decreasing
        if first_arg > arg:
            return 0
        first_arg = arg
        
    # defaults to every value being greater than each other
    return 1
    
def opposite_conditions(args):
    """
    args - list of true or false values
    
    If length of arguments is greater than 1 or 0 then
    can not evaluate expression so raise a SchemeEvaluationError
    
    Make the argument equal to the opposite boolean value, i.e.
        true --> false
        false --> true
    """
    if len(args) > 1 or len(args) == 0:
        raise SchemeEvaluationError
    
    # returns the opposite of the argument
    # originally true
    if args[0]:
        return 0
    # originally false
    elif not args[0]:
        return 1

def building_pair(args):
    """
    args- a list of numbers
    
    Checks if there are only two arguments in the args list, if not raise SchemeEvaluationError
    
    If two elements in the args list, return an instance of a Pair object
    """
    
    # checks if wrong number of arguments passed into function
    if len(args) != 2:
        raise SchemeEvaluationError
    
    # returns an instance of Pair
    return Pair(args[0], args[1])

def get_car(args):
    """
    args- list of Pair instances or other values
    
    If there is more than one argument or the argument is not 
    an instance of Pair object raise a SchemeEvaluationError
    
    Gets the car attribute from a Pair instance
    """
    # checks if there are too many arguments
    if len(args) !=1:
        raise SchemeEvaluationError
    
    # checks if the argument is not a list
    if not isinstance(args[0], Pair):
        raise SchemeEvaluationError
    
    # gets the car attribute from a Pair instance
    return args[0].car
    
def get_cdr(args):
    """
    args- list of Pair instances or other values
    
    If there is more than one argument or the argument is not 
    an instance of Pair object raise a SchemeEvaluationError
    
    Gets the cdr attribute from a Pair instance
    """
    # check if there are too many arguments
    if len(args) != 1:
        raise SchemeEvaluationError
    
    # checks if the argument is not a list
    if not isinstance(args[0], Pair):
        raise SchemeEvaluationError
    
    # gets the cdr attribute from a Pair instance
    return args[0].cdr

def construct_list(args=None):
    """
    args- None or list of values to put into a linked list
    
    Recursively creates a linked list
    """
    # base case
    if len(args) == 0:
        return []
    
    # base case
    if len(args) == 1:
        return building_pair((args[0], []))
    
    # recursive step
    else:
        first_arg = args[0] 
        rest_args = args[1:]
        
        # builds up the linked list
        return building_pair((first_arg , construct_list(rest_args)))

def is_linked_list(args):
    """
    Checks if argument is a linked list
    """

    # checks for no arguments 
    if not args:
        raise SchemeEvaluationError
        
    # checks for empty list-linked list
    # or the last element in linked list
    if args[0] == []:
        return True
    
    # checks if last item is not a Pair instance
    if not isinstance(args[0], Pair):
        return False
    
    # recurses on Pair instances
    else:
        # checks each subsequent element of linked list
        return is_linked_list([args[0].cdr])
    
def length(args):
    """
    args- a list of Pair instances (linked lists)
    
    Recursively finds the length of the linked list
    """
    # checks if argument is a linked list
    if not is_linked_list(args):
        raise SchemeEvaluationError 
    
    # checks if next argument is end of linked list(a number or empty list)
    if args[0] == []:
        return 0
    
    # recursive step
    else:
        return 1 + length([args[0].cdr])
    
def list_indexing(args):
    """
    args- a list of Pair instances (linked lists) 
    
    Recursively indexes into the linked lists
    """
    # checks if no arguments are passed in
    if not args:
        raise SchemeEvaluationError
  
    linked_list = args[0]
    index = args[1]
        
    # checks if at end of linked list and index exceeds length of list
    if linked_list == [] and index != 0:
        raise SchemeEvaluationError
    
    # checks if there's no list to index into
    if linked_list == []:
        raise SchemeEvaluationError
    
    if linked_list == [] and index == 0:
        return linked_list
    
    # check if not a con cell
    if isinstance(linked_list.cdr, (int, float)) and index!=0:
        raise SchemeEvaluationError
    
    # at the element you want to index
    if index == 0:
        return linked_list.car
    
    # recursive step
    else:
        # keeps on going down the linked elements
        return list_indexing([linked_list.cdr, index-1])
    
def adding_linked_element(args= None):
    """
    Combining linked lists together
    """
    # base case
    # check if empty list
    if not args:
        return []
    
    # checks that first argument is linked list
    if not is_linked_list([args[0]]):
        raise SchemeEvaluationError 

    # recursive case 1
    # at end of linked list
    if args[0] == []:
        return adding_linked_element(args[1:])
    
    # recursive case 2
    # more elements to link in first linked list
    else:
        first_linked_ele = args[0].car
        rest_linked_ele = [args[0].cdr] + args[1:]
        
        # recursively links elements from multiple linked list
        return building_pair([first_linked_ele, 
                             adding_linked_element(rest_linked_ele)])

def begin_expression(args):
    """
    args- list of expressions
    
    Returns the last argument
    """
    # returns the last argument in args
    return args[-1]

def evaluate_file(filename, frame=None):
    """
    filename- string of the file name
    frame- optional parameter of the Frame instance
    """
    # opens the file
    with open(filename) as f:
        # tokenizes, parses, and evaluates 
        # the file in a given frame
        return evaluate(parse(tokenize(f.read())), frame)    

scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": multiplying,
    "/": dividing,
    "#t": 1,
    "#f": 0,
    "equal?": equal_condition,
    ">": great_than_condition,
    ">=": greater_equal_condition,
    "<": less_than_condition,
    "<=": less_equal_condition,
    "not": opposite_conditions,
    "cons": building_pair,
    "list": construct_list,
    "nil": [],
    "car": get_car,
    "cdr": get_cdr,
    "list?":is_linked_list,
    "length": length,
    "list-ref": list_indexing,
    "append": adding_linked_element,
    "begin":begin_expression, 
}

BUILTIN_FUNCTIONS = Frame(scheme_builtins, None)

##############
# Evaluation #
##############
def evaluate(tree, frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    # checks if there is no global frame
    if frame is None:
        frame = Frame({}, BUILTIN_FUNCTIONS)
    
    # checks if input is just a number
    if isinstance(tree, (int, float)):
        return tree
    
    # checks if input is an operator
    elif isinstance(tree, str):
      
        # returns the function corresponding to operator
        return frame.get_value(tree) 
    
    # check if given an empty input
    elif tree == []:
        raise SchemeEvaluationError
        
    # check if you are trying to define a variable or function
    elif tree[0] == "define":          
        var_name = tree[1]              # gets variable name
        rest_tree = tree[2]             # gets variable value, either number or S-expression
        
        # checks if it is an S-expression, defining a function
        if isinstance(var_name, list):
            # gets the parameters from shortened function definition
            if len(var_name) >= 1:
                param = var_name[1:]
            
            else:
                param = []    
            
            var_value = Function(param, rest_tree, frame)
            frame.set_value(var_name[0], var_value)
        
        # defining a variable 
        else:    
            var_value = evaluate(rest_tree, frame)
            frame.set_value(var_name, var_value)
        
        return var_value
    
    # defines a user- defined function
    elif tree[0] == "lambda":
        parameters = tree[1]
        function_expression = tree[2]
        var_value = Function(parameters, function_expression, frame)
    
        # returns a function object 
        return var_value
    
    # checks for a conditional S-expression
    elif tree[0] == "if":
        condition = tree[1]
        true_expression = tree[2]
        false_expression = tree[3]
        
        expressions = (false_expression, true_expression)
        var_value = evaluate(condition, frame)
        
        # indexes the proper false or true expression
        # based on the evaluated truth value
        return evaluate(expressions[var_value] , frame)
    
    # and conditional
    elif tree[0] == "and": 
        rest_tree = tree[1:]
        
        for expression in rest_tree:
            boolean_value = evaluate(expression, frame)
            
            # checks if expression is not true
            if not boolean_value:
                return 0
        # defaults to every expression being true
        return 1
        
    # or conditional
    elif tree[0] == "or":    
        rest_tree = tree[1:]
        
        for expression in rest_tree:
            boolean_value = evaluate(expression, frame)
            if boolean_value:
                return 1
        return 0
    
    # deleting variable binding in current frame
    elif tree[0] == "del":
        var_name = tree[1]
        
        # checks if variable is not bound in frame
        if var_name not in frame.mapping:
            raise SchemeNameError
            
        # deletes item, returns removed value
        return frame.mapping.pop(var_name)
    
    elif tree[0] == "let":
        local_assignments = tree[1]
        expression = tree[2]
        local_frame = Frame({}, frame)
        
        # goes through all local variables
        for tree_list in local_assignments:
            var_name = tree_list[0]
            var_value = evaluate(tree_list[1], local_frame)
            local_frame.set_value(var_name, var_value) 
        
        return evaluate(expression, local_frame)
            
    elif tree[0] == "set!":
        # using something similar to .get value in Frame class
        var_name = tree[1]
        expression = tree[2]
        var_value = evaluate(expression, frame)
        frame.update_value(var_name, var_value)
        
        return var_value
        
    #checks if input has list of elements to evaluate
    elif isinstance(tree, list):
        first_token = tree[0]
        rest_tree = tree[1:]
        token = evaluate(first_token, frame) # grabs first element in S expression
        
        # gets the numerical value for all 
        other_tokens = [evaluate(token, frame) for token in rest_tree]
            
        # checks if token is not a valid function name
        if isinstance(token, (int, float)):
            raise SchemeEvaluationError
        evaluated_expression = token(other_tokens)
        
        # returns value of evaluated expression
        return evaluated_expression

############################
# Evaluate Helper Function #
############################
def result_and_frame(tree, frame=None):
    """
    Evaluates the tree expression
    
    Returns a tuple of the evaluated value and the frame you are working with
    """
    # checks if there is no frame to define variables/functions in
    if frame is None:
        frame = Frame({}, BUILTIN_FUNCTIONS)
    
    return evaluate(tree, frame), frame

########
# REPL #
########

def repl(raise_all=False):
    global_frame = None
    while True:
        # read the input.  pressing ctrl+d exits, as does typing "EXIT" at the
        # prompt.  pressing ctrl+c moves on to the next prompt, ignoring
        # current input
        try:
            inp = input("in> ")
            if inp.strip().lower() == "exit":
                print("  bye bye!")
                return
        except EOFError:
            print()
            print("  bye bye!")
            return
        except KeyboardInterrupt:
            print()
            continue

        try:
            # tokenize and parse the input
            tokens = tokenize(inp)
            ast = parse(tokens)
            # if global_frame has not been set, we want to call
            # result_and_frame without it (which will give us our new frame).
            # if it has been set, though, we want to provide that value
            # explicitly.
            args = [ast]
            if global_frame is not None:
                args.append(global_frame)
            result, global_frame = result_and_frame(*args)
            # finally, print the result
            print("  out> ", result)
        except SchemeError as e:
            # if raise_all was given as True, then we want to raise the
            # exception so we see a full traceback.  if not, just print some
            # information about it and move on to the next step.
            #
            # regardless, all Python exceptions will be raised.
            if raise_all:
                raise
            print(f"{e.__class__.__name__}:", *e.args)
        print()


if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    # initalize frame calls evaluate filename passing in new frame, evaluate will
    # auto update frame
    # start repl with the new frame you created
    repl()
