import copy
from classes.bag import Bag
from classes.word import Word
from classes.card import Card
from classes.dictionary import Dictionary
from constants.cards import CARDS_QUANTITY_BY_LETTER
from constants.measures import BOARD_SIDE
from constants.positions import TW, DW, DL, TL
from classes.position import NormalPosition, DWPosition, DLPosition, TWPosition, TLPosition
from classes.exceptions import FirstWordRulesNotRespectedException , WordNotConnectedException, WordDoesNotExistException, LessThanTwoLetters

class Board:
    def __init__(self):
        self.__bag = Bag(CARDS_QUANTITY_BY_LETTER)
        self.__dictionary = Dictionary()
        self.__current_word = Word()
        
        """
        This is a dictionary with current and adjacent words,
        populated during the submission process
        {'current': Word,
        'adjacents' = [Word, Word, Word]}
        """
        self.__current_adjacent_words_dict = {'current': None, 'adjacents': []}

        '''
        This attribute is a dictionary with the following structure:
        {(0,0) : {'horizontal': <WORD_IN_0,0_HORIZONTAL>,
                    'vertical': <WORD_IN_0,0_VERTICAL>},
        (0,1) : {'horizontal': <WORD_IN_0,1_HORIZONTAL>,
                    'vertical': <WORD_IN_0,1_VERTICAL>}}
        '''
        self.__valid_words_search_dict = {}
        for i in range(15):
            for j in range(15):
                self.__valid_words_search_dict[(i, j)] = {'horizontal': None, 'vertical': None}

        self.__positions = []
        self.__first_word_created = False

        for line in range(BOARD_SIDE):
            positions_line = []
            for column in range(BOARD_SIDE):
                position = NormalPosition((line, column))
                if ((line, column) in TW): position = TWPosition((line, column))
                elif ((line, column) in DW): position = DWPosition((line, column))
                elif ((line, column) in DL): position = DLPosition((line, column))
                elif ((line, column) in TL): position = TLPosition((line, column))
                positions_line.append(position)
            self.__positions.append(positions_line)

    @property
    def positions(self):
        return self.__positions

    @property
    def dictionary(self):
        return self.__dictionary
    
    @property
    def bag(self):
        return self.__bag

    @property
    def current_word(self):
        return self.__current_word

    @property
    def valid_words_search_dict(self):
        return self.__valid_words_search_dict
    
    @property
    def first_word_created(self):
        return self.__first_word_created

    @property
    def premium_spots(self):
        return self.__premium_spots
    
    @property
    def current_adjacent_words_dict(self):
        return self.__current_adjacent_words_dict
    
    @first_word_created.setter
    def first_word_created(self, created: bool):
        self.__first_word_created = created

    def calculate_player_score(self):
        total_score = 0
        word = self.__current_adjacent_words_dict['current']

        print(self.__current_word.get_string())
        print(self.current_word.get_string())

        word_multiply_const = 1
        for position in word.positions:
            if isinstance(position, DWPosition): word_multiply_const *= 2
            if isinstance(position, TWPosition): word_multiply_const *= 3

        for position in word.positions:
            letter_multiply_const = 1 
            if isinstance(position, DLPosition): letter_multiply_const *= 2
            if isinstance(position, TLPosition): letter_multiply_const *= 3
        
            letter_Score = position.card.value
            total_score += (letter_Score * letter_multiply_const * word_multiply_const)

        return total_score

    def verify_card_in_center(self):
        return self.positions[7][7].is_enabled == False
    
    def verify_first_word_rules(self):
        # verificar se há um card no centro do tabuleiro
        card_in_center = self.verify_card_in_center()

        more_then_one_card = True if self.current_word.get_lenght() else False

        if more_then_one_card and card_in_center: return True
        else: raise FirstWordRulesNotRespectedException


    def verify_valid_word(self) -> bool:
        self.verify_number_of_letters()
        self.verify_connected_positions()
        self.determine_adjacent_words()
        self.verify_words_existance_and_validity()
        
        return True


    def verify_number_of_letters(self):
        if len(self.current_word.positions) >= 2: return True
        else: raise LessThanTwoLetters


    def verify_connected_positions(self):
        aux = self.verify_current_word_same_line_or_column()
        direction = aux[1]
        
        self.current_word.direction = direction
        max_min_positions = self.current_word.get_min_max_positions()
        
        min_position = max_min_positions[0]
        max_position = max_min_positions[1]
        
        fill = self.verify_positions_filling(min_position.coordinate, max_position.coordinate)
        
        if not fill: raise WordNotConnectedException
    
    def determine_adjacent_words(self):
        """
        self.__current_adjacent_words_dict = 
        {'current': Word,
        'adjacents' = [Word, Word, Word]}

        
        self.__valid_words_search_dict =
        {(0,0) : {'horizontal': <WORD_IN_0,0_HORIZONTAL>,
                    'vertical': <WORD_IN_0,0_VERTICAL>},
        (0,1) : {'horizontal': <WORD_IN_0,1_HORIZONTAL>,
                    'vertical': <WORD_IN_0,1_VERTICAL>}}
        """
        current_word = copy.deepcopy(self.__current_adjacent_words_dict['current'])
        current_word = current_word if current_word else self.current_word
        search_dict = self.__valid_words_search_dict

        print(current_word.get_string())

        for position in current_word.positions:
            already_in_board = search_dict[position.coordinate]['horizontal'] or search_dict[position.coordinate]['vertical']
            if not already_in_board:
                if current_word.direction == 'horizontal':
                    # Coordenada abaixo
                    coord_below = (position.coordinate[0] + 1, position.coordinate[1])
                    # Coordenada acima
                    coord_above = (position.coordinate[0] - 1, position.coordinate[1])

                    if coord_above[0] >= 0 and coord_below[0] <= 14:
                        already_valid_word_below = copy.deepcopy(self.__valid_words_search_dict[coord_below]['vertical']) if self.__valid_words_search_dict[coord_below]['vertical'] != None else None
                        already_valid_word_above = copy.deepcopy(self.__valid_words_search_dict[coord_above]['vertical']) if self.__valid_words_search_dict[coord_above]['vertical'] != None else None

                        if already_valid_word_below and already_valid_word_above:
                            already_valid_word_above.add_position(position)
                            [already_valid_word_above.add_position(position) for position in already_valid_word_below.positions]
                            self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_above)   
                        elif already_valid_word_above:
                            already_valid_word_above.add_position(position)
                            self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_above)   
                        elif already_valid_word_below:
                            already_valid_word_above.add_position(position)
                            self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_above)   
                
                elif current_word.direction == 'vertical':
                    # Coordenada esquerda
                    coord_left = (position.coordinate[0], position.coordinate[1] - 1)
                    # Coordenada direita
                    coord_right = (position.coordinate[0], position.coordinate[1] + 1)

                    print(coord_left, coord_right)

                    if coord_left[1] >= 0 and coord_right[1] <= 14:
                        print(self.__valid_words_search_dict[coord_left]['horizontal'])
                        print(self.__valid_words_search_dict[coord_right]['horizontal'])

                        already_valid_word_left = copy.deepcopy(self.__valid_words_search_dict[coord_left]['horizontal']) if self.__valid_words_search_dict[coord_left]['horizontal'] != None else None
                        already_valid_word_right = copy.deepcopy(self.__valid_words_search_dict[coord_right]['horizontal']) if self.__valid_words_search_dict[coord_right]['horizontal'] != None else None

                        if already_valid_word_left and already_valid_word_right:
                            already_valid_word_left.add_position(position)
                            [already_valid_word_left.add_position(position) for position in already_valid_word_right.positions]
                            self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_left)   
                        elif already_valid_word_left:
                            already_valid_word_left.add_position(position)
                            self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_left)   
                        elif already_valid_word_right:
                            already_valid_word_right.add_position(position, 0)
                            self.__current_adjacent_words_dict['adjacents'].append(already_valid_word_right)
 
        max_min_positions = current_word.get_min_max_positions()
        direction = current_word.direction

        min_pos = max_min_positions[0]
        max_pos = max_min_positions[1]

        if direction == 'horizontal':
            inf_coord = (min_pos.coordinate[0], min_pos.coordinate[1] - 1)
            sup_coord = (max_pos.coordinate[0], max_pos.coordinate[1] + 1)
        else:
            inf_coord = (min_pos.coordinate[0] - 1, min_pos.coordinate[1])
            sup_coord = (max_pos.coordinate[0] + 1, max_pos.coordinate[1])

        in_board = True
        for coord in [inf_coord, sup_coord]: 
            for axis in coord: 
                if axis in [-1, 15]: in_board = False

        inf_word = self.__valid_words_search_dict[inf_coord][direction] if in_board else None
        sup_word = self.__valid_words_search_dict[sup_coord][direction] if in_board else None

        new_current = Word.concatenate(inf_word, current_word, sup_word)

        self.__current_adjacent_words_dict['current'] = new_current

        print(in_board)
        print(self.__valid_words_search_dict[inf_coord][direction])
        print(self.__valid_words_search_dict[sup_coord][direction])

        print(new_current.get_string())
        print(self.__current_adjacent_words_dict['adjacents'])

    def update_search_dict(self):
        """
        self.__current_adjacent_words_dict = 
        {'current': Word,
        'adjacents' = [Word, Word, Word]}

        
        self.__valid_words_search_dict =
        {(0,0) : {'horizontal': <WORD_IN_0,0_HORIZONTAL>,
                    'vertical': <WORD_IN_0,0_VERTICAL>},
        (0,1) : {'horizontal': <WORD_IN_0,1_HORIZONTAL>,
                    'vertical': <WORD_IN_0,1_VERTICAL>}}
        """

        # current_adjacent_words = self.__current_adjacent_words_dict
        current_word = self.__current_adjacent_words_dict['current']

        direction = current_word.direction
        current_direction_key = ''
        adjacent_direction_key = ''
        for position in current_word.positions:
            coordinate = position.coordinate
            if direction == 'horizontal':
                current_direction_key = 'horizontal'
                adjacent_direction_key = 'vertical'
            elif direction == 'vertical':
                current_direction_key = 'vertical'
                adjacent_direction_key = 'horizontal'
            self.__valid_words_search_dict[coordinate][current_direction_key] = current_word
            self.__valid_words_search_dict[coordinate][adjacent_direction_key] = Word([position])

        adjacents_words = copy.deepcopy(self.__current_adjacent_words_dict['adjacents'])
        for word in adjacents_words:
            positions_list = word.positions
            for position in positions_list:
                coordinate = position.coordinate
                self.__valid_words_search_dict[coordinate][adjacent_direction_key] = word

        for position in current_word.positions:
            coordinate = position.coordinate
            word = self.__valid_words_search_dict[coordinate][adjacent_direction_key]
            if word == None:
                new_word = Word()
                new_word.add_position(position)
                self.__valid_words_search_dict[coordinate][adjacent_direction_key] = word


    def verify_words_existance_and_validity(self):
        current_string = (self.__current_adjacent_words_dict['current'].get_string()).lower()

        already_valid_words = self.__dictionary.valid_words
        if not self.__dictionary.search_word(current_string) and current_string not in already_valid_words:
            raise WordDoesNotExistException

        for word in self.__current_adjacent_words_dict['adjacents']:
            adjacent_string = word.get_string().lower()
            if not self.__dictionary.search_word(adjacent_string) and current_string not in already_valid_words:
                raise WordDoesNotExistException

        self.__dictionary.set_new_valid_word(current_string)
        for word in self.__current_adjacent_words_dict['adjacents']:
            adjacent_string = word.get_string().lower()
            self.__dictionary.set_new_valid_word(adjacent_string)

        return True
    
    def verify_current_word_same_line_or_column(self):
        """
        Called whenever a submission of word is running
        Returns if the current word's cards are positioned in same line or column in the board
        """
        word = self.current_word
        line = None
        column = None
        direction = None

        for position in word.positions:
            l = position.coordinate[0]
            c = position.coordinate[1]

            # só entra aqui na primeira posição (eixo do vetor)
            if line == None:
                line = l
                column = c
            # só entra aqui na segunda posição (direção do vetor)
            elif direction == None:
                same_line = l - line

                if same_line == 0:
                    direction = 'horizontal'
                else:
                    same_column = c - column

                    if same_column == 0:
                        direction = 'vertical'
                    else:
                        raise WordNotConnectedException
            # entra aqui em todas as outras posições
            else:
                if direction == 'horizontal':
                    if (position.coordinate[0] - line) != 0:
                        raise WordNotConnectedException

                if direction == 'vertical':
                    if (position.coordinate[1] - column) != 0:
                        raise WordNotConnectedException

        return (True, direction)


    def verify_positions_filling(self, min_position: tuple, max_position: tuple) -> bool:
        all_coords = self.generate_coords(min_coord=min_position, max_coord=max_position, direction=self.current_word.direction)
        word = Word()
        for coord in all_coords:
            position = self.get_position(board_coord=coord)

            if position.is_enabled: return False
            word.add_position(position)
        word.direction = self.current_word.direction
        self.__current_adjacent_words_dict['current'] = word

        return True


    def get_position(self, board_coord: tuple):
        return self.__positions[board_coord[0]][board_coord[1]]


    def generate_coords(self, min_coord: tuple, max_coord: tuple, direction: str) -> list:
        """
        Gets the min and max coordinates and generate the full range of the coordinates
        """

        coords = []

        if direction == 'horizontal':
            for x in range(min_coord[1], max_coord[1]+1):
                coords.append((max_coord[0], x))

        elif direction == 'vertical':
            for y in range(min_coord[0], max_coord[0]+1):
                coords.append((y, min_coord[1]))

        return coords

    def reset_curr_adj_words_dict(self):
        self.__current_adjacent_words_dict = {'current': None, 'adjacents': []}

    def reset_valid_words_search_dict(self):
        for i in range(15):
            for j in range(15):
                self.__valid_words_search_dict[(i, j)] = {'horizontal': None, 'vertical': None}


    def update(self, string: str, positions: 'list[tuple[int]]', direction: str, dict_valid_words: 'dict[str]', bag: 'dict') -> None:
        for index, coord in enumerate(positions):
            letter = string[index]
            card_obj = Card(letter)

            position = self.positions[coord[0]][coord[1]]
            position.card = card_obj
            position.disable()

            self.current_word.add_position(position)

        self.current_word.direction = direction
        self.bag.cards_amount_per_letter = bag['cards_amount_per_letter']
        print(f'NO UPDATE {bag["enabled"]}')
        self.bag.enabled = True if bag['enabled'] == True else False
        self.dictionary.valid_words = dict_valid_words
        # valida as regras gerais da palavra
        self.determine_adjacent_words()
        self.update_search_dict()
        if not self.first_word_created: self.first_word_created = True

    def reset(self):
        self.reset_curr_adj_words_dict()
        self.reset_valid_words_search_dict()
        self.current_word.reset()
        self.dictionary.reset()
        self.bag.reset(CARDS_QUANTITY_BY_LETTER)
        for list in self.positions:
            for position in list:
                position.reset()
        self.first_word_created = False

        
