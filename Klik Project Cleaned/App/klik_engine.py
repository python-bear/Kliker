from App import klik_utils as utils
from pickle import dump as pickle_dump
from time import time as get_current_time
from random import randint as random_int
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame


def maintain_environment():
    if not os.path.exists('Data'):
        os.makedirs('Data')


class Game:
    def __init__(self):
        pygame.init()

        self.BLACK_COLOR = (0, 0, 0)
        self.WHITE_COLOR = (255, 255, 255)

        self.BACKGROUND_COLOR = (107, 194, 231)
        self.WINDOW_WIDTH = 200
        self.WINDOW_HEIGHT = 200

        self.BUTTON_IDLE_COLOR = (33, 117, 154)
        self.BUTTON_HOVER_COLOR = (235, 0, 58)
        self.BUTTON_CLICK_COLOR = (254, 0, 0)
        self.BUTTON_MESSAGE = 'Click Me!'
        self.BUTTON_CLICK_SOUNDS = (pygame.mixer.Sound('Lib/click_1.wav'), pygame.mixer.Sound('Lib/click_2.wav'))
        self.BUTTON_WIDTH = self.WINDOW_WIDTH - 10
        self.BUTTON_HEIGHT = 50
        self.button_rect = None
        self.button_text = None
        self.button_text_rect = None
        self.button_color = self.BUTTON_IDLE_COLOR

        base_path = os.path.dirname(os.path.abspath(__file__)).replace("\\App", "")
        self.README_PATH = f'{base_path}/App/README.md'

        self.ERROR_SOUND = pygame.mixer.Sound('Lib/error.wav')
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Kliker')
        pygame.display.set_icon(pygame.image.load('Lib/klik_icon.png'))

        self.FONT = pygame.font.SysFont('Courier New', 23, True)

        if __name__ == "__main__":
            self.cheater_alert()

        if os.path.exists('App/klik_engine.py'):
            with open('App/klik_engine.py', 'rb') as file:
                current_hash = utils.encrypt(file.read())

        if os.path.exists('App/klik_anti_cheat.pkl'):
            with open('App/klik_anti_cheat.pkl', 'rb') as file:
                saved_hash = self.unpickle(file)

        else:
            self.cheater_alert()

        if current_hash != saved_hash:
            self.cheater_alert()

        maintain_environment()

        if os.path.exists('Data/klik_save.pkl'):
            with open('Data/klik_save.pkl', 'rb') as file:
                self.current_score, self.high_score, self.high_cps, self.last_click_time, self.clicks = \
                    self.unpickle(file)

            if os.path.exists('Data/save_hash.pkl'):
                with open('Data/save_hash.pkl', 'rb') as file:
                    saved_file_hash = self.unpickle(file)

                scores_string = ''.join(str(elem) for elem in [self.current_score, self.high_score, self.high_cps,
                                                               self.last_click_time, self.clicks]).encode('utf-8')

                scores_hash = utils.encrypt(scores_string)

                if saved_file_hash != scores_hash:
                    self.cheater_alert()

        else:
            self.current_score = 0
            self.high_score = 0
            self.high_cps = 0
            self.last_click_time = get_current_time()
            self.clicks = []

        self.cps = 0

    def unpickle(self, data):
        unpickled_data = utils.unpickle(data)

        if not unpickled_data:
            self.cheater_alert()

        else:
            return unpickled_data

    def help_page(self, from_cheat=False):
        self.FONT = pygame.font.SysFont('Courier New', 14, True)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    if not from_cheat:
                        with open('Data/klik_save.pkl', 'wb') as file:
                            pickle_dump((self.current_score, self.high_score, self.high_cps, self.last_click_time,
                                         self.clicks), file)

                        scores_string = ''.join(str(elem) for elem in [self.current_score, self.high_score,
                                                                       self.high_cps, self.last_click_time,
                                                                       self.clicks]).encode('utf-8')

                        save_file_hash = utils.encrypt(scores_string)

                        with open('Data/save_hash.pkl', 'wb') as file:
                            pickle_dump(save_file_hash, file)

                    utils.finish()

                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL):
                    os.startfile(self.README_PATH)

            self.window.fill(self.BACKGROUND_COLOR)

            key_text = self.FONT.render(f'BACKSPACE : Reset H-CPS', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 8))

            key_text = self.FONT.render(f'ESCAPE    : End game', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 28))

            key_text = self.FONT.render(f'SHIFT     : Open help', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 48))

            key_text = self.FONT.render(f'CLICK     : Get point', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 68))

            key_text = self.FONT.render(f'TAB       : Reset score', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 88))

            key_text = self.FONT.render(f'If you\'re caught', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 118))

            key_text = self.FONT.render(f'cheating you will have', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 138))

            key_text = self.FONT.render(f'to delete all files in', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 158))

            key_text = self.FONT.render(f'the `Data` folder.', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 178))

            pygame.display.update()

            pygame.display.flip()

            pygame.display.update()

    def cheater_alert(self):
        self.ERROR_SOUND.play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    utils.finish()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.help_page(from_cheat=True)

                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        os.startfile(self.README_PATH)

            self.window.fill(self.BACKGROUND_COLOR)

            cheat_text = self.FONT.render('Cheater!', True, self.BLACK_COLOR)

            cheat_text_rect = cheat_text.get_rect()

            cheat_text_rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)

            self.window.blit(cheat_text, cheat_text_rect)

            pygame.display.flip()

            pygame.display.update()
            
    def change_button(self, text, bg, fg):
        self.button_color = bg
        self.button_text = self.FONT.render(text, True, fg)

    def update_game_image(self):
        self.window.fill(self.BACKGROUND_COLOR)

        pygame.draw.rect(self.window, self.button_color, self.button_rect)
        self.button_text_rect = self.button_text.get_rect(center=self.button_rect.center)
        self.window.blit(self.button_text, self.button_text_rect)

        score_text = self.FONT.render(f'H-SCR: {self.high_score}', True, self.BLACK_COLOR)
        self.window.blit(score_text, (10, 10))

        score_text = self.FONT.render(f'H-CPS: {self.high_cps:.3f}', True, self.BLACK_COLOR)
        self.window.blit(score_text, (10, 40))

        score_text = self.FONT.render(f'Score: {self.current_score}', True, self.BLACK_COLOR)
        self.window.blit(score_text, (10, 80))

        cps_text = self.FONT.render(f'CPS: {self.cps:.3f}', True, self.BLACK_COLOR)
        self.window.blit(cps_text, (10, 110))

        pygame.display.update()

    def run(self):
        self.button_rect = pygame.Rect((self.WINDOW_WIDTH - self.BUTTON_WIDTH) // 2,
                                       self.WINDOW_HEIGHT - (self.BUTTON_HEIGHT + 5), self.BUTTON_WIDTH,
                                       self.BUTTON_HEIGHT)
        self.button_color = self.BUTTON_IDLE_COLOR

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    with open('Data/klik_save.pkl', 'wb') as file:
                        pickle_dump((self.current_score, self.high_score, self.high_cps, self.last_click_time,
                                     self.clicks), file)

                    scores_string = ''.join(str(elem) for elem in [self.current_score, self.high_score, self.high_cps,
                                                                   self.last_click_time, self.clicks]).encode('utf-8')

                    save_file_hash = utils.encrypt(scores_string)

                    with open('Data/save_hash.pkl', 'wb') as file:
                        pickle_dump(save_file_hash, file)

                    utils.finish()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        self.update_game_image()
                        self.BUTTON_CLICK_SOUNDS[random_int(1, 2) - 1].play()
                        current_time = get_current_time()
                        time_since_last_click = current_time - self.last_click_time
                        self.last_click_time = current_time

                        if time_since_last_click > 1:
                            self.cps = 0

                        else:
                            self.cps = 1 / time_since_last_click

                        self.clicks.append(current_time)

                        if self.cps <= 30:
                            self.current_score += 1

                            if self.current_score > self.high_score:
                                self.high_score = self.current_score

                            if self.cps > self.high_cps:
                                self.high_cps = self.cps

                        else:
                            self.cheater_alert()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.current_score = 0

                    elif event.key == pygame.K_BACKSPACE:
                        self.high_cps = 0

                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.help_page()

                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        os.startfile(self.README_PATH)

            current_time = get_current_time()
            self.clicks = [click for click in self.clicks if current_time - click <= 1]

            if len(self.clicks) > 1:
                self.cps = len(self.clicks) / (self.clicks[-1] - self.clicks[0])

            else:
                self.cps = 0

            if self.button_rect.collidepoint(mouse_pos):
                self.change_button(self.BUTTON_MESSAGE, self.BUTTON_HOVER_COLOR, self.BLACK_COLOR)

            else:
                self.change_button(self.BUTTON_MESSAGE, self.BUTTON_IDLE_COLOR, self.WHITE_COLOR)

            if pygame.mouse.get_pressed()[0]:
                if self.button_rect.collidepoint(mouse_pos):
                    self.change_button(self.BUTTON_MESSAGE, self.BUTTON_CLICK_COLOR, self.WHITE_COLOR)

                else:
                    self.change_button(self.BUTTON_MESSAGE, self.BUTTON_IDLE_COLOR, self.WHITE_COLOR)

            self.update_game_image()
