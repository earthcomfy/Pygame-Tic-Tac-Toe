import sys
import pygame


# Define some constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
LINE_WIDTH = 10
RADIUS = 60
O_WIDTH = 15
X_WIDTH = 20
SPACE = 55

# RGB colors
LINE_COLOR = (255, 255, 255)
X_COLOR = (0, 100, 0)
O_COLOR = (255, 165, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Global variables
turn = 'X'
winner = None
draw = False
count = 0

# 3x3 board of TicTacToe game
board = [[None] * 3, [None] * 3, [None] * 3]

# Initializing pygame window
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Welcome to Tic Tac Toe")


def draw_line():
    """
        pygame.draw.line :
        1st parameter - the screen to draw the line on
        2nd parameter - the color of the line
        3rd parameter - starting coordinate of the line
        4th parameter - ending coordinate of the line
        5th parameter - width of the line
    """

    # THE HORIZONTAL LINES
    pygame.draw.line(screen, LINE_COLOR, (0, SCREEN_HEIGHT / 3), (SCREEN_WIDTH, SCREEN_HEIGHT / 3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, SCREEN_HEIGHT / 3 * 2), (SCREEN_WIDTH, SCREEN_HEIGHT / 3 * 2), LINE_WIDTH)

    # THE VERTICAL LINES
    pygame.draw.line(screen, LINE_COLOR, (SCREEN_WIDTH / 3, 0), (SCREEN_WIDTH / 3, SCREEN_HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SCREEN_WIDTH / 3 * 2, 0), (SCREEN_WIDTH / 3 * 2, SCREEN_HEIGHT), LINE_WIDTH)


def display_message(msg):
    # create a font object.
    font = pygame.font.Font('freesansbold.ttf', 30)

    # create a text surface object, on which text is drawn on it.
    text = font.render(msg, True, (0, 0, 255), (216, 191, 216))

    # create a rectangular object for the text surface object
    text_rect = text.get_rect()

    # set the center of the rectangular object.
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # draw text on to the rectangular object
    screen.blit(text, text_rect)

    pygame.display.update()


def create_screen():
    # Fill the background with white
    # screen.fill() accepts either a list or tuple specifying the RGB values for the color
    screen.fill(BLACK)

    # call function to draw lines on the screen
    draw_line()


def draw_xo():
    global board
    for i in range(len(board)):
        for j in range(len(board[i])):
            # Draw a circle for O's turn
            if board[i][j] == 'O':
                pygame.draw.circle(screen, O_COLOR, (j * 200 + 100, i * 200 + 100), RADIUS, O_WIDTH)

            # Draw a cross for X's turn
            elif board[i][j] == 'X':
                # left to right diagonal
                pygame.draw.line(screen, X_COLOR,
                                 (j * 200 + SPACE, i * 200 + 200 - SPACE),
                                 (j * 200 + 200 - SPACE, i * 200 + SPACE), X_WIDTH)

                # right to left diagonal
                pygame.draw.line(screen, X_COLOR, (j * 200 + SPACE, i * 200 + SPACE),
                                 (j * 200 + 200 - SPACE, i * 200 + 200 - SPACE), X_WIDTH)


def who_won(xo):
    if xo == 'X':
        return X_COLOR
    elif xo == 'O':
        return O_COLOR


def check_winner():
    global board, winner, count, draw

    # Winning rows / draw horizontal line
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2]) and (board[i][0] is not None):
            winner = board[i][0]
            color = who_won(str(winner))
            pygame.draw.line(screen, color, (15, i * 200 + 100),
                             (SCREEN_WIDTH - 15, i * 200 + 100), 20)
            break

    # Winning columns / draw vertical line
    for j in range(3):
        if (board[0][j] == board[1][j] == board[2][j]) and (board[0][j] is not None):
            winner = board[0][j]
            color = who_won(str(winner))
            pygame.draw.line(screen, color, (j * 200 + 100, 15),
                             (j * 200 + 100, SCREEN_HEIGHT - 15), 20)
            break

    # Winning diagonal / upper left to bottom right
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        color = who_won(str(winner))
        pygame.draw.line(screen, color, (40, 40), (SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40), 20)

    # Winning diagonal / upper right to bottom left
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = board[0][2]
        color = who_won(str(winner))
        pygame.draw.line(screen, color, (SCREEN_WIDTH - 40, 40), (40, SCREEN_HEIGHT - 40), 20)

    # All cells are filled without a winner, so it's a tie
    if count == 9 and winner is None:
        draw = True


def game_status():
    # draw XO on the screen
    draw_xo()

    # Check whether or not we have a winner
    check_winner()

    # Print who won
    if winner is not None:
        message = f'Winner is {winner} Press r to restart the game'
        display_message(message)

    # Restart the game if it's a draw
    if draw:
        message = 'It is a tie. Press r to restart the game'
        display_message(message)


def fill_in_available_pos(row, col):
    global board, turn, count

    # fill in X or O only if the cell is empty
    # and also flip between each player's turn
    if board[row][col] is None:
        if turn == 'X':
            board[row][col] = turn
            turn = 'O'

        elif turn == 'O':
            board[row][col] = turn
            turn = 'X'

        # Keep track of how many cells in the board have been filled
        count += 1

        # Keep track of who won or check if it's a tie
        game_status()


def restart():
    global turn, winner, board, draw, count

    # Create a screen and reset all variables
    create_screen()
    turn = 'X'
    winner = None
    draw = False
    count = 0
    board = [[None] * 3, [None] * 3, [None] * 3]


create_screen()


def main():
    # Main loop
    while True:
        # Check if the user clicked the window close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and winner is None:
                # Get the coordinate of mouse click
                x, y = pygame.mouse.get_pos()

                # Now we need to return which row/column of the board the user clicked on
                row = y // 200
                col = x // 200

                fill_in_available_pos(row, col)

            # Restart the game at any time when r is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()

        pygame.display.update()


if __name__ == '__main__':
    main()
