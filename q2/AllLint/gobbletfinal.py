import sys
import pygame

"""
Gobblet Jr. (3x3) game implementation using Pygame.
"""

# --------------------------------------------------------------------------------
# GLOBALS
# --------------------------------------------------------------------------------

SCREEN_WIDTH = 800  # Increased width to provide more space
SCREEN_HEIGHT = 600
CELL_SIZE = 150  # Each cell is 150x150 pixels
BOARD_OFFSET_X = 200  # Adjusted offset to center board horizontally with new width
BOARD_OFFSET_Y = 100  # Increased offset to create space for the text

# Colors for drawing
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED_COLOR = (206, 116, 90)  # #CE745A
GREEN_COLOR = (210, 229, 210)  # #D2E5D2
GREEN = (50, 200, 50)

# Board is 3x3
ROWS = 3
COLS = 3

pygame.init()
pygame.display.set_caption("Gobblet Jr. (3x3)")

# --------------------------------------------------------------------------------
# DATA STRUCTURES
# --------------------------------------------------------------------------------

class Piece:
    """
    Represents a single piece with a color and size.
      color: 'red' or 'green'
      size: 0 = small, 1 = medium, 2 = large
    """
    def __init__(self, color, size):
        self.color = color
        self.size = size
        self.dragging = False
        self.rect = pygame.Rect(0, 0, 40, 40)
        # We'll adjust rect size visually based on piece size.

    def draw(self, surface, pos):
        """
        Draw the piece on the given surface at position `pos` (center).
        """
        if self.color == 'red':
            c = RED_COLOR
        else:
            c = GREEN_COLOR

        # Adjust radius based on size
        radius_map = {0: 20, 1: 30, 2: 40}
        radius = radius_map[self.size]

        pygame.draw.circle(surface, c, pos, radius)

