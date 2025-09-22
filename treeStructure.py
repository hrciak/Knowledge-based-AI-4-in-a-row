from __future__ import annotations
from abc import abstractmethod
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from heuristics import Heuristic
    from board import Board


class Node:
    """Class defining a node
    """

    def __init__(self, player_id: int, board: Board) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            board: (fill in later)
        """
        self.player_id = player_id
        self.board = board

    def add_child(self, child: Node):           #the parents and the root are missing
        self.children = []                      #create an empty list for the children
        self.children.append(child)             #add the child to the children list

class TreeStructure:
    """Class defining the tree
    """

    def __init__(self, player_id: int, board: Board) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            board: (fill in later)
        """
        self.player_id = player_id
        self.board = board
        self.root_node = Node(self.player_id, self.board)


    def build_tree(self, depth: int):

        self.create_tree(self.root_node, depth)
        print("calling the build_tree method")


    def create_tree(self, node: Node, depth: int):

        for col in range(node.board.width):

            if node.board.is_valid(col):
                new_board: Board = node.board.get_new_board(col, self.player_id)
                child = Node(player_id=self.player_id, board=new_board)   #creating a child
                node.add_child(child)                                     #adding the child to the children list

                self.create_tree(child, depth)

        #print("calling the grow_tree method")