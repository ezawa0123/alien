import pygame
from pygame.sprite import Group
import game_functions as gf
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #Initialize pygame, settings, and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Make the Play button
    play_button = Button(ai_settings, screen, "Play")

    #Create an instance to store game stats
    stats = GameStats(ai_settings)    

    #Create a scoreboard to track the stats of the game
    sb = Scoreboard(ai_settings, screen, stats)

    #Create a group to store the aliens
    aliens = Group()    
    #Create a ship
    ship = Ship(ai_settings, screen)
    #make a group to store bullets in 
    bullets = Group()    

    #Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #Start the main loop for the game.
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, sb, stats, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
             
        gf.update_screen(ai_settings, sb, screen, stats, ship, aliens, bullets, play_button)
        
run_game()
