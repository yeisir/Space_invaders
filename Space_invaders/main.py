import pygame
import sys
from config import WINDOW_SIZE
from game_modes import ALIEN_SPEED_EASY, ALIEN_SPEED_MEDIUM, ALIEN_SPEED_HARD, start

def show_main_menu(screen, sound):
    font = pygame.font.Font('Space_invaders/honk.ttf', 75)
    start_text = font.render("Start", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))
    
    start_rect = start_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 50))
    quit_rect = quit_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 50))
    
    screen.fill((0, 0, 0))
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(mouse_pos):
                    return 'start'
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        start_color = (0, 255, 0) if start_rect.collidepoint(mouse_pos) else (255, 255, 255)
        quit_color = (0, 255, 0) if quit_rect.collidepoint(mouse_pos) else (255, 255, 255)
        
        start_text = font.render("Start", True, start_color)
        quit_text = font.render("Quit", True, quit_color)
        
        screen.fill((0, 0, 0))
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()

def show_difficulty_menu(screen, sound):
    font = pygame.font.Font('Space_invaders/honk.ttf', 75)
    easy_text = font.render("Easy", True, (255, 255, 255))
    medium_text = font.render("Medium", True, (255, 255, 255))
    hard_text = font.render("Hard", True, (255, 255, 255))
    
    easy_rect = easy_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 100))
    medium_rect = medium_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    hard_rect = hard_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 100))
    
    screen.fill((0, 0, 0))
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)
    pygame.display.flip()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(mouse_pos):
                    return 'easy'
                elif medium_rect.collidepoint(mouse_pos):
                    return 'medium'
                elif hard_rect.collidepoint(mouse_pos):
                    return 'hard'

        easy_color = (0, 255, 0) if easy_rect.collidepoint(mouse_pos) else (255, 255, 255)
        medium_color = (0, 255, 0) if medium_rect.collidepoint(mouse_pos) else (255, 255, 255)
        hard_color = (0, 255, 0) if hard_rect.collidepoint(mouse_pos) else (255, 255, 255)
        
        easy_text = font.render("Easy", True, easy_color)
        medium_text = font.render("Medium", True, medium_color)
        hard_text = font.render("Hard", True, hard_color)
        
        screen.fill((0, 0, 0))
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Space Invader")
    
    pygame.mixer.init()
    main_sound = pygame.mixer.Sound('Space_invaders/asset/space.wav')
    
    main_sound.play(-1)  # Reproduce el sonido en bucle
    
    while True:
        if show_main_menu(screen, main_sound) == 'start':
            if show_difficulty_menu(screen, main_sound) == 'easy':
                start(screen, alien_speed=ALIEN_SPEED_EASY)
            elif show_difficulty_menu(screen, main_sound) == 'medium':
                start(screen, alien_speed=ALIEN_SPEED_MEDIUM)
            elif show_difficulty_menu(screen, main_sound) == 'hard':
                start(screen, alien_speed=ALIEN_SPEED_HARD)

if __name__ == "__main__":
    main()
