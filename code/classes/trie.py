from classes.trie_node import TrieNode

class Trie:
    def __init__(self):
        self.__root = TrieNode()
    
    def __char_to_index(self, char: str):
        """
        Gets the index of the alphabetic array

        :param char: caracter a-z to be transformed
        """
        return ord(char) - ord('a')
    
    def insert(self, key: str):
        """
        Inserts the word in the Trie

        :param key: the word to be inserted 
        """
        ref = self.__root
        for letter in key:
            index = self.__char_to_index(letter)
            if not ref.children[index]:
                ref.children[index] = TrieNode()
            ref = ref.children[index]
        ref.is_end = True
    
    def search(self, key: str):
        """
        Search a word, level by level

        :param key: word to be searched
        :return: True if the word exists else False
        """
        ref = self.__root
        for letter in key:
            index = self.__char_to_index(letter)
            if not ref.children[index]:
                return False
            ref = ref.children[index]
        return ref.is_end

    def load_file(self, filepath: str):
        """
        Reads a file and inserts the words in the trie

        :param filepath: file to the path
        """
        with open(filepath, 'r') as file:
            words = file.readlines()
            for word in words:
                word = word.strip()
                self.insert(word.lower())
