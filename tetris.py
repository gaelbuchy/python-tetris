import sys, pygame, random

display_size = [200, 400]
board_size = [10, 20]
block_display_size = display_size[0] / board_size[0]

keys = {
    "escape": 27,
    "space": 32,
    "left": 276,
    "down": 274,
    "right": 275,
    "enter": 13
}

piece_types = [
    [[0, 1, 0],
     [1, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 1, ],
     [0, 1, 1]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]
     ],

    [[1],
     [1],
     [1],
     [1]
    ]
]

colors = {
    1: [51, 255, 51],
    2: [51, 97, 255],
    3: [255, 51, 51],
    4: [252, 255, 51],
    5: [255, 51, 255]
}

MOVEEVENT = pygame.USEREVENT + 1

class Piece:
    def __init__(self, screen):
        self.screen = screen

        # init piece type/color/position
        self.type = piece_types[random.randint(0, len(piece_types)-1)]

        self.max_x = 0
        self.max_y = 0

        color = random.randint(1, len(colors))
        self.color = colors[color]
        self.init_piece(color)

        self.position_x = int(board_size[0] / 2 - len(self.type[0]) / 2)
        self.position_y = 0

    # update value to save color + max
    def init_piece(self, color):
        for j, y in enumerate(self.type):
            for i, x in enumerate(y):
                if x:
                    self.max_x = max(self.max_x, i+1)
                    self.max_y = max(self.max_y, j+1)
                    self.type[j][i] = color

    def set_pos(self, pos):
        self.position_x = pos[0]
        self.position_y = pos[1]

    # check if piece in board bounds
    def in_bounds(self, new_x, new_y):
        min_x = new_x
        max_x = new_x + self.max_x
        min_y = new_y
        max_y = new_y + self.max_y
        if 0 <= min_x <= max_x <= board_size[0] and 0 <= min_y <= max_y <= board_size[1]:
            return True
        return False

    def collision_check(self, board, new_x=None, new_y=None):
        bottom = False
        # check if new position already occupied
        for j, y in enumerate(self.type):
            for i, x in enumerate(y):
                if x:
                    # position of the block
                    pos_x = (new_x if new_x is not None else self.position_x)+i
                    pos_y = (new_y if new_y is not None else self.position_y)+j

                    # if already something on this block:
                    # collision
                    if board[pos_y][pos_x]:
                        return True, False

                    # bottom of the board
                    if pos_y == board_size[1]-1:
                        bottom = True

        return bottom, bottom

    def draw(self):
        # draw all blocks for the piece
        for j, y in enumerate(self.type):
            for i, x in enumerate(y):
                if x:
                    pygame.draw.rect(
                        self.screen,
                        self.color,
                        pygame.Rect(
                            self.position_x*block_display_size + i*block_display_size,
                            self.position_y*block_display_size + j*block_display_size,
                            block_display_size,
                            block_display_size), 0)


class Tetris:
    def __init__(self):
        pygame.init()

        # set game state
        self.state = "game"
        self.screen = pygame.display.set_mode(display_size)

        # define current and next pieces
        self.piece = Piece(self.screen)
        self.next_piece = Piece(self.screen)

        # board size : 10x20
        self.board = [[0 for i in range(board_size[0])] for j in range(board_size[1])]

    def restart(self):
        # board size : 10x20
        self.board = [[0 for i in range(board_size[0])] for j in range(board_size[1])]
        # define current and next pieces
        self.piece = Piece(self.screen)
        self.next_piece = Piece(self.screen)

    def next(self):
        # new piece
        self.piece = self.next_piece
        self.next_piece = Piece(self.screen)

        # check if collision or bottom
        collision, bottom = self.piece.collision_check(self.board)
        if collision:
            # game over
            self.state = "gameover"

    def remove_rows(self, rows):

        # delete all rows
        for i in rows:
            del self.board[i]
        # add new rows at top
        self.board = self.board = [[0 for i in range(10)] for j in range(len(rows))] + self.board

    def add_to_board(self):
        print(self.piece.type, self.piece.position_y, self.piece.position_x)
        for y, row in enumerate(self.piece.type):
            for x, column in enumerate(row):
                if column:
                    self.board[self.piece.position_y + y][self.piece.position_x + x] = column
        self.print_board()

    def print_board(self):
        print("board::")
        for row in self.board:
            print(row)

    def move(self, direction=keys["down"]):
        # define next position based on movement type
        if direction == keys["left"]:
            new_x = self.piece.position_x - 1
            new_y = self.piece.position_y
        elif direction == keys["down"]:
            new_x = self.piece.position_x
            new_y = self.piece.position_y + 1
        else:
            new_x = self.piece.position_x + 1
            new_y = self.piece.position_y

        # check if in board bounds
        if self.piece.in_bounds(new_x, new_y):

            # check for collision
            collision, bottom = self.piece.collision_check(self.board, new_x, new_y)
            if collision:
                if bottom:
                    # update piece position
                    self.piece.set_pos([new_x, new_y])

                # add to board
                self.add_to_board()

                # check if any rows are complete
                rows_to_delete = []

                # starting from bottom
                for i in reversed(range(len(self.board))):
                    # if not 0
                    if 0 not in self.board[i]:
                        rows_to_delete.append(i)

                if rows_to_delete:
                    # delete rows if need
                    self.remove_rows(rows_to_delete)
                # self.add_cl_lines(cleared_rows)

                # add next piece
                self.next()
            else:
                # update piece positions
                self.piece.set_pos([new_x, new_y])

    def draw_board(self):
        # draw all blocks from board
        for j, y in enumerate(self.board):
            for i, x in enumerate(y):
                if x:
                    pygame.draw.rect(
                        self.screen,
                        colors[x],
                        pygame.Rect(
                            i * block_display_size,
                            j * block_display_size,
                            block_display_size,
                            block_display_size), 0)

    def run(self):

        # print("start app")

        # timer
        pygame.time.set_timer(MOVEEVENT, 1000)

        while 1:

            if self.state == "gameover":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == keys["escape"]:
                            sys.exit()
                        elif event.key == keys["enter"]:
                            self.restart()

                black = 0, 0, 0
                self.screen.fill(black)
                
                pygame.display.flip()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == MOVEEVENT:
                        self.move()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == keys["escape"]:
                            sys.exit()
                        elif event.key == keys["left"] or event.key == keys["right"] or event.key == keys["down"]:
                            self.move(event.key)
                        elif event.key == keys["space"]:
                            self.quick_drop()

                # redraw black screen
                black = 0, 0, 0

                self.screen.fill(black)

                # draw board
                self.draw_board()

                # draw curren piece
                self.piece.draw()

                # update screen
                pygame.display.flip()
