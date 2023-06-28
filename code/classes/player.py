from classes.pack import Pack
import json 
class Player:
    def __init__(self):
        self.__id = ''
        self.__name = ''
        self.__is_turn = False
        self.__score = 0
        self.__dropouts = 0
        self.__pack = Pack()

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
    
    @property
    def is_turn(self):
        return self.__is_turn

    @property
    def score(self):
        return self.__score
    
    @property
    def dropouts(self):
        return self.__dropouts
    
    @property
    def pack(self):
        return self.__pack

    @name.setter
    def name(self, name: str):
        self.__name = name

    @id.setter
    def id(self, id: str):
        self.__id = id

    @is_turn.setter
    def is_turn(self, is_turn: bool):
        self.__is_turn = is_turn
    
    @score.setter
    def score(self, score: int):
        self.__score = score

    @dropouts.setter
    def dropouts(self, dropouts: int):
        self.__dropouts = dropouts
    
    def reset(self) -> None:
        """
        Resets the player attributes (in case we start a new game) 
        """
        self.__name = ''
        self.__id = ''
        self.__is_turn = False
        self.__score = 0
        self.__dropouts = 0
        self.__pack.reset()


    def initialize(self, id: str, name: str) -> None:
        """
        Resets the player and initializes her id and name

        :param id: str
        :param name: str
        """
        self.reset()
        self.__id = id
        self.__name = name


    def toogle_turn(self) -> None:
        """
        Change logically the is_turn attribute (change the turn of the match)
        """
        self.__is_turn = not self.__is_turn


    def convert_to_json(self):
        a =  json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_string = a.replace("'", "\"").replace('_Pack__', '').replace('_Card__', '').replace('_Player__', '')
        _json = json.loads(json_string)
        return _json
    

    def increment_droupouts(self):
        self.__dropouts += 1

    def __str__(self):
        string = ""
        string += f'==== Player {self.__id} ====\n'
        string += f'{self.__name}\n'
        string += f'{self.__is_turn}\n'
        string += f'=============================='
        return string