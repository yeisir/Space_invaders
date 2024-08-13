import pygame
import sys
import random
from config import WINDOW_SIZE

# Ship and alien settings
SPACESHIP_SIZE = (50, 30)
BULLET_SIZE = (3, 15)
BULLET_SPEED = 15
ALIEN_SIZE = (40, 30)
ALIEN_SPEED_EASY = 6  
ALIEN_SPEED_MEDIUM = 8  
ALIEN_SPEED_HARD = 10  
ALIEN_SPAWN_INTERVAL = 40
FONT_PATH = 'honk.ttf'

def show_game_over(screen, score):
    font = pygame.font.Font(FONT_PATH, 75)
    score_font = pygame.font.Font(FONT_PATH, 30)
    
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 50))
    
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 10))
    
    button_font = pygame.font.Font(FONT_PATH, 50)
    
    def render_button_text(text, color, position):
        button_text = button_font.render(text, True, color)
        button_rect = button_text.get_rect(center=position)
        return button_text, button_rect

    # Buttons
    play_again_text, play_again_rect = render_button_text("Play Again", (255, 255, 255), (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 70))
    back_to_menu_text, back_to_menu_rect = render_button_text("Back to Menu", (255, 255, 255), (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 140))
    quit_text, quit_rect = render_button_text("Quit", (255, 255, 255), (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 210))
    
    screen.blit(game_over_text, text_rect)
    screen.blit(score_text, score_rect)
    screen.blit(play_again_text, play_again_rect)
    screen.blit(back_to_menu_text, back_to_menu_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(mouse_pos):
                    return 'play_again'
                elif back_to_menu_rect.collidepoint(mouse_pos):
                    return 'back_to_menu'
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))
        screen.blit(game_over_text, text_rect)
        screen.blit(score_text, score_rect)
        
        # Button colors
        play_again_color = (0, 255, 0) if play_again_rect.collidepoint(mouse_pos) else (255, 255, 255)
        back_to_menu_color = (0, 255, 0) if back_to_menu_rect.collidepoint(mouse_pos) else (255, 255, 255)
        quit_color = (0, 255, 0) if quit_rect.collidepoint(mouse_pos) else (255, 255, 255)
        
        play_again_text, _ = render_button_text("Play Again", play_again_color, (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 70))
        back_to_menu_text, _ = render_button_text("Back to Menu", back_to_menu_color, (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 140))
        quit_text, _ = render_button_text("Quit", quit_color, (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 210))
        
        screen.blit(play_again_text, play_again_rect)
        screen.blit(back_to_menu_text, back_to_menu_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()

def start(screen, alien_speed, alien_fire_interval=0):
    # Initialize sound
    pygame.mixer.init()

    # Load and scale images
    background = pygame.image.load('asset/bg.png')
    background = pygame.transform.scale(background, WINDOW_SIZE)

    spaceship = pygame.image.load('asset/spaceship.png')
    spaceship = pygame.transform.scale(spaceship, SPACESHIP_SIZE)

    alien_images = [
        pygame.transform.scale(pygame.image.load('asset/alien1.png'), ALIEN_SIZE),
        pygame.transform.scale(pygame.image.load('asset/alien2.png'), ALIEN_SIZE),
        pygame.transform.scale(pygame.image.load('asset/alien3.png'), ALIEN_SIZE),
        pygame.transform.scale(pygame.image.load('asset/alien4.png'), ALIEN_SIZE),
        pygame.transform.scale(pygame.image.load('asset/alien5.png'), (80, 60))  # Alien gigante
    ]

    # Load sounds
    laser_sound = pygame.mixer.Sound('asset/laser.wav')
    explosion_sound = pygame.mixer.Sound('asset/explosion.wav')
    explosion2_sound = pygame.mixer.Sound('asset/explosion2.wav')
    life_sound = pygame.mixer.Sound('asset/life.wav')  # Sonido para perder una vida

    # Initialize spaceship position and speed
    spaceship_x = WINDOW_SIZE[0] // 2 - SPACESHIP_SIZE[0] // 2
    spaceship_y = WINDOW_SIZE[1] - 60
    spaceship_speed = 10

    # Initialize score and lives
    score = 0
    lives = 3

    # Lists for bullets and aliens
    bullets = []
    aliens = []
    alien_timer = 0

    # Clock for frame rate control
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a new bullet
                    bullet_x = spaceship_x + SPACESHIP_SIZE[0] // 2 - BULLET_SIZE[0] // 2
                    bullet_y = spaceship_y
                    bullets.append([bullet_x, bullet_y])
                    laser_sound.play()  # Play laser sound

        # Movement of spaceship
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship_x -= spaceship_speed
        if keys[pygame.K_RIGHT]:
            spaceship_x += spaceship_speed

        spaceship_x = max(0, min(WINDOW_SIZE[0] - SPACESHIP_SIZE[0], spaceship_x))

        # Spawn new aliens
        alien_timer += 1
        if alien_timer >= ALIEN_SPAWN_INTERVAL:
            alien_timer = 0
            alien_x = random.randint(0, WINDOW_SIZE[0] - ALIEN_SIZE[0])
            alien_y = -50
            # Decide whether to spawn a normal or giant alien
            if alien_speed == ALIEN_SPEED_HARD and random.random() < 0.1:  # 10% chance for giant alien
                alien_image = alien_images[4]  # Alien gigante
                alien_type = 'giant'
                hit_points = 3
            else:
                alien_image = random.choice(alien_images[:4])  # Normal aliens
                alien_type = 'normal'
                hit_points = 1
            aliens.append([alien_image, alien_x, alien_y, alien_type, hit_points])

        # Move aliens and check for collisions with the spaceship
        for alien in aliens[:]:
            alien[2] += alien_speed
            # Check if alien collides with the spaceship
            if (spaceship_x < alien[1] + ALIEN_SIZE[0] and 
                spaceship_x + SPACESHIP_SIZE[0] > alien[1] and 
                spaceship_y < alien[2] + ALIEN_SIZE[1] and 
                spaceship_y + SPACESHIP_SIZE[1] > alien[2]):
                # Alien collides with spaceship
                aliens.remove(alien)
                lives -= 1
                life_sound.play()  # Play life lost sound
                if lives <= 0:
                    explosion_sound.play()  # Play explosion sound
                    action = show_game_over(screen, score)
                    if action == 'play_again':
                        return start(screen, alien_speed, alien_fire_interval)
                    elif action == 'back_to_menu':
                        return
                    else:
                        pygame.quit()
                        sys.exit()
            elif alien[2] >= WINDOW_SIZE[1] - ALIEN_SIZE[1]:
                # Alien reached the bottom, lose a life
                aliens.remove(alien)
                lives -= 1
                life_sound.play()  # Play life lost sound
                if lives <= 0:
                    explosion_sound.play()  # Play explosion sound
                    action = show_game_over(screen, score)
                    if action == 'play_again':
                        return start(screen, alien_speed, alien_fire_interval)
                    elif action == 'back_to_menu':
                        return
                    else:
                        pygame.quit()
                        sys.exit()

        # Move bullets and check for collisions with aliens
        for bullet in bullets[:]:
            bullet[1] -= BULLET_SPEED
            if bullet[1] < 0:
                bullets.remove(bullet)
            else:
                for alien in aliens[:]:
                    if (bullet[0] > alien[1] and bullet[0] < alien[1] + ALIEN_SIZE[0] and 
                        bullet[1] > alien[2] and bullet[1] < alien[2] + ALIEN_SIZE[1]):
                        aliens.remove(alien)
                        bullets.remove(bullet)
                        score += 10
                        explosion2_sound.play()  # Play explosion sound
                        break

        # Draw everything
        screen.blit(background, (0, 0))
        screen.blit(spaceship, (spaceship_x, spaceship_y))

        for bullet in bullets:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(bullet[0], bullet[1], BULLET_SIZE[0], BULLET_SIZE[1]))

        for alien in aliens:
            screen.blit(alien[0], (alien[1], alien[2]))

        # Draw score and lives
        score_font = pygame.font.Font(FONT_PATH, 30)
        lives_font = pygame.font.Font(FONT_PATH, 30)
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = lives_font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()
        #clock.tick(120)

