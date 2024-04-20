
import pygame
import random



pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Funkcje pomocnicze
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, BLACK, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

def draw_board(board):
    for y, row in enumerate(board):
        for x, color in enumerate(row):
            if color:
                draw_block(x, y, color)

def new_piece():
    return {
        'shape': random.choice(shapes),
        'rotation': random.randint(0, 3),
        'x': BOARD_WIDTH // 2 - 1,
        'y': 0
    }

def is_valid_position(board, piece):
    if piece['rotation'] >= len(piece['shape'].shapes):
        piece['rotation'] = 0
    shape = piece['shape'].shapes[piece['rotation']] 
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and (piece['y'] + y >= BOARD_HEIGHT or piece['x'] + x < 0 or piece['x'] + x >= BOARD_WIDTH or board[piece['y'] + y][piece['x'] + x]):
                return False
    return True




def merge_piece(board, piece):
    shape = piece['shape'].shapes[piece['rotation']] 
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[piece['y'] + y][piece['x'] + x] = piece['shape'].color


# Kształty klocków
class Shape:
    def __init__(self, shapes, color):
        self.shapes = shapes
        self.color = color

shapes = [
    Shape([[[1, 1, 1, 1]]], (255, 0, 0)),    # I
    Shape([[[0, 1, 0], [1, 1, 1]], [[0, 1], [1, 1], [0, 1]], [[0, 1, 0], [1, 1, 1], [0, 1]], [[1, 0], [1, 1], [1, 0]]], (0, 255, 0)),   # T
    Shape([[[1, 0], [1, 0], [1, 1]], [[1, 1, 1], [0, 0, 1]], [[1, 1], [1, 0], [1, 0]], [[0, 0, 1], [1, 1, 1]]], (0, 0, 255)),   # J
    Shape([[[1, 1], [1, 0], [1, 0]], [[1, 1, 1], [0, 0, 1]], [[1, 0], [1, 0], [1, 1]], [[0, 0, 1], [1, 1, 1]]], (255, 255, 0)), # L
    Shape([[[1, 1], [1, 1]]], (255, 0, 255)),   # O
    Shape([[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]], (0, 255, 255)), # Z
    Shape([[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]], (255, 140, 0))  # S
]


# Główna pętla gry
def main():
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    piece = new_piece()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece['x'] -= 1
                    if not is_valid_position(board, piece):
                        piece['x'] += 1
                elif event.key == pygame.K_RIGHT:
                    piece['x'] += 1
                    if not is_valid_position(board, piece):
                        piece['x'] -= 1
                elif event.key == pygame.K_DOWN:
                    piece['y'] += 1
                    if not is_valid_position(board, piece):
                        piece['y'] -= 1
                elif event.key == pygame.K_UP:
                    piece['rotation'] = (piece['rotation'] + 1) % len(piece['shape'].shapes)
                    if not is_valid_position(board, piece):
                        piece['rotation'] = (piece['rotation'] - 1) % len(piece['shape'].shapes)

        piece['y'] += 1
        if not is_valid_position(board, piece):
            piece['y'] -= 1
            merge_piece(board, piece)
            piece = new_piece()
            if not is_valid_position(board, piece):
                game_over = True

        screen.fill(WHITE)
        draw_board(board)
        shape = piece['shape'].shapes[piece['rotation']]  
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    draw_block(piece['x'] + x, piece['y'] + y, piece['shape'].color)

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()


if __name__ == "__main__":
    main()


