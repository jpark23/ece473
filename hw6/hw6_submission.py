from tracemalloc import start
from pyrsistent import b
import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def start(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 0
        # END_YOUR_CODE

    def goalp(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return state == len(self.query)
        # END_YOUR_CODE

    def expand(self, state):
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        current_state = state
        expansions = []
        string = ""
        for letter in self.query[(state):]:
            string += letter
            cost = self.unigramCost(string)
            current_state += 1
            expansions.append((string, current_state, cost))
        return expansions
        # END_YOUR_CODE

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return " ".join(ucs.actions)
    # END_YOUR_CODE

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords # list of words
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def start(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return (wordsegUtil.SENTENCE_BEGIN, 0)
        # END_YOUR_CODE

    def goalp(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return state[1] == len(self.queryWords) 
        # END_YOUR_CODE

    def expand(self, state): # state = (previous word, index of current word)
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        prev_word = state[0]
        current_index = state[1]
        current_word = self.queryWords[current_index]
        expansions = []
        fills = self.possibleFills( current_word )
        if not fills: return [ (current_word, (current_word, current_index+1), self.bigramCost(prev_word, current_word)) ]
        for fill in fills:
            expansions.append( ( fill, (fill, current_index+1), self.bigramCost(prev_word, fill) ) )
        return expansions
        # END_YOUR_CODE

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    if len(queryWords) == 0: return ""
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))
    return " ".join(ucs.actions)
    # END_YOUR_CODE

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def start(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return (wordsegUtil.SENTENCE_BEGIN, 0)
        # END_YOUR_CODE

    def goalp(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return state[0] == len(self.query)
        # END_YOUR_CODE

    def expand(self, state):
        # BEGIN_YOUR_CODE (our solution is 5 lines of code, but don't worry if you deviate from this)
        # 2 loops, for every space added, think of every vowel instance of that space, put that combo into the cost function
        prev_word = state[0]
        index = state[1]
        expansions = []
        string = ""
        while index < len(self.query):
            string += self.query[index]
            fills = self.possibleFills(string)
            index += 1
            if not fills: continue 
            else:
                for fill in fills: expansions.append( (fill, (fill, index), self.bigramCost(prev_word, fill)) )
                break
        return expansions
        # END_YOUR_CODE

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    if len(query) == 0: return ""
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills))
    print(ucs.actions)
    return " ".join(ucs.actions)
    # END_YOUR_CODE

############################################################

if __name__ == '__main__':
    shell.main()
