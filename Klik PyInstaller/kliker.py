from App import klik_engine, klik_utils
import os


# Create engine
game = klik_engine.Game()

# Check for running this program instead of the main program
if __name__ != "__main__":
    game.cheater_alert()
        
# Check for editing of the program (cheating)
if os.path.exists('App/klik_engine.py'):
    with open('App/klik_engine.py', 'rb') as file:
        current_hash = klik_utils.encrypt(file.read())

if os.path.exists('App/klik_anti_cheat.pkl'):
    with open('App/klik_anti_cheat.pkl', 'rb') as file:
        saved_hash = game.unpickle(file)

else:
    game.cheater_alert()

if current_hash != saved_hash:
    game.cheater_alert()
            
# Run the game
game.run()

# Exit program
klik_utils.finish(pygame_quit=False)
