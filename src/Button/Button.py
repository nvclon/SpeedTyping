import pygame
from src import config

pygame.init()
text_font = pygame.font.Font("resources/fonts/Domine-Regular.ttf", 24)


'''template button'''
class Button:
    def __init__(self, x_coord, y_coord, width, height, text, function, screen):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height
        self.text = text
        self.function = function
        self.activated = False
        self.screen = screen

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)
        self.buttonText = text_font.render(text, 2, config.bg_color)

    def check(self):
        '''checking if it is pressed or not
           function will trigger once when is held
        '''
        x, y = pygame.mouse.get_pos()

        self.buttonSurface.fill(config.other_color)

        if self.buttonRect.collidepoint((x, y)) and pygame.mouse.get_pressed()[0]:
            if not self.activated:
                self.activated = True
                self.function()
        else:
            self.activated = False

        self.buttonSurface.blit(self.buttonText, [
            self.buttonRect.width / 2 - self.buttonText.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonText.get_rect().height / 2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)
