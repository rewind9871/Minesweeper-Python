import pygame
import numpy as np

from cell import Cell

class Grid:
    """Sets up the grid to hold all the squares"""

    def __init__(self, minesweeper):
        self.minesweeper = minesweeper
        self.settings = minesweeper.settings
        self.width = self.settings.grid_width
        self.height = self.settings.grid_height

        self.screen = minesweeper.screen
        self.screen_rect = minesweeper.screen.get_rect()

        self.cells = pygame.sprite.Group()
        self.cells_arr = []
        self.columns = self.settings.grid_columns
        self.rows = self.settings.grid_rows
        self.generated = 0

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        num = 0
        for column in range(self.columns):
            for row in range(self.rows):
                cell = Cell(self.minesweeper, 
                            self.rect.x+(self.settings.cell_width*column),
                            self.rect.y+(self.settings.cell_height*row),
                            num)
                num += 1
                self.cells.add(cell)
                self.cells_arr.append(cell)

        self.color = minesweeper.settings.grid_bg_color

    def draw_grid(self):
        """Draws grid background and all cells"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        for cell in self.cells:
            cell.draw_cell()

    def generate_grid(self, ignore_id):
        """Generates bomb positions and numbers for cells"""
        if self.generated == 0:
            while True:
                self.value_arr =  [-1 for _ in range(self.settings.bomb_count)]
                self.value_arr += [0 for _ in range(self.settings.grid_count-self.settings.bomb_count)]
                np.random.shuffle(self.value_arr)
                if self.value_arr[ignore_id] == -1:
                    continue

                offset = self.settings.grid_rows
                for x,y in enumerate(self.value_arr):
                    if y != -1:
                        continue
                    #adjacent_inds includes self to handle row adjacency with modulus
                    adjacent_inds = (x-offset-1,  x-offset,  x-offset+1,
                                     x-1,         x,         x+1,
                                     x+offset-1,  x+offset,  x+offset+1)
                    current_row = -2
                    for loop,ind in enumerate(adjacent_inds):
                        if loop%3 == 0:
                            current_row += 1
                        if ind < 0 or ind >= self.settings.grid_count:
                            continue
                        if self.value_arr[ind] < 0:
                            continue
                        if ind//offset != (x//offset)+current_row:
                            continue
                        self.value_arr[ind] += 1
                if self.value_arr[ignore_id] == 0:
                    break

            for num, cell in enumerate(self.cells):
                cell.update_value(self.value_arr[num])

            self.generated = 1

    def clear_adjacent(self, index):
        offset = self.settings.grid_rows
        #adjacent_inds includes self to handle row adjacency with modulus
        adjacent_inds = (index-offset-1,  index-offset,  index-offset+1,
                         index-1,         index,         index+1,
                         index+offset-1,  index+offset,  index+offset+1)
        
        current_row = -2
        for loop,ind in enumerate(adjacent_inds):
            if loop%3 == 0:
                current_row += 1
            #Skip if ajacent index is out of bounds, on a different row, itself, or already cleared
            if (ind < 0 or ind >= self.settings.grid_count or
                    ind//offset != (index//offset)+current_row or
                    ind == index or
                    self.cells_arr[ind].hidden == 1):
                continue

            self.cells_arr[ind].hidden = 1
            if self.cells_arr[ind].hidden_value == 0:
                self.clear_adjacent(ind)

    def check_win(self):
        num_cleared = 0
        for cell in self.cells_arr:
            if cell.hidden == 1:
                num_cleared += 1

        print(f"Num cleared: {num_cleared}\nBomb Count: {self.settings.bomb_count}")
        
        if num_cleared == self.settings.grid_count - self.settings.bomb_count:
            return 1
        return 0

    def show_mines(self, mine_index):
        for cell in self.cells_arr:
            if cell.hidden_value == -1 and cell.flagged == 0:
                cell.hidden = 1
                if cell.id == mine_index:
                    cell.clicked_mine = 1
            elif cell.flagged == 1 and cell.hidden_value != -1:
                cell.wrong_flag = 1
