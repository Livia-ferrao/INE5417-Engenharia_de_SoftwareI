from classes.trie import Trie
import json

class Dictionary:
    def __init__(self):
        self.__valid_words = []
        self.__trie = Trie()
        self.__trie.load_file('src/dictionary/br-sem-acentos.txt')

    @property
    def valid_words(self):
        return self.__valid_words

    @valid_words.setter
    def valid_words(self, words_list: 'list[str]'):
        self.__valid_words = words_list
    
    def is_valid(self, word: str) -> bool:
        # Verifies if the word is already valid
        return word in self.__valid_words
    
    def search_word(self, word: str) -> bool:
        # Calls the Trie.serch method
        return self.__trie.search(word)
    
    def set_new_valid_word(self, word: str):
        # Set new word already in board
        self.__valid_words.append(word)
    
    def convert_to_json(self):
        move_dict = {'valid_words': self.valid_words}
        json_string =  json.dumps(move_dict)
        _json = json.loads(json_string)
        return _json

    def reset(self):
        self.__valid_words = []