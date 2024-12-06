import pygame
import time

class WinDialog():
    """Dialog box for displaying a win condition"""
    def __init__(self, minesweeper):
        self.minesweeper = minesweeper
        self.settings = minesweeper.settings
        self.screen = minesweeper.screen
        self.screen_rect = self.screen.get_rect()
        self.time = 0

        self.rect = pygame.Rect(0, 0, self.settings.dialog_width, self.settings.dialog_height)
        self.rect.center = self.screen_rect.center
        self.dialog_borders = [
            (self.rect.x, self.rect.y),
            (self.rect.x+self.settings.dialog_width, self.rect.y),
            (self.rect.x+self.settings.dialog_width, self.rect.y+self.settings.dialog_height),
            (self.rect.x, self.rect.y+self.settings.dialog_height),
            (self.rect.x, self.rect.y)
        ]

        self.button1_rect = pygame.Rect(0, 0, self.settings.dialog_button_width, self.settings.dialog_button_height)
        self.button1_rect.center = self.rect.center
        self.button1_rect.y += self.settings.dialog_height/4
        self.button1_rect.x -= self.settings.dialog_width/4
        self.button1_borders = [
            (self.button1_rect.x, self.button1_rect.y),
            (self.button1_rect.x+self.settings.dialog_button_width, self.button1_rect.y),
            (self.button1_rect.x+self.settings.dialog_button_width, self.button1_rect.y+self.settings.dialog_button_height),
            (self.button1_rect.x, self.button1_rect.y+self.settings.dialog_button_height),
            (self.button1_rect.x, self.button1_rect.y)
        ]

        self.button2_rect = pygame.Rect(0, 0, self.settings.dialog_button_width, self.settings.dialog_button_height)
        self.button2_rect.center = self.rect.center
        self.button2_rect.y += self.settings.dialog_height/4
        self.button2_rect.x += self.settings.dialog_width/4
        self.button2_borders = [
            (self.button2_rect.x, self.button2_rect.y),
            (self.button2_rect.x+self.settings.dialog_button_width, self.button2_rect.y),
            (self.button2_rect.x+self.settings.dialog_button_width, self.button2_rect.y+self.settings.dialog_button_height),
            (self.button2_rect.x, self.button2_rect.y+self.settings.dialog_button_height),
            (self.button2_rect.x, self.button2_rect.y)
        ]

        self.font = pygame.font.SysFont("Arial", self.settings.dialog_font_size)
        self.button_font = pygame.font.SysFont("Arial", self.settings.dialog_button_font_size)

    def draw_dialog(self):
        """Draw dialog window and buttons"""
        win_text = self.font.render("YOU WIN!!!!!!!", True, "black")
        win_text_rect = win_text.get_rect()
        win_text_rect.center = self.rect.center
        win_text_rect.y -= self.settings.dialog_height/4

        new_text = self.button_font.render("New Game", True, "black")
        new_text_rect = new_text.get_rect()
        new_text_rect.center = self.button1_rect.center

        preview_text = self.button_font.render("View Game", True, "black")
        preview_text_rect = preview_text.get_rect()
        preview_text_rect.center = self.button2_rect.center
        
        pygame.draw.rect(self.screen, self.settings.dialog_color, self.rect)
        pygame.draw.rect(self.screen, self.settings.dialog_button_color, self.button1_rect)
        pygame.draw.rect(self.screen, self.settings.dialog_button_color, self.button2_rect)
        self.screen.blit(new_text, new_text_rect)
        self.screen.blit(preview_text, preview_text_rect)
        self.screen.blit(win_text, win_text_rect)

        for i in range(4):
            pygame.draw.aaline(self.screen, "black", self.dialog_borders[i], self.dialog_borders[i+1])
            pygame.draw.aaline(self.screen, "black", self.button1_borders[i], self.button1_borders[i+1])
            pygame.draw.aaline(self.screen, "black", self.button2_borders[i], self.button2_borders[i+1])

    def update(self, events):
        """Return button pressed or 0 if not pressed"""
        current_time = time.time()*1000
        for event in events:
            #Do not check for events if there is no time when window appeared
            if self.time == 0:
                continue
            #Only return button press if pressed 200ms after appearing
            if (event.type == pygame.MOUSEBUTTONUP and 
                    self.button1_rect.collidepoint(event.pos) and
                    current_time-self.time > 200):
                return 1 #New Game
            if (event.type == pygame.MOUSEBUTTONUP and 
                    self.button2_rect.collidepoint(event.pos) and
                    current_time-self.time > 200):
                return 2 #View Game
        return 0
    
    def setTime(self, val = -1):
        """Set time to current time or value provided"""
        if val == -1:
            self.time = time.time()*1000
        else:
            self.time = val