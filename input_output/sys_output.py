"""
In this module are methods that format the output to the terminal.
"""

# Format: \033[i;j;km
START = '\033['
END = 'm'
RESET = '\033[0;0m'
# i = style
NORMAL = '0'
BOLD = '1'
UNDERLINE = '2'
NEGATIVE1 = '3'
NEGATIVE2 = '5'
# j = font color
BLACK_FONT = '30'
RED_FONT = '31'
GREEN_FONT = '32'
YELLOW_FONT = '33'
BLUE_FONT = '34'
PURPLE_FONT = '35'
CYAN_FONT = '36'
WHITE_FONT = '37'
# k = background color
BLACK_BG = '40'
RED_BG = '41'
GREEN_BG = '42'
YELLOW_BG = '43'
BLUE_BG = '44'
PURPLE_BG = '45'
CYAN_BG = '46'
WHITE_BG= '47'

FAIL_COLOR = START + BOLD + ';' + RED_FONT + END


def fail(string):
    print(FAIL_COLOR + string + RESET)