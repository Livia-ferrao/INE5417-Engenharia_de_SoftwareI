class TrieNode:
    def __init__(self):
        self.__children = [None]*26
        self.__is_end = False
    
    @property
    def children(self):
        return self.__children

    @property
    def is_end(self):
        return self.__is_end
    
    @is_end.setter
    def is_end(self, is_end: bool):
        self.__is_end = is_end
