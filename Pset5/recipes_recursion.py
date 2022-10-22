# Recipes Database
# NO ADDITIONAL IMPORTS!
import sys

sys.setrecursionlimit(20_000)

def replace_item(recipes, old_name, new_name):
    """
    Returns a new recipes list based on the input list, where all mentions of
    the food item given by old_name are replaced with new_name.
    """
    new_recipe = []
    
    # iterates through all the elements in recipe list
    for ingredients in recipes:
        
        # checks if ingredient is atomic and has old name
        if ingredients[0] == "atomic" and ingredients[1] == old_name:
            new_recipe.append(("atomic", new_name, ingredients[2]))
        
        # checks if ingredient is compound
        elif ingredients[0] == "compound":
            new_compound_list = []
            new_ele = ingredients[1]
            
            if new_ele == old_name:
                new_ele = new_name
            
            # iterates through all ingredients in compound recipe list
            for ingred in ingredients[2]:
                new_ingred = ingred[0]
                
                # checks if inner ingredient tuple has old ingredient
                if new_ingred == old_name:
                    new_ingred = new_name
                
                new_compound_list.append((new_ingred, ingred[1]))
            
            new_recipe.append(("compound", new_ele, new_compound_list))
        # adds atomic ingredient to recipe list
        else:
            new_recipe.append(ingredients)
    
    # returns new list of ingredients for recipe
    return new_recipe
        
    """new_compound_list = [(new_name, ingred[1]) 
                         if ingred[0] == old_name 
                         else (old_name, ingred[1])
                         for ingred in ingredients[2]]"""

def lowest_cost(recipes, food_item, forbidden_food_items=[]):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    transformed_recipes = transform_data(recipes) # transforms the data structure of recipes
    
    # helper recursive function to find lowest cost to create food
    def recursive_lowest_cost(recur_food_item):
        """
        Recursively call function until you find the minimum cost to make a
        specific compound food item
        """
        min_cost = float("inf")
        
        # check if food item is forbidden to use
        if recur_food_item in forbidden_food_items:
            return None
     
        # check for a valid key
        if recur_food_item not in transformed_recipes:
            return None    
        
        # base case
        # checks if food item is atomic
        #if isinstance(transformed_recipes[recur_food_item], int):
        if isinstance(transformed_recipes[recur_food_item], (int, float)):
            # returns cost to make atomic food item
            return transformed_recipes[recur_food_item]
        
        # recursive step
        # food item is a compound, comprised of other compound or atomic food items
        else:
            
            # iterates through all the ways to make a compound food item
            for food_recipe_list in transformed_recipes[recur_food_item]:
                
                cost_to_make = 0
                
                # iterates through all the food items
                for food_items in food_recipe_list:
            
                    food_cost = recursive_lowest_cost(food_items[0])
                    
                    # checks if food is in not in recipe
                    if food_cost == None:
                        break
        
                    cost_to_make += food_cost*food_items[1]
                
                # calculates min only for valid recipes
                else:
                    min_cost = min(cost_to_make, min_cost) # updates minimum cost
        
        # returns the min cost to make a specific food item
        return min_cost if min_cost != float("inf") else None
    
    # finds the minimum cost of all the different ways to make a specific food item
    return recursive_lowest_cost(food_item)

