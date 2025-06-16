from chess_game import ChessGame
import pygame

def run_game():
    game = ChessGame()
    game.setup()
    while game.running:
        game.update_loop()
    pygame.quit()

if __name__ == "__main__":
    run_game()




