from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
import tkinter as tk
from tkinter import Frame, Label, messagebox, Button, Menu, Canvas, simpledialog, PhotoImage
from PIL import Image, ImageTk
from constants.positions import POSITIONS_RGB
from constants.cards import CARDS_VALUES_BY_LETTER

from classes.round_manager import RoundManager
from classes.enums import State, Move
from constants import messages, interface
class PlayerInterface(DogPlayerInterface):
	def __init__(self, window_size: tuple, board_side:int, title: str):
		self.round_manager = RoundManager()
		self.round_manager.player_interface = self
		self.window_size = window_size
		self.board_side = board_side
		self.board_size = 2/3 * window_size[0]
		self.title = title
		self.window = tk.Tk()
		self.window.title(title)
		self.menu_bar = Menu(self.window)
		self.window.config(menu=self.menu_bar)
		self.file_menu = Menu(self.menu_bar)
		self.file_menu.add_command(
			label='Start game',
			command=self.start_game
		)
		self.file_menu.add_command(
			label='Exit game',
			command=self.window.destroy,
		)
		self.file_menu.add_command(
			label='Reset game',
			command= self.reset_game,
		)
		self.menu_bar.add_cascade(
			label="Game options",
			menu=self.file_menu,
			underline=0
		)
		# Dictionary with images charged
		self.__images = {
			'CARDS': {}, 
			'POSITIONS': {}
		}
		# Matrix of labels
		self.board_positions = []
		# List of labels
		self.pack_positions = []
		self.buttons = {
			'button(submit)': {'btn_description': 'Submeter palavra',
		      				   'btn_position': (20,15)},
			'button(return)': {'btn_description': 'Retornar cards', 
		      				   'btn_position': (20,50)},
			'button(giveup)': {'btn_description': 'Passar a vez',
		    				   'btn_position': (20,85)},
			'button(change)': {'btn_description': 'Trocar cards',
		      				   'btn_position': (20,120)}
		}
		self.local_pack_cards = []
		self.scores = {}
		self.main_frame = Frame(self.window, width=window_size[0], height=window_size[1], relief='raised', bg=interface.BG_MAIN_COLOR)
		self.player_frame_height = 1/6*window_size[0]
		self.board_frame = Frame(self.main_frame, width=self.board_size, height=self.board_size, bg=interface.BG_MAIN_COLOR)
		self.remote_player_frame = Frame(self.main_frame, width=window_size[0], height=self.player_frame_height, bg=interface.BG_PLAYERS_SPACE)
		self.remote_player_frame.pack(side='top')
		self.local_player_frame = Frame(self.main_frame, width=window_size[0], height=self.player_frame_height, bg=interface.BG_PLAYERS_SPACE)
		self.local_player_frame.pack(side='bottom')
		for frame in [self.board_frame, self.main_frame]:
			frame.pack()
			frame.pack_propagate(0)
		self.__load_images()
		self.__render_gui()
		self.window.mainloop()

	@property
	def dog_server_interface(self):
		return self.__dog_server_interface

	#Rendering game window
	def __render_gui(self):
		self.__initialize_dog()
		self.__draw_packs((self.board_size/self.board_side*7, 1/3*self.player_frame_height), self.board_size/self.board_side)
		self.scores['local'] = self.__draw_score(self.local_player_frame, (200,100), (720, 30))
		self.scores['remote'] = self.__draw_score(self.remote_player_frame, (200,100), (720, 30))
		self.__draw_board(self.board_size/self.board_side, self.board_side)
		self.__draw_buttons()
		

	def __initialize_dog(self):
		player_name = simpledialog.askstring(title='Identificação de jogador', prompt='Digite o seu nome:')
		self.__dog_server_interface = DogActor()
		message = self.__dog_server_interface.initialize(player_name, self)
		messagebox.showinfo(message=message)

	def __load_images(self):
		for letter in CARDS_VALUES_BY_LETTER.keys():
			self.__images['CARDS'][f'{letter}'] = self.__load_card_img(letter, self.board_size/self.board_side)
		for position in POSITIONS_RGB.keys():
			self.__images['POSITIONS'][f'{position}'] = self.__load_position_img(position, self.board_size/self.board_side)


	def __load_position_img(self, pos_type: str, size: int) -> ImageTk.PhotoImage:
		RELATIVE_PATH = 'src/images/positions/scrabble'
		image = self.__load_img(f'{RELATIVE_PATH}_{pos_type.upper()}.png', int(size)-6)
		return image

	
	def __load_img(self, img_path: str, size: int) -> ImageTk.PhotoImage:
		"""
		Loads the image in the label, using ImageTk from PIL
		
		:param img_path: path to the image
		:param size: size of the image
		"""
		pil_img = Image.open(img_path)
		resized_img = pil_img.resize((size, size), Image.ANTIALIAS)
		tk_img = ImageTk.PhotoImage(resized_img)
		return tk_img
	
	# TODO substituir isso por uma classe ou dicionário que já fique carregado com as imagens
	# (demora muito ir carregando tudo durante a execução)
	def __load_card_img(self, letter: str, size: int) -> ImageTk.PhotoImage:
		RELATIVE_PATH = 'src/images/cards/scrabble'
		image = self.__load_img(f'{RELATIVE_PATH}_{letter.upper()}.png', int(size)-6)
		return image


	#Drawing button
	def __draw_button(self, btn_text: str, width: float, height: float, position: tuple, main_frame: Frame, name: str) -> Button: 
		new_button = Button(main_frame, text=btn_text, name=name)
		new_button.place(x=position[0], y=position[1])
		return new_button


	def __draw_buttons(self):
		for button_name, button_config in self.buttons.items():
			button = self.__draw_button(button_config['btn_description'], None, None, button_config['btn_position'], self.local_player_frame, button_name)
			if button_name == 'button(submit)':
				button.bind(
					"<Button-1>",
					lambda event: self.submit_word(event))
			elif button_name == 'button(return)':
				button.bind(
					"<Button-1>",
					lambda event: self.return_cards_to_pack(event))
			elif button_name == 'button(giveup)':
				button.bind(
					"<Button-1>",
					lambda event: self.give_up_round(event))
					#    general_click(event,
				    #   'Passar a vez', 'Certeza que quer passar a vez?',
					#   'Trocando de turno', 'Voltando ao jogo'))
			elif button_name == 'button(change)':
				button.bind(
					"<Button-1>",
					lambda event: self.change_cards_from_pack(event))
					# 	general_click(event,
				    #   'Trocar de cards', 'Certeza que quer trocar os cards do seu pack?',
					#   'Cards serão selecionados e a troca ocorrerá', 'Voltando ao jogo'))
			self.buttons[button_name]['btn_object'] = button


	#Drawing packs
	def __draw_packs(self, pack_size: tuple, card_size: float):
		font = interface.FONT_PLAYERS_NAMES
		position_bg = interface.BG_PACKS_POSITIONS
		player_name = interface.INITIAL_PLAYER_NAME

		self.frame_remote_pack = Frame(self.remote_player_frame, width=pack_size[0], height=pack_size[1])
		self.frame_local_pack = Frame(self.local_player_frame, width=pack_size[0], height=pack_size[1])
		
		self.label_remote_player = Label(self.remote_player_frame, font=font, text=player_name, width=29, borderwidth=5)
		self.label_local_player = Label(self.local_player_frame, font=font, text=player_name, width=29, borderwidth=5)

		self.label_local_player.place(x=340, y=40)
		self.label_remote_player.place(x=340, y=100)
		self.frame_remote_pack.place(x=340,y=30)
		self.frame_local_pack.place(x=340, y=90)

		for i in range(7):
			new_remote_pack_pos = Frame(self.frame_remote_pack, width=card_size, height=card_size, bg=position_bg, highlightthickness=1, name=f'remote({0,i})')
			new_local_pack_pos = Frame(self.frame_local_pack, width=card_size, height=card_size, bg=position_bg, highlightthickness=1, name=f'local({0,i})')
			new_local_pack_pos.bind("<Button-1>", lambda event: self.select_card_from_pack(event))
			for pack_position in [new_local_pack_pos, new_remote_pack_pos]:
				pack_position.place(x=i*card_size, y=5)
				self.pack_positions.append(pack_position)
			label = self.__draw_card(new_local_pack_pos, card_size, 'A')
			label.id = f'local{i}, A'
			self.local_pack_cards.append(label)


	# drawing the 255 positions of the board
	def __draw_board(self, position_size: int, board_side: int):
		RELATIVE_PATH = 'src/images/positions/scrabble'
		POSITIONS_IMG_DICT = {
			'DW' : f'{RELATIVE_PATH}_DW.png',
			'DL' : f'{RELATIVE_PATH}_DL.png',
			'TW' : f'{RELATIVE_PATH}_TW.png',
			'TL' : f'{RELATIVE_PATH}_TL.png',
			'NORMAL' : f'{RELATIVE_PATH}_NORMAL.png',
			'*' : f'{RELATIVE_PATH}_*.png'
		}
		
		tw = [(0,0), (0,7), (0,14), (7,0), (7,14), (14,0), (14,7), (14,14)]
		dw = [(1,1), (2,2), (3,3), (4,4), (13,13), (12,12), (11,11), (10,10), (1,13), (2,12), (3,11), (4,10), (13,1), (12,2), (11,3), (10,4)]
		dl = [(0,3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8,12), (11,0), (11,7), (11,14), (12,6), (12,8), (14,3), (14,11)]
		tl = [(1,5), (1,9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13,5), (13,9)]
		
		for line in range(board_side):
			positions_line = []
			for column in range(board_side):
				# Defining positions
				x0 = column * position_size
				y0 = line * position_size
				frame_position = Frame(self.board_frame, width=position_size, height=position_size, bg='gray', highlightthickness=1)
				
				# We create the Label's image depending on the type o the position
				dict_key = 'NORMAL'
				if ((line, column) in tw): dict_key = 'TW'
				elif ((line, column) in dw): dict_key = 'DW'
				elif ((line, column) in dl): dict_key = 'DL'
				elif ((line, column) in tl): dict_key = 'TL'
				elif ((line, column) == (7,7)): dict_key = '*'
				
				# Creating Label's image
				image = self.__images['POSITIONS'][dict_key]	
				label = Label(
					frame_position, 
					bg=interface.BG_BOARD_POSITIONS,
					image=image,
					borderwidth=3,
					name=f'board{line, column}'
				)
				label.image = image
				label.bind(
				'<Button-1>',
				lambda event: self.select_board_position(
					event)
				)
				label.pack()
				frame_position.place(x=x0, y=y0)

				# Iserting label on line
				positions_line.append(label)

			# Iserting line on positions matrix
			self.board_positions.append(positions_line)


	#click event in positions of the board
	def click(self, event, main_message: str, message: str, color: str):
		messagebox.showinfo(f'{main_message}', \
							f'{message}: {(str(event.widget)).split(".")[-1]}')
		event.widget.configure(bg=f'{color}')


	#click event in the buttons
	def general_click(self, event, main_message: str, ask_message: str, affirm_message: str, negat_message: str):
		answer = messagebox.askquestion(f'{main_message}', \
				  						f'{ask_message}', icon='warning')
		if answer == 'yes':
			messagebox.showinfo('', \
		       					affirm_message)
		else:
			messagebox.showinfo('', \
		       					negat_message)


	def submit_word(self, event):
		try:
			self.round_manager.submit_word()
		except Exception as e:
			self.show_message("ERRO", f'Erro ao submeter palavra -> {e}')


	def return_cards_to_pack(self, event):
		try:
			self.round_manager.return_cards_to_pack()
		except Exception as e:
			self.show_message("ERRO", f'Erro ao retornar cards para o pack -> {e}')


	def change_cards_from_pack(self, event):
		try:
			self.round_manager.change_cards_from_pack()
		except Exception as e:
			self.show_message("ERRO", f'Erro ao trocar cards do pack -> {e}')


	def give_up_round(self, event):
		try:
			self.round_manager.give_up_round()
		except Exception as e:
			self.show_message("ERRO", f'Erro ao desistir da partida -> {e}')


	def __askquestion(self, title: str, ask_message: str) -> None:
		answer = messagebox.askquestion(title, ask_message, icon='question')
		return True if answer == 'yes' else False


	def show_message(self, title: str, message: str) -> None:
		messagebox.showinfo(title=title, message=message)

	
	#draw card (using Label widget)
	def __draw_card(self, position: Frame, size: int, letter: str) -> Label:
		image = self.__load_card_img(letter, size)
		
		card = Label(
					position, 
					bg='green',
					image=image,
					borderwidth=3,
					name=f'card {letter}'
				)
		card.image = image
		card.bind(
		'<Button-1>',
		lambda event: self.select_card_from_pack(event)
		)
		card.pack()
		return card


	# Drawing scores (using Canvas widget)
	def __draw_score(self, main_frame: Frame, size: tuple, position: tuple) -> Canvas:
		# TODO definir essas variáveis como globais, para que fique tudo paramétrico
		title_font = interface.FONT_SCORE_TITLE
		score_font = interface.FONT_SCORE_NUMBER
		bg = interface.BG_PLAYERS_SPACE
		score_bg = interface.BG_PLAYERS_SCORE
		new_score = Canvas(main_frame, width=size[0], height=size[1], bg=bg, borderwidth=3, highlightthickness=0)
		label_title = Label(new_score, width=int(size[0]), text='Pontuação', font=title_font, bg=bg, borderwidth=10)
		new_score.create_window(70, 14, window=label_title)
		label_score = Label(new_score, text='0', font=score_font, bg=score_bg)
		new_score.create_window(70, 60, window=label_score, width=int(size[0]/2))

		new_score.place(x=position[0], y=position[1])
		return label_score
	
	def start_game(self) -> None:
		# Se o estado do jogo estiver em NOT_INITIALIZED
		if (self.round_manager.match_state == State.NOT_INITIALIZED):
			answer = self.__askquestion(messages.START_MATCH_TITLE, messages.START_MACTH_QUESTION)
			if answer:
				start_status = self.__dog_server_interface.start_match(2)
				code = start_status.get_code()
				message = start_status.get_message()
				# 0 - file game.id not found; 1 - not connected to server; 2 - connected without match; 3 - waiting move (even if it's the local player's turn)
				if code == '0' or code == '1':
					self.show_message(messages.START_MATCH_DOG_RESPONSE_TITLE, message)
				else:
					players_response = start_status.get_players()

					# Building player dict and order list to pass as parameter in RoundManager.start_match()
					players = self.__status_response_to_dict(players_response)

					self.round_manager.start_game(players)
					#TODO Não podemos fazer isso, temos que conferir se a partida está em andamento (se foi iniciada) no clique
					self.show_message(messages.START_MATCH_DOG_RESPONSE_TITLE, message)

					self.send_move()

					self.update_gui_local_pack()
					self.__update_gui_players_names()

	def send_move(self) -> None:
		dict_json = self.round_manager.convert_move_to_dict()
		self.dog_server_interface.send_move(dict_json)
		if not dict_json['move_type'] == 'INITIAL':
			self.round_manager.match_state == State.WAITING_REMOTE_MOVE

	def receive_move(self, a_move: dict) -> None:
		if a_move['move_type'] == 'INITIAL':
			# Passthe control to the round manager
			self.round_manager.receive_move(Move.INITIAL, a_move)
			# Updates user interface
			self.__update_gui(Move.INITIAL)

		elif a_move['move_type'] == 'CHANGE':
			# Passthe control to the round manager
			self.round_manager.receive_move(Move.CHANGE, a_move)

		elif a_move['move_type'] == 'GIVE_UP':
			self.round_manager.receive_move(Move.GIVE_UP, a_move)
		
		elif a_move['move_type'] == 'CONSTRUCTION':
			self.round_manager.receive_move(Move.CONSTRUCTION, a_move)

	def __update_gui(self, move_type: Move = None) -> None:
		self.update_gui_local_pack()
		self.__update_gui_players_names()
		self.update_gui_players_score()
			
	
	def update_gui_players_score(self):
		local_score = self.round_manager.local_player.score
		remote_score = self.round_manager.remote_player.score
		print(local_score)
		self.scores['remote'].configure(text=f'{str(remote_score)}')
		self.scores['local'].configure(text=f'{str(local_score)}')

	# def update_gui_board_position(self, coord: tuple, letter: str):
	# 	new_image = self.__images['CARDS'](letter, self.board_size/self.board_side)
	# 	self.board_positions[coord[0]][coord[1]].configure(image=new_image)
	# 	self.board_positions[coord[0]][coord[1]].image = new_image


	def update_gui_board_positions(self, coords_letters: dict):
		for coord, letter in coords_letters.items():
			if letter == 'TW':
				new_image = self.__images['POSITIONS']['TW']
			elif letter == 'DW':
				new_image = self.__images['POSITIONS']['DW']
			elif letter == 'DL':
				new_image = self.__images['POSITIONS']['DL']
			elif letter == 'TL':
				new_image = self.__images['POSITIONS']['TL']
			elif letter == '*':
				new_image = self.__images['POSITIONS']['*']
			elif letter == 'NORMAL':
				new_image = self.__images['POSITIONS']['NORMAL']
			else:
				new_image = self.__images['CARDS'][letter]

			self.board_positions[coord[0]][coord[1]].configure(image=new_image)
			self.board_positions[coord[0]][coord[1]].image = new_image

		
	def update_gui_local_pack(self, indexes_letters : dict = None):
		#TODO Fazer uma otimização aqui: Por que atualizar tudo se apenas 2 letras mudarem?
		if indexes_letters:
			for index, letter in indexes_letters.items():
				new_image = self.__images['CARDS'][letter] if letter != 'NORMAL' else self.__images['POSITIONS']['NORMAL']
				self.local_pack_cards[index].configure(image=new_image)
				self.local_pack_cards[index].image = new_image
				self.local_pack_cards[index].id = f'local({index}, NORMAL)'
				self.mark_off_card(index)
		else:
			for index, card in enumerate(self.round_manager.local_player.pack.cards):
				letter = ''
				if card:
					letter = f'{card.letter}'
					new_image = self.__images['CARDS'][f'{card.letter}']
				else:
					letter = 'NORMAL'
					new_image = self.__images['POSITIONS']['NORMAL']
				self.local_pack_cards[index].configure(image=new_image)
				self.local_pack_cards[index].image = new_image
				self.local_pack_cards[index].id = f'local({index}, {letter})'
	
	# def exchange_cards(self, board_coordinates: 'list(tuple)', pack_indexes: 'list(int)') -> None:

		# if len(board_coordinates) <= len(pack_indexes):
		# 	print('Exchanging cards on PlayerInterface')
		# 	print(board_coordinates)
		# 	for index, coord in enumerate(board_coordinates):
		# 		print(f'coord = ({coord[0]}, {coord[1]}) para index = {pack_indexes[index]}')
		# 		pack_label_image = self.local_pack_cards[pack_indexes[index]].image
		# 		board_label_image = self.board_positions[coord[0]][coord[1]].image
		# 		print(f'image {pack_label_image} para {board_label_image}')
		# 		self.local_pack_cards[pack_indexes[index]].configure(image=board_label_image)
		# 		self.local_pack_cards[pack_indexes[index]].image = board_label_image
		# 		self.board_positions[coord[0]][coord[1]].configure(image=pack_label_image)
		# 		self.board_positions[coord[0]][coord[1]].image = pack_label_image
		# else:
		# 	for i, pack_index in enumerate(pack_indexes):
		# 		print(f'{self.local_pack_cards[pack_index].cget("image")}')


	def mark_card(self, index: int) -> None:
		"""
		Just change the color of the background of the Label in local pack
		"""
		self.local_pack_cards[index].configure(bg=f'red')
		

	def mark_off_card(self, index: int) -> None:
		self.local_pack_cards[index].configure(bg=f'green')


	def mark_change_button(self) -> None:
		"""
		Just change the color of the background of the button
		"""
		self.buttons['button(change)']['btn_object'].configure(bg="#a0a0a0")
		

	def mark_off_change_button(self) -> None:
		"""
		Just change the color of the background of the button
		"""
		self.buttons['button(change)']['btn_object'].configure(bg="#d9d9d9")
		
	
	def __update_gui_players_names(self):
		self.label_remote_player.configure(text=f'{self.round_manager.remote_player.name}') 
		self.label_local_player.configure(text=f'{self.round_manager.local_player.name}')


	def __status_response_to_dict(self, response: list):
		dict = {'local': 
					{'id': response[0][1],
					'name': response[0][0],
					'turn': True if response[0][2] == '1' else False},
				'remote':
					{'id': response[1][1],
					'name': response[1][0],
					'turn': True if response[1][2] == '1' else False}
				}
		return dict


	def select_board_position(self, event) -> None:
		"""
		Method to handle with selected board position
		Calls RoundManager.select_board_position(coordinates)

		:param event: event generxated by click in position
		"""
		try:
			label_name = event.widget.winfo_name()

			coord_list = label_name.replace('(', '').replace(')', '').replace('board', '').split(',')
			coord_tuple = (int(coord_list[0]), int(coord_list[1]))

			self.round_manager.select_board_position(coord_tuple)

		except Exception as e:
			self.show_message("ERRO", f'Erro ao selecionar posição do tabuleiro -> {e}')


	#Receiving game's start from DOG
	def receive_start(self, start_status: StartStatus) -> None:
		#self.reset_game()
		players_response = start_status.get_players()
		players = self.__status_response_to_dict(players_response)
		self.round_manager.configure_players(players)
	
		if players['local']['turn']:
			#TODO tratar aqui, as vezes nenhum jogador fica com a vez
			self.round_manager.local_player.toogle_turn()
			self.round_manager.match_state = State.IN_PROGRESS
		else:
			self.round_manager.remote_player.toogle_turn()
			self.round_manager.match_state = State.WAITING_REMOTE_MOVE

		# self.round_manager.start_game(players)
		message = start_status.get_message()

		self.show_message(title='Mensagem do DOG', message=message)

	def select_card_from_pack(self, event) -> None:
		pack_index = f"{str(event.widget.id).replace('local(', '')[0]}"
		try:
			self.round_manager.select_card_from_pack(int(pack_index))
		except Exception as e:
			self.show_message("ERRO", f'Erro ao selecionar letra -> {e}')

	def reset_game(self) -> None:
		self.round_manager.reset_game()
		self.__update_gui()
		self.__draw_board(self.board_size/self.board_side, self.board_side)
		self.show_message("RESET GAME", f'O jogo foi resetado! Para jogar um novo jogo, clique em START GAME')
	
	def receive_withdrawal_notification(self):
		self.round_manager.receive_withdrawal_notification()