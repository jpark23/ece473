from audioop import avg
import random 
from hw5_submission import kmeans
from util import *

def check(iteration, examples, old_centroids, centroids, distances, assignments):
    print("\niteration: "+str(iteration))
    print("examples = "+str(examples))
    print("old centroids = "+str(old_centroids))
    print("new centroids = "+str(centroids))
    print("distances = "+str(distances))
    print("assignments = "+str(assignments)+"\n")

def kmeans(examples, K, maxIters):
        import random, copy
        def calculateLoss(centroidsLoss, assignmentsLoss, examplesLoss):
                loss = 0
                pre_comp = [dotProduct(examplesLoss[i], examplesLoss[i]) for i in range(len(examplesLoss))]
                for i in range(len(examplesLoss)):
                        mu_zi = centroidsLoss[assignmentsLoss[i]]
                        phi_xi = examplesLoss[i]
                        addTo = dotProduct(mu_zi, mu_zi) - 2*dotProduct(mu_zi, phi_xi) + pre_comp[i]
                        assert(addTo >= 0)
                        loss += addTo
                return loss
        def initalize_centroids(examples, K):
                centroids = [examples.pop(random.randrange(len(examples))) for _ in range(K)]
                return centroids, examples
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
        def compute_centroids(examples_cc, assignments):
                # print(examples)
                # print(assignments)
                new_centroids = []
                for i in range(max(assignments)+1):
                    avg_these = []
                    for j in range(len(assignments)):
                        if (i == assignments[j]): 
                            example = examples_cc[j]
                            avg_these.append(example)
                    for k in range(len(avg_these)-1):
                        increment(avg_these[k+1], 1, avg_these[k])
                    for key in avg_these[-1]:
                        avg_these[-1][key] /= len(avg_these) 
                    new_centroids.append(avg_these[-1])
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
        # centroids = [{0:2, 1:3}, {0:2, 1:-1}]
        # examples = [{0:1, 1:0}, {0:1, 1:2}, {0:3, 1:0}, {0:2, 1:2}]
        precomp_dps = [dotProduct(example, example) for example in examples]
        for _ in range(maxIters): 
                distances = find_distances(examples, centroids, precomp_dps)
                assignments = assign_points(examples, centroids, distances)
                old_centroids = copy.deepcopy(centroids)
                more_examples = copy.deepcopy(examples)
                centroids = compute_centroids(more_examples, assignments)
                if (old_centroids == centroids): 
                    print("converged before max iterations")
                    break 
                # check(_, examples, old_centroids, centroids, distances, assignments)
        loss = calculateLoss(centroids, assignments, examples)
        check(_, examples, old_centroids, centroids, distances, assignments)
        return centroids, assignments, loss
        # END_YOUR_CODE

random.seed(42)
x1 = {0:0, 1:0}
x2 = {0:0, 1:1}
x3 = {0:0, 1:2}
x4 = {0:0, 1:3}
x5 = {0:0, 1:4}
x6 = {0:0, 1:5}
examples = [x1, x2, x3, x4, x5, x6]
K = 2
maxIters = 10

centroids, assignments, loss = kmeans(examples, K, maxIters)