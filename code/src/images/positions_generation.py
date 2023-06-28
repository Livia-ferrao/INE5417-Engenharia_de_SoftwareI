from PIL import Image, ImageDraw, ImageFont
import sys

sys.path.insert(1, '../../constants')

from positions import POSITIONS_RGB

#Path to save the positions
PATH = 'positions'

# Define constants for the size and layout of the position
POSITION_WIDTH = 100
POSITION_HEIGHT = 100
BORDER_WIDTH = 1
LETTER_SIZE = 50
LETTER_FONT = ImageFont.truetype('../fonts/Roboto-Medium.ttf', LETTER_SIZE)

# Define the colors for the position background and border
POSITION_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)

# Define a function to draw a position for a given description
def draw_position(pos_desc: str) -> None:
    # Create a new image for the position
    position_color = POSITIONS_RGB[pos_desc]

    position = Image.new('RGB', (POSITION_WIDTH, POSITION_HEIGHT), position_color)
    
    draw = ImageDraw.Draw(position)
    
    # Draw the description in the center of the position
    if (pos_desc != 'NORMAL'):
        letter_width, letter_height = draw.textsize(pos_desc, font=LETTER_FONT)
        x = (POSITION_WIDTH - letter_width) / 2
        y = (POSITION_HEIGHT - letter_height) / 2
        draw.text((x, y), pos_desc, fill=BORDER_COLOR, font=LETTER_FONT)
    
    # Draw a border around the position
    # draw.rectangle((0, 0, POSITION_WIDTH, POSITION_HEIGHT), outline=BORDER_COLOR, width=BORDER_WIDTH)
    
    filename = f'scrabble_{pos_desc}.png'
    position.save(f'{PATH}/{filename}')
    print(f'File {PATH}/{filename} saved')

    # return position

for description in POSITIONS_RGB.keys():
    card = draw_position(description)
