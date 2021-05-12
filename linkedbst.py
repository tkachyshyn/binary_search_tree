"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import time as t
import random


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            s(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        # height = self.height()
        # size = self._size
        return self.height() < 2 * log(self._size + 1, 2) - 1

    def inorder(self):
        if not self.isEmpty():
            lst = []
            for item in self.subtree_inorder(self._root):
                lst.append(item)
        return lst
    
    def subtree_inorder(self, p):
        if p.left is not None:
            # for other in self.subtree_inorder(p.left):
            lst = [other for other in self.subtree_inorder(p.left)]
            # return lst
                # yield other
        lst = [p]
        # yield p
        if p.right is not None:
            # for other in self.subtree_inorder(p.right):
            #     yield other
            lst = [other for other in self.subtree_inorder(p.right)]
            # return lst
        return lst


    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = self.inorder()
        print(lst)
        result = [item for item in lst if lst.index(item) >= lst.index(low) and lst.index(item) <= lst.index(high)]
        result.sort()
        return result

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        result_lst = []
        def make_lst(lst):
            middle = len(lst) // 2
            result_lst.append(lst[middle])

            if len(lst[:middle]) // 2 != 0:
                return make_lst(lst[:middle]), make_lst(lst[middle + 1:])

        lst = [item for item in self]
        lst.sort()
        make_lst(lst)

        for lmnt in lst:
            if lmnt not in result_lst:
                result_lst.append(lmnt)

        self.clear()
        for item in result_lst:
            self.add(item)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = [el for el in self]
        if item not in lst:
            lst.append(item)
        lst.sort()
        if lst.index(item) == len(lst) - 1:
            return None
        return lst[lst.index(item) + 1]

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = [el for el in self]
        if item not in lst:
            lst.append(item)
        lst.sort()
        if lst.index(item) == 0:
            return None
        return lst[lst.index(item) - 1]
        
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        path = open(path)
        lst = [line[:-1] for line in path]
        word_list = []
        for _ in range(10000):
            word = random.choice(lst)
            word_list.append(word)

        # find word in list
        cur_time = t.time()
        for word in word_list:
            lst.index(word)
        print(t.time() - cur_time)

        # find word in binary tree from sorted list
        tree = LinkedBST()
        for _ in range(900):
            tree.add(random.choice(word_list))
        cur_time  = t.time()
        for word in lst:
            tree.find(word)
        print(t.time() - cur_time)

        # find word from tree created randomly
        new_tree =  LinkedBST()
        for _ in range(900):
            tree.add(random.choice(word_list))
        cur_time = t.time()
        for word in lst:
            tree.find(word)
        print(t.time() - cur_time)

        # find word from balanced tree
        tree.rebalance()
        time = t.time()
        for word in lst:
            tree.find(word)
        print(t.time() - cur_time)
        path.close()

if __name__ == "__main__":
    bst = LinkedBST()
    for el in [1, 3, 7, 2, 8, 9]:
        bst.add(el)
    print(bst.height())
    print(bst)
    bst.rebalance()
    # bst.rebalance_yana()
    # print(bst)
    # for item in bst:
    #     print(item)
    # print(bst.find(-1))
    # print(bst.range_find())
    # print(bst.is_balanced())
    # print(bst.successor(5))
    # print(bst.height())
    # print(bst.range_find(1, 7))
    path = "words.txt"
    print(t.time())
    print(bst.demo_bst(path))