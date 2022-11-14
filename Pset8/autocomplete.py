# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree, or reassign the
        associated value if it is already present.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is not
        a string.
        """
        # raises a type error if key is not a string
        if not isinstance(key, str):
            raise TypeError
            
        # checks if you are at the last element
        if len(key) == 0:
            self.value = value
            
        # recursive case
        else:
            key_first_element = key[0]
            
            # checks if you need to add child to node
            if key_first_element not in self.children:
                self.children[key_first_element] = PrefixTree()
            
            rest_of_key = key[1:] # if key is length 1 it will return empty string
                
            self.children[key_first_element].__setitem__(rest_of_key, value)
            
    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the prefix tree, raise a KeyError.  If the given key is not a string,
        raise a TypeError.
        """
        # checks if key is a string
        if not isinstance(key, str):
            raise TypeError
         
        # tries to get the value of key
        #try:
            # base case:
        if len(key) == 0:
            if self.value is None:
                raise KeyError
                
            return self.value
            
        # recursive step
        else:
            key_first = key[0]
            
            if key_first not in self.children:
                raise KeyError
            
            key_rest = key[1:]
            
            # checks if first element is a child of the node
            return self.children[key_first].__getitem__(key_rest)
        
    def get_rest_of_tree(self, prefix):
        """
        Return the rest of the Prefix Tree instance after a specific node
        indicated by prefix- a string presumably comprised of prefix of 
        a word in prefix tree
        """
        # checks for valid prefixes types
        if not isinstance(prefix, str):
            raise TypeError
        
        # base case
        if len(prefix) == 0:
            # returns the prefix tree
            return self
        
        else:
            prefix_first = prefix[0]
            prefix_rest = prefix[1:]
            
            # checks if prefix points to another node in prefix tree
            if prefix_first not in self.children:
                raise KeyError
            
            # recursive call to go further down prefix tree
            return self.children[prefix_first].get_rest_of_tree(prefix_rest)

    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists. If the given
        key is not in the prefix tree, raise a KeyError.  If the given key is
        not a string, raise a TypeError.
        """
        # checks if key is a string
        if not isinstance(key, str):
            raise TypeError
            
        if len(key) == 0:
            if self.value is None:
                raise KeyError
            
            else:
                self.value = None # a None value means the node should be deleted 
          
        else:
            key_first = key[0]
            
            if key_first not in self.children:
                raise KeyError
                
            key_rest = key[1:]
            
            self.children[key_first].__delitem__(key_rest)

    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.  If the given
        key is not a string, raise a TypeError.
        """
        # checks if key is a string
        if not isinstance(key, str):
            raise TypeError
        
        if len(key) == 0:
            if self.value is None:
                return False
            return True
        
        else:
            key_first = key[0]
            
            if key_first not in self.children:
                return False
            key_rest = key[1:]
            
            return self.children[key_first].__contains__(key_rest)

    def __iter__(self, key=""):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        
        # checks if there are no more children
        if not self.children:
            # checks if value should be displayed
            if self.value is not None:
                yield (key, self.value)
        
        # recursive step
        else:
            # checks if there is a value to return
            if self.value is not None:
                yield (key, self.value)
                
            # goes through all the children nodes
            for key2 in self.children:                
            
                yield from self.children[key2].__iter__(key+key2)

def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """
    list_of_sentences = tokenize_sentences(text)
    list_of_words = [word for sentence in list_of_sentences 
                             for word in sentence.split(" ")]
    frequency = {}
    
    # creates a dictionary mapping a word to its frequency in text
    for word2 in list_of_words:
        
        # adds word to dictionary mapping word to it's frequency
        if word2 not in frequency:
            frequency[word2] = 0
        frequency[word2]+=1
    
    prefix_tree = PrefixTree()
    
    # adds each word to the prefix tree instance
    for word3, freq in frequency.items():
        prefix_tree[word3] = freq
        
    # returns a prefix tree instance
    return prefix_tree

def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    """
    
    # checks if prefix is a string
    if not isinstance(prefix, str):
        raise TypeError
    
    # tries to get all the rest of the prefix 
    # tree beginning with specific prefix
    try:
        tree_prefix = tree.get_rest_of_tree(prefix)
    
    # runs into a key error
    except:
        return []
    
    # execute the code as normal
    else:
        list_of_nodes = [(prefix + suffix_, value) for suffix_, value in tree_prefix]
        
        # checks if you are to print entire prefix tree with specific prefix
        if max_count is None or len(list_of_nodes) < max_count:
            return [prefix + suffix for suffix, value in tree_prefix]
        
        
        freq_word_list = []
        
        # goes until there is either no more nodes to print or
        # have gotten the most frequently words seen in text
        while max_count and list_of_nodes:
            max_freq_word_tuple = list_of_nodes[0]
            # finds word with maximum frequency in text
            for word_tuple in list_of_nodes:
                
                if max_freq_word_tuple[1] < word_tuple[1]:
                    max_freq_word_tuple = word_tuple
                
            list_of_nodes.remove(max_freq_word_tuple)
            freq_word_list.append(max_freq_word_tuple[0])
            max_count-=1
    
    # returns a list of words with the max frequency up to max_count
    return freq_word_list

