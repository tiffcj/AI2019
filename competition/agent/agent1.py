# Modify this function
def start():
    print('start')
    return None


# Modify this function
def end(victory):
    print(f'Victor: {victory}')
    return None


# def futureUse1410(board):
#     for x in board:
#         if x['type'] is "minion" and (x['id'] == 10 or x['id'] ==14):
#             return True
#     return False
#
#
# def hasStrongNew(oppBoard, mana):
#     ret = {'bool': False}
#     maxAtt = 0
#     for x in range(1,len(oppBoard)):
#         if oppBoard[x]['atk']>5 and oppBoard[x]['atk']>maxAtt and oppBoard[x]['mana']+3>=mana:
#             maxAtt=oppBoard[x]['atk']
#             ret = {'bool': True, 'index': x}
#     return ret
#
#
# def get_best_move_for_ids(state, legal_moves, move_id):
#     moves_with_id = []
#     for move in legal_moves:
#         if move[0] == move_id:
#             moves_with_id.append(move)
#
#     return get_best_move(state, moves_with_id)


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

    # return {'value': max_ratio, 'move': best_move}
    return best_move


def get_nb_minions(state):
    nb_minions = 0

    for i in range(len(state['player_target'])):
        if state['player_target'][i]['type'] == 'minion':
            nb_minions += 1

    return nb_minions


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


def play(state):
    legal_moves = get_legal_moves(state)
    return get_best_move(state, legal_moves)


# def play(state):
#     target = 0
#
#     legal_moves = get_legal_moves(state)
#
#     if futureUse1410(state['player_target']):
#         return get_best_move_for_ids(state, legal_moves, 3)['move']
#
#     if (hasStrongNew(state['opponent_target'], state['opponent_mana'])['bool']):
#         target = hasStrongNew['index']
#
#     if (len(state['player_hand']) < 2):
#         if (state['player_mana'] < 2):
#             move = get_best_move_for_ids(state, legal_moves, 3)['move']
#             move[1][1] = target
#             return move
#         else:
#             bests = get_best_move_for_ids(state, legal_moves, 2)
#             bests['move'][1][1] = target
#
#             bestm = get_best_move_for_ids(state, legal_moves, 3)
#             bestm['move'][1][1] = target
#
#             if (bests['value'] < 1 and bestm['value'] < 0):
#                 return 0, None
#             else:
#                 if (bests['value'] > bestm['value']):
#                     return bests['move']
#                 else:
#                     return bestm['move']
#     elif len(state['player_target']) < 2 or len(state['player_hand']) > 8:
#         best = get_best_move_for_ids(state, legal_moves, 1)
#         if best['value'] < 0:
#             best = get_best_move_for_ids(state, legal_moves, 3)
#             best['move'][1][1] = target
#             if best['value'] < 0:
#                 best = get_best_move_for_ids(state, legal_moves, 2)
#                 best['move'][1][1] = target
#         return best['move']
#     else:
#         bests = get_best_move_for_ids(state, legal_moves, 2)
#         bests['move'][1][1] = target
#
#         bestm = get_best_move_for_ids(state, legal_moves, 3)
#         bestm['move'][1][1] = target
#
#         bestd = get_best_move_for_ids(state, legal_moves, 1)
#         if bests['value'] < 1 and bestm['value'] < 0 and bestd['value'] < 0:
#             return 0, None
#         else:
#             if bests['value'] > bestm['value'] and bests['value'] > bestd['value']:
#                 return bests['move']
#             elif bestd['value'] > bestm['value'] and bestd['value'] > bests['value']:
#                 return bestd['move']
#             else:
#                 return bestm['move']


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

