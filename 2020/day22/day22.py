#!/usr/bin/env python3
import sys, re
import argparse

global debug

realprint = print

def dprint(*args):
    if debug:
        realprint(*args)

print = dprint

def main(args):
    global debug
    #global hashed_matches
    decks = {}
    hashed_matches = {}
    with open(args.filename, 'r') as fd:
        state = "playername"
        for line in [line.strip() for line in fd.readlines()]:
            print("State: {}, line: {}".format(state, line))
            if state == "playername":
                current_player = int(re.match("Player (\d+):", line).group(1))
                state = 'deck'
                decks[current_player] = []
                continue
            if state == "deck":
                match = re.match("(\d+)", line)
                if match:
                    decks[current_player].append(int(match.group(1)))
                    continue
                else:
                    state = 'playername'
                    continue
    print(decks)
    players = list(decks.keys())
    players.sort()
    print(hash_round(decks))
    round = 1
    game_ended = False
    play_recursive_combat(decks)
    #play_combat(decks)

def play_recursive_combat(decks, game=1):
    players = list(decks.keys())
    players.sort()
    round = 1
    additional_games_played = 0
    print("=== Game {} ===".format(game))
    new_hashed_matches = {}
    while True:
        print("-- Round {} (Game {}) --".format(round, game))
        print("Player {}'s deck: {}".format(players[0], ', '.join([str(elem) for elem in decks[players[0]]])))
        print("Player {}'s deck: {}".format(players[1], ', '.join([str(elem) for elem in decks[players[1]]])))
        round_hash = hash_round(decks)
        # realprint("G:{}:H{}".format(game, round_hash))
        card_0 = decks[players[0]].pop(0)
        card_1 = decks[players[1]].pop(0)
        print("Player {} plays: {}".format(players[0], card_0))
        print("Player {} plays: {}".format(players[1], card_1))
        if round_hash in new_hashed_matches.keys():
            winner = 0
            print("Player {} wins the game by default - match has already occurred".format(players[winner]))
            break
        else:
            # add new round to hashed rounds
            new_hashed_matches[round_hash] = True
            # check if a sub-game needs to be played
            if len(decks[players[0]]) >= card_0 and len(decks[players[1]]) >= card_1:
                # need to play a sub-game
                # generate new decks
                new_decks = {players[0]: [], players[1]: []}
                for i in range(0, card_0):
                    new_decks[players[0]].append(decks[players[0]][i]) 
                for i in range(0, card_1):
                    new_decks[players[1]].append(decks[players[1]][i]) 
                additional_games_played += 1
                print("Playing a sub-game to determine winner...\n")
                played, winner = play_recursive_combat(new_decks, game=game+additional_games_played)
                print("...back to game {}".format(game))
                additional_games_played += played
                # for elem in round_hashes:
                #     new_hashed_matches[elem] = True
            else:
                if card_0 > card_1:
                    winner = 0
                elif card_0 < card_1:
                    winner = 1
                else:
                    print("ERROR: same valued card found???")
                    sys.exit(-1)
        # resolve winners per round
        if winner == 0:
            decks[players[0]] += [card_0, card_1]
        else:
            decks[players[1]] += [card_1, card_0]
        # add all hashes to new hashed matches
        # for elem in new_hashed_matches.keys():
        #      new_hashed_matches[elem] = True
        print("Player {} wins round {} of game {}!\n".format(players[winner], round, game))
        if len(decks[players[0]]) == 0 or len(decks[players[1]]) == 0:
            game_ended = True
            break
        round += 1 
    print("== Post-game results ==")
    print("Player {}'s deck: {}".format(players[0], ', '.join([str(elem) for elem in decks[players[0]]])))
    print("Player {}'s deck: {}".format(players[1], ', '.join([str(elem) for elem in decks[players[1]]])))
    score = get_score(decks, winner)
    if game == 1:
        realprint(score)
    return additional_games_played, winner

def hash_round(decks):
    players = list(decks.keys())
    players.sort()
    player0_hand = ','.join([str(elem) for elem in decks[players[0]]])
    player1_hand = ','.join([str(elem) for elem in decks[players[0]]])
    match_hash = "{}|{}".format(player0_hand,player1_hand)
    return match_hash
    
def get_score(decks, winner):
    score = 0
    players = list(decks.keys())
    players.sort()
    value = len(decks[players[winner]])
    for card in decks[players[winner]]:
        score += value*card
        value -= 1
    return score


def play_combat(decks):
    players = list(decks.keys())
    players.sort()
    round = 1 
    game_ended = False
    while not game_ended:
        print("-- Round {} --".format(round))
        print("Player {}'s deck: {}".format(players[0], ', '.join([str(elem) for elem in decks[players[0]]])))
        print("Player {}'s deck: {}".format(players[1], ', '.join([str(elem) for elem in decks[players[1]]])))
        card_0 = decks[players[0]].pop(0)
        card_1 = decks[players[1]].pop(0)
        print("Player {} plays: {}".format(players[0], card_0))
        print("Player {} plays: {}".format(players[1], card_1))
        if card_0 > card_1:
            winner = 0
            decks[players[0]] += [card_0, card_1]
        elif card_0 < card_1:
            winner = 1
            decks[players[1]] += [card_1, card_0]
        else:
            print("ERROR: same valued card found???")
            sys.exit(-1)
        print("Player {} wins the round!\n".format(players[winner]))
        if len(decks[players[0]]) == 0 or len(decks[players[1]]) == 0:
            game_ended = True
            break
        round += 1 
    print("== Post-game results ==")
    print("Player {}'s deck: {}".format(players[0], ', '.join([str(elem) for elem in decks[players[0]]])))
    print("Player {}'s deck: {}".format(players[1], ', '.join([str(elem) for elem in decks[players[1]]])))
    score = get_score(decks, winner)
    realprint(score)
        

if __name__ == '__main__':
    global debug
    debug = True
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Select an input file. Defaults to input.txt", default="input.txt", type=str)
    parser.add_argument("-d", help="Debug. Defaults to False", action='store_true')
    args = parser.parse_args()
    if not args.d:
        debug = False
    print("Debug mode on")
    realprint("This should print regardless of debug")
    main(args)
