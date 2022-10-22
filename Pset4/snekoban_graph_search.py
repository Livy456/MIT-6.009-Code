# Snekoban Game

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}

def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    Return a dictionary representation of the game
        height: int, height of the game
        width: int, width of the game
        player: tuple, (x, y) coordinates of player
        wall: set of tuples, (x, y) coordinates of walls
        empty: set of tuples, (x, y) coordinates of empty spaces
        target: set of tuples, (x, y) coordinates of target/flags
        computer: set of tuples, (x, y) coordinates of computer
    """
    player = ()
    walls = set()
    height = len(level_description)
    width = len(level_description[0])
    empty = set()
    computers = set()
    targets = set()
    
    # iterates through all the rows of game
    for y_coord in range(len(level_description)):
        
        # iterates through all the columns and board objects in game
        for x_coord, board_object in enumerate(level_description[y_coord]):
            
            # checks if board object is wall
            if "wall" in board_object:
                walls.add((x_coord, y_coord))
            
            # checks if board object is target    
            if "target" in board_object:
                targets.add((x_coord, y_coord))   
            
            # checks if board object is computer
            if "computer" in board_object:
                computers.add((x_coord, y_coord))    
            
            # checks if board object is an empty space
            if board_object == []:
                empty.add((x_coord, y_coord))    
            
            # checks if the player is in board object location 
            if "player" in board_object:
                player = (x_coord, y_coord)
                
    # return a dictionary representation of Snekoban game
    return {"height": height,
            "width": width,
            "player": player,
            "wall": walls,
            "empty": empty,
            "target": targets,
            "computer": computers
        }
    
def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """    
    # checks if no flags present, or more computers than flags -> impossible to win game
    if (len(game["computer"]) != len(game["target"])) or len(game["target"]) == 0:
        return False
    
    # iterates through all the computer positions           
    for computer_pos in game["computer"]:
        
        # checks if computer position is not in target
        if computer_pos not in game["target"]:
            return False
               
    # defaults to True, if all computer positions are in set of target positions
    return True

def valid_move(game, new_player, old_player, direc_vec):
    """
    Parameters
    game : dict
        height: int, height of the game
        width: int, width of the game
        player: list, (x, y) coordinates of player
        wall: set of tuples, (x, y) coordinates of walls
        empty: set of tuples, (x, y) coordinates of empty spaces
        target: set of tuples, (x, y) coordinates of target/flags
        computer: set of tuples, (x, y) coordinates of computer.
    new_player, tuple
        (x, y) coordinates of new position of player
    old_player, tuple
        (x, y) coordinates of previous position of player
    direc_vect, tuple
        (x, y) coordinates of direction player wants to move
    
    Returns
        returns a set of tuples with updated locations of empty spaces
    """

    new_computer_copy = game["computer"].copy()
    empty_pos_copy = game["empty"].copy()
    
    # checks if player is moving into wall
    if new_player in game["wall"]:
        return (old_player, new_computer_copy, empty_pos_copy) 
    
    # checks if player will be moving a computer
    if new_player in game["computer"]:
        return valid_computer_move(game, new_player, old_player, direc_vec)
    
    # checks if player will be moving to a target
    if new_player in game["target"]:
        return (new_player, new_computer_copy, empty_pos_copy)
    
    # checks if player will move to empty space 
    else:
        # assumes that player didn't try to go to a wall, computer, or target
        new_empty_pos = valid_empty_move(empty_pos_copy, new_player, old_player)
        new_computer_pos = new_computer_copy
    
    # return tuple of updated board object locations
    return (new_player, new_computer_pos, new_empty_pos)

def valid_empty_move(empty_pos, new_player, old_player):
    """
    Parameters
        game : dict
            height: int, height of the game
            width: int, width of the game
            player: list, (x, y) coordinates of player
            wall: set of tuples, (x, y) coordinates of walls
            empty: set of tuples, (x, y) coordinates of empty spaces
            target: set of tuples, (x, y) coordinates of target/flags
            computer: set of tuples, (x, y) coordinates of computer.
        new_player, tuple
            (x, y) coordinates of new position of player
        old_player, tuple
            (x, y) coordinates of previous position of player
    
    Returns
        returns a set of tuples with updated locations of empty spaces
    """
    empty_pos.discard(new_player)    # removes location where player is, no longer empty
    empty_pos.add(old_player)       # adds on the previous location of player, now empty
        
    # returns a set of tuples with locations of empty spaces
    return empty_pos
    
