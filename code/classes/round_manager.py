from classes.enums import State, Move
from classes.player import Player
from classes.board import Board
from classes.position import TWPosition, DLPosition, DWPosition, TLPosition
from classes.exceptions import NotYourTurnException, MatchFinishedException, PositionAlreadyHasCardException, InvalidOperation, CardNotSelectedException

class RoundManager:
    def __init__(self):
        self.__match_state = State.NOT_INITIALIZED
        self.__remote_player = Player()
        self.__local_player = Player()
        self.__board = Board()
        self.__player_interface = None
        self.__move_type = None
        self.__winner = None
    
    @property
    def winner(self):
        return self.__winner
    
    @property
    def player_interface(self):
        return self.__player_interface
    
    @player_interface.setter
    def player_interface(self, interface):
        self.__player_interface = interface

    @property
    def board(self) -> Board:
        return self.__board       
    
    @property
    def match_state(self) -> State:
        return self.__match_state

    @property
    def local_player(self) -> Player:
        return self.__local_player

    @property
    def remote_player(self) -> Player:
        return self.__remote_player
    
    @property
    def move_type(self) -> Move:
        return self.__move_type
    
    @winner.setter
    def winner(self, winner: Player):
        self.__winner = winner

    @move_type.setter
    def move_type(self, move_type: Move):
        self.__move_type = move_type
    
    @match_state.setter
    def match_state(self, match_state: State) -> None:
        self.__match_state = match_state

    @local_player.setter
    def local_player(self, local_player: Player):
        self.__local_player = local_player

    @remote_player.setter
    def remote_player(self, remote_player: Player):
        self.__remote_player = remote_player
    
    def configure_players(self, players: dict) -> None:
        self.local_player.initialize(players['local']['id'], players['local']['name'])
        self.remote_player.initialize(players['remote']['id'], players['remote']['name'])


    def start_game(self, players: dict) -> None:
        """
        Define the players and their turn (who starts the match)

        :param players: dict{'local' or 'remote' : {'id': str,
                                                    'name': str,
                                                    'turn': True or False}}
        """
        self.configure_players(players)
        self.__match_state = State.IN_PROGRESS
        self.__move_type = Move.INITIAL
        self.__distribute_cards()

        if players['local']['turn']:
            self.local_player.toogle_turn()
        else:
            self.remote_player.toogle_turn()
            self.__match_state = State.WAITING_REMOTE_MOVE


    def __distribute_cards(self):
        """
        Method to initialize bag's cards and distribute then to players
        """
        remote_cards = self.__board.bag.get_random_cards(7)
        local_cards = self.__board.bag.get_random_cards(7)

        self.local_player.pack.insert_cards(local_cards, [0,1,2,3,4,5,6])
        self.remote_player.pack.insert_cards(remote_cards, [0,1,2,3,4,5,6])


    def select_board_position(self, coord: tuple) -> int:
        """
        Method to handle with the SELECT BOARD POSITION use case

        :param coord: tuple indicating the position selectd
        :return int: 0 if the operation is invalid, 1 if the operation is valid 
        """
        if self.match_state != State.FINISHED:
            if self.local_player.is_turn:
                if self.move_type == Move.CONSTRUCTION:
                    if self.local_player.pack.any_cards_selected:
                        position = self.board.positions[coord[0]][coord[1]]
                        card = self.local_player.pack.current_selected_cards[0]

                        if position.is_enabled:
                            self.player_interface.update_gui_board_positions({(coord[0], coord[1]): card.letter})
                            
                            # desabilita o card do board pra não poder mais adicionar lá
                            position.card = card
                            position.disable()

                            # limpa e desabilita o card do pack
                            indexes = self.local_player.pack.remove_selected_cards()
                            self.player_interface.update_gui_local_pack({indexes[0]: 'NORMAL'})

                            # adicionando a posição na currrent word
                            self.board.current_word.add_position(position)
                            palavra = self.board.current_word.get_string()
                        else:
                            raise PositionAlreadyHasCardException
                    else:
                        raise CardNotSelectedException
                else:
                    raise InvalidOperation
            else:
                raise NotYourTurnException
        else: raise MatchFinishedException

    def convert_move_to_dict(self):
        move = {}
        move['match_status'] = str(self.__match_state).replace('State.', '')
        move['move_type'] = str(self.__move_type).replace('Move.', '')

        if self.move_type == Move.INITIAL:
            move['remote_player'] = self.__remote_player.convert_to_json()
            move['local_player'] = self.__local_player.convert_to_json()
            move['bag'] = self.board.bag.convert_to_json()

        elif self.move_type == Move.CONSTRUCTION:
            move['valid_word'] = self.board.current_word.convert_to_json()
            move['dict_valid_words'] = self.board.dictionary.convert_to_json()
            move['bag'] = self.board.bag.convert_to_json()
            move['player_score'] = self.local_player.convert_to_json()

        elif self.move_type == Move.CHANGE:
            # move['pack'] = self.local_player.pack.convert_to_json()
            move['bag'] = self.board.bag.convert_to_json()
        return move


    def update_player_pack(self, player: Player, letters: 'list[str]', positions: 'list[int]') -> None:
        """
        Sets local player pack (in case the remote made the INITIAL move)
        """
        cards = self.__board.bag.get_cards_by_letters(letters)
        player.pack.insert_cards(cards, positions)


    def select_card_from_pack(self, index: int):
        """
        Verify turn and move type and pass the control to pack

        :param index: index of the position of the pack selected in GUI
        """
        if self.match_state != State.FINISHED:
            if self.__local_player.is_turn:
                if self.move_type != Move.CHANGE:
                    self.move_type = Move.CONSTRUCTION
                self.proceed_card_selection(index)
            else: raise NotYourTurnException
        else: raise MatchFinishedException

    
    def proceed_card_selection(self, index: int):
        """
        Proceeds card selection

        :param index: index of the position of the pack clicked in GUI
        """
        pack = self.__local_player.pack

        if self.move_type == Move.CONSTRUCTION:
            any_selected = pack.any_cards_selected()
            if any_selected:
                #: gets the current selected card index
                selected_index = pack.get_selected_card_index()
                pack.deselect_all_cards()
                self.player_interface.mark_off_card(selected_index)

            pack.select_card(index)
            self.player_interface.mark_card(index)

        elif self.move_type == Move.CHANGE:
            is_selected = pack.is_current_card_selected(index)

            if is_selected:
                pack.deselect_card(index)
                self.player_interface.mark_off_card(index)
            else:
                pack.select_card(index)
                self.player_interface.mark_card(index)
                

    def receive_move(self, move_type: Move, move_dict: dict):
        if move_type == Move.INITIAL:
            # Gets cards distribuited remotely and updates local instances
            local_initial_letters = [card['letter'] for card in move_dict['remote_player']['pack']['cards']]
            remote_initial_letters = [card['letter'] for card in move_dict['local_player']['pack']['cards']]

            self.update_player_pack(self.local_player, local_initial_letters, range(len(local_initial_letters)))
            self.update_player_pack(self.remote_player, remote_initial_letters, range(len(remote_initial_letters)))

            # Updates state and move type
            self.move_type == Move.INITIAL
            self.__match_state = State.IN_PROGRESS
        else:
            if move_type == Move.CHANGE:
                cards_bag = move_dict['bag']['cards_amount_per_letter']
                self.board.bag.cards_amount_per_letter = cards_bag
                self.__player_interface.show_message(title='Jogada recebida', message="O outro jogador trocou de letras. É sua vez de jogar!")

            elif move_type == Move.GIVE_UP:
                self.remote_player.increment_droupouts()
                self.verify_game_end()
                self.show_message()

            elif move_type == Move.CONSTRUCTION:
                string = move_dict['valid_word']['string']
                positions = move_dict['valid_word']['positions']
                dict_valid_words = move_dict['dict_valid_words']['valid_words']
                remote_player_score = move_dict['player_score']['score']
                direction = move_dict['valid_word']['direction']
                bag = move_dict['bag']

                self.board.update(string, positions, direction, dict_valid_words, bag)

                for index, coord in enumerate(positions):
                    self.player_interface.update_gui_board_positions({(coord[0], coord[1]): string[index]})

                self.remote_player.score = remote_player_score
                self.player_interface.update_gui_players_score()

                self.reset_move()
                self.verify_game_end()
                self.show_message()
    
            self.local_player.toogle_turn()
            self.remote_player.toogle_turn()

    def show_message(self):        
        if self.__match_state != State.FINISHED:
            self.__player_interface.show_message(title='Jogada recebida', message="Sua vez de jogar!")
        else:
            self.__player_interface.show_message(title='PARTIDA FINALIZADA', message="O JOGO ACABOU")
            

    def submit_word(self):
        if self.move_type == Move.CONSTRUCTION:
            try:
                if not self.board.first_word_created:
                    self.board.verify_first_word_rules()

                # valida as regras gerais da palavra
                self.board.verify_valid_word()

                self.board.update_search_dict()
                
                if not self.board.first_word_created: self.board.first_word_created = True

                total = self.board.calculate_player_score()
                self.local_player.score += total

                # preenchendo o pack do jogador
                indexes_empty_cards = self.local_player.pack.get_empty_indexes()
                board_cards = [position.card.letter for position in self.board.current_word.positions]
                cards = self.__board.bag.get_random_cards(len(board_cards), [])

                if cards:
                    self.local_player.pack.insert_cards(cards, indexes_empty_cards)
                    aux_dict = {}
                    for index_empty in indexes_empty_cards:
                            aux_dict[index_empty] = self.local_player.pack.cards[index_empty].letter

                    self.player_interface.update_gui_local_pack(aux_dict)

                self.player_interface.update_gui_players_score()

                # verificar final do jogo
                self.verify_game_end()

                self.__player_interface.show_message(title='Palavra válida', message="Palavra válida!")
                self.__player_interface.send_move()

                self.local_player.toogle_turn()
                self.remote_player.toogle_turn()

                self.__player_interface.show_message(title='Jogada enviada', message="Você acabou de jogar, aguarde a jogada do outro jogador!")

            except Exception as e:
                self.__player_interface.show_message(title='Palavra inválida', message=str(e))
                self.proceed_cards_returning()

            finally:
                self.reset_move()
        else:
            self.__player_interface.show_message(title='Jogada inválida', message="Jogada inválida, é preciso formar uma palavra para submetê-la!")
    
    def reset_move(self):
        """
        Resets the move
        """
        if self.move_type != Move.GIVE_UP:
            self.local_player.dropouts = 0
            self.remote_player.dropouts = 0
        self.board.current_word.reset()
        # self.local_player.pack.deselect_all_cards()
        self.board.reset_curr_adj_words_dict()
    
    def return_cards_to_pack(self):
        """
        Return cards main methos (called in the execution of the use case)
        """
        if self.match_state != State.FINISHED:
            if self.local_player.is_turn:
                self.proceed_cards_returning()
            else:
                raise NotYourTurnException
        else: raise MatchFinishedException

    def proceed_cards_returning(self):
        if self.move_type != Move.CHANGE:
            
            positions = self.board.current_word.positions
            positions_coords = self.board.current_word.get_positions_coords()

            self.board.current_word.reset()

            empty_pack_indexes = self.local_player.pack.get_empty_indexes()

            cards = [position.card for position in positions]

            [card.self_unselect() for card in cards]
            [position.reset() for position in positions]

            self.local_player.pack.insert_cards(cards, empty_pack_indexes)

            # verificação das posições do board (se for uma posição especial é preciso reiniciar como especial)
            self.reset_board_positions(positions, positions_coords)

            aux_dict = {}
            for index, empty_index in enumerate(empty_pack_indexes):
                aux_dict[empty_index] = cards[index].letter
            self.player_interface.update_gui_local_pack(aux_dict)
            
        else:
            self.player_interface.show_message(title='Jogada inválida', message="Não é permitido retornar os cards em uma jogada de troca de cards!")

    def reset_board_positions(self, positions, positions_coords):
        aux_dict = {}
        for index, position in enumerate(positions):
            coordinate = positions_coords[index]
            coord_type = 'NORMAL'
            if isinstance(position, TWPosition): coord_type = 'TW'
            elif isinstance(position, DWPosition): coord_type = 'DW'
            elif isinstance(position, DLPosition): coord_type = 'DL'
            elif isinstance(position, TLPosition): coord_type = 'TL'
            elif coordinate == (7,7): coord_type = '*'
            else: coord_type = 'NORMAL'
            aux_dict[coordinate] = coord_type

        self.player_interface.update_gui_board_positions(aux_dict)
    

    def change_cards_from_pack(self):
        """
        Change cards main methos (called in the execution of the use case)
        """
        if self.match_state != State.FINISHED:
            if self.local_player.is_turn:
                if self.move_type == Move.CHANGE:
                    self.proceed_change_cards()
                    self.reset_move()
                    self.player_interface.mark_off_change_button()
                    self.__player_interface.send_move()
                    self.local_player.toogle_turn()
                    self.remote_player.toogle_turn()
                    self.move_type = Move.CONSTRUCTION
                    self.player_interface.show_message(title='Jogada enviada', message="Você acabou de jogar, aguarde a jogada do outro jogador!")
                else:
                    self.proceed_cards_returning()
                    self.move_type = Move.CHANGE
                    self.player_interface.show_message(title='Troca de letras', message="Selecione as letras que deseja trocar")
                    self.player_interface.mark_change_button()
            else:
                raise NotYourTurnException
        else: raise MatchFinishedException

    def proceed_change_cards(self):
        selected_cards = self.local_player.pack.current_selected_cards
        cards = self.__board.bag.exchange_cards(selected_cards)

        aux_dict = {}
        for index, card in enumerate(self.local_player.pack.cards):
            for card_selected in selected_cards:
                if card_selected == card:
                    self.local_player.pack.insert_cards([cards[0]], [index])
                    cards.pop(0)
                    self.player_interface.mark_off_card(index)
                    aux_dict[index] = self.local_player.pack.cards[index].letter

        self.player_interface.update_gui_local_pack(aux_dict)

        self.local_player.pack.deselect_all_cards()


    def give_up_round(self):
        if self.match_state != State.FINISHED:
            if self.local_player.is_turn:
                self.__move_type = Move.GIVE_UP
                self.return_cards_to_pack()
                self.reset_move()
                self.local_player.dropouts += 1
                self.__match_state = State.WAITING_REMOTE_MOVE
                self.verify_game_end()

                #: desseleciona todos os cads do pack antes de enviar 
                any_selected = self.local_player.pack.any_cards_selected()
                if any_selected:
                    selected_index = self.local_player.pack.get_selected_card_index()
                    self.local_player.pack.deselect_all_cards()
                    self.player_interface.mark_off_card(selected_index)

                self.local_player.toogle_turn()
                self.remote_player.toogle_turn()

                self.__player_interface.send_move()
                
                self.player_interface.show_message(title='Jogada enviada', message="Você acabou de jogar, aguarde a jogada do outro jogador!")

            else:
                raise NotYourTurnException 
        else: raise MatchFinishedException

    def verify_game_end(self):
        if (self.local_player.dropouts == 2 and self.remote_player.dropouts == 2) or (self.board.bag.enabled == False):
            print(self.board.bag.enabled)
            print(self.local_player.dropouts)
            print(self.remote_player.dropouts)
            if self.local_player.score >= self.remote_player.score:
                self.player_interface.show_message(title='Fim de jogo', message="Parabéns! Você ganhou a partida!")
                self.winner = self.local_player
            elif self.local_player.score < self.remote_player.score:
                self.player_interface.show_message(title='Fim de jogo', message="Que pena! Você perdeu.")
                self.winner = self.remote_player
            self.__match_state = State.FINISHED
        

    def reset_game(self):
        self.match_state = State.NOT_INITIALIZED
        self.remote_player.reset()
        self.local_player.reset()
        self.board.reset()
        self.winner = None
        self.move_type = None

    def receive_withdrawal_notification(self):
        self.player_interface.show_message(title='Partida encerrada', message="O seu adversário desistiu da partida!")
        self.reset_game()