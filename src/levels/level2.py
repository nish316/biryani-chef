import pygame
import os

class Level2:
    def __init__(self):
        self.done = False          # Shows the Result Overlay
        self.ready_to_move = False # Signals the Engine to change levels
        self.next_level = "LEVEL3"
        
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_info = pygame.font.SysFont("Verdana", 18)
        
        # Setup Rice Image [cite: 15]
        path = os.path.join("assets", "images", "basmati_rice.png")
        try:
            self.rice_img = pygame.image.load(path).convert_alpha()
            self.rice_img = pygame.transform.scale(self.rice_img, (400, 300))
        except:
            self.rice_img = pygame.Surface((400, 300))
            self.rice_img.fill((255, 255, 255))
            
        self.rice_rect = self.rice_img.get_rect(center=(400, 350))

        # Cloudy Water Mask (Starch)
        self.mask = pygame.Surface((400, 300), pygame.SRCALPHA)
        self.mask.fill((220, 220, 220, 200)) # Semi-transparent grey
        
        self.clean_percent = 0
        self.is_soaking = False
        self.soak_timer = 0
        self.message = "Rinse the rice well to remove starch! (Scrub with Mouse)"

    def handle_events(self, events):
        for event in events:
            # If the result screen is showing, only listen for SPACE
            if self.done:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.ready_to_move = True
                continue # Skip game controls if we are done

            # Standard game events (Not needed for this specific scrubbing logic)
            if event.type == pygame.QUIT:
                pygame.quit()

    def update(self):
        if self.done:
            return # Freeze the game logic to show the fact screen

        # Logic for Phase 2: Soaking (Recipe requires 30 mins) 
        if self.is_soaking:
            self.soak_timer += 1
            # Simulate 30 mins in approx 3 seconds (180 frames)
            if self.soak_timer >= 180:
                self.done = True # Triggers result screen
            return

        # Logic for Phase 1: Scrubbing/Rinsing
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.rice_rect.collidepoint(mouse_pos):
            # Calculate local coordinates on the mask
            lx = mouse_pos[0] - self.rice_rect.x
            ly = mouse_pos[1] - self.rice_rect.y
            
            # Erase circles from the mask to "clean" the rice
            pygame.draw.circle(self.mask, (0, 0, 0, 0), (lx, ly), 30)
            self.clean_percent += 0.5
            
        if self.clean_percent >= 100:
            self.is_soaking = True
            self.message = "Rinsed well! Now soaking for 30 minutes..."

    def draw(self, screen):
        screen.fill((240, 248, 255)) # Water-like background
        
        # HUD
        pygame.draw.rect(screen, (70, 130, 180), [0, 0, 800, 90])
        title = self.font_main.render("LEVEL 2: PREPARING THE RICE", True, (255, 255, 255))
        msg = self.font_info.render(self.message, True, (255, 255, 0))
        screen.blit(title, (20, 15))
        screen.blit(msg, (20, 45))

        # Gameplay Visuals
        screen.blit(self.rice_img, self.rice_rect)
        screen.blit(self.mask, self.rice_rect)

        # Show Result Overlay with Educational Fact
        if self.done:
            self.draw_result(screen)

    def draw_result(self, screen):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        txt, col = "RICE PREPPED!", (50, 255, 50)
        # Educational Facts from Recipe 
        fact1 = "Chef's Tip: Rinsing removes starch so rice stays separate."
        fact2 = "Soaking for 30 minutes lets grains expand without breaking."
        
        screen.blit(self.font_main.render(txt, True, col), (310, 240))
        screen.blit(self.font_info.render(fact1, True, (200, 200, 200)), (130, 300))
        screen.blit(self.font_info.render(fact2, True, (130, 200, 200)), (130, 330))
        
        screen.blit(self.font_info.render("Press SPACE to start Frying Paneer", True, (255, 255, 255)), (230, 420))