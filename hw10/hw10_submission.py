from hashlib import new
from sympy import N
import util, math, random
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem 1a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: list of integers (face values for each card included in the deck)
        multiplicity: single integer representing the number of cards with each face value
        threshold: maximum number of points (i.e. sum of card values in hand) before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look closely at this function to see an example of state representation for our Blackjack game.
    # Each state is a tuple with 3 elements:
    #   -- The first element of the tuple is the sum of the cards in the player's hand.
    #   -- If the player's last action was to peek, the second element is the index
    #      (not the face value) of the next card that will be drawn; otherwise, the
    #      second element is None.
    #   -- The third element is a tuple giving counts for each of the cards remaining
    #      in the deck, or None if the deck is empty or the game is over (e.g. when
    #      the user quits or goes bust).
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be placed into the succAndProbReward function below.
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Given a |state| and |action|, return a list of (newState, prob, reward) tuples
    # corresponding to the states reachable from |state| when taking |action|.
    # A few reminders:
    # * Indicate a terminal state (after quitting, busting, or running out of cards)
    #   by setting the deck to None.
    # * If |state| is an end state, you should return an empty list [].
    # * When the probability is 0 for a transition to a particular new state,
    #   don't include that state in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 37 lines of code, but don't worry if you deviate from this)
        # ( (totalCardValueinHand, nextCardIndexifPeeked, deckCardCounts), prob, reward )

        def bust(card_val, hand_val, threshold):
            return card_val + hand_val > threshold
        import copy

        hand_value, peek_next_index, card_counts = state[0], state[1], state[2]
        if not card_counts: return [] # are we at a terminal state
        
        if action == 'Quit': return [( (hand_value, None, None), 1, hand_value )]
        elif action == 'Take':  
            stateProbReward = []
            if peek_next_index is None: # normal take action, show all possible next states
                if sum(list(card_counts)) == 1: empty = True
                else: empty = False
                for index, count in enumerate(card_counts):
                    if not count: continue
                    card_val = self.cardValues[index]
                    if bust(card_val, hand_value, self.threshold): succState = ((card_val + hand_value), None, None)
                    else:
                        if empty: succState = (card_val+hand_value, None, None)
                        else:
                            card_count_list = list(copy.copy(card_counts))
                            card_count_list[index] -= 1
                            succState = (card_val+hand_value, None, tuple(card_count_list))
                    probability = count / sum(card_counts)
                    if empty: reward = hand_value + card_val
                    else: reward = 0
                    stateProbReward.append( (succState, probability, reward)  )
            elif peek_next_index is not None: # we must take the card at peek_next_index
                if sum(list(card_counts)) == 1: empty = True
                else: empty = False
                card_val = self.cardValues[peek_next_index]
                if bust(card_val, hand_value, self.threshold): succState = ((card_val + hand_value), None, None)
                else:
                    if empty: succState = (card_val+hand_value, None, None)
                    else:
                        card_count_list = list(copy.copy(card_counts))
                        card_count_list[peek_next_index] -= 1
                        succState = (card_val+hand_value, None, tuple(card_count_list))
                probability = 1
                if empty: reward = hand_value + card_val
                else: reward = 0
                stateProbReward.append( (succState, probability, reward)  )
            else: assert 0, "Error Code: Benjamin"
        elif action == 'Peek':
            if peek_next_index is not None: return []
            stateProbReward = []
            for index, count in enumerate(card_counts):
                if not count: continue
                succState = (hand_value, index, card_counts)
                probability = count / sum(card_counts)
                reward = -1*self.peekCost
                stateProbReward.append( (succState, probability, reward) )
        else: assert 0, "Error Code: Sarah"

        return stateProbReward
        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 1b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action at least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    # change ONLY cardValues and multiplicity
    return BlackjackMDP(cardValues=[1, 3, 17], multiplicity=20, threshold=20, peekCost=1)
    # END_YOUR_CODE

