#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!

def transform_data(raw_data):
    """
    Parameter:
        raw_data, list of tuples
            1st element is actor_id1
            2nd element is actor_id2
            3rd element is film_id
   
    Task:
        transform the raw_data from a list of tuples to two different
    dictionary representations
    
    Return:
        a list of length 2 of dictionaries,  
    where the first dictionary actor_id1 : {(actor_id, film_id)}
    and the second dictionary film_id: {actor1, actor2}
    """
    
    def transform_actor_actor_film(data):
        """
        Parameters:
            data, list of tuples
                1st element is actor_id1
                2nd element is actor_id2
                3rd element is film_id
            
        Task:
            transforms the raw data from a list of tuples to dictionary, 
        where the key is the actor_id1 or actor_id2 and the value is a set of tuples
        of all the actors (actor_id) and the film that have acted in together
        - must include that an actor acted with themselves
        
        Return:
            a dictionary 
                actor_id1 : {(actor_id, film_id), ...}
        """
        dict_actor_film = {}
        
        # iterates through each tuple containing actor id1 and id2, and film id
        for actor_data in data:
            actor_id1 = actor_data[0]
            actor_id2 = actor_data[1]
            film_id = actor_data[2]
            
            # checks if actor_id1 is a key in dictionary
            if actor_id1 not in dict_actor_film:
                dict_actor_film[actor_id1] = {(actor_id1, film_id), (actor_id2, film_id)}
    
            # checks if actor_id2 is a key in dictionary            
            if actor_id2 not in dict_actor_film:
                dict_actor_film[actor_id2] = {(actor_id2, film_id), (actor_id1, film_id)}
                
            # checks if actor_id2 has not already been added to list of actors acted with actor1
            if actor_id2 not in dict_actor_film[actor_id1]:
                dict_actor_film[actor_id1].add((actor_id2, film_id))
            
            # checks if actor_id1 has not already been added to list of actors acted with actor2
            if actor_id1 not in dict_actor_film[actor_id2]:
                dict_actor_film[actor_id2].add((actor_id1, film_id))
                
        # returns a dict with unique films mapped to actors who acted in that film
        return dict_actor_film
    
    def transform_film_actor(data):
        """
        Parameters:
            data, list of tuples
                1st element is actor_id1
                2nd element is actor_id2
                3rd element is film_id
            
        Task:
            transforms the raw data from a list of tuples to dictionary, 
        where the key is the film id value is a set of tuples
        of all the actors that have acted in that movie
        
        Return:
            a dictionary 
                film_id : {actor_id, actor_id, ....}
        """
        
        dict_film_actor = {}
        
        # iterating through all the data
        for film_data in data:
            actor1 = film_data[0]
            actor2 = film_data[1]
            film = film_data[2]
            
            # check if film_id has not been added to keys
            if film not in dict_film_actor:
                dict_film_actor[film] = set()
            
            # adds actor1 to set of actors acted in film
            if actor1 not in dict_film_actor[film]:
                dict_film_actor[film].add(actor1)
            
            # adds actor2 to set of actors acted in film
            if actor2 not in dict_film_actor[film]:
                dict_film_actor[film].add(actor2)
        
        # returns dictionary, {film_id1: {actor_id1, actor_id2, ...}, ...}
        return dict_film_actor
    
    # list of two data represenations of film database            
    return (transform_actor_actor_film(raw_data), transform_film_actor(raw_data))

