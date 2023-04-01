import pickle
import time
import hashlib
import os
import random
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame


def maintain_environment():
    if not os.path.exists('Data'):
        os.makedirs('Data')


class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up some variables
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

        # Set up the self.window
        self.ERROR_SOUND = pygame.mixer.Sound('Lib/error.wav')
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Kliker')
        pygame.display.set_icon(pygame.image.load('Lib/klik_icon.png'))

        # Set up the self.FONT
        self.FONT = pygame.font.SysFont('Courier New', 23, True)

        # Check for running this program instead of the main program
        if __name__ == "__main__":
            self.cheater_alert()

        # Check for editing of the program (cheating)
        if os.path.exists('App/klik_engine.py'):
            with open('App/klik_engine.py', 'rb') as file:
                current_hash = hashlib.sha256(file.read()).hexdigest()

        if os.path.exists('App/klik_anti_cheat.pkl'):
            with open('App/klik_anti_cheat.pkl', 'rb') as file:
                saved_hash = self.unpickle(file)

        else:
            self.cheater_alert()

        if current_hash != saved_hash:
            self.cheater_alert()

        # Load the scores from the file
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

                scores_hash = hashlib.sha256(scores_string).hexdigest()

                if saved_file_hash != scores_hash:
                    self.cheater_alert()

        else:
            self.current_score = 0
            self.high_score = 0
            self.high_cps = 0
            self.last_click_time = time.time()
            self.clicks = []

        # Set cps
        self.cps = 0

    def unpickle(self, pickled_file):
        try:
            unpickled_data = pickle.load(pickled_file)
            return unpickled_data

        except Exception as _error:
            self.cheater_alert()

    def finish(self):
        # Quit program
        pygame.quit()
        sys.exit()

    def help_page(self):
        self.FONT = pygame.font.SysFont('Courier New', 14, True)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # Save the scores to the file
                    with open('Data/klik_save.pkl', 'wb') as file:
                        pickle.dump((self.current_score, self.high_score, self.high_cps, self.last_click_time,
                                     self.clicks), file)

                    scores_string = ''.join(str(elem) for elem in [self.current_score, self.high_score, self.high_cps,
                                                                   self.last_click_time, self.clicks]).encode('utf-8')

                    save_file_hash = hashlib.sha256(scores_string).hexdigest()

                    with open('Data/save_hash.pkl', 'wb') as file:
                        pickle.dump(save_file_hash, file)

                    self.finish()

                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL):
                    # Opens the README.md file
                    os.startfile(self.README_PATH)

            # Clear the screen
            self.window.fill(self.BACKGROUND_COLOR)

            # Draw the keybinds
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

            # Draw the help message
            key_text = self.FONT.render(f'If you\'re caught', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 118))

            key_text = self.FONT.render(f'cheating you will have', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 138))

            key_text = self.FONT.render(f'to delete all files in', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 158))

            key_text = self.FONT.render(f'the `Data` folder.', True, self.BLACK_COLOR)
            self.window.blit(key_text, (10, 178))

            # Update the screen
            pygame.display.update()

            # Update the display
            pygame.display.flip()

            # Update the screen
            pygame.display.update()

    def cheater_alert(self):
        self.ERROR_SOUND.play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # Quit Pygame
                    self.finish()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        # Open help message
                        self.help_page()

                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        # Opens the README.md file
                        os.startfile(self.README_PATH)

            # Clear the screen
            self.window.fill(self.BACKGROUND_COLOR)

            # Create the text message
            cheat_text = self.FONT.render('Cheater!', True, self.BLACK_COLOR)

            # Get the message dimensions
            cheat_text_rect = cheat_text.get_rect()

            # Set the position of the message
            cheat_text_rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)

            # Display the message on the screen
            self.window.blit(cheat_text, cheat_text_rect)

            # Update the display
            pygame.display.flip()

            # Update the screen
            pygame.display.update()
            
    def change_button(self, text, bg, fg):
        self.button_color = bg
        self.button_text = self.FONT.render(text, True, fg)

    def update_game_image(self):
        # Clear the screen
        self.window.fill(self.BACKGROUND_COLOR)

        # Draw the button
        pygame.draw.rect(self.window, self.button_color, self.button_rect)
        self.button_text_rect = self.button_text.get_rect(center=self.button_rect.center)
        self.window.blit(self.button_text, self.button_text_rect)

        # Draw the high score
        score_text = self.FONT.render(f'H-SCR: {self.high_score}', True, self.BLACK_COLOR)
        self.window.blit(score_text, (10, 10))

        # Draw the high self.cps
        score_text = self.FONT.render(f'H-CPS: {self.high_cps:.3f}', True, self.BLACK_COLOR)
        self.window.blit(score_text, (10, 40))

        # Draw the score
        score_text = self.FONT.render(f'Score: {self.current_score}', True, self.BLACK_COLOR)
        self.window.blit(score_text, (10, 80))

        # Draw the self.cps
        cps_text = self.FONT.render(f'CPS: {self.cps:.3f}', True, self.BLACK_COLOR)
        self.window.blit(cps_text, (10, 110))

        # Update the screen
        pygame.display.update()

    def run(self):
        # Set up the button
        self.button_rect = pygame.Rect((self.WINDOW_WIDTH - self.BUTTON_WIDTH) // 2,
                                       self.WINDOW_HEIGHT - (self.BUTTON_HEIGHT + 5), self.BUTTON_WIDTH,
                                       self.BUTTON_HEIGHT)
        self.button_color = self.BUTTON_IDLE_COLOR

        # Run the game loop
        while True:
            # Check if the mouse is hovering over the button
            mouse_pos = pygame.mouse.get_pos()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # Save the scores to the file
                    with open('Data/klik_save.pkl', 'wb') as file:
                        pickle.dump((self.current_score, self.high_score, self.high_cps, self.last_click_time, 
                                     self.clicks), file)

                    scores_string = ''.join(str(elem) for elem in [self.current_score, self.high_score, self.high_cps,
                                                                   self.last_click_time, self.clicks]).encode('utf-8')

                    save_file_hash = hashlib.sha256(scores_string).hexdigest()

                    with open('Data/save_hash.pkl', 'wb') as file:
                        pickle.dump(save_file_hash, file)

                    self.finish()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        self.update_game_image()
                        self.BUTTON_CLICK_SOUNDS[random.randint(1, 2) - 1].play()
                        current_time = time.time()
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
                        # Reset the score to 0 when the tab key is pressed
                        self.current_score = 0

                    elif event.key == pygame.K_BACKSPACE:
                        # Reset the high self.cps to 0
                        self.high_cps = 0

                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        # Open help message
                        self.help_page()

                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        # Opens the README.md file
                        os.startfile(self.README_PATH)

            # Calculate self.cps
            current_time = time.time()
            self.clicks = [click for click in self.clicks if current_time - click <= 1]

            if len(self.clicks) > 1:
                self.cps = len(self.clicks) / (self.clicks[-1] - self.clicks[0])

            else:
                self.cps = 0

            # Get mouse color
            if self.button_rect.collidepoint(mouse_pos):
                self.change_button(self.BUTTON_MESSAGE, self.BUTTON_HOVER_COLOR, self.BLACK_COLOR)

            else:
                self.change_button(self.BUTTON_MESSAGE, self.BUTTON_IDLE_COLOR, self.WHITE_COLOR)

            if pygame.mouse.get_pressed()[0]:
                if self.button_rect.collidepoint(mouse_pos):
                    self.change_button(self.BUTTON_MESSAGE, self.BUTTON_CLICK_COLOR, self.WHITE_COLOR)

                else:
                    self.change_button(self.BUTTON_MESSAGE, self.BUTTON_IDLE_COLOR, self.WHITE_COLOR)

            # Update the screen
            self.update_game_image()