############################################################
# Problem 2a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a dict of {feature name => feature value}.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f,v in self.featureExtractor(state, action).items():
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
        def attendance(cardCounts):
            ''''Normalize card counts to 1 or 0'''
            present = []
            for count in cardCounts:
                if not count: present.append(0)
                else: present.append(1)
            return present

        eta = self.getStepSize()
        q_opt= self.getQ(state, action)
        if newState is not None: v_opt = max([self.getQ(newState, newAction) for newAction in self.actions(newState)])
        else: v_opt = 0
        c = eta * (q_opt - reward - self.discount * v_opt)
        feature_dict = self.featureExtractor(state, action)

        try:
            featureKey = (state, action)
            featureValue = feature_dict[featureKey]
            newQ = q_opt - c * featureValue 
            self.weights[featureKey] = newQ
        except:
            try:
                featureKey = (state[0], action)
                featureValue = feature_dict[featureKey]
                newQ = q_opt - c * featureValue 
                self.weights[featureKey] = newQ
            except:
                try:
                    present = attendance(state[2])
                    featureKey = (tuple(present), action)
                    featureValue = feature_dict[featureKey]
                    newQ = q_opt - c * featureValue 
                    self.weights[featureKey] = newQ
                except:
                    # i'm not entirely sure how to handle the value ones
                    assert 0, "Error Code: Jean Luc"


        # END_YOUR_CODE

# Return a single-element dict containing a binary (indicator) feature
# for the existence of the (state, action) pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return {featureKey: featureValue}

############################################################
# Problem 2b: convergence of Q-learning
# Small test case
smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# Large test case
largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)

def simulate_QL_over_MDP(mdp, featureExtractor):
    '''NOTE: adding more code to this function is totally optional, but it will probably be useful
    to you as you work to answer question 2b (a written question on this assignment).  We suggest
    that you add a few lines of code here to run value iteration, simulate Q-learning on the MDP,
    and then print some stats comparing the policies learned by these two approaches.'''
    # BEGIN_YOUR_CODE (our solution is 9 lines of code, but don't worry if you deviate from this)
    value_iteration = ValueIteration() 
    value_iteration.solve(mdp)
    # statesToValues = value_iteration.V
    statesToActions = value_iteration.pi

    rl = QLearningAlgorithm(mdp.actions, mdp.discount(), featureExtractor)
    util.simulate(mdp, rl, numTrials=30000)
    rl.explorationProb = 0

    # but how do the policies compare? 
    print("for how many states does value iteration produce a different action than q-learning?")
    different = 0
    possible = len(mdp.states)
    for state in mdp.states:
        vi_action = statesToActions[state]
        q_action = rl.getAction(state)
        if (vi_action is not q_action): different += 1
    print(" - value iteration produced a different state", different, "times on", possible, "chances\n")
    # END_YOUR_CODE

############################################################
# Problem 2c: features for Q-learning.

# You should return a dict of {feature key => feature value}.
# (See identityFeatureExtractor() above for a simple example.)
# Include the following features in the dict you return:
# -- Indicator for the action and the current total (1 feature).
# -- Indicator for the action and the presence/absence of each face value in the deck. (1 feature)
#       Example: if the deck is (3, 4, 0, 2), then your indicator on the presence of each card is (1, 1, 0, 1)
#       Note: only add this feature if the deck is not None.
# -- For each face value, add an indicator for the action and the number of cards remaining with that face value (len(counts) features)
#       Note: only add these features if the deck is not None.
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state
    # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
    featureDict = {}
    # featureDict[((total, nextCard, counts)), action] = 1
    featureDict[(total, action)] = 1
    if counts is not None:
        present = []
        for value in counts: # but what if total is equal to value?
            featureDict[(value, action)] = 1
            if value: present.append(1)
            elif not value: present.append(0)
            else: assert 0, "Error Code: Autumn"
        featureDict[(tuple(present), action)] = 1
    # if counts is not None: 
    #     assert len(featureDict.keys()) == (2 + len(counts)), "Error Code: Jeremy"
    # else: assert len(featureDict.keys()) == 1, "Error Code: Melissa"
    return featureDict
    # END_YOUR_CODE

############################################################
# Problem 2d: What happens when the MDP changes underneath you?!
#    -- Spring 2022 semester: this problem is provided for your entertainment and enrichment.  Do not turn anything in.

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)

def compare_changed_MDP(original_mdp, modified_mdp, featureExtractor):
    # NOTE: as in 2b above, adding more code to this function is completely optional, but we've added
    # this partial function here to help you figure out the answer to 2d (a written question).
    # Consider adding some code here to simulate two different policies over the modified MDP
    # and compare the rewards generated by each.
    # BEGIN_YOUR_CODE (our solution is 11 lines of code, but don't worry if you deviate from this)
    pass
    # END_YOUR_CODE

