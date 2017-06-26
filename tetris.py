import sys, pygame, random, copy, math, time

display_size = [360, 420]  # pixels
board_size = [10, 20]
board_position = [20, 0]
block_display_size = 20

walls_map = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

keys = {
    "escape": 27,
    "space": 32,
    "left": 276,
    "down": 274,
    "right": 275,
    "enter": 13,
    "r": 114
}

piece_types = [
    [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]],

    [[1, 0, 0],
     [1, 1, 1],
     [0, 0, 0]],

    [[0, 0, 1],
     [1, 1, 1],
     [0, 0, 0]],

    [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 0]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]
     ],
    [[0, 1, 0],
     [0, 1, 0],
     [0, 1, 0]
    ],
    [[1, 1],
     [1, 1],
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


def draw_block(screen, color, x, y):
    pygame.draw.rect(
        screen,
        [color[0]*.75, color[1]*.75, color[2]*.75],
        pygame.Rect(
            x + 1,
            y + 1,
            block_display_size - 2,
            block_display_size - 2), 0)

    pygame.draw.rect(
        screen,
        color,
        pygame.Rect(
            x + 5,
            y + 5,
            block_display_size - 10,
            block_display_size - 10), 0)


def draw_text(screen, text, color, x, y):
    font = pygame.font.Font('font.ttf', 20)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


class Piece:
    def __init__(self, screen):
        self.screen = screen

        # init piece type/color/position
        self.type = copy.deepcopy(piece_types[random.randint(0, len(piece_types)-1)])

        # [min_x, max_x, min_y, max_y]
        self.edges = [len(self.type[0]) - 1, 0, len(self.type) - 1, 0]

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
                    self.edges[0] = min(self.edges[0], i)
                    self.edges[2] = min(self.edges[2], j)
                    self.edges[1] = max(self.edges[1], i)
                    self.edges[3] = max(self.edges[3], j)
                    self.type[j][i] = color

    def set_pos(self, pos):
        self.position_x = pos[0]
        self.position_y = pos[1]

    # check if piece in board bounds
    def in_bounds(self, new_x=None, new_y=None, edges=None):

        if not edges:
            edges = self.edges

        min_x = (new_x if new_x is not None else self.position_x) + edges[0]
        max_x = (new_x if new_x is not None else self.position_x) + edges[1]
        min_y = (new_y if new_y is not None else self.position_y) + edges[2]
        max_y = (new_y if new_y is not None else self.position_y) + edges[3]

        if 0 <= min_x <= max_x < board_size[0] and 0 <= min_y <= max_y < board_size[1]:
            return True
        return False

    def collision_check(self, board, new_x=None, new_y=None, type=None):

        if not type:
            type = self.type

        bottom = False
        # check if new position is already occupied
        for j, y in enumerate(type):
            for i, x in enumerate(y):
                # if its a part of the block
                if x:
                    # position of the block
                    # check new position or current one
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

    def rotate(self):

        if len(self.type) < 3:
            return

        new_type = [[0 for col in self.type[0]] for row in self.type]
        max_x = 0
        max_y = 0
        min_x = len(self.type[0]) - 1
        min_y = len(self.type) - 1

        # for each block of the piece
        for y, j in enumerate(self.type):
            for x, i in enumerate(j):
                if i:

                    origin = [1, 1]

                    current_x = x - origin[0]
                    current_y = y - origin[1]

                    # rotate 90 degrees = pi/2 radians

                    new_x = current_x * int(math.cos(math.pi/2)) - current_y * int(math.sin(math.pi/2))
                    new_y = current_x * int(math.sin(math.pi/2)) + current_y * int(math.cos(math.pi/2))

                    converted_x = new_x + origin[0]
                    converted_y = new_y + origin[1]

                    min_x = min(min_x, converted_x)
                    min_y = min(min_y, converted_y)
                    max_x = max(max_x, converted_x)
                    max_y = max(max_y, converted_y)

                    new_type[converted_y][converted_x] = i
                    # self.max_x = max(self.max_x, i+1)
                    # self.max_y = max(self.max_y, j+1)
                    # self.type[j][i] = color

        return new_type, [min_x, max_x, min_y, max_y]

    def confirm_rotation(self, type, edges):
        self.type = type
        self.edges = edges

    def draw(self, next_pos=False):
        # /2 because default pos is in the middle of the board
        add_x = (board_position[0] + board_size[0]/2*block_display_size + 3*block_display_size) if next_pos else board_position[0]
        add_y = block_display_size*3 if next_pos else board_position[1]

        # draw all blocks for the piece
        for j, y in enumerate(self.type):
            for i, x in enumerate(y):
                if x:
                    draw_block(self.screen,
                               self.color,
                               add_x + self.position_x * block_display_size + i * block_display_size,
                               add_y + self.position_y * block_display_size + j * block_display_size)


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

        self.dropping = False
        self.default_timer = 1000

    def update_timer(self, time):
        pygame.time.set_timer(MOVEEVENT, time)

    def restart(self):
        # board size : 10x20
        self.board = [[0 for i in range(board_size[0])] for j in range(board_size[1])]
        # define current and next pieces
        self.piece = Piece(self.screen)
        self.next_piece = Piece(self.screen)
        self.state = "game"

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
        for y, row in enumerate(self.piece.type):
            for x, column in enumerate(row):
                if column:
                    self.board[self.piece.position_y + y][self.piece.position_x + x] = column

    def print_board(self):
        print("board::")
        for row in self.board:
            print(row)

    def move(self, direction=keys["down"]):

        down_move = False
        # define next position based on movement type
        if direction == keys["left"]:
            new_x = self.piece.position_x - 1
            new_y = self.piece.position_y
        elif direction == keys["down"]:
            new_x = self.piece.position_x
            new_y = self.piece.position_y + 1
            down_move = True
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

                if down_move:
                    # add to board
                    self.add_to_board()

                    self.cancel_drop()

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

        return 0

    def cancel_drop(self):
        if self.dropping:
            self.dropping = False
            self.update_timer(self.default_timer)

    def quick_drop(self):
        self.dropping = True
        self.update_timer(25)

    def draw_board(self):
        # draw all blocks from board
        for j, y in enumerate(self.board):
            for i, x in enumerate(y):
                if x:
                    draw_block(self.screen,
                               colors[x],
                               board_position[0] + i * block_display_size,
                               board_position[1] + j * block_display_size)

    def draw_walls(self):

        draw_text(self.screen, "NEXT", (255, 255, 255),
                  display_size[0] - (display_size[0] - (board_position[0] + board_size[0] * block_display_size))/2,
                  2 * block_display_size)

        for y, i in enumerate(walls_map):
            for x, j in enumerate(i):
                if j:
                    draw_block(self.screen,
                               [146, 146, 146],
                               x*block_display_size,
                               y*block_display_size)

        # for r in rects:
        #     # draw walls
        #     pygame.draw.rect(
        #         self.screen,
        #         ,
        #         pygame.Rect(
        #             r[0], r[1], r[2], r[3]), 0)

    def rotate(self):
        type, edges = self.piece.rotate()

        allow_rotation = False
        # check new edges
        if self.piece.in_bounds(None, None, edges):
            # check for collision
            collision, bottom = self.piece.collision_check(self.board, None, None, type)
            if not collision:
                allow_rotation = True

        if allow_rotation:
            self.piece.confirm_rotation(type, edges)

    def run(self):

        # timer
        self.update_timer(self.default_timer)

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

                draw_text(self.screen, "GAME OVER", (255, 255, 255),
                          display_size[0] / 2,
                          display_size[1] / 2)

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
                            self.cancel_drop()
                            self.move(event.key)
                        elif event.key == keys["space"]:
                            self.quick_drop()
                        elif event.key == keys["r"]:
                            self.cancel_drop()
                            self.rotate()

                # redraw black screen
                black = 0, 0, 0

                self.screen.fill(black)

                # draw walls
                self.draw_walls()

                # draw board
                self.draw_board()

                # draw current piece
                self.piece.draw()

                self.next_piece.draw(True)

                # update screen
                pygame.display.flip()
