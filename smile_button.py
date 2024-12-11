import pygame
import sys
import os

class SmileButton():
    """Button for restarting the game"""

    def __init__(self, minesweeper):
        self.settings = minesweeper.settings
        self.screen = minesweeper.screen

        if getattr(sys, 'frozen', False):
            self.image = pygame.image.load(os.path.join(sys._MEIPASS, "images", "Smile.png"))
        else:
            self.image = pygame.image.load("images/Smile.png")
        self.rect = self.image.get_rect()

        self.rect.midtop = minesweeper.screen.get_rect().midtop
        self.rect.y += 10

    def draw_smile(self):
        """Draw the smile image"""
        self.screen.blit(self.image, self.rect)

    def update(self, events):
        """Return 1 if sprite was clicked on"""
        for event in events:
            if (event.type == pygame.MOUSEBUTTONUP and 
                    self.rect.collidepoint(event.pos)):
                return 1
        return 0