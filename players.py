from __future__ import annotations
from abc import abstractmethod
import numpy as np
from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from heuristics import Heuristic
    from board import Board
    #from treeStructure import TreeStructure


class Node:
    """Class defining a node
    """

    def __init__(self, board: Board, player_id: int, depth: int = 0) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            board: (fill in later)
        """
        self.player_id = player_id
        self.board = board
        self.depth = depth

        self.children: List[Node] = []  # create an empty list for the children where each item is a Node object
        self.parent: Optional[Node] = None #not sure about optional
        self.value: Optional[float] = None #not sure about optional


    def add_child(self, child: Node):
        child.parent = self                      #the parents and the root are missing
        self.children.append(child)             #add the child to the children list
        #print("list", self.children)

class PlayerController:
    """Abstract class defining a player
    """
    def __init__(self, player_id: int, game_n: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            heuristic (Heuristic): heuristic used by the player
        """
        self.player_id = player_id
        self.game_n = game_n
        self.heuristic = heuristic


    def get_eval_count(self) -> int:
        """
        Returns:
            int: The amount of times the heuristic was used to evaluate a board state
        """
        return self.heuristic.eval_count
    

    def __str__(self) -> str:
        """
        Returns:
            str: representation for representing the player on the board
        """
        if self.player_id == 1:
            return 'X'
        return 'O'
        

    @abstractmethod
    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        pass


class MinMaxPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm
    Inherits from Playercontroller
    """
    def __init__(self, player_id: int, game_n: int, depth: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.depth: int = depth


    def min_max(self, node: Node, depth: int, max_player: bool):
        print("min_max method is reached")

        if self.player_id == 2:
            max_player = True
        else:
            max_player = False

        max_move = 0

        if max_player == True:
            max_eval = -np.inf
            for col in range(node.board.width):
                if node.board.is_valid(col):
                    new_board = node.board.get_new_board(col, self.player_id) #get a new board
                    child = Node(new_board, node.depth + 1)  # going one depth deeper, the new child
                    #evaluated_value: int = self.heuristic.evaluate_board(self.player_id, new_board)
                    child_value = self.min_max(child, depth - 1, False)
        else:
            min_eval = np.inf
            for col in range(node.board.width):
                if node.board.is_valid(col):
                    new_board = node.board.get_new_board(col, self.player_id) #get a new board
                    child = Node(new_board, node.depth + 1)  # going one depth deeper, the new child
                    #evaluated_value: int = self.heuristic.evaluate_board(self.player_id, new_board)

                    child_value = self.min_max(child, depth - 1, True)




        return max_move



    def make_move(self, board: Board) -> int:

        place_holder_move = 2   #just a placeholder

        root_node = Node(board, 0) #depth is 0, get the root node (first node)

        trying_out_move = self.min_max(root_node, self.depth, True)

        print("trying out move is", trying_out_move)
        print("The best move is", trying_out_move)

        return trying_out_move




class AlphaBetaPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm with alpha-beta pruning
    Inherits from Playercontroller
    """
    def __init__(self, player_id: int, game_n: int, depth: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.depth: int = depth


    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """

        # TODO: implement minmax algorithm with alpha beta pruning!
        return 0

class HumanPlayer(PlayerController):
    """Class for the human player
    Inherits from Playercontroller
    """
    def __init__(self, player_id: int, game_n: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)

    
    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        print(board)

        if self.heuristic is not None:
            print(f'Heuristic {self.heuristic} calculated the best move for human is:', end=' ')
            print(self.heuristic.get_best_action(self.player_id, board) + 1, end='\n\n')


        col: int = self.ask_input(board)

        print(f'Selected column: {col}')
        return col - 1


    

    def ask_input(self, board: Board) -> int:
        """Gets the input from the user

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        try:
            col: int = int(input(f'Player {self}\nWhich column would you like to play in?\n'))
            assert 0 < col <= board.width
            assert board.is_valid(col - 1)
            return col
        except ValueError: # If the input can't be converted to an integer
            print('Please enter a number that corresponds to a column.', end='\n\n')
            return self.ask_input(board)
        except AssertionError: # If the input matches a full or non-existing column
            print('Please enter a valid column.\nThis column is either full or doesn\'t exist!', end='\n\n')
            return self.ask_input(board)

