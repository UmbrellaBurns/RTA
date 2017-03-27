class Sentence:
    def __init__(self):
        self.__text = None
        self.__syntax_tree = None

    def set_text(self, text):
        self.__text = text

    def set_syntax_tree(self, tree):
        self.__syntax_tree = tree

    def get_text(self):
        return self.__text

    def get_syntax_tree(self):
        return self.__syntax_tree


class SyntaxTree:
    def __init__(self):
        self.__nodes = []
        self.__root = None

    def add_node(self, node):
        self.__nodes.append(node)

    def get_nodes(self):
        return self.__nodes

    def get_root(self):
        return self.__root

    def set_root(self, root):
        self.__root = root
        
    def get_node_by_id(self, id):
        for node in self.__nodes:
            if node.get_id() == id:
                return node
        return None

    def traversal(self):
        pass
    
    
class Node:
    def __init__(self, id=None, word=None):
        self.__id = id
        self.__word = word
        
        self.__parent = None
        self.__link_type = None
        
    def set_id(self, id):
        self.__id = id
    
    def set_word(self, word):
        self.__word = word
        
    def set_parent(self, node):
        self.__parent = node
        
    def set_link_type(self, type):
        self.__link_type = type

    def get_id(self):
        return self.__id

    def get_word(self):
        return self.__word

    def get_parent(self):
        return self.__parent

    def get_link_type(self):
        return self.__link_type
