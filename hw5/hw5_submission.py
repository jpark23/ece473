#!/usr/bin/python

import random
import collections
import math
import sys
from util import *

############################################################
# Problem 1: k-means
############################################################
def check(iteration, examples, old_centroids, centroids, distances, assignments):
    print("\niteration: "+str(iteration))
    print("examples = "+str(examples))
    print("old centroids = "+str(old_centroids))
    print("new centroids = "+str(centroids))
    print("distances = "+str(distances))
    print("assignments = "+str(assignments)+"\n")

def kmeans(examples, K, maxIters):
        import random, copy
        def calculateLoss(centroids, assignments, examples):
                loss = 0
                pre_comp = [dotProduct(examples[i], examples[i]) for i in range(len(examples))]
                for i in range(len(examples)):
                        mu_zi = centroids[assignments[i]]
                        phi_xi = examples[i]
                        addTo = dotProduct(mu_zi, mu_zi) - 2*dotProduct(mu_zi, phi_xi) + pre_comp[i]
                        assert(addTo >= 0)
                        loss += addTo
                return loss
        def initalize_centroids(examples_ic, K):
                centroids_ic = [examples_ic.pop(random.randrange(len(examples_ic))) for _ in range(K)]
                return centroids_ic, examples_ic
        def find_distances(examples2, centroids2, precomp2):
                distances2 = [[0]*len(centroids2) for _ in range(len(examples2))]
                for i in range(len(examples2)):
                        for j in range(len(centroids2)):
                                distances2[i][j] = precomp2[i] - 2*dotProduct(examples2[i], centroids2[j]) + dotProduct(centroids2[j], centroids2[j]) 
                return distances2 
        def assign_points(examples_ap, centroids, distances_ap):
                assignments_ap = [0 for example_ap in examples_ap]
                for i in range(len(distances_ap)):
                        test_ap = distances_ap[i]
                        assignments_ap[i] = test_ap.index(min(test_ap))
                return assignments_ap
        def compute_centroids(examples, assignments, centroids):
                new_centroids = []
                for i in range(len(centroids)):
                    avg_these = []
                    new_centroid = {}
                    # get values to average
                    for j in range(len(assignments)):
                        if (i == assignments[j]): avg_these.append(examples[j])    
                    for k in range(len(avg_these)):
                        increment(new_centroid, 1, avg_these[k])
                    for key in new_centroid:
                        new_centroid[key] /= len(avg_these)
                    new_centroids.append(new_centroid)
                return new_centroids
        '''
        examples: list of examples, each example is a string-to-double dict representing a sparse vector.
        K: number of desired clusters. Assume that 0 < K <= |examples|.
        maxIters: maximum number of iterations to run (you should terminate early if the algorithm converges).
        Return: (length K list of cluster centroids,
                list of assignments (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
                final reconstruction loss)
        '''
        # BEGIN_YOUR_CODE (our solution is 28 lines of code, but don't worry if you deviate from this)
        centroids, examples = initalize_centroids(examples, K)
        # print("inital centroids: "+str(centroids))
        # print("examples: "+str(examples)+"\n")
        precomp_dps = [dotProduct(example, example) for example in examples]
        for _ in range(maxIters):
                distances = find_distances(examples, centroids, precomp_dps)
                assignments = assign_points(examples, centroids, distances)
                old_centroids = copy.deepcopy(centroids)
                more_examples = copy.deepcopy(examples)
                centroids = compute_centroids(more_examples, assignments, centroids)
                # check(_, examples, old_centroids, centroids, distances, assignments)
                if (old_centroids == centroids): 
                        # print("coverged before max iterations")
                        break
        loss = calculateLoss(centroids, assignments, examples)
        # print("\ncentroids = "+str(centroids))
        # print("assignments = "+str(assignments))
        # print("loss = "+str(round(loss, 3))+"\n")
        return centroids, assignments, loss
        # END_YOUR_CODE
