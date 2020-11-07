import random
import time
from collections import Counter
from functools import reduce
from game_agent import Nim, NimAI
from optimal import optimal_nim


def train(n):
    """
    Train an AI by playing `n` games against itself.
    """
    print("Training for {} games".format(n))
    agent = NimAI()

    # Play n games
    for i in range(n):
        #if (i+1) % 100 == 0:
            #print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last_move = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = agent.choose_action(game.piles)

            # Keep track of last state and action
            last_move[game.player]["state"] = state
            last_move[game.player]["action"] = action

            game.take_turn(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                agent.qlearning_step(state, action, new_state, -1)
                agent.qlearning_step(
                    last_move[game.player]["state"],
                    last_move[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last_move[game.player]["state"] is not None:
                agent.qlearning_step(
                    last_move[game.player]["state"],
                    last_move[game.player]["action"],
                    new_state,
                    0
                )

    #print("Done training")

    # Return the trained AI
    return agent


def play(ai, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player take their turn first or second.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()
    ai_nim = []
    human_nim = []
    rounds_played = 0
    # Game loop
    while True:
        rounds_played += 1
        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print("nim-sum =", "{0:b}".format(xor_all(game.piles)))
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human take a turn
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI take a turn
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        game.take_turn((pile, count))
        print("nim-sum =", "{0:b}".format(xor_all(game.piles)))

        if game.player == human_player:
            ai_nim.append(xor_all(game.piles) == 0)
        else:
            human_nim.append(xor_all(game.piles) == 0)


        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            print()
            print("Number of nim-sums of zero made by AI", Counter(ai_nim))
            print("Number of nim-sums of zero made by Human", Counter(human_nim))
            print("Number of rounds played", rounds_played)
            return

def play2(ai, ai2):
    player = random.randint(0, 1)
    if player == 0:
        print("AI_2 started")
    else:
        print("AI started")

    game = Nim()
    ai_nim = []
    ai2_nim = []
    ctr = 0
    while True:
        ctr += 1
        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        # Let AI_2 take a turn
        if game.player == player:
            pile, count = ai2.choose_action(game.piles, epsilon=False)
        # Have AI take a turn
        else:
            pile, count = ai.choose_action(game.piles, epsilon=False)
        prev_nim = xor_all(game.piles)

        game.take_turn((pile, count))

        if game.player == player:
            if xor_all(game.piles) == 0 and prev_nim != 0:
                ai_nim.append(True)
            if xor_all(game.piles) != 0 and prev_nim != 0:
                ai_nim.append(False)
        else:
            if xor_all(game.piles) == 0 and prev_nim != 0:
                ai2_nim.append(True)
            if xor_all(game.piles) != 0 and prev_nim != 0:
                ai2_nim.append(False)

        # Check for winner
        if game.winner is not None:
            winner = "AI_2" if game.winner == player else "AI"
            print("Number of times AI converted the nim-sum to 0 when it could:", Counter(ai_nim))
            print("Number of times AI_2 converted the nim-sum to 0 when it could:", Counter(ai2_nim))
            print("Number of rounds played", ctr)
            return winner

def play_perfect():
    game = Nim()
    player = random.randint(0, 1)
    ctr = 0
    while True:
        ctr += 1
        available_actions = Nim.available_actions(piles=game.piles)
        if game.player == player:
            pile, count = optimal_nim(game.piles, available_actions)
        else:
            pile, count = optimal_nim(game.piles, available_actions)
        game.take_turn((pile, count))
        if game.winner is not None:
            return ctr

def play3(ai):
    player = random.randint(0, 1)
    game = Nim()

    perfect_game_steps = play_perfect()

    predestined = ""
    if (player == 0 and xor_all(game.piles) != 0) or (player == 1 and xor_all(game.piles) == 0):
        predestined = "PerfectNim"
    elif (player == 1 and xor_all(game.piles) != 0) or (player == 0 and xor_all(game.piles) == 0):
        predestined = "AI"

    ai_nim = []
    perfect_nim = []
    ctr = 0
    while True:
        ctr += 1
        available_actions = Nim.available_actions(game.piles)
        if game.player == player:
            pile, count = optimal_nim(game.piles, available_actions)
        else:
            pile, count = ai.choose_action(game.piles, epsilon=False)
        prev_nim = xor_all(game.piles)
        game.take_turn((pile, count))

        if game.player == player:
            if xor_all(game.piles) == 0 and prev_nim != 0:
                ai_nim.append(True)
            elif xor_all(game.piles) != 0 and prev_nim != 0:
                ai_nim.append(False)
        else:
            if xor_all(game.piles) == 0 and prev_nim != 0:
                perfect_nim.append(True)
            elif xor_all(game.piles) != 0 and prev_nim != 0:
                perfect_nim.append(False)

        if game.winner is not None:
            winner = "PerfectNim" if game.winner == player else "AI"
            if perfect_nim:
                perfect_nim.pop()
            if ai_nim:
                ai_nim.pop()

            perfect_nim_correct_move_percent = None if not perfect_nim else perfect_nim.count(True) / len(perfect_nim)
            ai_nim_correct_move_percent = None if not ai_nim else ai_nim.count(True) / len(ai_nim)
            return winner, predestined, perfect_nim_correct_move_percent, ai_nim_correct_move_percent, ctr, perfect_game_steps

def xor_all(l):
    return reduce(lambda x, y: x^y, l)