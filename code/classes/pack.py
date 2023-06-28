from classes.exceptions import PositionAlreadyHasCardException
from classes.exceptions import PositionDoesNotHaveCardException
from classes.exceptions import CardNotSelectedException
from classes.card import Card 
import json
class Pack:  
    def __init__(self):
        self.__cards = [None for _ in range(7)]
        self.__current_selected_cards = []
    
    @property
    def cards(self):
        return self.__cards
    
    @property
    def current_selected_cards(self):
        return self.__current_selected_cards
    
    def any_cards_selected(self):
        return self.__current_selected_cards != []
    
    def insert_cards(self, cards: list, coords: list) -> None:
        """
        Inserts cards on the specified positions in pack
        """
        for index, position in enumerate(coords):
            self.__cards[position] = cards[index]


    def select_card(self, index: int) -> None:
        if self.__cards[index] == None: raise PositionDoesNotHaveCardException
        else: 
            self.__cards[index].self_select()
            self.__current_selected_cards.append(self.__cards[index])


    def deselect_card(self, index: int) -> None:
        if self.__cards[index] == None: raise PositionDoesNotHaveCardException
        elif not self.__cards[index].selected : raise CardNotSelectedException
        else: 
            self.__cards[index].self_unselect()
            self.__current_selected_cards.remove(self.__cards[index])


    def reset(self):
        self.__cards = [None for _ in range(7)]
        self.__current_selected_cards = []


    def count_cards(self) -> int:
        return len(self.__cards)


    def deselect_all_cards(self) -> None:
        [selected.self_unselect() for selected in self.__current_selected_cards]
        self.__current_selected_cards = []


    def get_selected_card_index(self) -> int:
        return self.__cards.index(self.__current_selected_cards[0])


    def get_empty_indexes(self):
        indexes = []
        for index, card in enumerate(self.cards):
            if not card: indexes.append(index)
        return indexes


    def remove_selected_cards(self) -> 'list[int]':
        indexes = []
        for card in self.__current_selected_cards:
            index = self.__cards.index(card)
            card.self_disable()
            self.__cards[index] = None
            indexes.append(index)

        self.__current_selected_cards = []

        return indexes


    def is_current_card_selected(self, index) -> bool:
        is_selected = self.__cards[index].selected

        return is_selected


    def convert_to_json(self):
        a =  json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_string = a.replace("'", "\"").replace('_Pack__', '').replace('_Card__', '')
        _json = json.loads(json_string)

        return _json
