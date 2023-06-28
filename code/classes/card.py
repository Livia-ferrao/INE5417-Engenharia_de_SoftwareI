from constants.cards import CARDS_VALUES_BY_LETTER
class Card:
    def __init__(self, letter: str):
        self.__letter = letter
        self.__value = CARDS_VALUES_BY_LETTER[letter]
        self.__enabled = False
        self.__selected = False
    
    @property
    def letter(self):
        return self.__letter
    
    @property
    def value(self):
        return self.__value
    
    @property
    def enabled(self):
        return self.__enabled
    
    @property
    def selected(self):
        return self.__selected
    
    def self_enable(self):
        self.__enabled = True

    def self_disable(self):
        self.__enabled = False
    
    def self_unselect(self):
        self.__selected = False

    def self_select(self):
        self.__selected = True

    
        