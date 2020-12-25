import torch
from boards import LargeBoard
from game import Game

class ConvLayers(torch.nn.Module):
    def __init__(self, in_channels, out_channels=None, stride=None):
        super().__init__()
        self.in_channels = in_channels
        out_channels = 128 if out_channels is None else out_channels
        stride = 1 if stride is None else stride
        self.conv = torch.nn.Conv2d(in_channels=self.in_channels,
            out_channels=out_channels,
            stride=stride,
            kernel_size=3,
            padding=1,
            bias=True)
        self.batch_norm = torch.nn.BatchNorm2d(num_features=out_channels)

    def forward(self, state):
        state = state.view(-1, self.in_channels, 8, 8)
        return torch.nn.functional.relu(self.batch_norm(self.conv(state)))


class ResLayers(torch.nn.Module):
    def __init__(self, in_channels=None, out_channels=None, stride=None):
        super().__init__()
        in_channels = 128 if in_channels is None else in_channels
        out_channels = 128 if out_channels is None else out_channels
        stride = 1 if stride is None else stride
        self.conv1 = torch.nn.Conv2d(in_channels=in_channels,
            out_channels=out_channels,
            stride=stride,
            kernel_size=3,
            padding=1,
            bias=False)
        self.batch_norm1 = torch.nn.BatchNorm2d(num_features=out_channels)
        self.conv2 = torch.nn.Conv2d(in_channels=out_channels,
            out_channels=out_channels,
            stride=stride,
            kernel_size=3,
            padding=1,
            bias=False)
        self.batch_norm2 = torch.nn.BatchNorm2d(num_features=out_channels)

    def forward(self, x):
        out = torch.nn.functional.relu(self.batch_norm1(self.conv1(x)))
        out = self.batch_norm2(self.conv2(out)) + x
        return torch.nn.function.relu(out)


class OutLayers(torch.nn.Module):
    def __init__(self, in_channels=None):
        super.__init__()
        in_channels = 128 if in_channels is None else in_channels
        self.conv_v torch.nn.Conv2d(in_channels=in_channels,
            out_channels=1,
            kernel_size=1)
        self.batch_norm_v = torch.nn.BatchNorm2d(1)
        self.fc_v1 = torch.nn.Linear(81, 64)
        self.fc_v2 = torch.nn.Linear(64, 1)

        self.conv_p = torch.nn.Conv2d(in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=1)
        self.batch_norm_p = torch.nn.BatchNorm2d(2)
        self.fc_p = torch.nn.Linear(128, 81)

    def forward(self, x):
        v = toch.nn.functional.relu(self.batch_norm_v(self.conv_v(x)))
        v = v.view(-1, 81)
        v = torch.nn.functional.relu(self.fc_v1(v))
        v = torch.tanh(self.fc_v2(v))

        p = torch.nn.functional.relu(self.batch_norm_p(self.conv_p(x)))
        p = p.view(-1, 128)
        p = torch.nn.functional.softmax(self.fc_p(p), dim=1).flatten()

        return v, p


class TacticToeNet(torch.nn.Module):
    def __init__(self, num_res_layers=None):
        super().__init__()
        # set up layers here
        self.num_res_layers = 3 if num_res_layers is None else num_res_layers
        self.in_channels = 2

        self.conv_layers = ConvLayers(in_channels=self.in_channels)
        self.res_layers = torch.nn.Sequential(*[ResLayers() for _ in range(self.num_res_layers)])
        self.out_layers = OutLayers()

    def forward(self, board):
        x = self.conv_layers(TacticToeNet.encode_board(board))
        x = self.res_layers(x)
        v,p = self.out_layers(x)
        return v.flatten(), p


    @staticmethod
    def encode_board(game):
        # def encode_board(board: LargeBoard) -> torch.tensor:
        layers = torch.zeros((2,9,9), dtype=torch.float64)

        board, pm = game.getState()
        # print(pm)
        # layer for board
        l1 = torch.tensor(board.getArray())
        if game.turn is 'o':
            l1 *= -1

        # layer for pervious move
        l2 = torch.zeros((9,9), dtype=torch.float64)
        if pm is not None:
            b, square = pm
            dc, dr = (3 * (b%3), 3 * (b//3))
            # print(dr, dc)
            l2[square[0] + dr, square[1] + dc] = 1

        layers[0,:,:] = l1
        layers[1,:,:] = l2
        # layer for who's turn it is - not needed, always from x pov
        return layers


def main():
    g = Game()
    g.move((2, (1,1)))
    g.move((4, (0,0)))
    print(TacticToeNet.encode_board(g))


if __name__ == "__main__":
    main()
