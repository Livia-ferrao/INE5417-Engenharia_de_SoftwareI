from classes.position import Position
import json

class Word:
    def __init__(self, positions=None): 
        self.__positions = positions if positions else []
        self.__direction = ''

    @property
    def positions(self):
        return self.__positions
    
    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction: str):
        self.__direction = direction
    
    @positions.setter
    def positions(self, positions: list):
        self.__positions = positions

    def add_position(self, position: Position, index: int = None) -> None:
        if not index: self.__positions.append(position)
        else: self.__positions.insert(index, position)
    
    def get_lenght(self) -> int:
        return len(self.__positions)
    

    def get_positions_coords(self) -> 'list[tuple]':
        coordinates = []
        for position in self.__positions:
            coordinates.append(position.coordinate)
        return coordinates

    @staticmethod
    def concatenate(*words: 'list[Word]') -> 'Word':
        print('22222222222222222222222222222222222222222222')
        concatenated_positions = []
        direction = ''
        for word in words:
            if word != None and word.positions != []:
                print(word.get_string())
                concatenated_positions.extend(word.positions)
                direction = word.direction

        new_word = Word(concatenated_positions)
        new_word.direction = direction
        return new_word

    
    def get_min_max_positions(self) -> 'tuple(Position, Position)':
        """
        Sort the positions array based on the coordinates attribute

        :returns tuple<Position, Position>: 
        """  
        self.__positions = sorted(self.__positions, key=lambda position: position.coordinate[1] if self.__direction == "horizontal" else position.coordinate[0])
        min_position = self.positions[0]
        max_position = self.positions[-1]

        return (min_position, max_position)


    def get_string(self) -> str:
        """
        Returns the Word in string format based on the Position.card.letter attribute

        :return string: The string of the word
        """
        string = ''
        for position in self.__positions:
            string += position.card.letter
        return string

    def reset(self):
        self.__positions = []
        self.__direction = ''

    def convert_to_json(self):
        move_dict = {
            'string': self.get_string(),
            'positions': [p.coordinate for p in self.__positions],
            'direction': self.direction}

        json_string =  json.dumps(move_dict)
        _json = json.loads(json_string)

        return _json