# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Regular Expression Tree
# Francisco Rosal - 18676
# -------------------------------------------------------

import re as regex
from binarytree import Node as BinaryTreeNode

class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    @staticmethod
    def convert_to_binary_tree(parent_node, binary_tree_parent=None):
        if binary_tree_parent is None:
            binary_tree_parent = BinaryTreeNode(ord(parent_node.data))

        if parent_node.left is not None and parent_node.left.data is not None:
            binary_tree_parent.left = BinaryTreeNode(ord(parent_node.left.data))
            Node.convert_to_binary_tree(parent_node.left, binary_tree_parent.left)

        if parent_node.right is not None and parent_node.right.data is not None:
            binary_tree_parent.right = BinaryTreeNode(ord(parent_node.right.data))
            Node.convert_to_binary_tree(parent_node.right, binary_tree_parent.right)

        return binary_tree_parent


class RETree:
    def __init__(self, initial_regular_expression):
        self.current_node_head = None
        self.temp_roots = []
        self.get_nodes(initial_regular_expression, None)

    def get_tree(self):
        return Node.convert_to_binary_tree(self.current_node_head)

    def add_node(self, temp_root_index, content, left, right, use_head_for):
        if temp_root_index is None:
            self.current_node_head = Node(content, left, right) if self.current_node_head is None else (Node(content, self.current_node_head, right) if use_head_for == 'l' else Node(content, left, self.current_node_head))
        else:
            if temp_root_index == len(self.temp_roots):
                self.temp_roots.append(Node(content, left, right))
            elif temp_root_index < len(self.temp_roots):
                self.temp_roots[temp_root_index] = Node(content, left, right) if self.temp_roots[temp_root_index] is None else (Node(content, self.temp_roots[temp_root_index], right) if use_head_for == 'l' else Node(content, left, self.temp_roots[temp_root_index]))

    @staticmethod
    def get_final_of_expression(partial_expression):
        i = 0
        while i < len(partial_expression):
            if partial_expression[i] == '«':
                parentheses_counter = 1
                for j in range(i+1, len(partial_expression)):
                    if partial_expression[j] in ['«', '»']: parentheses_counter = parentheses_counter + 1 if partial_expression[j] == '«' else parentheses_counter - 1

                    if parentheses_counter == 0 and partial_expression[j] == '»':
                        extra = 2 if j + 1 < len(partial_expression) and partial_expression[j+1] in ['±', '+', '?'] else 0
                        fin = j + extra
                        return fin

            elif regex.match(r'[a-zA-Z±"\'/*=.|()[\]{}<> ]', partial_expression[i]):
                fin = i
                for j in range(i + 1, len(partial_expression)):
                    if not regex.match(r'[a-zA-Z±"\'/*=.|()[\]{}<> ]', partial_expression[j]): break
                    fin = j
                return fin
            i += 1


    def get_nodes(self, partial_expression, temp_root_index):
        # print('Partial expression:', temp_root_index, partial_expression)

        i = 0
        while i < len(partial_expression):
            if partial_expression[i] == '«':
                if i == 0:
                    parentheses_counter = 1
                    for j in range(i+1, len(partial_expression)):
                        if partial_expression[j] in ['«', '»']: parentheses_counter = parentheses_counter + 1 if partial_expression[j] == '«' else parentheses_counter - 1

                        if parentheses_counter == 0:
                            extra = 2 if partial_expression[j] == '»' and j + 1 < len(partial_expression) and partial_expression[j+1] in ['±', '+', '?'] else 0
                            fin = j + extra
                            self.get_nodes(partial_expression[i+1:fin], temp_root_index)
                            i = j
                            break
                else:
                    if partial_expression[i-1] in ['»', '±', '+', '?'] or regex.match(r'[a-zA-Z"\'/*=.|()[\]{}<> ]', partial_expression[i-1]):
                        fin_sub_re = self.get_final_of_expression(partial_expression[i:])
                        fin = i + 1 + fin_sub_re
                        self.get_nodes(partial_expression[i:fin], len(self.temp_roots))

                        sub_tree_root = self.temp_roots.pop() if temp_root_index is None else self.temp_roots.pop(temp_root_index + 1)
                        if sub_tree_root is not None: self.add_node(temp_root_index, '.', None, sub_tree_root, 'l')
                        i = i + fin + 1

            elif regex.match(r'[a-zA-Z#"\'/*=.|()[\]{}<> ]', partial_expression[i]):
                if ((temp_root_index is None and self.current_node_head is None) or i == 0) and i + 1 < len(partial_expression) and regex.match(r'[a-zA-Z#"\'/*=.|()[\]{}<> ]', partial_expression[i+1]):
                    if i + 2 < len(partial_expression) and partial_expression[i+2] in ['±', '+', '?']:
                        self.add_node(temp_root_index, '.', Node(partial_expression[i]), Node(partial_expression[i+2], Node(partial_expression[i+1]), None), 'l')
                        i += 2
                    else:
                        self.add_node(temp_root_index, '.', Node(partial_expression[i]), Node(partial_expression[i+1]), 'l')
                        i += 1
                elif (temp_root_index is None and self.current_node_head is not None) or i != 0:
                    self.add_node(temp_root_index, '.', None, Node(partial_expression[i]), 'l')
                else:
                    self.add_node(temp_root_index, partial_expression[i], None, None, 'l')

                if i + 1 < len(partial_expression):
                    if partial_expression[i+1] in ['±', '+', '?']:
                        self.add_node(temp_root_index, partial_expression[i+1], Node(partial_expression[i]), None, 'l')
                    elif partial_expression[i+1] == '»':
                        if i + 2 < len(partial_expression) and partial_expression[i+2] in ['±', '+', '?']:
                            self.add_node(temp_root_index, partial_expression[i+2], Node(partial_expression[i]), None, 'l')

            elif partial_expression[i] in ['¦']:
                fin_sub_re = self.get_final_of_expression(partial_expression[i+1:])
                fin = i + 1 + fin_sub_re + 1
                self.get_nodes(partial_expression[i+1:fin], len(self.temp_roots))

                sub_tree_root = self.temp_roots.pop() if temp_root_index is None else self.temp_roots.pop(temp_root_index + 1)
                if sub_tree_root is not None: self.add_node(temp_root_index, partial_expression[i], Node(partial_expression[i-1]), sub_tree_root, 'l')

                if fin < len(partial_expression) and partial_expression[fin] == '»':
                    if fin + 1 < len(partial_expression) and partial_expression[fin+1] in ['±', '+', '?']:
                        self.add_node(temp_root_index, partial_expression[fin+1], Node(partial_expression[fin+1]), None, 'l')

                i = i + fin + 1
            else:
                pass
                # print('-', partial_expression[i])
            i += 1
