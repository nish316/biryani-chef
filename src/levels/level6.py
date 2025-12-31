import pygame
import os
import random

class Level6:
    def __init__(self):
        self.done = False          
        self.ready_to_move = False 
        self.next_level = "LEVEL7"
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_info = pygame.font.SysFont("Verdana", 18)
        
        # Cooking Logic
        self.cook_progress = 0
        self.is_boiling = False
        self.water_temp = 0
        self.final_grade = ""
        
        # Timing Window: 92% to 98% is the "Sweet Spot"
        self.target_range = range(92, 99)
        
        # Visuals
        self.bubbles = []
        self.message = "Click the pot to bring the water to a boil!"
        
        try:
            self.pot_img = pygame.image.load(os.path.join("assets", "images", "pot.png")).convert_alpha()
            self.pot_img = pygame.transform.scale(self.pot_img, (450, 350))
            self.rice_grains = pygame.image.load(os.path.join("assets", "images", "basmati_rice.png")).convert_alpha()
        except:
            self.pot_img = pygame.Surface((450, 350), pygame.SRCALPHA)
            self.pot_img.fill((150, 150, 150))
            
        self.rect = self.pot_img.get_rect(center=(400, 350))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.is_boiling:
                    self.water_temp += 20
                    if self.water_temp >= 100:
                        self.is_boiling = True
                        self.message = "RICE IS COOKING! Press SPACE at 95% (Al Dente)!"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.is_boiling and not self.done:
                    self.check_result()
                elif self.done:
                    # If they succeeded, move to Level 7
                    if "PERFECT" in self.final_grade:
                        self.ready_to_move = True 
                    else:
                        # If they failed, restart the level
                        self.__init__()

    def update(self):
        if self.done: return

        if self.is_boiling:
            # The rice cooks at a steady pace
            self.cook_progress += 0.25 
            
            # Boiling animation logic
            if len(self.bubbles) < 15:
                self.bubbles.append([random.randint(250, 550), 450, random.randint(2, 5)])
            for b in self.bubbles:
                b[1] -= b[2] # Move up
                if b[1] < 220:
                    b[1] = 450
                    b[0] = random.randint(250, 550)

            # Auto-fail if it hits 100% (Overcooked)
            if self.cook_progress >= 105:
                self.check_result()

    def check_result(self):
        self.done = True
        score = int(self.cook_progress)
        
        if score in self.target_range:
            self.final_grade = "PERFECT! Al Dente (95%)"
        elif score < 92:
            self.final_grade = "UNDERCOOKED! Grains are still hard."
        else:
            self.final_grade = "OVERCOOKED! You made rice porridge."

    def draw(self, screen):
        screen.fill((240, 248, 255)) # Water blue background
        
        # Pot and Water
        pygame.draw.rect(screen, (0, 150, 255), [220, 220, 360, 200]) # Water
        screen.blit(self.pot_img, self.rect)
        
        # Bubbles
        if self.is_boiling:
            for b in self.bubbles:
                pygame.draw.circle(screen, (255, 255, 255), (b[0], b[1]), b[2], 1)

        # UI Header
        pygame.draw.rect(screen, (70, 130, 180), [0, 0, 800, 100])
        screen.blit(self.font_main.render(f"WATER TEMP: {int(self.water_temp)}°C", True, (255, 255, 255)), (25, 15))
        screen.blit(self.font_info.render(self.message, True, (255, 255, 0)), (25, 55))

        # Precision Progress Bar
        pygame.draw.rect(screen, (40, 40, 40), [500, 40, 250, 30])
        # Color changes as it gets closer to 95%
        bar_col = (255, 255, 255)
        if 90 < self.cook_progress < 100: bar_col = (50, 255, 50) # Green zone
        
        pygame.draw.rect(screen, bar_col, [500, 40, min(self.cook_progress, 100) * 2.5, 30])
        # Target Line at 95%
        pygame.draw.line(screen, (255, 0, 0), (500 + (95 * 2.5), 35), (500 + (95 * 2.5), 75), 3)

        if self.done:
            self.draw_result(screen)

    def draw_result(self, screen):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        col = (50, 255, 50) if "PERFECT" in self.final_grade else (255, 50, 50)
        screen.blit(self.font_main.render(self.final_grade, True, col), (220, 250))
        
        fact = "Fact: Par-boiling rice to 95% ensures it finishes perfectly during 'Dum'."
        screen.blit(self.font_info.render(fact, True, (200, 200, 200)), (100, 310))
        
        prompt = "Press SPACE to move to Final Assembly" if "PERFECT" in self.final_grade else "Press SPACE to try again"
        screen.blit(self.font_info.render(prompt, True, (255, 255, 255)), (250, 400))