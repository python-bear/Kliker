from Klik.App import klik_engine
import sys
import os
import hashlib
import pickle
import pygame


# Initialize Pygame
pygame.init()

# Set up some variables
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

BACKGROUND_COLOR = (107, 194, 231)
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200

# Set up the window
ERROR_SOUND = pygame.mixer.Sound('Lib/error.wav')
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Kliker')
pygame.display.set_icon(pygame.image.load('Lib/klik_icon.png'))

base_path = os.path.dirname(os.path.abspath(__file__)).replace("\\App", "")
README_PATH = f'{base_path}/App/README.md'

# Set up the FONT
FONT = pygame.font.SysFont('Courier New', 23, True)


# Exit function
def finish():
    # Quit program
    pygame.quit()
    sys.exit()
    
    
# Help page
def help_page():
    FONT = pygame.font.SysFont('Courier New', 14, True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                finish()

            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL):
                # Opens the README.md file
                os.startfile(README_PATH)

        # Clear the screen
        window.fill(BACKGROUND_COLOR)

        # Draw the keybinds
        key_text = FONT.render(f'BACKSPACE : Reset H-CPS', True, BLACK_COLOR)
        window.blit(key_text, (10, 8))

        key_text = FONT.render(f'ESCAPE    : End game', True, BLACK_COLOR)
        window.blit(key_text, (10, 28))

        key_text = FONT.render(f'SHIFT     : Open help', True, BLACK_COLOR)
        window.blit(key_text, (10, 48))

        key_text = FONT.render(f'CLICK     : Get point', True, BLACK_COLOR)
        window.blit(key_text, (10, 68))

        key_text = FONT.render(f'TAB       : Reset score', True, BLACK_COLOR)
        window.blit(key_text, (10, 88))

        # Draw the help message
        key_text = FONT.render(f'If you\'re caught', True, BLACK_COLOR)
        window.blit(key_text, (10, 118))

        key_text = FONT.render(f'cheating you will have', True, BLACK_COLOR)
        window.blit(key_text, (10, 138))

        key_text = FONT.render(f'to delete all files in', True, BLACK_COLOR)
        window.blit(key_text, (10, 158))

        key_text = FONT.render(f'the `Data` folder.', True, BLACK_COLOR)
        window.blit(key_text, (10, 178))

        # Update the screen
        pygame.display.update()

        # Update the display
        pygame.display.flip()

        # Update the screen
        pygame.display.update()
    
    
# Cheater alert
def cheater_alert():
    ERROR_SOUND.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # Quit Pygame
                finish()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    # Open help message
                    help_page()

                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    # Opens the README.md file
                    os.startfile(README_PATH)

        # Clear the screen
        window.fill(BACKGROUND_COLOR)

        # Create the text message
        cheat_text = FONT.render('Cheater!', True, BLACK_COLOR)

        # Get the message dimensions
        cheat_text_rect = cheat_text.get_rect()

        # Set the position of the message
        cheat_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Display the message on the screen
        window.blit(cheat_text, cheat_text_rect)

        # Update the display
        pygame.display.flip()

        # Update the screen
        pygame.display.update()
        
        
# Unpickling function
def unpickle(pickled_file):
    try:
        unpickled_data = pickle.load(pickled_file)
        return unpickled_data

    except Exception as _error:
        cheater_alert()


# Check for running this program instead of the main program
if __name__ != "__main__":
    cheater_alert()
        
# Check for editing of the program (cheating)
if os.path.exists('App/klik_engine.py'):
    with open('App/klik_engine.py', 'rb') as file:
        current_hash = hashlib.sha256(file.read()).hexdigest()

if os.path.exists('App/klik_anti_cheat.pkl'):
    with open('App/klik_anti_cheat.pkl', 'rb') as file:
        saved_hash = unpickle(file)

else:
    cheater_alert()

if current_hash != saved_hash:
    cheater_alert()
            
# Run the game
game = klik_engine.Game()
game.run()

finish()
