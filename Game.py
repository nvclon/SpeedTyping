import pygame
import random
import sys
import time
import Button
import math
import config

file = open("bestscore.txt", 'r+')

class Game:
    def __init__(self):
        self.width = config.width
        self.height = config.height
        self.running = True
        self.ended = False
        self.active = False
        self.ready = True

        self.bg_color = config.bg_color
        self.other_color = config.other_color
        self.sound = pygame.mixer.Sound("impressive.mp3")

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.accuracy = 0
        self.time_first = 0
        self.time_last = 0
        self.this_score = 0
        self.miss = 0
        self.cur_letter = -1
        self.word = ''
        self.best_score = 0
        self.current_word = ''

        self.restart_button = Button.Button(config.button_x, config.button_y, config.button_width, config.button_height, "Restart", self.restart, self.screen)

        pygame.init()
        pygame.display.set_caption("SpeedTyping")

    def restart(self):
        '''starting a new game'''
        self.ended = False
        self.active = True
        self.ready = True

        self.accuracy = 0
        self.time_first = time.time()
        self.time_last = 0
        self.this_score = 0
        self.miss = 0
        self.cur_letter = 0
        self.word = self.get_word()
        self.current_word = ''
        file.seek(0)
        self.best_score = int(file.read())
        pygame.time.wait(config.delay)

    def show_text(self, screen, text, x, y, size, color):
        '''function to show text on screen'''
        text_font = pygame.font.Font("Domine-Regular.ttf", size)
        text_phrase = text_font.render(text, 1, color)
        text_rect = text_phrase.get_rect(center=(x,y))
        screen.blit(text_phrase, text_rect)

    def run(self):
        '''main loop'''
        self.restart()
        while self.running:
            self.screen.fill(self.bg_color)
            pygame.draw.line(self.screen, self.other_color, config.left_point, config.right_point, config.thickness)
            self.show_text(self.screen, self.word, config.word_x, config.word_y, config.font_size_large, self.other_color)
            self.show_res(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                    elif self.active and not self.ended:
                        if self.word[self.cur_letter] == event.unicode:
                            self.cur_letter += 1
                            self.current_word += event.unicode
                        else:
                            self.miss += 1
                    print(self.miss, self.cur_letter)
            self.show_text(self.screen, self.current_word, config.cur_word_x, config.cur_word_y, config.font_size_large, self.other_color)
            self.restart_button.check()
            pygame.display.update()
            if self.cur_letter == len(self.word):
                self.chill_end()
            print(self.running)


    def get_word(self):
        file_text = open("text.txt").read().split('\n')
        word = random.choice(file_text)
        while len(word) < config.len_of_text:
            word += ' '
            word += random.choice(file_text)
        return word

    def show_res(self, screen):
        '''shows all current stats to screen'''
        self.time_last = time.time() - self.time_first

        self.accuracy = len(self.word)/(self.miss + len(self.word)) * 100

        self.this_score = int(1000 * len(self.word) / self.time_last * math.sqrt(self.accuracy))
        self.show_text(screen, "Accuracy {}".format(round(self.accuracy, 2)), config.acc_text_x, config.acc_text_y, config.font_size_small, self.other_color)
        self.show_text(screen, "Time     {:.3f}".format(self.time_last), config.time_text_x, config.time_text_y, config.font_size_small, self.other_color)
        self.show_text(screen, "Misses   {}".format(self.miss), config.miss_text_x, config.miss_text_y, config.font_size_small, self.other_color)
        self.show_text(screen, "Score      {}".format(self.this_score), config.score_text_x, config.score_text_y, config.font_size_medium, self.other_color)
        self.show_text(screen, "Best Score      {}".format(self.best_score), config.best_score_text_x, config.best_score_text_y, config.font_size_medium, self.other_color)

    def chill_end(self):
        '''time to chill and see your great score'''
        self.show_res(self.screen)
        if self.this_score > self.best_score:
            file.seek(0)
            file.truncate()
            file.write(str(self.this_score))
        self.sound.play()
        self.restart()

Game().run()

file.close()
