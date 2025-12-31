import pygame
import os

class Level5:
    def __init__(self):
        self.done = False          
        self.ready_to_move = False 
        self.next_level = "LEVEL6"
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_info = pygame.font.SysFont("Verdana", 18)
        
        # 0: Empty, 1: Yogurt, 2: Masala, 3: Puree, 4: Onions, 5: Heat, 6: Bloom/Simmer
        self.step = 0
        self.total_steps = 6
        self.heat_level = 2 
        self.message = "Click to add the Yogurt!"
        
        self.simmer_timer = 0
        self.is_simmering = False
        
        # Load Assets
        self.assets = {}
        names = ["yogurt", "masala", "puree", "onions", "gravy"]
        for name in names:
            try:
                img = pygame.image.load(os.path.join("assets", "images", f"{name}.png")).convert_alpha()
                self.assets[name] = pygame.transform.scale(img, (400, 400))
            except:
                self.assets[name] = pygame.Surface((400, 400), pygame.SRCALPHA)
                
        self.rect = pygame.Rect(200, 150, 400, 400)
        self.active_ingredients = []

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.is_simmering and not self.done:
                    self.advance_step()
            
            if self.done and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ready_to_move = True

    def advance_step(self):
        self.step += 1
        if self.step == 1:
            self.active_ingredients.append("yogurt")
            self.message = "Click to add the Biryani Masala!"
        elif self.step == 2:
            self.active_ingredients.append("masala")
            self.message = "Click to add the Tomato Puree!"
        elif self.step == 3:
            self.active_ingredients.append("puree")
            self.message = "Click to add the Fried Onions!"
        elif self.step == 4:
            self.active_ingredients.append("onions")
            self.message = "Click to REDUCE HEAT to LOW."
        elif self.step == 5:
            self.heat_level = 0 
            self.message = "Low Heat Set. Click to Simmer & Bloom!"
        elif self.step == 6:
            self.active_ingredients = ["gravy"]
            self.message = "Simmering... the spices are blooming!"
            self.is_simmering = True

    def update(self):
        if self.is_simmering and not self.done:
            self.simmer_timer += 1
            if self.simmer_timer >= 120:
                self.done = True

    def draw(self, screen):
        screen.fill((255, 248, 230))
        
        # Pot Rendering
        pygame.draw.circle(screen, (50, 50, 50), (400, 350), 220)
        pygame.draw.circle(screen, (30, 30, 30), (400, 350), 205)
        
        for ing in self.active_ingredients:
            screen.blit(self.assets[ing], self.rect)

        # --- CIRCLE PROGRESS BAR ---
        pygame.draw.rect(screen, (101, 67, 33), [0, 0, 800, 100])
        
        # Draw 6 circles representing the progress
        start_x = 450
        for i in range(1, self.total_steps + 1):
            color = (255, 215, 0) if i <= self.step else (80, 80, 80)
            # Gold circle for completed steps, dark grey for remaining
            pygame.draw.circle(screen, color, (start_x + (i * 45), 45), 15)
            # Add a small white border to the active/completed ones
            if i <= self.step:
                pygame.draw.circle(screen, (255, 255, 255), (start_x + (i * 45), 45), 15, 2)

        # UI Text
        h_text = ["LOW", "MEDIUM", "HIGH"][self.heat_level]
        h_col = (100, 255, 100) if self.heat_level == 0 else (255, 100, 100)
        
        screen.blit(self.font_main.render(f"FLAME: {h_text}", True, h_col), (25, 15))
        screen.blit(self.font_info.render(self.message, True, (255, 255, 255)), (25, 55))

        if self.done:
            self.draw_result(screen)

    def draw_result(self, screen):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        txt, col = "GRAVY READY!", (50, 255, 50)
        fact = "The gravy is the soul of the biryani—rich, thick, and aromatic."
        
        screen.blit(self.font_main.render(txt, True, col), (300, 250))
        screen.blit(self.font_info.render(fact, True, (200, 200, 200)), (130, 310))
        screen.blit(self.font_info.render("Press SPACE for Level 6", True, (255, 255, 255)), (300, 400))