def valid_computer_move(game, new_player, old_player, direction):
    """
    Parameters
        game, dict
            height: int, height of the game
            width: int, width of the game
            player: list, (x, y) coordinates of player
            wall: set of tuples, (x, y) coordinates of walls
            empty: set of tuples, (x, y) coordinates of empty spaces
            target: set of tuples, (x, y) coordinates of target/flags
            computer: set of tuples, (x, y) coordinates of computer.
        new_player, tuple
            (x, y) coordinates of new position of player
        old_player, tuple
            (x, y) coordinates of previous position of player
        direction, tuple
            (x, y) coordinates of direction you want the player to move
    Return 
        returns a tuple of updated computer positions as 1st element
    and the updated positions of empty spaces as 2nd element
    """
    new_empty_pos = game["empty"].copy()
    new_computer_pos = game["computer"].copy()
    
    new_computer = (new_player[0] + direction[1], new_player[1] + direction[0])

    # checks if another computer or wall is already at new computer position
    if (new_computer in game["computer"]) or (new_computer in game["wall"]):
        return (old_player, new_computer_pos, new_empty_pos)
        
    # MAYBE GET RID OF THIS AND PUT 
    new_empty_pos.discard(new_player)
    new_empty_pos.add(old_player)
    
    new_computer_pos.discard(new_player)
    new_computer_pos.add(new_computer)
        
    # returns updated computer and empty spaces locations
    return (new_player, new_computer_pos, new_empty_pos)

def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    old_player_pos = game["player"]
    dir_vector = direction_vector[direction]
    
    # makes potential player position 
    new_player_pos = (game["player"][0] + dir_vector[1], game["player"][1] + dir_vector[0])
    
    # gets valid new positions of board objects
    (new_player_pos, new_computer_pos, new_empty_pos) = valid_move(game, new_player_pos, 
                                                                 old_player_pos, dir_vector)
        
    # MAKE THIS MORE EFFICIENT
    
    # returns a copy of the dictionary representation of Snekoban game
    return {"height": game["height"],
            "width": game["width"],
            "player": new_player_pos,
            "wall": game["wall"].copy(),
            "empty": new_empty_pos,
            "target": game["target"].copy(),
            "computer": new_computer_pos
        }

def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    new_game = []
    
    # Helper function
    def find_board_object(game, location):
        """
        game, dict
            height: int, height of the game
            width: int, width of the game
            player: list, (x, y) coordinates of player
            wall: set of tuples, (x, y) coordinates of walls
            empty: set of tuples, (x, y) coordinates of empty spaces
            target: set of tuples, (x, y) coordinates of target/flags
            computer: set of tuples, (x, y) coordinates of computer.
        location, tuple
            (x, y) coordinates of game 
        """
        board_object = []
        
        # checks if board object is a wall
        if location in game["wall"]:
            board_object.append("wall")
            
        # checks if board object is target
        if location in game["target"]:
            board_object.append("target")
        
        # checks if board object is computer
        if location in game["computer"]:
            board_object.append("computer")
        
        # checks if board object is a player   
        if location == game["player"]:
            board_object.append("player")
        
        # returns the board object
        return board_object
    
    # iterates through every row
    for y in range(game["height"]):
        row = []
        # iterates through every column
        for x in range(game["width"]):
            board_object = find_board_object(game, (x,y))
            row.append(board_object)
        new_game.append(row)
    
    # returns list of lists of lists of string
    return new_game

def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    all_game_states = [game]    # list of game states
    all_paths = [[]]            # list of list of directions taken to potentially solve puzzle
    
    visited_game = {(game["player"], 
                     frozenset(game["computer"]))}       # keeps track of each game state
    
    # checks if you don't have to move to win the game
    if victory_check(game):
        return []

    # checks all possible paths to potentially solving game
    while all_game_states:
        current_game_state = all_game_states.pop(0)                
        current_path = all_paths.pop(0) 
        
        # iterates through all the directions
        for direc in direction_vector:
            next_path = current_path.copy()   # copies the list of directions
            next_game_state = step_game(current_game_state, direc)  # makes new game state
            board_objects = (next_game_state["player"],
                                     frozenset(next_game_state["computer"]))
            
            # checks if game has already been to these board objects
            if board_objects in visited_game:
                continue
            
            # check if you have solved the puzzle
            elif victory_check(next_game_state):
                current_path.append(direc)
                return current_path
            
            next_path.append(direc)
                
            visited_game.add(board_objects) 
            all_paths.append(next_path)
            all_game_states.append(next_game_state)
            
    # defaults to game being unsolvable
    return None

if __name__ == "__main__":
     pass

