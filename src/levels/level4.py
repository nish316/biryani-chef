import pygame
import os

class Level4:
    def __init__(self):
        self.done = False
        self.ready_to_move = False
        self.next_level = "LEVEL5"
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_info = pygame.font.SysFont("Verdana", 18)
        
        self.progress = 0 
        self.heat_level = 2 # 0: Low, 1: Medium, 2: High
        self.burn_meter = 0
        self.message = "Flame is HIGH! Regulate it as they brown!"
        
        try:
            path = os.path.join("assets", "images", "onions.png")
            self.orig_onions = pygame.image.load(path).convert_alpha()
            self.orig_onions = pygame.transform.scale(self.orig_onions, (250, 200))
        except:
            self.orig_onions = pygame.Surface((250, 200), pygame.SRCALPHA)
            self.orig_onions.fill((255, 239, 213)) 
            
        self.onions_img = self.orig_onions.copy()
        self.onions_rect = self.onions_img.get_rect(center=(400, 350))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Cycle: High (2) -> Medium (1) -> Low (0)
                self.heat_level = (self.heat_level - 1) % 3
            
            if self.done and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.burn_meter < 100:
                        self.ready_to_move = True  # Tell manager to go to Level 5
                    else:
                        self.__init__() # Restart if they burnt the onions

    def update(self):
        if self.progress >= 100 or self.burn_meter >= 100:
            self.done = True
            return

        # RECIPE LOGIC: Regulate flame from high to medium to low 
        if self.heat_level == 2: # High
            self.progress += 0.12
            # High heat is dangerous after initial moisture is gone
            if self.progress > 30:
                self.burn_meter += 0.3 
                self.message = "DANGER! Too hot! Onions are charring!"

        elif self.heat_level == 1: # Medium
            self.progress += 0.08
            if self.progress > 75:
                self.burn_meter += 0.15 # Still risky at the end 
                self.message = "Careful... Medium heat might be too much now."

        else: # Low
            self.progress += 0.04
            # REMOVED: Burn meter no longer decreases. Burnt is burnt!
            self.message = "Low heat: Safely finishing the browning."

        self.update_visuals()

    def update_visuals(self):
        ratio = self.progress / 100
        burn_ratio = self.burn_meter / 100
        temp_img = self.orig_onions.copy()
        
        # Golden Tint (Recipe Goal: Golden Brown) 
        golden_overlay = pygame.Surface(temp_img.get_size(), pygame.SRCALPHA)
        gold_alpha = int(ratio * 160)
        golden_overlay.fill((139, 69, 19, gold_alpha))
        temp_img.blit(golden_overlay, (0,0))
        
        # Black Char Tint (Fail State: Burnt) 
        if self.burn_meter > 0:
            burn_overlay = pygame.Surface(temp_img.get_size(), pygame.SRCALPHA)
            burn_alpha = int(burn_ratio * 220)
            burn_overlay.fill((10, 5, 0, burn_alpha)) # Deep black-brown
            temp_img.blit(burn_overlay, (0,0))
            
        self.onions_img = temp_img

    def draw(self, screen):
        screen.fill((255, 245, 230))
        pygame.draw.circle(screen, (65, 65, 65), (400, 350), 195)
        screen.blit(self.onions_img, self.onions_rect)
        
        # UI Header
        pygame.draw.rect(screen, (101, 67, 33), [0, 0, 800, 85])
        h_text = ["LOW", "MEDIUM", "HIGH"][self.heat_level]
        title = self.font_info.render(f"FLAME: {h_text}", True, (255,255,255))
        hint = self.font_info.render(self.message, True, (255, 215, 0))
        screen.blit(title, (20, 15))
        screen.blit(hint, (20, 45))

        # Progress Bars
        pygame.draw.rect(screen, (218, 165, 32), [500, 20, self.progress * 2.5, 20])
        pygame.draw.rect(screen, (255, 0, 0), [500, 50, self.burn_meter * 2.5, 15])
        
        if self.done:
            self.draw_result(screen)

    def draw_result(self, screen):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        # Grading Logic
        if self.burn_meter >= 100:
            txt, col = "RUINED: COMPLETELY BURNT", (255, 50, 50)
            sub = "The onions are bitter. Restart the level!"
        elif self.burn_meter > 0:
            txt, col = "OKAY: SLIGHTLY SINGED", (255, 165, 0)
            sub = "Decent, but a true chef regulates the flame better!"
        else:
            txt, col = "PERFECT: MASTER BIRISTA!", (50, 255, 50)
            sub = "Excellently browned without a single burnt edge!"
            
        screen.blit(self.font_main.render(txt, True, col), (200, 250))
        screen.blit(self.font_info.render(sub, True, (200, 200, 200)), (180, 310))
        screen.blit(self.font_info.render("Press SPACE", True, (255, 255, 255)), (340, 400))