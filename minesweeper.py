import sys
import pygame

from settings import Settings
from grid import Grid
from counter import Counter
from smile_button import SmileButton
from win_dialog import WinDialog

class Minesweeper:
    """Class to initialize and run game components"""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, 
                                               self.settings.screen_height))
        pygame.display.set_caption("Minesweeper")
        #pygame.display.set_icon("images/")
        self.clock = pygame.time.Clock()
        self.running = 0
        self.dead = 0
        self.win = 0

    def start_game(self):
        """Instatiate all the objects"""
        self.counter = Counter(self)
        self.grid = Grid(self)
        self.smile_button = SmileButton(self)
        self.win_dialog = WinDialog(self)

    def run_game(self):
        """Main game loop for checking events and creating disaplays"""
        self.running = 1
        while self.running == 1:
            self.check_events()
            self.screen.fill(self.settings.color)

            self.counter.draw_counter()
            self.grid.draw_grid()
            self.smile_button.draw_smile()
            if self.win == 1:
                self.win_dialog.draw_dialog()

            pygame.display.flip()
            self.clock.tick(60)

    def check_events(self):
        """Check for mouse/keyboard events and run object's update functions"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        if self.dead != 1:
            self.grid.cells.update(events)

        win_return = self.win_dialog.update(events)
        if (self.smile_button.update(events) == 1 or
                win_return == 1):
            print("RESTARTING GAME")
            self.running = 0
            self.dead = 0
            self.win = 0
            self.win_dialog.setTime(0)

        if win_return == 2:
            self.win = 0
            self.win_dialog.setTime(0)

    def generate(self, ignore_id):
        self.grid.generate_grid(ignore_id)

    def clear_adjacent(self, index):
        self.grid.clear_adjacent(index)

    def game_over(self, mine_index):
        self.dead = 1
        self.grid.show_mines(mine_index)

    def check_win(self):
        win_status = self.grid.check_win()
        if win_status == 1:
            self.dead = 1
            self.win = 1
            self.win_dialog.setTime()


if __name__=='__main__':
    ms=Minesweeper()
    while True:
        ms.start_game()
        ms.run_game()