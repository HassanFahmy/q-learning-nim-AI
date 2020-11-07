import random


class Nim():

    def __init__(self, initial=[7, 5, 3, 1]):
        """
        Initialize game board.
        Each game board has
            - `piles`: a list of how many elements remain in each pile
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) takes a state (`piles` list) as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, piles[i] + 1):
                actions.add((i, j))
        return actions


    def take_turn(self, action):
        """
        Make the `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        #update which player its turn is
        self.player = 0 if self.player == 1 else 1

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def qlearning_step(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old_q = self.get_qvalue(old_state, action)
        best_future = max([self.get_qvalue(new_state, a) for a in Nim.available_actions(list(new_state))]+[0])
        action_feature = (old_state[action[0]], action[1])
        state_feature = sorted(old_state[:])
        self.q[(tuple(state_feature), action_feature)] = old_q + self.alpha * (reward + best_future - old_q)

    def get_qvalue(self, state, action):
        action_feature = (state[action[0]], action[1])
        state_feature = sorted(state[:])
        return self.q[(tuple(state_feature), action_feature)] if (tuple(state_feature), action_feature) in self.q else 0



    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        best_action = None
        best_reward = 0
        actions = list(Nim.available_actions(list(state)))

        for action in actions:
            if best_action is None or self.get_qvalue(state, action) > best_reward:
                best_reward = self.get_qvalue(state, action)
                best_action = action

        if epsilon:
            # Distribute probability weights:
            #   (1 - epsilon) --> best_action
            #   epsilon       --> among all the other actions
            weights = [(1 - self.epsilon) if action == best_action else
                       (self.epsilon / (len(actions) - 1)) for action in actions]

            best_action = random.choices(actions, weights=weights, k=1)[0]

        return best_action