def cheapest_flat_recipe(recipes, food_item, forbidden_food_items=[]):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing a full recipe for
    the given food item.
    """
    transformed_recipes = transform_data(recipes)
    
    def cost_for_recipe(food_dict):
        """
        food_dict- dict, {food_name: scaled_quantity, ...}
        
        Gets the total cost to make a provided recipe
        """
        return sum(transformed_recipes[food]*quantity for food, quantity in food_dict.items())
       
    def scaling_quantity(recipe_dict, scaling_factor):
        """
        recipe_dict, dict, {food_name: quantity}
        scaling_factor, the amount of food items needed to make a compound food item 
        
        Returns a dictionary with the scaled quantities for food items in a recipe
        """
                
        return {food:quantity*scaling_factor for food, quantity in recipe_dict.items()}

    def sum_quantities_dict(dict1, dict2):
        """
        Combines two dictionaries with all the {food_name:quantity} mapping
        together into one dictionary
        """
        dict3 = {}
        
        # gets all the food from the first dictionary and new mapping to its quantity
        for food, quantity in dict1.items():
            
            if food not in dict3:
                dict3[food] = 0
            
            dict3[food]+=quantity
        
        # gets all the food from the second dictionary and new mapping to its quantity
        for food, quantity in dict2.items():
            
            if food not in dict3:
                dict3[food] = 0
            
            dict3[food]+=quantity
             
        # combines the two dictionaries and sums corresponding values
        return dict3
    
    def recursive_cheapest_flat_recipe(recur_food_item):
        """
        Gets the cheapest costing flat recipe for a given food item
        """
          
        min_flat_recipes = {}
    
        # checks you don't want to buy food item
        if recur_food_item in forbidden_food_items:
            return None
        
        # checks if food not in store
        if recur_food_item not in transformed_recipes:
            return None
        
        # base case
        # checks if food item is atomic
        if isinstance(transformed_recipes[recur_food_item], (int, float)):
            return {recur_food_item: 1}
        
        # recursive step
        else:
            # iterates through all the ways to make a food item
            for recipe_list in transformed_recipes[recur_food_item]:
                
                new_flat_recipe = {}
                
                # iterates through all the food items in the recipe
                for food_tuple in recipe_list:
                    
                    flat_dict = recursive_cheapest_flat_recipe(food_tuple[0])
                    
                    # checks if there's no possible flat possible
                    if flat_dict == None:
                        break
                    
                    # scales the quantities of the current flat recipe
                    flat_dict = scaling_quantity(flat_dict, food_tuple[1])
                    
                    # recombines the flat dictionary
                    new_flat_recipe = sum_quantities_dict(flat_dict, new_flat_recipe)
                
                # only executes if valid flat recipe
                else:
                    recipe_cost = cost_for_recipe(new_flat_recipe)
                    min_flat_recipes[recipe_cost] = new_flat_recipe
            
        # gets the minimum costing flat recipe
        if min_flat_recipes != {}:
            return min_flat_recipes[min(min_flat_recipes.keys())]
            
        # no possible flat recipe
        else: 
            return None
    
    # returns the cheapest costing flat recipe, if there is one
    return recursive_cheapest_flat_recipe(food_item)

def all_flat_recipes(recipes, food_item, forbidden_food_items=[]):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.
    """
    transformed_recipes = transform_data(recipes)
    
    def scaling_quantity_list_dict(list_of_dict, scaling_factor):
        """
        Given a list of flat recipes. Goes through each food item in the flat 
        recipe recipe(dictionary) and scales it and updates the flat recipe 
        dictionary in the list
        """
        # iterates through the list of possible food items
        for index, recipe_dict in enumerate(list_of_dict):
            # scales each food item in the flat recipe dictionary
            list_of_dict[index] = {food_name: quantity*scaling_factor 
                                   for food_name, quantity in recipe_dict.items()}    
            
        # returns a list of flat recipe dictionaries
        return list_of_dict
    
    def sum_quantities_dict(dict1, dict2):
        """
        Given two dictionaries, combine the two dictionaries into one dictionary
        """
        dict3 = {}
        
        # gets all the food from the first dictionary and new mapping to its quantity
        for food, quantity in dict1.items():
            
            if food not in dict3:
                dict3[food] = 0
            
            dict3[food]+=quantity
        
        # gets all the food from the second dictionary and new mapping to its quantity
        for food, quantity in dict2.items():
            
            if food not in dict3:
                dict3[food] = 0
            
            dict3[food]+=quantity
             
        # combines the two dictionaries and sums corresponding values
        return dict3
    
    def sum_quantities_list_dict(list_of_dict1, list_of_dict2):
        """
        Makes Combines two dictionaries together
        """
        list_of_dict3 = []
        
        # iterates through every flat recipe 
        for recipe_dict1 in list_of_dict1:
            
            # iterates through every flat recipe
            for recipe_dict2 in list_of_dict2:
                
                # makes a new flat recipe combinations
                new_recipe_dict = sum_quantities_dict(recipe_dict1, recipe_dict2)
            
                # adds new combination of flat recipes
                list_of_dict3.append(new_recipe_dict)
             
        # combines two lists of flat recipe dictionaries
        return list_of_dict3
        
    def recursive_all_flat_recipes(recur_food_item):
        """
        Finds all possible flat recipes for a food item
        """
        all_flat_recipes = []
        
        # checks if food item is not available in store
        if recur_food_item in forbidden_food_items:
            return []
        
        # checks if not a valid food item
        if recur_food_item not in transformed_recipes:
            return []
        
        # base case
        # checks if the food item is atomic
        if isinstance(transformed_recipes[recur_food_item], (int, float)):
            return [{recur_food_item: 1}]
        
        # recursive step
        else:
            # gets all the different recipes for a food item
            for food_recipe in transformed_recipes[recur_food_item]:
                # list of all flat recipes to ake food items for a recipe
                new_recipe = [{}]
            
                # gets all the food in a food item recipe
                for food_tuple in food_recipe: 
                    
                    # all the different ways to make a flat recipe
                    flat_recipe = recursive_all_flat_recipes(food_tuple[0])
                    
                    # checks if no valid flat recipe
                    if flat_recipe == []:
                        break
                    
                    flat_recipe = scaling_quantity_list_dict(flat_recipe, food_tuple[1])
                    new_recipe = sum_quantities_list_dict(flat_recipe, new_recipe)
                    
                else:
                    all_flat_recipes.extend(new_recipe)
        
        # returns every possible combination of food items that would create the provided food
        return all_flat_recipes
    
    # returns all the flat recipes
    return recursive_all_flat_recipes(food_item)

