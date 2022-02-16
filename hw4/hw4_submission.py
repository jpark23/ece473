#!/usr/bin/python

import random
import collections
import math
import sys

from sklearn.metrics import hinge_loss
from util import *

############################################################
# Problem 2: binary classification
############################################################

############################################################
# Problem 2a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    words = x.split()
    word_features = dict()
    for word in words:
        if word in word_features.keys():
            word_features[word] += 1
        else:
            word_features[word] = 1
    return word_features
    # END_YOUR_CODE

############################################################
# Problem 2b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta):
    '''Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!  You should call
    evaluatePredictor() on both trainExamples and testExamples to see
    how you're doing as you learn after each iteration, storing the
    results as required for the resulting print statement included below.
    '''
    # BEGIN_YOUR_CODE (our solution is 13 lines of code, but don't worry if you deviate from this)    
    weights = {}

    ## sgd
    for _ in range(numIters): 
        for x, y in trainExamples:
            word_features = featureExtractor(x)
            for key in word_features:
                if ( (key not in weights) or ((word_features[key] * y * weights[key]) >= 1) ):
                    word_features[key] = 0
                else:
                    word_features[key] = -(word_features[key] * y) 
            increment(weights, -eta, word_features)
        
        ## testing
        def predictor(x):
            dot = dotProduct(weights, featureExtractor(x))
            if dot >= 0: return 1
            elif dot < 0: return -1

        trainError = evaluatePredictor(trainExamples, predictor)
        testError = evaluatePredictor(testExamples, predictor)
        print("Training error rate: {:.4f}, Validation error rate: {:.4f}".format(trainError, testError))
    
    # END_YOUR_CODE
    return weights

############################################################
# Problem 2c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a nonzero score under the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 2e: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces mapped to their n-gram counts.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE
    return extract

