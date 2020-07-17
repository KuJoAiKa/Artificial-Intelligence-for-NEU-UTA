from numpy import *

class Board(object):
    def __init__(self):
        self._board = [ '-' for _ in range(16)]

    def _move(self, action, take):
        if self._board[action] == '-':
            self._board[action] = take

    def _unmove(self, action):
        self._board[action] = '-'

    # get all legal actions(bottom-most)
    def get_legal_actions(self):
        actions = []
        for i in [12,8,4,0]:
            if self._board[i] == '-':
                actions.append(i)
                break
        for i in [13,9,5,1]:
            if self._board[i] == '-':
                actions.append(i)
                break
        for i in [14,10,6,2]:
            if self._board[i] == '-':
                actions.append(i)
                break
        for i in [15,11,7,3]:
            if self._board[i] == '-':
                actions.append(i)
                break
        return actions

    # Judge whether the action is legal
    def is_legal(self, action):
        temp = self._board[action::4]
        if temp[0] == '-':
            if len(temp) > 1 and '-' not in self._board[action+4::4]:
                return True
            if len(temp) == 1 :
                return True

    # terminal state check
    def terminal(self):
        board = self._board
        lines = [board[0:3], board[1:4], board[4:7], board[5:8], board[8:11], board[9:12], board[12:15], board[13:16],
                 board[0:9:4], board[4:13:4], board[1:10:4], board[5:14:4], board[2:11:4], board[6:15:4], board[3:12:4],
                 board[7:16:4], board[0:11:5], board[5:16:5], board[3:10:3], board[6:13:3], board[1::5], board[4::5],
                 board[2:9:3], board[7:14:3]]

        if ['W'] * 3 in lines or ['B'] * 3 in lines or '-' not in board:
            return True
        else:
            return False


    def get_winner(self):
        board = self._board
        lines = [board[0:3], board[1:4], board[4:7], board[5:8], board[8:11], board[9:12], board[12:15], board[13:16],
                 board[0:9:4], board[4:13:4], board[1:10:4], board[5:14:4], board[2:11:4], board[6:15:4], board[3:12:4],
                 board[7:16:4], board[0:11:5], board[5:16:5], board[3:10:3], board[6:13:3], board[1::5], board[4::5],
                 board[2:9:3], board[7:14:3]]

        if ['W'] * 3 in lines:
            return 0
        elif ['B'] * 3 in lines:
            return 1
        else:
            return 2

    # print the board
    def print_b(self):
        board = self._board
        for i in range(len(board)):
            print(board[i], end='')
            if (i + 1) % 4 == 0:
                print()


class Player(object):
    def __init__(self, take='W'):
        self.take = take

    def move(self, board, action):
        board._move(action, self.take)

class HumanPlayer(Player):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):
        while True:
            action = input('Please input a num in 1~16(bottom-most FIRST):')
            action = int(action)-1
            if action >= 0 and action <= 15 and board.is_legal(action):
                return action


class AIPlayer(Player):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):
        print('AI is thinking ...')
        take = ['W', 'B'][self.take == 'W']
        player = AIPlayer(take)  # imaginary enemy to simulate the player
        _, action = self.minimax(board, player)
        return action

    # minimax search with α-β pruning
    def minimax(self, board, player, depth=0):
        if self.take == "B":
            bestVal = -17
        else:
            bestVal = 17

        if board.terminal():
            if board.get_winner() == 0:
                return -17 + depth, None
            elif board.get_winner() == 1:
                return 17 - depth, None
            elif board.get_winner() == 2:
                return 0, None

        for action in board.get_legal_actions():  # Traverse all legal actions
            board._move(action, self.take)
            val, _ = player.minimax(board, self, depth + 1)  #switch to imaginary enemy
            board._unmove(action)  # undo the change

            if self.take == "B":  #pruning
                if val > bestVal:
                    bestVal, bestAction = val, action
            else:
                if val < bestVal:
                    bestVal, bestAction = val, action

        return bestVal, bestAction


class Game(object):
    def __init__(self):
        self.board = Board()
        self.current_player = None


    def switch_player(self, player1, player2):
        if self.current_player is None:
            return player1
        else:
            return [player1, player2][self.current_player == player1]


    def print_winner(self, winner):  # winner in [0,1,2]
        if self.ps == 'W':
            print(['You Win', 'You Lose', 'Draw'][winner])
        else:
            print(['You Lose', 'You Win', 'Draw'][winner])

    def run(self):
        self.ps = input("W-human first\nB-computer first\nchoose your colour(white first):")
        if self.ps == 'W':
            player1, player2 = HumanPlayer('W'), AIPlayer('B')  # W FIRST
        else:
            player1, player2 = AIPlayer('W'), HumanPlayer('B')

        print('\nGame start!\n')
        self.board.print_b()
        while True:
            self.current_player = self.switch_player(player1, player2)  # switch the player

            action = self.current_player.think(self.board)  # thinking

            self.current_player.move(self.board, action)  # Perform the operation to change the board

            self.board.print_b()  # print the board

            if self.board.terminal():  #Judge whether to terminate
                winner = self.board.get_winner()  # get the winner
                break

        self.print_winner(winner)
        print('Game over!')


if __name__ == '__main__':
    Game().run()