import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(1, '../../constants')

from cards import CARDS_VALUES_BY_LETTER

#Path to save the cards
PATH = 'cards'

# Define constants for the size and layout of the card
CARD_WIDTH = 100
CARD_HEIGHT = 100
BORDER_WIDTH = 2
CARD_TO_BOARD_SPACING = 2
LETTER_SIZE = 70
VALUE_SIZE = 30
LETTER_FONT = ImageFont.truetype('../fonts/Roboto-Medium.ttf', LETTER_SIZE)
VALUE_FONT = ImageFont.truetype('../fonts/Roboto-Medium.ttf', VALUE_SIZE)

# Define the colors for the card background and border
CARD_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)

# Define a function to draw a card for a given letter and its point value
def draw_card(letter: str, value: int) -> None:
    # Create a new image for the card
    card = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), CARD_COLOR)
    
    # Draw the letter in the center of the card
    draw = ImageDraw.Draw(card)
    letter_width, letter_height = draw.textsize(letter, font=LETTER_FONT)
    x = (CARD_WIDTH - letter_width) / 2
    y = (CARD_HEIGHT - letter_height) / 2
    draw.text((x, y), letter, fill=BORDER_COLOR, font=LETTER_FONT)
    
    # Draw the point value in the bottom right corner of the card
    value_text = str(value)
    value_width, value_height = draw.textsize(value_text, font=VALUE_FONT)
    x = CARD_WIDTH - value_width - BORDER_WIDTH - CARD_TO_BOARD_SPACING
    y = CARD_HEIGHT - value_height - BORDER_WIDTH - CARD_TO_BOARD_SPACING
    draw.text((x, y), value_text, fill=BORDER_COLOR, font=VALUE_FONT)
    
    # Draw a border around the card
    draw.rectangle((0, 0, CARD_WIDTH - 1, CARD_HEIGHT - 1), outline=BORDER_COLOR, width=BORDER_WIDTH)
    
    filename = f'scrabble_{letter}.png'
    card.save(f'{PATH}/{filename}')
    print(f'File {PATH}/{filename} saved')
    
    # return card

for letter, value in CARDS_VALUES_BY_LETTER.items():
    draw_card(letter, value)