def all_single_character_swap(tree, prefix, valid_words_set, autocomplete_words):
    """
    Generates a list of all possible prefixes that
    has any two adjacent letters swapped with each other
    """
    all_prefixes = set()
    
    # goes through each character in prefix
    for i in range(len(prefix)-1):
        char1 = prefix[i]
        char2 = prefix[i+1]
        
        # swaps two letters in prefix
        new_prefix = prefix[0:i] + char2 + char1 + prefix[i+2:]
        
        # checks if the new edit is in prefix tree
        if ((new_prefix in valid_words_set) and (autocomplete_words is not None)
            and (new_prefix not in autocomplete_words)):
            all_prefixes.add((new_prefix, tree[new_prefix]))
    
    return all_prefixes

def all_single_character_replace(tree, prefix, valid_words_set, autocomplete_words):
    """
    Generates a list of all possible prefixes that has any of 
    the letters replaced by any of the letters in the alphabet
    """
    all_prefixes = set()
    
    # iterates through each letter in prefix
    for i in range(len(prefix)):
        
        # goes through each letter in alphabet
        for alphabet_int in range(97, 123):
            char = chr(alphabet_int)
           
            # replace one of the letters in prefix
            # with any letter in alphabet
            new_prefix = prefix[0:i] + char + prefix[i+1:]
            
            # checks if the new edit is in prefix tree
            if ((new_prefix in valid_words_set) and (autocomplete_words is not None)
                and (new_prefix not in autocomplete_words)):
                all_prefixes.add((new_prefix, tree[new_prefix]))
    
    return all_prefixes

def all_single_character_insert(tree, prefix, valid_words_set, autocomplete_words):
    """
    Generates a list of all possible prefixes that have 
    one letter inserted into the prefix
    """
    all_prefixes = set()  
    
    # 
    for i in range(len(prefix)):
        for alphabet_int in range(97, 123):
            char = chr(alphabet_int)
            
            # inserts alphabet letter at beginning of prefix
            if i == 0:
                new_prefix = char + prefix
            # inserts alphabet letter at any other point in prefix
            else:
                new_prefix = "" + prefix[0:i+1] + char + prefix[i+1:]
            
            # checks if the new edit is in prefix tree
            if ((new_prefix in valid_words_set) and (autocomplete_words is not None) 
                and (new_prefix not in autocomplete_words)):
                
                all_prefixes.add((new_prefix, tree[new_prefix]))
                
    return all_prefixes

def all_single_character_del(tree, prefix, valid_words_set, autocomplete_words):
    """
    Generates a list of all possible prefixes that have one letter removed
    """
    all_prefixes = set()
    
    # iterates through the prefix
    for i in range(len(prefix)):
        # deletes a letter from prefix
        new_prefix = prefix[0:i] + prefix[i+1:]
        
        # checks if the new edit is in prefix tree
        if ((new_prefix in valid_words_set) and (autocomplete_words is not None)
            and (new_prefix not in autocomplete_words)):
            all_prefixes.add((new_prefix, tree[new_prefix]))
            
    return all_prefixes

def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    all_valid_words_set = set()
    max_freq_words_list = autocomplete(tree, prefix, max_count) 
    
    # checks if you have already reached the max count for most frequent words list
    if len(max_freq_words_list) == max_count:
        return max_freq_words_list
    
    max_freq_words_set = set(max_freq_words_list)
    all_nodes = {nodes[0] for nodes in tree}
    
    # all possible prefix edits
    words_set1 = all_single_character_del(tree, prefix, all_nodes, max_freq_words_set)
    words_set2 = all_single_character_insert(tree, prefix, all_nodes, max_freq_words_set)
    words_set3 = all_single_character_replace(tree, prefix, all_nodes, max_freq_words_set)
    words_set4 = all_single_character_swap(tree, prefix, all_nodes, max_freq_words_set)
    
    all_valid_words_set.update(words_set1, words_set2, words_set3, words_set4)
        
    # checks if you should return all possible words
    if max_count is None:
        all_words = [word[0] for word in all_valid_words_set]
        all_words.extend(max_freq_words_list)
        return all_words
    
    all_valid_words_list = list(all_valid_words_set)
    
    while max_count-len(max_freq_words_list) > 0 and all_valid_words_set:
        max_word_tuple = all_valid_words_list[0]
        
        # finds the max element in the all valid words list
        for word_tuple in all_valid_words_list:
            if max_word_tuple[1] < word_tuple[1]:
                max_word_tuple = word_tuple
        
        all_valid_words_list.remove(max_word_tuple)
        max_freq_words_list.append(max_word_tuple[0])
        
    return max_freq_words_list

