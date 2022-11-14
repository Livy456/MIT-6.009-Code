#!/usr/bin/env python3

import sys
import typing
import doctest

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS

def new_cnf_formula(old_formula, checking_literal):
    """
    Shortens the CNF formula
    
    If the literal we are checking - (variable, boolean) has a
    boolean value of True then we skip the clause and if 
    it has a boolean value of False then keep the clause and omit
    the literal that has the same variable value
    """
    new_formula = []
    variable = checking_literal[0]
    boolean_value = checking_literal[1]
    
    # iterates through all clauses, inner list, of the formula
    for clause in old_formula:        
        new_clause = []
        
        # skip if the variable has the same boolean 
        # assignment in its clause
        if checking_literal in clause:
            continue
        
        # iterates through every tuple in clause
        for literal in clause:
            if literal[0] != variable:
                new_clause.append(literal)
        
        new_formula.append(new_clause)
    
    # returns a shorten cnf formula - list of lists of tuples--> (variable, boolean)
    return new_formula

def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    final_cnf_dictionary = {}
    # base case 1: if there is no clauses to check
    if len(formula) == 0:
        return {}
    
    new_formula = formula
    for clause in new_formula:
        # checks if unit clause  
        if len(clause) == 1: 
            literal = clause[0]
            
            # checks if variable is not already been assigned a value
            if literal[0] not in final_cnf_dictionary:
                final_cnf_dictionary[literal[0]] = literal[1]
            
            # checks for contradictory assigment
            elif literal[1] != final_cnf_dictionary[literal[0]]:
                return None
            
            new_formula = new_cnf_formula(new_formula, literal)
        
    # base case 1: if there is no clauses to check
    if len(new_formula) == 0:
        return final_cnf_dictionary
    
    # base case 2: checks if there is no possible way to solve a clause
    if [] in new_formula:
        return None
    
    # recursive step
    else:
        variable, boolean_value = new_formula[0][0]   # gets the first inner list, then first tuple
       
        # makes two versions of the cnf formula, checking if
        # True or False assignment works the
        for new_bool_value in (boolean_value, not boolean_value):            
            shorten_formula = new_cnf_formula(new_formula, (variable, new_bool_value))
                        
            # tries a potential assignment for a variable
            potential_assignment = satisfying_assignment(shorten_formula)
            
            # check if you have a valid assignment for a variable
            if potential_assignment is None:
                continue

            else:
                
                potential_assignment |= {variable:new_bool_value}
                
                final_cnf_dictionary.update(potential_assignment)
                
                # returns the final mapping for each variable
                return final_cnf_dictionary