def transform_data(recipes):
    """
    Given a list of recipes transform the data into a dictionary mapping 
    dictionary maps compounds to all its ingredients it is comprised of
    or an atomic food mapped to the cost to make it
    
    {compound_food1: [(food_item1, food_value1), (food_item2, food_value2), ...],
     ..., 
     atomic_food1: food_value1,
     atomic_food2: food_value2,
     ...}
    """
    
    # transformed_recipes = {ingred[1]:ingred[2] for ingred in recipes}
    transformed_recipes = {}
    
    # iterates through all the food items
    for ingred in recipes:
        
        # checks if you have not already 
        if ingred[1] not in transformed_recipes and ingred[0] == "atomic":
            transformed_recipes[ingred[1]] = ingred[2]
        
        # checks if you have not already 
        if ingred[1] not in transformed_recipes and ingred[0] == "compound":
            transformed_recipes[ingred[1]] = []
        
        # checks if food item is a compound
        if ingred[0] == "compound":
            transformed_recipes[ingred[1]].append(ingred[2])
    
    # returns a dictionary representation of the list of recipes
    return transformed_recipes

if __name__ == "__main__":
  
    smaller_recipes = [
    ('compound', 'chili', [('cheese', 2), ('protein', 3), ('tomato', 2)]),
    ('compound', 'milk', [('cow', 1), ('milking stool', 1)]),
    ('compound', 'cheese', [('milk', 1), ('time', 1)]),
    ('compound', 'protein', [('cow', 1)]),
    ('atomic', 'cow', 100),
    ('atomic', 'tomato', 10),
    ('atomic', 'milking stool', 5),
    ('atomic', 'time', 10000),
    ]
        
    cookie_monsta = [
    ('compound', 'cookie sandwich', [('cookie', 2), ('ice cream scoop', 3)]),
    ('compound', 'cookie', [('chocolate chips', 3)]),
    ('compound', 'cookie', [('sugar', 10)]),
    ('atomic', 'chocolate chips', 200),
    ('atomic', 'sugar', 5),
    ('compound', 'ice cream scoop', [('vanilla ice cream', 1)]),
    ('compound', 'ice cream scoop', [('chocolate ice cream', 1)]),
    ('atomic', 'vanilla ice cream', 20),
    ('atomic', 'chocolate ice cream', 30),
    ]
    
    #minimum_cost = lowest_cost(cookie_monsta, 'cookie sandwich')
    #print(minimum_cost)
    
    #all_recipes1 = all_flat_recipes(cookie_monsta, "cookie sandwich")
    #print(all_recipes)
    
    #all_recipes2 = all_flat_recipes(cookie_monsta, 'sugar')
    #print(all_recipes2)
    
    #all_recipes3 = all_flat_recipes(cookie_monsta, 'tomato')
    #print(all_recipes3)
    
    #all_recipes4 = all_flat_recipes(cookie_monsta, 'cookie sandwich', ('sugar',))
    #print(all_recipes4)
    
    #all_recipes5 = all_flat_recipes(cookie_monsta, 'cookie sandwich', ('sugar', 'chocolate ice cream'))
    #print(all_recipes5)
    
    #all_recipes6 = all_flat_recipes(cookie_monsta, 'cookie sandwich', ('cookie',))
    #print(all_recipes6)
