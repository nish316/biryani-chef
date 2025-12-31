import pygame
import sys

class WinScreen:
    def __init__(self):
        self.done = False
        self.ready_to_move = False
        self.next_level = "LEVEL1" # Allows them to restart
        
        self.font_title = pygame.font.SysFont("Verdana", 50, bold=True)
        self.font_main = pygame.font.SysFont("Verdana", 32, bold=True)
        self.font_info = pygame.font.SysFont("Verdana", 20)
        

        self.title = "BOMBASTIC BIRYANI CHEF"
        self.message = "You have successfully mastered the art of Dum Biryani!"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ready_to_move = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update(self):
        pass

    def draw(self, screen):
        # Professional dark background with gold accents
        screen.fill((20, 10, 0)) 
        
        # Draw some "Confetti" or decorative circles
        pygame.draw.circle(screen, (139, 69, 19), (400, 300), 250, 5) # Outer ring
        pygame.draw.circle(screen, (255, 215, 0), (400, 300), 240, 2) # Inner gold ring

        # Text Rendering
        title_surf = self.font_title.render(self.title, True, (255, 215, 0))
        msg_surf = self.font_info.render(self.message, True, (255, 255, 255))
        restart_surf = self.font_info.render("Press SPACE to Restart | ESC to Quit", True, (200, 200, 200))

        screen.blit(title_surf, (screen.get_width()//2 - title_surf.get_width()//2, 220))
        screen.blit(msg_surf, (screen.get_width()//2 - msg_surf.get_width()//2, 320))
        screen.blit(restart_surf, (screen.get_width()//2 - restart_surf.get_width()//2, 450))

        # Visual Flourish: A gold star
        pygame.draw.polygon(screen, (255, 215, 0), [(400, 100), (420, 150), (470, 150), (430, 180), (450, 230), (400, 200), (350, 230), (370, 180), (330, 150), (380, 150)])