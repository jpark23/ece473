import collections
import math

############################################################
# Problem 3a

def findAlphabeticallyLastWord(text):
    """
    Given a string |text|, return the word in |text| that comes last
    alphabetically (that is, the word that would appear last in a dictionary).
    A word is defined by a maximal sequence of characters without whitespaces.
    You might find max() and list comprehensions handy here.
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return (max(text.casefold().split()))
    # END_YOUR_CODE

############################################################
# Problem 3b

def euclideanDistance(loc1, loc2):
    """
    Return the Euclidean distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    from math import sqrt 
    ydiff = loc1[1] - loc2[1]
    xdiff = loc1[0] - loc2[0]
    ysquare = ydiff**2
    xsquare = xdiff**2
    return(sqrt(ysquare + xsquare))
    # END_YOUR_CODE

############################################################
# Problem 3c
def find_similars_helper(similars, word_dict, current_word, word_count, current_word_count):
#     print(str(current_word)+" "+str(current_word_count))
    nexts = word_dict.get(current_word, 0)
    if (current_word_count == word_count):
        similars.append(current_word)
        return 
    if not nexts:
        similars.append(current_word)
        return 
    for next_word in nexts:
        word = find_similars_helper(similars, word_dict, next_word, word_count, current_word_count + 1)
        similars.append(current_word)
        return

def mutateSentences(sentence):
    """
    Given a sentence (sequence of words), return a list of all "similar"
    sentences.
    We define a sentence to be similar to the original sentence if
      - it has the same number of words, and
      - each pair of adjacent words in the new sentence also occurs in the original sentence
        (the words within each pair should appear in the same order in the output sentence
         as they did in the original sentence.)
    Notes:
      - The order of the sentences you output doesn't matter.
      - You must not output duplicates.
      - Your generated sentence can use a word in the original sentence more than
        once.
    Example:
      - Input: 'the cat and the mouse'
      - Output: ['and the cat and the', 'the cat and the mouse', 'the cat and the cat', 'cat and the cat and']
                (reordered versions of this list are allowed)
    """
    # BEGIN_YOUR_CODE (our solution is 21 lines of code, but don't worry if you deviate from this)
    # build the next word dictionary
    word_dict = {}
    words = sentence.split()
    index = 0
    while(index < len(words)-1):
        test_entry = words[index]
        if(test_entry not in word_dict):
            new_value = list()
            new_value.append(words[index + 1])
            word_dict[test_entry] = new_value
        else:
            word_dict[test_entry].append(words[index+1]) 
        index += 1
    word_dict[words[len(words)-1]] = []
    # getting word count
    word_count = len(words)
    # starting recursion
    similar_sentences = list()
    similar_sentences.append(sentence)
    for key in word_dict:
        similars = list()
        find_similars_helper(similars, word_dict, key, word_count, 1)
        similars.reverse()
        similar_sentence = ' '.join(map(str, similars))
        if(len(similars) == 5):
            similar_sentences.append(similar_sentence)
    return similar_sentences
    # END_YOUR_CODE

############################################################
# Problem 3d

def sparseVectorDotProduct(v1, v2):
    """
    Given two sparse vectors |v1| and |v2|, each represented as collections.defaultdict(float), return
    their dot product.
    You might find it useful to use sum() and a list comprehension.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    v1_values = list()
    v2_values = list()
    vector_size = max(len(v1.keys()), len(v2.keys()))
    for value in v1.values():
        v1_values.append(value)
    for value in v2.values():
        v2_values.append(value)
    v2_values.reverse()
    while(len(v1_values) != vector_size):
        v1_values.append(0)
    while(len(v2_values) != vector_size):
        v2_values.append(0)
    index = 0
    sum = 0
    while(index < vector_size):
        sum += v1_values[index] * v2_values[index]
        index += 1
    return sum
    # END_YOUR_CODE

############################################################
# Problem 3e

def incrementSparseVector(v1, scale, v2):
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    for key in v2:
        v1[key] += scale * v2[key]
    # END_YOUR_CODE

############################################################
# Problem 3f

def findSingletonWords(text):
    """
    Splits the string |text| by whitespace and returns the set of words that
    occur exactly once.
    You might find it useful to use collections.defaultdict(int).
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    words = text.split()
    occurences = collections.defaultdict(int)
    for word in words:
        occurences[word] += 1
    singletons = set()
    for word in occurences:
        if(occurences[word] == 1):
            singletons.add(word)
    return(singletons)
    # END_YOUR_CODE

############################################################
# Problem 3g

def computeLongestPalindromeLength(text):
    """A palindrome is a string that is equal to its reverse (e.g., 'ana').
    Compute the length of the longest palindrome that can be obtained by deleting
    letters from |text|.
    For example: the longest palindrome in 'animal' is 'ama'.
    Your algorithm should run in O(len(text)^2) time.
    You should first define a recurrence before you start coding.

    Hint: Let lpl(i,j) be the longest palindrome length of the substring text[i...j].

    Argue that lpl(i,j) = lpl(i+1, j-1) + 2 if text[i] == text[j], and
                          max{lpl(i+1, j), lpl(i, j-1)} otherwise
    (be careful with the boundary cases)

    Instead of writing a recursive function to find lpl (the most
    straightforward way of implementation has exponential running time
    due to repeated computation of the same subproblems), start by
    defining a 2-dimensional array which stores lpl(i,j), and fill it
    up in the increasing order of substring length.
    """
    # BEGIN_YOUR_CODE (our solution is 13 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE
