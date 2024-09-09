"""Trie implementation for simpliciality.

This is not meant to be user-facing, but rather
contains auxiliary functions for the simpliciality
methods.
"""

# This Trie implementation comes from user Ajay Rawat, https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python

__all__ = ["Trie"]


class TrieNode:
    def __init__(self):
        # Dict: Key = letter, Item = TrieNode
        self.children = {}
        self.end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def build_trie(self, words):
        for word in words:
            self.insert(word)

    def insert(self, word):
        node = self.root
        for char in sorted(word):
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end = True

    def search(self, word):
        node = self.root
        for char in sorted(word):
            if char in node.children:
                node = node.children[char]
            else:
                return False

        return node.end
