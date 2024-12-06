import pygame
from pygame.sprite import Sprite

class Cell(Sprite):
    """Class for individual cells on grid"""

    def __init__(self, minesweeper, x, y, id):
        super().__init__()
        self.minesweeper = minesweeper
        self.settings = minesweeper.settings
        self.screen = minesweeper.screen
        self.offset=self.settings.cell_gap_offset
        self.id = id

        self.height = self.settings.cell_height
        self.width = self.settings.cell_width
        self.color = self.settings.cell_color
        self.light_color = self.settings.cell_light_color
        self.dark_color = self.settings.cell_dark_color

        self.hidden = 0
        self.flagged = 0
        self.clicked = 0
        self.clicked_mine = 0
        self.hidden_value = 0
        self.wrong_flag = 0

        self.num_colors = ["#0000FF", "#008200", "#FE0000", "#000084", "#840000", "#008284", "#840084", "#757575"]

        self.mainrect = pygame.Rect(x+self.offset, y+self.offset,
                self.width-(2*self.offset)+1, self.height-(2*self.offset)+1)
        self.gaps = [
            pygame.Rect(x, y, self.width-self.offset+1,
                        self.offset+1),
            pygame.Rect(x, y+self.offset, self.offset+1, 
                        self.height-(2*self.offset)+1),
            pygame.Rect(x+self.offset, y+self.height-self.offset, 
                        self.width-self.offset+1, self.offset+1),
            pygame.Rect(x+self.width-self.offset, y+self.offset,
                        self.offset+1, self.height-(2*self.offset)+1)
        ]
        self.triangles = [
            (
                (x+self.width-self.offset, y+self.offset),
                (x+self.width-self.offset, y),
                (x+self.width, y)
            ),
            (
                (x, y+self.height-self.offset),
                (x+self.offset, y+self.height-self.offset),
                (x, y+self.height)
            ),
            (
                (x+self.offset, y+self.height-self.offset),
                (x, y+self.height),
                (x+self.offset, y+self.height)
            ),
            (
                (x+self.width-self.offset, y+self.offset),
                (x+self.width, y),
                (x+self.width, y+self.offset)
            )
        ]
        self.x_lines = [
            (x+self.offset, y+self.offset),
            (x+self.width-self.offset, y+self.height-self.offset),
            (x+self.width-self.offset, y+self.offset),
            (x+self.offset, y+self.height-self.offset)
        ]
        self.bg_lines = [
            (x, y),
            (x+self.width, y),
            (x+self.width, y+self.height),
            (x, y+self.height),
            (x,y)
        ]

        self.flag = pygame.image.load('images/Flag.png')
        self.flag = pygame.transform.scale(self.flag, 
                (self.width-10, self.height-10))
        self.flag_rect = self.flag.get_rect()
        self.flag_rect.center = self.mainrect.center

        self.font = pygame.font.SysFont("Motion-Control", self.settings.cell_font_size)

        self.bomb = pygame.image.load("images/Bomb.png")
        self.bomb = pygame.transform.scale(self.bomb, 
                (self.width-10, self.height-10))
        self.bomb_rect = self.bomb.get_rect()
        self.bomb_rect.center = self.mainrect.center

    def draw_cell(self):
        """Draw the cell"""
        if self.hidden != 1:
            pygame.draw.rect(self.screen, self.color, self.mainrect)
            num = 0
            for gap in self.gaps:
                if self.clicked != 1 or self.flagged == 1:
                    pygame.draw.rect(self.screen, 
                        (self.light_color if num<len(self.gaps)/2 else self.dark_color),
                        gap)
                    pygame.draw.polygon(self.screen,
                        (self.light_color if num<len(self.gaps)/2 else self.dark_color),
                        self.triangles[num])
                else:
                    pygame.draw.rect(self.screen, 
                        (self.dark_color if num<len(self.gaps)/2 else self.light_color),
                        gap)
                    pygame.draw.polygon(self.screen,
                        (self.dark_color if num<len(self.gaps)/2 else self.light_color),
                        self.triangles[num])
                num += 1
        else:
            for i in range(4):
                pygame.draw.aaline(self.screen, "#757575", self.bg_lines[i], self.bg_lines[i+1])
            if self.hidden_value > -1:
                pygame.draw.rect(self.screen, self.settings.grid_bg_color, self.mainrect)
            elif self.clicked_mine == 1:
                pygame.draw.rect(self.screen, "red", self.mainrect)
            if self.hidden_value > 0:
                self.text = self.font.render(str(self.hidden_value), True, self.num_colors[self.hidden_value-1])
                self.text_rect = self.text.get_rect()
                self.text_rect.center = self.mainrect.center
                self.screen.blit(self.text, self.text_rect)
            elif self.hidden_value < 0:
                self.screen.blit(self.bomb, self.bomb_rect)
        if self.flagged == 1:
            self.screen.blit(self.flag, self.flag_rect)
        if self.wrong_flag == 1:
            for i in range(0, 3, 2):
                pygame.draw.aaline(self.screen, "black", self.x_lines[0+i], self.x_lines[1+i])


    def update(self, events):
        """Check for clicking to mark the flag or hide the cell"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_cell(event, self.mainrect)
                for gap in self.gaps:
                    self.click_cell(event, gap)
            if event.type == pygame.MOUSEBUTTONUP:
                self.hide_cell(event, self.mainrect)
                for gap in self.gaps:
                    self.hide_cell(event, gap)
                self.clicked = 0

    def hide_cell(self, event, obj):
        if (obj.collidepoint(event.pos) and 
                self.clicked == 1 and 
                self.flagged == 0):
            self.hidden = 1
            self.minesweeper.generate(self.id)
            if self.hidden_value == 0:
                self.minesweeper.clear_adjacent(self.id)
            elif self.hidden_value == -1:
                self.minesweeper.game_over(self.id)
            if self.hidden_value > -1:
                self.minesweeper.check_win()
                self.minesweeper.preview_adjacent(0, self.id)

    def click_cell(self, event, obj):
        if not obj.collidepoint(event.pos):
            return
        if (obj.collidepoint(event.pos) and 
                event.button == 1):
            self.clicked = 1
        elif (obj.collidepoint(event.pos) and
                event.button == 3 and
                self.hidden == 0):
            self.flagged = self.flagged ^ 1
            self.minesweeper.counter.update_counter(1-(2*self.flagged))
        if (obj.collidepoint(event.pos) and 
                self.hidden == 1 and 
                self.hidden_value > 0):
            #Hold down 8 adjacent tiles
            self.minesweeper.preview_adjacent(1, self.id)

    def update_value(self, val):
        self.hidden_value = val