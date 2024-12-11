import pygame
import sys
import os

class Counter:
    """Counter to track how many bombs are left in the game"""

    def __init__(self, minesweeper):
        self.settings = minesweeper.settings

        self.count=self.settings.bomb_count

        self.screen = minesweeper.screen
        self.screen_rect = minesweeper.screen.get_rect()
        self.height = self.settings.counter_height
        self.width = self.settings.counter_width
        self.bg_color = self.settings.counter_bg_color
        self.font_color = self.settings.counter_font_color

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x += 5
        self.rect.y += 5

        if getattr(sys, 'frozen', False):
            self.font = pygame.font.Font(os.path.join(sys._MEIPASS, "fonts", "digitalism.ttf"), self.settings.counter_font_size)
        else:
            self.font = pygame.font.Font(os.path.join("fonts", "digitalism.ttf"), self.settings.counter_font_size)

    def draw_counter(self):
        """Draw the counter"""
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        text = self.font.render(str(self.count), True, self.font_color)

        font_rect = text.get_rect()
        font_rect.midright = self.rect.midright
        font_rect.y += self.height/10
        font_rect.x -= 3
        self.screen.blit(text, font_rect)

    def update_counter(self, increment):
        """Update the counter to the number of mines"""
        self.count+=increment
        if self.count < 0:
            self.count = 0
        