def word_filter(tree, pattern):
    """
    Return list of (word, freq) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    # shorten the pattern so omit repeated stars
    
    
    def recursive_word_filter(recursive_tree, recursive_pattern, word=""):
        """
        Recursively generates a set of all possible words 
        that can be a part of the provided pattern
        """
        all_word_tuple_set = set()
        
        # base case
        if len(recursive_pattern) == 0:
            
            # checks if there is a valid word to return
            if recursive_tree.value is not None:
                return [(word, recursive_tree.value)]
                
        # recursive step
        else:
            pattern_first = recursive_pattern[0]
            pattern_rest = recursive_pattern[1:]
            
            # checks for the * case
            if pattern_first == '*':
                # makes a list of all possible list returned 
                # from recursive call maybe have to use extend
                all_word_tuple_set.update(recursive_word_filter(recursive_tree, 
                                                                  pattern_rest, word))
                
                for child in recursive_tree.children:
                    all_word_tuple_set.update(recursive_word_filter(recursive_tree.children[child], 
                                                                      recursive_pattern, 
                                                                      word+child))
            # checks for the ? case
            elif pattern_first == '?':
                
                # make a list of all possible options
                for child in recursive_tree.children:
                    all_word_tuple_set.update(recursive_word_filter(recursive_tree.children[child], 
                                                                      pattern_rest, word+child))
             
            # checks for the alphabet letter case
            else:
                if pattern_first in recursive_tree.children:
                    all_word_tuple_set.update(recursive_word_filter(recursive_tree.children[pattern_first], 
                                                      pattern_rest, word + pattern_first))
                            
        return all_word_tuple_set
            
    # returns the list of (word, freq) for all  
    # words in prefix tree matching the pattern
    return list(recursive_word_filter(tree, pattern))

# you can include test cases of your own in the block below.
if __name__ == "__main__":
    doctest.testmod()
    
    text = "toonces was a cat who could drive a car very fast until he crashed"
    tree = word_frequencies("bat bat bark bar")
    #tree = PrefixTree()
    #tree["bat"] = 7
    #tree["bark"] = 4
    #tree["bar"] = 1
    #tree["happy"] = 2
    #tree["heart"] = 4
    #tree["hope"] = 5
    #tree["positive"] = 2
    prefix = "ba"
    #answer = autocomplete(tree, prefix, 1)
    #new_answer = autocorrect(tree, prefix, 10)
    #print(new_answer)
    with open('testing_data/frankenstein.txt', encoding='utf-8') as f:
        text2 = f.read()
    tree2 = word_frequencies(text2)
    #answer = autocorrect(tree2, 'mon', 15)
    #for i, ans in enumerate(answer):
    #    print(f"this is the {i}th element: {ans}")
    
    with open("testing_data/pride_and_prejudice.txt", encoding="utf-8") as f:
        text3 = f.read()
    tree3 = word_frequencies(text3)
    
    with open("testing_data/alice_in_wonderland.txt", encoding="utf-8") as f:
        text4 = f.read()
    tree4 = word_frequencies(text4)

    with open("testing_data/dracula.txt", encoding="utf-8") as f:
        text5 = f.read()
    tree5 = word_frequencies(text5)
    
    with open("testing_data/a_tale_of_two_cities.txt", encoding="utf-8") as f:
        text6 = f.read()
    tree6 = word_frequencies(text6)
    
    with open("testing_data/metamorphosis.txt", encoding="utf-8") as f:
        text7 = f.read()
    tree7 = word_frequencies(text7)
    all_nodes5 = [node for node in tree5]
    #print(f"number of words in dracula: {len(all_nodes5)}")
    
    total_sum = 0
    
    #for word, value in all_nodes5:
    #    total_sum+=value
        
    #print(f"these are all the words in dracula: {total_sum}")
    complete = autocomplete(tree7, "gre", 6)
    #print(f"this is auto complete for metamorphosis: {complete}")
    
    all_correction = autocorrect(tree4, 'hear', 12)
    #print(f"this is all corrections for alice in wonderland: {all_correction}")
    
    all_correction = autocorrect(tree3, 'hear', None)
    #print(f"this is all corrections for pride and prejudice: {all_correction}")
    
    #result = word_filter(tree, "bat")
    #print(f"this is my result: {result}")
    
    #result = word_filter(tree7, "c*h")
    #print(f"this is word filter for metamorphosis: {result}")
    
    #result = word_filter(tree6, "r?c*t")
    #print(f"this is word filter for a tale of two cities: {result}")
