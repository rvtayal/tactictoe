import os
import pickle
import torch
import copy
import numpy as np
import matplotlib.pyplot as plt


from network import TacticToeNet, TacticToeLoss
from mcts import MCTS
from tactictoe_mcts_state import Tactictoe_State
from game import Game

network_path = './ttt_saved_network.pt'
data_path = './training/'
filename = 'game_1.pickle'

def load_network():
    net = TacticToeNet()
    if os.path.exists(network_path):
        net.load_state_dict(torch.load(network_path))
    return net

def make_games(network, num=10, time=10):
    print("############### Making Games #####################")
    data = []
    for i in range(num):
        print("game {}/{}".format(i+1, num))
        cur_game_data = []
        cur_game = Game()
        while not cur_game.isOver():
            mcts = MCTS(cur_game, Tactictoe_State, network)
            policy, move = mcts.run(time)
            policy = decode_policy(cur_game, policy)
            game_copy = copy.deepcopy(cur_game)
            cur_game_data += [(game_copy, policy)]
            cur_game.move(move)
        start = 1 if cur_game.getWinner() is 'x' else -1
        for i, datum in enumerate(cur_game_data):
            g, p = datum
            data.append((g, p, ((-1)**i) * start))

    with open(data_path + filename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def decode_policy(game, policy):
    ret = torch.zeros(81)
    valid_moves = game.getValidMoves()
    for i, move in enumerate(valid_moves):
        p = policy[i]
        ret[TacticToeNet.encode_move(move)] = p

    return ret

def encode_move(move):
    b, square = move
    dc, dr = (3 * (b%3), 3 * (b//3))
    r = square[0] + dr
    c = square[1] + dc
    ret = 9*r + c
    return ret


def load_data():
    with open(data_path + filename, 'rb') as f:
        dataset = pickle.load(f)
    return dataset


def train(net, dataset):
    optimizer = torch.optim.Adam(net.parameters(), weight_decay=1e-4)
    criterion = TacticToeLoss()
    lr_scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer,
        milestones=[x for x in range(0, 1000, 200)],
        gamma=.1)

    loss_array = []


    for game, policy, value in dataset:
        policy = torch.tensor(policy)
        value = torch.tensor(value)
        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()
        v_pred, p_pred = net(game)
        loss = criterion(v_pred, p_pred, value, policy)
        loss_array.append(loss.detach().numpy())
        loss.backward()

    return net, loss_array


if __name__ == "__main__":
    net = load_network()
    l = []
    for i in range(10):

        make_games(net, num=1, time=5)
        dataset = load_data()
        net, loss = train(net, dataset)
        l.append(loss)

    plt.plot(l)
    plt.show()
    torch.save(net.state_dict(), network_path)

