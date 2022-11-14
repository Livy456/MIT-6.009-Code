#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
NEIGHBOR = (-1, 0, 1)

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)

# 2-D IMPLEMENTATION
def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    return new_game_nd((num_rows, num_cols), bombs)

def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    return dig_nd(game, (row, col))

def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """  
    return render_nd(game, xray)

def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    
    board = ""
    rendered_board = render_2d_locations(game, xray)
    num_cols = game["dimensions"][1]
    
    for row in range(game["dimensions"][0]):
        for col in range(game["dimensions"][1]):
            board+= rendered_board[row][col]
          
        if row < game["dimensions"][0] -1: 
            board+="\n"
    return board
      
def possible_neighbors(recursive_dimensions, recursive_location):
     """
     Returns all possible valid neighbor locations to go to 
     Will not add neighbors if they are out of bounds
     """
     # use a generator for this section as well
     
     # base case
     if len(recursive_dimensions) == 1:
         # goes through -1, 0, 1
         for location_shift in NEIGHBOR:
             # checks if neighbor is valid location
             if 0<= location_shift +recursive_location[0] < recursive_dimensions[0]:
                 yield (location_shift + recursive_location[0],)
         
     # recursive step
     else:
         # goes through -1, 0, 1
         for location_shift in NEIGHBOR:
             
             # gets all neighbors locations from previous dimensions
             for possible_location in possible_neighbors(recursive_dimensions[1:], recursive_location[1:]):
                 
                 # checks if valid new location
                 if 0<= location_shift + recursive_location[0] < recursive_dimensions[0]:
                     yield (location_shift + recursive_location[0], )+ possible_location
     
def possible_locations(recursive_dimensions):
    """
    Returns a list of all possible locations on the board
    """
    # base case
    if len(recursive_dimensions) == 1:
        # gets all possible locations for one dimension
                
        #return [(i,) for i in range(recursive_dimensions[0])]
        for i in range(recursive_dimensions[0]):
            yield (i,) 
            
    # recursive step
    else:    
        # j is the range of locations from 0 to highest dimension    
        for j in range(recursive_dimensions[0]):
            # location is all locations from previous dimensions
            for location in possible_locations(recursive_dimensions[1:]):
                yield (j,) + location 
        
def get_value_on_board(location, board):
    """
    Gets value of particular location on the board
    >>> get_value_on_board((0, 1, 2), [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9],[10, 11, 12]]])
    6
    """
    # base case
    if len(location) == 1:
        return board[location[0]]
    
    # recursive
    else:
        return get_value_on_board(location[1:], board[location[0]])

def set_value_on_board(location, board, value):
    """
    Sets the value of to value at particular board location
    """
    # base case
    if len(location) == 1:
        board[location[0]] = value
    
    # recursive step
    else:
        set_value_on_board(location[1:], board[location[0]], value)
            
def game_state_nd(game):
    """
    Returns the state of the game, either "defeat", "victory", or "ongoing"
    """    
    # goes through all possible locations
    for location in possible_locations(game["dimensions"]):
        hidden_element = get_value_on_board(location, game["hidden"])
        board_value = get_value_on_board(location, game["board"])
        
        # checks if any hidden objects that are not bombs
        if hidden_element and not(board_value == "."):
            return "ongoing"
    
    # defaults to winning game
    return "victory"
     
def recursive_build_nd_board(recursive_dimensions, val):
    """
    Recursively initializes an n dimensional board of the hidden elements
    """
    # base case
    if len(recursive_dimensions) == 1:
        return [val for i in range(recursive_dimensions[0])]
    # recursive step
    else:
        # builds up one dimension of the board at a time
        return [recursive_build_nd_board(recursive_dimensions[1:], val) 
                for j in range(recursive_dimensions[0])]
        
# N-D IMPLEMENTATION
def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    """
    set_bombs = set(bombs)
    new_board = recursive_build_nd_board(dimensions, 0)
    
    # goes through all the locations of the bombs on the mine sweeper board game
    for bomb_coordinate in bombs:
        
        # goes through all the neighbor
        for neighbor in possible_neighbors(dimensions, bomb_coordinate):
            board_value = get_value_on_board(neighbor, new_board)
            
            if neighbor not in set_bombs:
                set_value_on_board(neighbor, new_board, int(board_value)+1)
        
        set_value_on_board(bomb_coordinate, new_board, ".")
    
    # returns a dictionary representation of the mine sweeper game
    return {"dimensions": dimensions,
            "board": new_board,
            "hidden": recursive_build_nd_board(dimensions, True),
            "state": "ongoing"} 

def is_bomb_nd_game(coordinate, board):
    """
    Checks if the value at a specific coordinate is a bomb
    """
    # checks if value is bomb
    if get_value_on_board(coordinate, board) == ".":
        return True
    # defaults to value not being a bomb
    return False

def dig_nd(game, coordinates, recursion_depth=0):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat
    """
    # checks if you already lost/won
    if game["state"] != "ongoing":
        return 0
    
    # checks if new coordinate is bomb    
    if is_bomb_nd_game(coordinates, game["board"]):
        game["state"] = "defeat"
        set_value_on_board(coordinates, game["hidden"], False)
        return 1
    
    if get_value_on_board(coordinates, game["hidden"]) == True:
        set_value_on_board(coordinates, game["hidden"], False)
        revealed = 1
    # skips locations you have already been to
    else:
        return 0
    
    # checks if no bombs near coordinate
    if get_value_on_board(coordinates, game["board"]) == 0:
    
        # moves to different locations
        for neighbor in possible_neighbors(game["dimensions"], coordinates):
            
            if not is_bomb_nd_game(neighbor, game["board"]):
                if get_value_on_board(neighbor, game["hidden"]):               
                    revealed+= dig_nd(game, neighbor, 1)
    
    if recursion_depth == 0:
        game["state"] = game_state_nd(game)
    
    # returns the number of revealed squares
    return revealed
    
def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    mine_board = recursive_build_nd_board(game["dimensions"], 0) # initializes N-d board
    
    # iterates through all the coordinates
    for location in possible_locations(game["dimensions"]):
        
        board_value = get_value_on_board(location, game["board"])
        hidden_value = get_value_on_board(location, game["hidden"])
        
        # checks if element is not hidden or should be shown --> xray
        if not hidden_value or xray:
            # checks if you need to add a blank
            if board_value == 0:
                set_value_on_board(location, mine_board, " ")
            # adds on other revealed board values
            else:
                set_value_on_board(location, mine_board, str(board_value))
        else:
            set_value_on_board(location, mine_board, "_")
            
                
    return mine_board    
        
if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    #neighbors = possible_neighbors(((10, 20, 3)), ((5, 13, 0)))
    
    
    #for ele in all_locations:
    #    print(ele)
    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    #doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
