from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from heuristics import Heuristic
    from board import Board


class Node:
    """Class defining a node
    """

    def __init__(self, player_id: int, board: Board, depth: int = 0) -> None:
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
        self.parent: Node = None                      #the parents and the root are missing
        self.children.append(child)             #add the child to the children list
        #print("list", self.children)

class TreeStructure:
    """Class defining the tree
    """
    def __init__(self, player_id: int, board: Board, heuristic: Heuristic, depth: int = 0) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            board: (fill in later)
        """
        self.player_id = player_id
        self.board = board
        self.heuristic = heuristic
        self.depth = depth
        self.root_node = Node(player_id, board, 0)

        #print("depth:", self.depth)
        #print("root_node:", self.root_node)
        #print("player_id", self.player_id)


    def create_tree(self, node: Node, depth: int):
        #print("the create_tree method is called")

        max_value: float = -np.inf  # negative infinity
        min_value: float = np.inf  # positive infinity
        max_move: int = 0
        min_move: int = 0

        current_player = node.player_id

        if node.depth == depth:     #stop the recursion once the depth is reached
            print("depth", depth, "is reached")
        else:
            for col in range(node.board.width):
                if node.board.is_valid(col):
                    new_board: Board = node.board.get_new_board(col, current_player)

                    if current_player == 2: #one player plays then the other plays and so on
                        next_player = 1
                    else:
                        next_player = 2

                    child = Node(player_id=next_player, board=new_board, depth=node.depth+1)   #creating a child
                    node.add_child(child)                                     #adding the child to the children list


                    value: int = self.heuristic.evaluate_board(self.player_id, new_board)

                    if self.player_id == 1:
                        #print("human player")
                        if value < min_value:
                            min_move = value
                            #print("min_move is:", min_move)

                    elif self.player_id == 2:
                        #print("computer player")
                        if value > max_value:
                            max_move = value
                            #print("max_move is:", max_move)

                    #print("value is", value)


                    #print(new_board)

                    self.create_tree(child, depth)              #recursion is happening

        return min_move, max_move