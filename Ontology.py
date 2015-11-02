__author__ = 'nitinpasumarthy'

from collections import deque


class TrieNode:
    def __init__(self):
        self.count = 0
        self.children = {}  # a-zA-Z ?


class Trie:
    def __init__(self):
        self.head = TrieNode()

    def insert(self, sentence):
        current = self.head
        for c in sentence:
            current = self.upsert(current, c, 1)

    def upsert(self, d, key, value):
        """
        Creates a new child node if not present for d or updates the value of the child if present
        :param d: node whose child has to created or updated
        :param key: name of the child to update or create
        :param value: value of the child to increment if present or set if not present
        :return: the child node either created or updated
        """
        if key in d.children:
            d.children[key].count += value
        else:
            d.children[key] = TrieNode()
            d.children[key].count = value
        return d.children[key]

    def query(self, q):
        current = self.head
        try:
            for c in q:
                current = current.children[c]
            return current.count
        except KeyError:
            return 0


class TreeNode:
    def __init__(self):
        self.trie = Trie()
        self.children = []


class Tree:
    def __init__(self):
        self.treemap = {}  # "Reptiles": treeNodeInstance, ...

    def add_node(self, parent, children):
        """
        Adds 'child' as a child to 'parent' node
        :param parent: parent node string name
        :param children: child nodes as an array of strings
        :return: None
        """
        if parent not in self.treemap:
            self.treemap[parent] = TreeNode()
        self.treemap[parent].children += children

    def insert_sentence(self, nodename, sentence):
        """
        Adds this sentence to the given node
        Assumes this node is added using add_node()
        :param nodename: name of the node to which this sentence has to be added as string
        :param sentence: sentence to save
        :return: None
        """
        self.treemap[nodename].trie.insert(sentence)

    def query(self, nodename, q):
        """
        Returns the number of times this sentence appeared under this node
        :param nodename: name of the node to search this sentence as a string
        :param q: sentence to search
        :return: number of the times this sentence is found as an integer
        """
        return self.treemap[nodename].trie.query(q)


class Ontology:
    def __init__(self):
        self.t = Tree()
        pass

    def parse_flat_tree(self, flat_tree):
        """
        Parses a flat tree to a Tree instance
        :param flat_tree: tree structure as a string
        :return: instance of Tree
        """
        import copy
        s = copy.copy(flat_tree)
        words = deque(s.split(" "))
        root = words.popleft()
        if words.popleft() == '(':  # if the root has children
            self.parse_flat_tree_helper(self.t, root, words)
        return self.t

    def save_query(self, query):
        node, sentence = query.split(":")
        self.t.insert_sentence(node.strip(), sentence.strip())

    def find_queries(self, matching_to):
        """
        Finds the count of matching queries to matching_to query passed
        :param matching_to: query to match with
        :return: count of matched queries
        """
        node, sep, query = matching_to.partition(" ")
        return self.t.query(node, query)

    def parse_flat_tree_helper(self, t, parent, words):
        current_word = words.popleft()
        children = []
        while len(words) > 0:
            children.append(current_word)
            t.add_node(current_word, [])  # add this parent node with zero children by default
            previous_word = current_word
            current_word = words.popleft()
            if current_word == "(":
                self.parse_flat_tree_helper(t, previous_word, words)
                current_word = words.popleft()
            elif current_word == ")":
                if len(children) > 0:
                    t.add_node(parent, children)  # add the children to parent node created before
                break  # reading the children of this parent is done


def main():
    t = Tree()
    t.add_node("Fruit", ["Apple"])
    t.add_node("Fruit", ["Banana"])
    t.add_node("Banana", [])
    t.insert_sentence("Fruit", "Apple")
    t.insert_sentence("Fruit", "Apple")
    t.insert_sentence("Fruit", "Ape")
    t.insert_sentence("Fruit", "A")
    t.insert_sentence("Fruit", "App")
    t.insert_sentence("Fruit", "Appl")
    t.insert_sentence("Banana", "Apple")
    res = t.query("Fruit", "A")
    res = t.query("Fruit", "Ap")
    res = t.query("Fruit", "App")
    res = t.query("Fruit", "Appl")
    res = t.query("Fruit", "Apple")
    res = t.query("Banana", "Apple")

    o = Ontology()
    o.parse_flat_tree("Animals ( Reptiles Birds ( Eagles Pigeons Crows ) Mammals ( Elephant Man ) )")

    o.save_query("Reptiles: Why are many reptiles green?")
    o.save_query("Birds: How do birds fly?")
    o.save_query("Eagles: How endangered are eagles?")
    o.save_query("Pigeons: Where in the world are pigeons most densely populated?")
    o.save_query("Eagles: Where do most eagles live?")

    print o.find_queries("Eagles How en")
    print o.find_queries("Birds Where")
    print o.find_queries("Reptiles Why do")
    print o.find_queries("Animals Wh")
    pass


if __name__ == '__main__':
    main()
