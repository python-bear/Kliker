from App import klik_engine, klik_utils
from os.path import exists


game = klik_engine.Game()

if __name__ != "__main__":
    game.cheater_alert()
        
if exists('App/klik_engine.py'):
    with open('App/klik_engine.py', 'rb') as file:
        current_hash = klik_utils.encrypt(file.read())

if exists('App/klik_anti_cheat.pkl'):
    with open('App/klik_anti_cheat.pkl', 'rb') as file:
        saved_hash = game.unpickle(file)

else:
    game.cheater_alert()

if current_hash != saved_hash:
    game.cheater_alert()
            
game.run()

klik_utils.finish(pygame_quit=False)