def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Parameters:
        transformed_data, dict
            actor_id: set of tuples with the film and 
        actor they acted with (actor_id2, film_id)
        actor_id_1, int
        actor_id_2, int
    Task:
        checks if two actors acted together
    Return:
        returns a boolean value, of whether actors acted together
    """
    dict_actor_film = transformed_data[0]
    
    for actor_tuple in list(dict_actor_film[actor_id_1]):
        
        # checks if actors acted together
        if (actor_id_2, actor_tuple[1]) == actor_tuple:
            # actors have acted together
            return True
        
    # defaults to actors not acting together
    return False

def actors_with_bacon_number(transformed_data, n):
    """
    Parameters:
        transformed_data, dict
            actor_id: set of tuples with the film and 
        actor they acted with (actor_id2, film_id)     
        n, int
            the bacon number 
            (Bacon number to be the smallest number of 
             films separating a given actor from Kevin Bacon)
    Task:
        finds all the actors in a corresponding degree of seperation
    Return:
        a set of the actors in corresponding bacon number
    """         
    
    # returns a set of actors at a specific bacon number
    return actors_with_degree_of_separation(transformed_data, 4724, n)

def actors_with_degree_of_separation(transformed_data, actor_id, n):
    """
    Parameters:
        transformed_data, dict
            actor_id: set of tuples with the film and 
        actor they acted with (actor_id2, film_id)
        actor_id, int
            the id of the actor you starting with
        n, int
            the degree of separation you are trying to find 
            (Bacon number to be the smallest number of 

    Task:
        finds all the actors in a corresponding degree of seperation
    
    Return:
        a set of the actors in corresponding degree of separation
    """
    dict_actor_film = transformed_data[0]
    deg_of_separation = 0
    actor_visited = {actor_id}
    current_level = {actor_id}
    next_level = set()
    
    # while you have not reached the specificed degree of separation
    while (deg_of_separation != n) and (current_level):
        
        # checks for the actors that acted with actor at current 
        # degree of separato=ion
        for actors in current_level:
            actor_set = {actor[0] 
                         for actor in dict_actor_film[actors]
                         if actor[0] not in actor_visited}
            next_level.update(actor_set)
            actor_visited.update(actor_set)
        
        current_level = next_level
        next_level = set()
        deg_of_separation+=1
        
    # returns a set of actors in corresponding degree of separation       
    return current_level

def bacon_path(transformed_data, actor_id):
    """
    Parameters:
        transformed_data, dict
            actor_id: set of tuples with the film and 
        actor they acted with (actor_id2, film_id)
        actor_id, int
            id of actor
    
    Task:
        find the shortests possible path, if there is one from
    Kevin Bacon to the indicated actor id
    
    Return:
        list of actors that go from Kevin Bacon to the indicated actor,
        None, if no possible path exists
    """
    #print(type(transformed_data))
    # returns the shortest possible path to actor_id, or None
    return actor_to_actor_path(transformed_data, 4724, actor_id)
    
def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Parameters:
        transformed_data, dict
            actor_id: set of tuples with the film and 
        actor they acted with (actor_id2, film_id)
        actor_id_1, int
            id of actor 1
        actor_id_2, int
            id of actor 2
    
    Task:
        find the shortests possible path, if there is one from
    actor_id_1 to actor_id_2
    
    Return:
        list of actors that go from actor_id_1 to actor_id_2,
        None, if no possible path exists
    """
    def goal_test_function(actor_id):
        """
        Parameters:
            actor_id, int
                id of actor
        
        Task:
            checks if actor_id is the desired destination
        
        Returns:
            True, if actor_id is actor_id_2
            False, if actor_id is not actor_id_2
        """
        return actor_id == actor_id_2

    return actor_path(transformed_data, actor_id_1, goal_test_function)

def movie_to_movie_path(transformed_data, actor_id1, actor_id2):
     """
     Parameters:
         transformed_data, dict
             actor_id: set of tuples with the film and 
         actor they acted with (actor_id2, film_id)
         actor_id_1, int
             id of actor 1
         actor_id_2, int
             id of actor 2
     
     Task:
         find the shortests possible path, if there is one from
     the movie that actor1 acted in to actor2 
     
     Return:
         list of films that go from actor1 to actor2,
         None, if no possible path exists
     """   
     dict_actor_film = transformed_data[0]
     actor_path = actor_to_actor_path(transformed_data, actor_id1, actor_id2)
     
     # checks if no possible path to particular movie
     if actor_path is None:
         # no possible path
         return None
     
     actor_path_copy = actor_path.copy()
     actor1 = actor_path_copy.pop(0)
     movie_path = []
     
     # zips through two actors at a time
     for actor1, actor2 in zip(actor_path, actor_path[1:]):
         
         #print(f"actor1: {actor1}")
         # iterates through every value for actor 1
         for actor_tuple in dict_actor_film[actor1]:
             
             # checks if they actor2 acted with actor1
             if actor2 == actor_tuple[0]:
                 movie_path.append(actor_tuple[1])
     
     # returns list of movies connecting actors
     return movie_path
             
def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    Parameters:
        transformed_data, dict
            actor_id: set of tuples with the film and 
        actor they acted with (actor_id2, film_id)
        actor_id_1, int
            id of actor 1
        goal_test_function, function
            a function that returns True or False if the inputted
        actor_id is the goal actor
    
    Task:
        find the shortests possible path, if there is one from
    actor_id_1 to actor_id_2
    
    Return:
        list of actors that go from actor_id_1 to actor_id_2,
        None, if no possible path exists
    """
    # referenced Flood Fill Reading notes
    dict_actor_film = transformed_data[0]
    all_path = [[actor_id_1]]
    visited_actors = {actor_id_1}
    
    # checks if the input actor id passes the goal test function
    # i.e. the start actor is the destination
    if goal_test_function(actor_id_1):
        return all_path.pop(0)

    # checks all possible paths
    while all_path:
        current_path = all_path.pop(0)
        last_actor = current_path[-1]
        neighbor_actor = actors_with_degree_of_separation(transformed_data, last_actor, 1)
        
        # iterates through all neighboring actors
        for actor in neighbor_actor:
            new_path = current_path.copy()
            
            # chekcs if you have already seen this actor
            if actor in visited_actors:
                continue
            
            # checks if actor passes the goal test_function
            if goal_test_function(actor):
                
                current_path.append(actor)
                return current_path
            
            visited_actors.add(actor)
            new_path.append(actor)
            all_path.append(new_path)
    
    # defaults to no possible path
    return None

def actors_connecting_films(transformed_data, film1, film2):
    """
    Parameters:
        transformed_data, dict
            actor_id: set of tuples with the film and 
        actor they acted with (actor_id2, film_id)
        film1, int
            id of film 1
        film2, int
            id of film 2
        goal_test_function, function
            a function that returns True or False if the inputted
        actor_id is the goal actor
    
    Task:
        find the shortests possible path, if there is one from
    film1 to film2 
    
    Return:
        list of actors that go from film1 to film2,
        None, if no possible path exists
    """
    short_path = None
    short_path_len = float("inf")
    dict_film_actor = transformed_data[1] 

    # helper function
    def goal_test_function(actor_id):
        """
        Parameters:
            actor_id, int
                id of actor
        
        Task:
            checks if actor id acted in film2
        
        Returns:
            True, if actor_id in set of actors in film2
            False, if actor_id is not in sect of actors of film2
        """
        # returns true or false if acted in film
        return actor_id in dict_film_actor[film2]
    
    actor_film1 = [actor for actor in dict_film_actor[film1]]
    
    # iterates through all potential starting points for path
    for actor in actor_film1:
        film_path = actor_path(transformed_data, actor, goal_test_function) # finds potential shortest path
        
        # checks if current path is actual shortest path
        if len(film_path) < short_path_len:
            # updates shortest path and length of path
            short_path = film_path
            short_path_len = len(short_path)
    
    # returns shortest path
    return short_path

if __name__ == "__main__":
    
    # make a function to load in data
    # loads in small database data
    with open("resources/small.pickle", "rb") as f:
        smalldb = pickle.load(f)
    
    # loads in names database data
    with open("resources/names.pickle", "rb") as f:
        namesdb = pickle.load(f)
    
    # loads in tiny database data
    with open("resources/tiny.pickle", "rb") as f:
        tinydb = pickle.load(f)
    
    # loads in large database data
    with open("resources/large.pickle", "rb") as f:
        largedb = pickle.load(f)
    
    # loads in movie database data
    with open("resources/movies.pickle", "rb") as f:
        moviedb = pickle.load(f)
    
    # Which of the following best describes the Python 
    # object that results from loading resources/names.pickle?
    #print(namesdb)              # dictionary key- actor name, value- actor id
    
    # What is Pierre Cochard's ID number?
    #print(type(namesdb))        # dictionary
    
    # Which actor has the ID 613224?
    #for key, value in namesdb.items(): 
    #    if value == 613224:
    #        print(key)          # ID number: 1265212
     
    # Check if actors acted together
    # Rose Byrne and Jill Eikenberry
    #dict_set_film = transform_data(smalldb)
    #acted_film1 = acted_together(dict_set_film, namesdb["Rose Byrne"], namesdb["Jill Eikenberry"])
    #print(acted_film1)       # False
           
    # Theresa Russell and Kevin Bacon
    #acted_film2 = acted_together(dict_set_film, namesdb["Theresa Russell"], namesdb["Kevin Bacon"])
    #print(acted_film2)    # True
    
    # Caluclating Bacon Number for 0, 1, 2, and 3
    transformed_data = transform_data(tinydb)
    
    # set of actors with indicated bacon number    
    #bacon_num0 = actors_with_bacon_number(transformed_data, 0)
    #bacon_num1 = actors_with_bacon_number(transformed_data, 1)
    #bacon_num2 = actors_with_bacon_number(transformed_data, 2)
    #bacon_num3 = actors_with_bacon_number(transformed_data, 3)
    
    #print(bacon_num0) # {4724}
    #print(bacon_num1) # {2876, 1532}
    #print(bacon_num2) # {1640}
    #print(bacon_num3) # set()
    
    
    # Calculating the Bacon Path
    transformed_data2 = transform_data(largedb)
    
    #bacon_path1 = bacon_path(transformed_data, 1640)
    #bacon_path2 = bacon_path(transformed_data2, 1019975)
    #print(namesdb["Amy Meredith"])   # 1019975

    #print(bacon_path1)   # [4724, 2876, 1640]
    #print(bacon_path2)   # [4724, 4610, 16483, 16660, 933065, 1019975]
    
    #bacon_actor_path = bacon_path2.copy()
    #actor_name_list = []
    
    # goes until you get all the actor names
    #while bacon_actor_path:
        
        # gets the first actor id
    #    actor_id = bacon_actor_path.pop(0)
        
    #    for key, value in namesdb.items():
            
    #        if value != actor_id:
    #            continue
    #        actor_name_list.append(key)
        
    #print(actor_name_list)  # ['Kevin Bacon', 'John Landis', 
                            # 'Sylvester Stallone', 'Sage Stallone', 
                            # 'Jim VanBebber', 'Amy Meredith']
                            
                            
    #print(namesdb["Jenny Alpha"])       # 543619
    #print(namesdb["Peter Riegert"])     # 20899
    
    #actor_actor_path = actor_to_actor_path(transformed_data2, 543619, 20899)
    #actor_name_list2 = []
    #actor_paths = actor_actor_path.copy()
    
    """while actor_paths:
        actor_id = actor_paths.pop(0)
        
        for key, value in namesdb.items():
            if value == actor_id:
                actor_name_list2.append(key)"""
                
    #print(actor_name_list2) # ['Jenny Alpha', 'Mati Diop', 
                            #  'Brady Corbet', 'Jeremy Sisto', 
                            #  'Ornella Muti', 'Peter Riegert']
 
    
    #print(namesdb["Max Elliott Slade"])   # 8187
    #print(namesdb["Anton Radacic"])         # 1345461
    #actor_actor_path = actor_to_actor_path(transformed_data2, 8187, 1345461)
    #actor_name_list2 = []
    #actor_paths = actor_actor_path.copy()
    
    #while actor_paths:
    #    actor_id = actor_paths.pop(0)
        
    #    for key, value in namesdb.items():
    #        if value == actor_id:
    #            actor_name_list2.append(key)
    
    #print("here are correct actors", actor_name_list2)
    #print()
    #movie_path2 = []
    #dict_actor_film2 = transformed_data2[0]
    #print(f"transformed_data: {transformed_data2}")
    #for actor1, actor2 in zip(actor_actor_path, actor_actor_path[1:]):
        
    #    for actor_tuple in dict_actor_film2[actor1]:
            
    #        if actor_tuple[0] == actor2:
    #            movie_path2.append(actor_tuple[1])
    #print(f"this is movie path: {movie_path2}")
            
    #movie_movie_path = movie_to_movie_path(transformed_data2, 8187, 1345461)
    #movie_path = movie_movie_path.copy()
    #movie_name = []
    
    #print(movie_movie_path)
    # goes through all the movies
    #while movie_path:
    #    id_movie = movie_path.pop(0)
    #    print("yo")
        # checks every film in the database
    #    for movie, movie_id in moviedb.items():
    #        print("hello there")
            # checks if you found correct movie
    #        if id_movie == movie_id:
                
    #            movie_name.append(movie)
    
    #print(movie_name)   # ['Apollo 13', 'Galaxy of Terror', 
                        # 'Hatchet', 'Alien Escape', 
                        # 'Ribbit', 'It Ends with the Taste of Smoke']