def all_sudoku_subgrids(n):
    """
    Gets every subgrid in an n x n sudoku board.
    Returns a list of list of coordinates for a given subgrid
    """
    all_subgrids = [[] for _ in range(n)] # initalizes a list of all subgrids
    subgrid_n = int(n**(1/2)) # dimension of subgrid
    subgrid_area = subgrid_n**2 

    # iterates through each subgrid
    for subgrid_number in range(n):
        
        # iterate through area of a given subgrid
        for location in range(subgrid_area):
            # row = location // subgrid_n
            # col = location % subgrid_n
            row, col = divmod(location, subgrid_n) 
            
            # scaling to different subgrid location
            coord_col = int(col) + (subgrid_number%subgrid_n)*subgrid_n
            coord_row = int(row) + (subgrid_number // subgrid_n) * subgrid_n
           
            all_subgrids[subgrid_number].append((coord_row, coord_col))
             
    return all_subgrids

def at_most_one_subgrid(n, all_subgrids):
    """
    Generates a cnf formula that checks that a 
    number can be in any subgrid at most once
    """
    formula = []
    
    # goes through each possible number in sudoku board
    for number in range(1, n+1):
        # goes through each subgrid on sudoku board
        for subgrid in all_subgrids:
            
            # goes through each coordinate in sudoku board
            # and checks that it is at most once in a subgrid
            for coordinate1 in subgrid:
                variable1 = (number, coordinate1[0], coordinate1[1])
                literal1 = (variable1, False)
                
                for coordinate2 in subgrid:
                    
                    if coordinate1 == coordinate2:
                        continue 
                    variable2 = (number, coordinate2[0], coordinate2[1])
                    literal2 = (variable2, False)
                    formula.append([literal1, literal2])
    
    return formula

def at_least_one_subgrid(n, all_subgrids):
    """
    Generates a cnf formula that checks that a 
    number can be in any subgrid at least once
    """
    formula = []
    
    # goes through each possible number for sudoku board
    for number in range(1, n+1):
        # goes through each subgrid on the sudoku board
        for subgrid in all_subgrids:
            clause = []
            # goes through each coordinate in a subgrid
            # and checks if a number is in any coordinate
            # in a given subgrid
            for coordinate in subgrid:
                variable = (number, coordinate[0], coordinate[1])
                literal = (variable, True)
                clause.append(literal)
        
        formula.append(clause)
            
    return formula

def at_most_one_coordinate_rule(rows, cols):
    """
    Generates a cnf formula that checks that
    a number can be in any position at most once
    """
    formula = []
    
    # goes through entire sudoku board
    for row in range(rows):
        for col in range(cols):
            
            for num1 in range(1, cols+1):   
                variable1 = (num1, row, col)
                literal1 = (variable1, False)
                # checks that any given number is
                # at any coordinate at most once
                for num2 in range(1, cols+1):
                    if num1 == num2:
                        continue
                    variable2 = (num2, row, col)
                    literal2 = (variable2, False)
                    formula.append([literal1, literal2])
                    
    return formula

def at_least_one_coordinate_rule(rows, cols):
    """
    Generates a cnf formula that checks that 
    a number can be in any position at least once
    """
    formula = []
    
    for number in range(1, cols+1):
        clause = []
        for row in range(rows):
            for col in range(cols):
                variable = (number, row, col)
                literal = (variable, True)
                clause.append(literal)
        formula.append(clause)
                                
    return formula

def inital_number_position_rule(rows, cols, board):
    """
    Generates a cnf formula that checks that 
    all the numbers initally on the sudoku
    board remain there
    """
    formula = []
    # goes through each element in the sudoku 
    # board and determines if the value is blank
    for row in range(rows):
        for col in range(cols):
            number = board[row][col]
            
            # checks if location is not empty
            if number != 0:
                variable = (number, row, col)
                literal = (variable, True)
                formula.append([literal])
    
    return formula

def at_most_one_col_rule(rows, cols):
    """
    Generates a cnf formula that checks that
    every number is in each column at most once
    """
    formula = []
    
    # iterates through each number
    for number in range(1, cols+1):
        
        for col in range(cols):
            # goes through each element in a given column
            for row in range(rows):
                variable1 = (number, row, col)
                literal1 = (variable1, False)
                
                for other_row in range(rows):
                    if other_row != row:
                        variable2 = (number, other_row, col)
                        literal2 = (variable2, False)
                        formula.append([literal1, literal2])
            
    return formula

def at_least_one_col_rule(rows, cols):
    """
    Generates a cnf formula that checks that 
    every number is in each column at least once
    """
    formula = []
    
    # goes through numbers 1, n
    for number in range(1, cols+1):
        # iterates through each column in sudoku board
        for col in range(cols):
            clause = []
            # iterate through each row in sudoku board
            for row in range(rows):
                variable = (number, row, col)
                literal = (variable, True)
                clause.append(literal)
        formula.append(clause)
    
    # returns a formula for having every number in each column at least once
    return formula

def at_most_one_row_rule(rows, cols):
    """
    Generates a cnf formula that checks that 
    every number is in each row at most once
    """
    formula = []
    
    # gets the values for a number in a board
    for number in range(1, cols+1):
        
        # iterate through all the rows
        for row in range(rows):
            
            # iterates through each column
            for col in range(cols):
                variable1 = (number, row, col)
                literal1 = (variable1, False)
                
                # checks if each number in a row is
                # see at most once
                for other_col in range(cols):
                    if other_col != col:
                        variable2 = (number, row, other_col)
                        literal2 = (variable2, False)
                        formula.append([literal1, literal2])
    # returns the formula for having every # at moste once in each row            
    return formula

def at_least_one_row_rule(rows, cols):
    """
    Generates a cnf formula that checks that 
    every number is in each row at least once
    """
    formula = []
    
    # goes through numbers 1, n
    for number in range(1, cols+1):
        # iterates through each row in sudoku board
        for row in range(rows):
            clause = []
            
            # iterates through each column in sudoku board
            for col in range(cols):
                # col+1 corresponds to number on 
                variable = (number, row, col)
                literal = (variable, True)
                clause.append(literal)
            formula.append(clause)
            
    return formula

def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    # gets dimensions of n x n sudoku board
    num_rows = len(sudoku_board)
    num_cols = num_rows
    all_subgrids = all_sudoku_subgrids(num_rows)
    rule1 = at_least_one_col_rule(num_rows, num_cols)
    rule2 = at_most_one_col_rule(num_rows, num_cols)
    rule3 = at_least_one_row_rule(num_rows, num_cols)
    rule4 = at_most_one_row_rule(num_rows, num_cols)
    rule5 = at_least_one_coordinate_rule(num_rows, num_cols)
    rule6 = at_most_one_coordinate_rule(num_rows, num_cols)
    rule7 = at_least_one_subgrid(num_rows, all_subgrids)
    rule8 = at_most_one_subgrid(num_rows, all_subgrids)
    rule9 = inital_number_position_rule(num_rows, num_cols, sudoku_board)
    
    all_rules = rule1 + rule2 + rule3 + rule4 + rule5 + rule6 + rule7 + rule8 + rule9
    
    # cnf formula with all the sudoku rules
    return all_rules

def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolveable board, return None
    instead.
    """
    # initialized sudoku board of just zero's
    sudoku_board = [[0 for _ in range(n)] for _ in range(n)]
    
    
    if assignments is None:
        return None
    
    for variable, boolean_value in assignments.items():
        number, row, col = variable
        
        # updates the value at sudoku board location
        # if variable is assigned to True
        if boolean_value:
            sudoku_board[row][col] = number
             
    return sudoku_board

if __name__ == "__main__":
    import doctest

    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    
    dylan = False
    adam = False
    rob = False
    pete = False
    tim = True
    
    pickles = False
    vanilla = True
    chocolate = False

    rule1 = (dylan or adam or rob or pete or tim)
# At least one of them must have committed the crime!  Here, one of these
# variables being True represents that person having committed the crime.

    rule2 = ((not dylan or not adam)
     and (not dylan or not rob)
     and (not dylan or not pete)
     and (not dylan or not tim)
     and (not adam or not rob)
     and (not adam or not pete)
     and (not adam or not tim)
     and (not rob or not pete)
     and (not rob or not tim)
     and (not pete or not tim))
# At most one of the suspects is guilty.  In other words, for any pair of
# suspects, at least one must be NOT guilty (so that we cannot possibly find
# two or more people guilty).

# Together, rule2 and rule1 guarantee that exactly one suspect is guilty.


    rule3 = ((not chocolate or not vanilla or not pickles)
     and (chocolate or vanilla)
     and (chocolate or pickles)
     and (vanilla or pickles))
# Here is our rule that the cupcakes included exactly two of the flavors.  Put
# another way: we can't have all flavors present; and, additionally, among
# any pair of flavors, at least one was present.


    rule4 = ((not dylan or pickles)
     and (not dylan or not chocolate)
     and (not dylan or not vanilla))
# If Dylan is guilty, this will evaluate to True only if only pickles-flavored
# cupcakes were present.  If Dylan is not guilty, this will always evaluate to
# True.  This is our way of encoding the fact that, if Dylan is guilty, only
# pickles-flavored cupcakes must have been present.


    rule5 = (not rob or pete) and (not pete or rob)
# If Rob ate cupcakes without sharing with Pete, the first case will fail
# to hold.  Likewise for Pete eating without sharing.  Since Rob and Pete
# only eat cupcakes together, this rule excludes the possibility that only one
# of them ate cupcakes.

    rule6 = ((not adam or chocolate)
     and (not adam or vanilla)
     and (not adam or pickles))
# If Adam is the culprit and we left out a flavor, the corresponding case here
# will fail to hold.  So this rule encodes the restriction that Adam can only
# be guilty if all three types of cupcakes are present.


    satisfied = rule1 and rule2 and rule3 and rule4 and rule5 and rule6
    #print(satisfied)
    
    # CNF Values
    # not means "False" value
    # just variable means "True" value
    # a tuples in a list will be interpreted as "or" values
    # multiple lists will be interpreted as "and" value
    
    # c and (a or d) and (not b or a) and (not a or e or not d)
    cnf_question1  =  [[("c", True)], 
                       [("a", True), ("d", True)],      
                       [("b", False), ("a", True)], 
                       [("a", False), ("e", True), ("d", False)]]
    
    # (a and b) or (c and not d)
    # think of it like foil technique to create CNF formula
    # (a or c) and (a or not d) and (b or c) and (b or not d) 
    
    
    # a and (not b or (c and d))
    
    #[("a", True)], [("b", False), ("c", True)], [("b", False), ("d", True)]
    
    cnf_question2 = [[("a", True)], [("b", False), ("c", True)], [("b", False), ("d", True)]]

    cnf = [
            [("a", True), ("b", True)],
            [("a", False), ("b", False), ("c", True)],
            [("b", True), ("c", True)],
            [("b", True), ("c", False)],
        ]
    #result_formula = satisfying_assignment(cnf)
    #print("at least one: ",at_least_one_row_rule(3,3))
    #sudoku_board = at_most_one_row_rule(3, 3)
    #x = 0
    #for row in sudoku_board:
    #    x+=1
    #    print(f"at row {x}:{row}")
    cnf2 = [
            [("a", True)],
            [("a", False)]
            ]
    #assignment = satisfying_assignment(cnf2)
    #print("debugging:", assignment)
    #short_cnf = new_cnf_formula(cnf, ("a", True))
    #print(short_cnf)
    #new_short_cnf = new_cnf_formula(short_cnf, ('b', True))
    #print(new_short_cnf)
    #all_subgrids = all_sudoku_subgrids(9)
    
    #sudoku_board = [[0 for _ in range(4)] for _ in range(4)]
    #num_rows = len(sudoku_board)
    #num_cols = num_rows
    #all_subgrids = all_sudoku_subgrids(num_rows)
    #rule1 = at_least_one_col_rule(num_rows, num_cols)
    #rule2 = at_most_one_col_rule(num_rows, num_cols)
    #rule3 = at_least_one_row_rule(num_rows, num_cols)
    #rule4 = at_most_one_row_rule(num_rows, num_cols)
    #rule5 = at_least_one_coordinate_rule(num_rows, num_cols)
    #rule6 = at_most_one_coordinate_rule(num_rows, num_cols)
    #rule7 = at_least_one_subgrid(num_rows, all_subgrids)
    #rule8 = at_most_one_subgrid(num_rows, all_subgrids)
    #rule9 = inital_number_position_rule(num_rows, num_cols, sudoku_board)
    
    #for clause in rule1:
    #    print(f"this is rule1:{clause}")
    
    #for subgrid in all_subgrids:
    #    print(subgrid)