class GameState:
    """
    Holds the entire state of the 3x3 Gobblet Jr. game:
      - board: a 3x3 array (list of lists), where each cell is a list of pieces (bottom->top).
      - next_player: 'red' or 'green' to indicate whose turn it is.
      - off_board_pieces: dictionary tracking how many pieces each player has left off the board
        e.g. off_board_pieces['red'] = {0:2, 1:2, 2:2} for small=2, med=2, large=2
    """
    def __init__(self):
        # 3x3 board; each cell is a stack (list) of pieces bottom->top
        self.board = [[[] for _ in range(COLS)] for _ in range(ROWS)]
        self.next_player = 'red'
        self.game_over = False
        self.winner = None

        # 2 small, 2 medium, 2 large for each color
        self.off_board_pieces = {
            'red': {0: 2, 1: 2, 2: 2},
            'green': {0: 2, 1: 2, 2: 2}
        }

        self.off_board_positions = {
            'red': {0: [], 1: [], 2: []},
            'green': {0: [], 1: [], 2: []}
        }

    def switch_player(self):
        if self.next_player == 'red':
            self.next_player = 'green'
        else:
            self.next_player = 'red'

    def cell_coords_to_index(self, x, y):
        """
        Convert (mouse_x, mouse_y) in screen coords to board cell (row, col) index.
        Returns (row, col) or None if out of bounds.
        """
        # Subtract offset
        board_x = x - BOARD_OFFSET_X
        board_y = y - BOARD_OFFSET_Y

        if 0 <= board_x < (CELL_SIZE * COLS) and 0 <= board_y < (CELL_SIZE * ROWS):
            col = board_x // CELL_SIZE
            row = board_y // CELL_SIZE
            return (int(row), int(col))
        return None

    def top_piece_at(self, row, col):
        """
        Return the top piece at board[row][col], or None if empty.
        """
        stack = self.board[row][col]
        return stack[-1] if stack else None

    def place_piece(self, piece, dest_row, dest_col):
        """
        Place or move the piece onto the cell. We assume the move is valid.
        """
        # Gobbling check: can only place on top if top piece is smaller
        top = self.top_piece_at(dest_row, dest_col)
        if top is None or top.size < piece.size:
            # Place it
            self.board[dest_row][dest_col].append(piece)
            return True
        # If there's a top piece of same or bigger size, invalid
        return False

    def remove_top_piece(self, row, col):
        """
        Remove and return the top piece from the board cell.
        """
        if self.board[row][col]:
            return self.board[row][col].pop()
        return None

    def has_three_in_a_row(self, color):
        """
        Check if `color` has 3 in a row among visible (top) pieces.
        Return True if so, else False.
        """
        # We can check each row, column, diagonal for 3 in a row
        # but we must only consider the topmost piece in each cell.
        visible = [[None for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                top = self.top_piece_at(r, c)
                if top is not None:
                    visible[r][c] = (top.color, top.size)
                else:
                    visible[r][c] = None

        # Check rows
        for r in range(ROWS):
            if (visible[r][0] is not None and
                visible[r][1] is not None and
                visible[r][2] is not None):
                if (visible[r][0][0] == color and
                    visible[r][1][0] == color and
                    visible[r][2][0] == color):
                    return True

        # Check cols
        for c in range(COLS):
            if (visible[0][c] is not None and
                visible[1][c] is not None and
                visible[2][c] is not None):
                if (visible[0][c][0] == color and
                    visible[1][c][0] == color and
                    visible[2][c][0] == color):
                    return True

        # Check diagonals
        # Main diagonal
        if (visible[0][0] is not None and
            visible[1][1] is not None and
            visible[2][2] is not None):
            if (visible[0][0][0] == color and
                visible[1][1][0] == color and
                visible[2][2][0] == color):
                return True

        # Anti-diagonal
        if (visible[0][2] is not None and
            visible[1][1] is not None and
            visible[2][0] is not None):
            if (visible[0][2][0] == color and
                visible[1][1][0] == color and
                visible[2][0][0] == color):
                return True

        return False

    def check_exposed_opponent_win(self, removed_row, removed_col, placed_row, 
                                   placed_col, moving_color):
        """
        If removing a piece from (removed_row, removed_col) exposes a 3-in-a-row for the opponent,
        and the new placement at (placed_row, placed_col) does not cover that 3-in-a-row,
        then the opponent wins immediately.

        Return the winning color if there's an immediate forced win, else None.
        """
        # The opponent color
        opponent = 'green' if moving_color == 'red' else 'red'

        # After you remove the piece (which has presumably happened),
        # check if opponent has 3 in a row now.
        if self.has_three_in_a_row(opponent):
            # The only way to avoid losing immediately is if your new placement
            # covers one of the cells in that new three-in-a-row.
            # We'll do a second check: revert the newly placed piece, check if
            # opponent still has 3 in a row, etc. If so, you lose.
            # This is a simplified approach. A more thorough approach would find
            # the exact 3-in-a-row that formed, but here we simply do a second pass
            # where we remove the newly placed piece and see if the opponent
            # still has 3 in a row.

            # Temporarily remove the newly placed piece
            new_piece = self.remove_top_piece(placed_row, placed_col)
            if self.has_three_in_a_row(opponent):
                # That means your covering did not break the opponent's 3 in a row
                # => immediate loss
                # Put the piece back
                self.board[placed_row][placed_col].append(new_piece)
                return opponent
            # else:
            #     # If removing your newly placed piece re-exposes the 3 in a row,
            #     # but with your piece there it doesn't exist, you are safe.
            #     # Put the piece back
            #     self.board[placed_row][placed_col].append(new_piece)

        return None

    def check_for_winner(self):
        """
        After a valid move, check if current player (or forced opponent scenario) has won.
        """
        # Check if the current player has 3 in a row
        if self.has_three_in_a_row(self.next_player):
            self.game_over = True
            self.winner = self.next_player

    def draw_board(self, surface):
        # Draw the 3x3 grid lines
        for row in range(ROWS + 1):
            pygame.draw.line(surface, BLACK,
                             (BOARD_OFFSET_X, BOARD_OFFSET_Y + row * CELL_SIZE),
                             (BOARD_OFFSET_X + COLS * CELL_SIZE, BOARD_OFFSET_Y + row * CELL_SIZE),
                             2)
        for col in range(COLS + 1):
            pygame.draw.line(surface, BLACK,
                             (BOARD_OFFSET_X + col * CELL_SIZE, BOARD_OFFSET_Y),
                             (BOARD_OFFSET_X + col * CELL_SIZE, BOARD_OFFSET_Y + ROWS * CELL_SIZE),
                             2)

        # Draw pieces on the board
        for r in range(ROWS):
            for c in range(COLS):
                stack = self.board[r][c]
                if stack:
                    # Draw only the top piece as visible
                    top_piece = stack[-1]
                    center_x = BOARD_OFFSET_X + c * CELL_SIZE + CELL_SIZE // 2
                    center_y = BOARD_OFFSET_Y + r * CELL_SIZE + CELL_SIZE // 2
                    top_piece.draw(surface, (center_x, center_y))

    def draw_off_board_pieces(self, surface):
        """
        Draw placeholders for off-board pieces (so players can click/drag them).
        We'll arrange them along the left side for Red and right side for green, for example.
        """
        # Off-board for red on left
        # Off-board for green on right
        start_x_red = 50  # Adjusted to provide more space
        start_y_red = 50
        start_x_green = SCREEN_WIDTH - 100  # Adjusted to provide more space
        start_y_green = 50
        gap = 80  # Increased gap

        self.off_board_positions['red'] = {0: [], 1: [], 2: []}
        self.off_board_positions['green'] = {0: [], 1: [], 2: []}

        # We'll just draw circles representing off-board slots
        for size in [2, 1, 0]:  # largest to smallest
            count_red = self.off_board_pieces['red'][size]
            for i in range(count_red):
                # Create a temporary Piece for rendering
                p = Piece('red', size)
                p.draw(surface, (start_x_red, start_y_red))
                radius_map = {0: 20, 1: 30, 2: 40}
                r = radius_map[size]
                rect = pygame.Rect(start_x_red - r, start_y_red - r, 2*r, 2*r)
                self.off_board_positions['red'][size].append(rect)
                start_y_red += gap

        for size in [2, 1, 0]:
            count_green = self.off_board_pieces['green'][size]
            for i in range(count_green):
                p = Piece('green', size)
                p.draw(surface, (start_x_green, start_y_green))
                r = radius_map[size]
                rect = pygame.Rect(start_x_green - r, start_y_green - r, 2*r, 2*r)
                self.off_board_positions['green'][size].append(rect)
                start_y_green += gap

    def print_debug(self):
        """
        Print a small text status if you like debugging in the console.
        """
        pass

# --------------------------------------------------------------------------------
# MAIN GAME LOOP & HELPER FUNCTIONS
# --------------------------------------------------------------------------------

def draw_button(surface, text, rect, color):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    font = pygame.font.SysFont(None, 30)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = GameState()

    dragged_piece = None
    origin_cell = None  # (row, col) from which the piece was lifted, or None if from off-board
    piece_start_pos = (0, 0)  # so we can track the drag offset

    font = pygame.font.SysFont(None, 30)
    restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)
    button_color = (100, 149, 237)  # Cornflower Blue

    while True:
        clock.tick(30)  # Limit to 30 FPS
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button_rect.collidepoint(event.pos):
                        game = GameState()  # Restart the game
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    mx, my = event.pos
                    # Check if user clicked a top piece on the board
                    cell_idx = game.cell_coords_to_index(mx, my)
                    if cell_idx is not None:
                        top = game.top_piece_at(cell_idx[0], cell_idx[1])
                        if top is not None and top.color == game.next_player:
                            # This piece can be dragged
                            dragged_piece = top
                            origin_cell = cell_idx
                            piece_start_pos = (mx, my)
                            # We remove it from the board so it can "follow the mouse"
                            game.board[cell_idx[0]][cell_idx[1]].pop()
                    else:
                        # Check exact click on off-board pieces
                        color = game.next_player
                        for size, rects in game.off_board_positions[color].items():
                            for rct in rects:
                                if rct.collidepoint(mx, my):
                                    if game.off_board_pieces[color][size] > 0:
                                        dragged_piece = Piece(color, size)
                                        origin_cell = None
                                        piece_start_pos = (mx, my)
                                        game.off_board_pieces[color][size] -= 1
                                    break
                            else:
                                continue
                            break

            elif event.type == pygame.MOUSEMOTION:
                if dragged_piece:
                    # Just track piece center with mouse
                    pass

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragged_piece:
                    mx, my = event.pos
                    dest_idx = game.cell_coords_to_index(mx, my)

                    # We will attempt to place the dragged piece
                    if dest_idx is not None:
                        dest_row, dest_col = dest_idx
                        # If the piece was on the board, remember where it came from
                        old_row, old_col = origin_cell if origin_cell else (None, None)

                        # If we moved from the board, remove the piece from that old cell
                        # (already removed above). Check if removing it exposes an
                        # opponent 3-in-a-row. If so, we might have to see if the new placement
                        # is blocking it.
                        forced_opponent_win = None
                        if origin_cell is not None:
                            forced_opponent_win = game.check_exposed_opponent_win(
                                old_row, old_col, dest_row, dest_col, dragged_piece.color
                            )

                        if forced_opponent_win:
                            # The move automatically loses
                            game.game_over = True
                            game.winner = forced_opponent_win
                            # The piece does not actually land. We'll just discard it.
                            # Return the piece to its old stack if we want to keep board consistent,
                            # or do nothing if we declare game ended.
                            # Let's put it back for consistency:
                            game.board[old_row][old_col].append(dragged_piece)
                        else:
                            # Attempt to place on new cell
                            if game.place_piece(dragged_piece, dest_row, dest_col):
                                # Successfully placed
                                # Now check if current player formed a 3 in a row
                                game.check_for_winner()
                                if not game.game_over:
                                    # Switch turn
                                    game.switch_player()
                            else:
                                # Invalid move because top piece is same or bigger
                                # Return the piece to old cell or off-board
                                if origin_cell is not None:
                                    game.board[origin_cell[0]][origin_cell[1]].append(dragged_piece)
                                else:
                                    # Return to off-board
                                    game.off_board_pieces[dragged_piece.color][dragged_piece.size] += 1
                        # Reset
                    else:
                        # Dropped outside the board, revert
                        if origin_cell is not None:
                            game.board[origin_cell[0]][origin_cell[1]].append(dragged_piece)
                        else:
                            # Return to off-board
                            game.off_board_pieces[dragged_piece.color][dragged_piece.size] += 1

                    dragged_piece = None
                    origin_cell = None

        # Draw everything
        game.draw_board(screen)
        game.draw_off_board_pieces(screen)

        if dragged_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Draw the dragged piece following the mouse
            dragged_piece.draw(screen, (mouse_x, mouse_y))

        # Show text info
        if game.game_over:
            msg = f"Game Over! Winner: {game.winner.upper()}"
            text_surf = font.render(msg, True, BLACK)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2,
                                                   10 + text_surf.get_height() // 2))
            screen.blit(text_surf, text_rect)
            draw_button(screen, "Restart", restart_button_rect, button_color)
        else:
            msg = f"Next Player: {game.next_player.upper()}"
            text_surf = font.render(msg, True, BLACK)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2,
                                                   10 + text_surf.get_height() // 2))
            screen.blit(text_surf, text_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()
