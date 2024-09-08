# This Trie implementation comes from user Ajay Rawat, https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python


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

    def _walk_trie(self, node, word, word_list):

        if node.children:
            for char in node.children:
                word_new = word + char
                if node.children[char].end:
                    # if node.end:
                    word_list.append(word_new)
                    # word_list.append( word)
                self._walk_trie(node.children[char], word_new, word_list)

    def auto_complete(self, partial_word):
        node = self.root

        word_list = []
        # find the node for last char of word
        for char in partial_word:
            if char in node.children:
                node = node.children[char]
            else:
                # partial_word not found return
                return word_list

        if node.end:
            word_list.append(partial_word)

        #  word_list will be created in this method for suggestions that start with partial_word
        self._walk_trie(node, partial_word, word_list)
        return word_list

    # Return the powerset of a set
