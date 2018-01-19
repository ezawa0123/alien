import sys 
import pygame
from bullet import Bullet
from alien import Alien

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if the limit is not reached"""
    #Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events( ai_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship, aliens, bullets):
    """Update imagse on the screen and flip to the new screen."""

    #Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    #Redraw all bullets behind ship and alients
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Update the bullet position and remove the old bullets"""

    #Update bullet positions 
    bullets.update()

    #Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    #Check for any bullets that have any aliens
    #If so, get rid of the bullet and the alien
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets):
    """Check for bullet alien collisions"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        #Destroy existing bullets and create a new fleet
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def update_aliens(ai_settings, aliens):
    """Update the aliens new positions and change directions if at edge"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_spacex = ai_settings.screen_width - 2 * alien_width
    number_aliensx = int(available_spacex / (2 * alien_width) )
    return number_aliensx

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (
        ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 *alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet( ai_settings, screen, ship, aliens):
    """Create a fleet of aliens """

    alien = Alien(ai_settings, screen)
    number_aliensx = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliensx):
            #Create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached the edge"""

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """ Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

