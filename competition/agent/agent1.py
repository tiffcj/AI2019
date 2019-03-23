import pprint
import random
from random import randint

"""
Make sure your HP doesn't go below 0: possible with a move by you?-
Make sure that you have enough mana?
Make sure that you don't have too much mana?
What does mana reset mean?
Minions have to wait a turn after being summoned before attacking: can't attack = true

- Is there a f'n to simulate state?
- Is there a time limit?
- Can you play a card that requires more mana than you have?
- What does mana reset mean?

Make sure that card not empty
"""



# Modify this function
def start():
    print('start')
    return None


# Modify this function
def play(state):
    print("-----")
    # pprint.pprint(state)
    legal = get_legal_moves(state)
    print(legal)
    # # print(len(legal))
    #
    test = random.choice(legal)
    print(test)
    return test[0], test[1]
    # # return 'a', (None,)

    # test = get_best_move(state)
    # print(test)

    # return test


# Modify this function
def end(victory):
    print(f'Victor: {victory}')
    return None


def get_best_move_for_ids(state, legal_moves, move_id):
    dict = {}
    for i in range(1, 4):
        moves_with_id = []
        for move in legal_moves:
            if move[0] == i:
                moves_with_id.append(move)
        dict['i'] = get_best_move(state, moves_with_id)

    return dict


def get_best_move(state, moves):
    # moves = get_legal_moves(state)
    max_ratio = 0  # Heuristic
    best_move = (4, None)
    for move in moves:
        if move[0] == 0:
            ratio = 1
            if ratio > max_ratio:
                max_ratio = ratio
                best_move = move
        elif move[0] == 1:
            ratio = state['player_hand'][move[1]]['atk']/state['player_hand'][move[1]]['cost']
            if ratio >= max_ratio:
                max_ratio = ratio
                best_move = move
        elif move[0] == 2:
            ratio = state['player_hand'][move[1][0]]['zone_position']/state['player_hand'][move[1][0]]['cost']
            if ratio > max_ratio:
                max_ratio = ratio
                best_move = move
        elif move[0] == 3:
            ratio = state['player_target'][move[1][0]]['atk']/state['player_target'][move[1][0]]['cost']
            if ratio >= max_ratio:
                max_ratio = ratio
                best_move = move

    return {'ratio': max_ratio, 'move': best_move}
    # return best_move


def get_legal_moves(state):
    moves = []

    if state['player_mana'] >= 2:
        moves.append((0, None))

    if len(state['player_hand']) > 1:
        for i in range(len(state['player_hand'])):
            curr_card = state['player_hand'][i]
            if curr_card['cost'] <= state['player_mana']:
                if curr_card['type'] == 'minion' and get_nb_minions(state) < 7:
                    moves.append((1, i))
                else:
                    if curr_card['id'] == 2 or curr_card['id'] == 13:
                        moves.append((2, (i, 0)))
                    else:
                        for j in range(len(state['opponent_target'])):
                            moves.append((2, (i, j)))

    for i in range(len(state['player_target'])):
        curr_target = state['player_target'][i]
        if curr_target['type'] == 'minion' and curr_target['turns_in_play'] > 0:
            for j in range(len(state['opponent_target'])):
                moves.append((3, (i, j)))

    moves.append((4, None))

    return moves


def get_nb_minions(state):
    nb_minions = 0

    for i in range(len(state['player_target'])):
        if state['player_target'][i]['type'] == 'minion':
            nb_minions += 1

    return nb_minions


# Don't touch this function
def communicate(pipe, *args, **kwargs):
    while True:
        packet = pipe.recv()
        action = packet['action']
        if action == 'start':
            pipe.send(start())
        elif action == 'play':
            pipe.send(play(packet['args']))
        elif action == 'end':
            pipe.send(end([packet['args']]))


class CommunicateDebug:
    def __init__(self, *args):
        self.out = None

    def send(self, packet):
        action = packet['action']
        if action == 'start':
            start()
        elif action == 'play':
            self.out = play(packet['args'])
        elif action == 'end':
            end([packet['args']])

    def recv(self):
        return self.out

