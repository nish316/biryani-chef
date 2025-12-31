import pygame
import random
import os
import sys

# Goal based on the recipe requirements for 2 cups rice and spices
SPICE_GOAL = 10 

class Level1:
    def __init__(self):
        self.done = False          # STEP 1: Shows the Result Overlay
        self.ready_to_move = False # STEP 2: Signals Engine to change levels
        self.next_level = "LEVEL2"
        
        self.score = 0
        self.lives = 3
        
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_info = pygame.font.SysFont("Verdana", 18)
        
        # Ingredients refined to your image list and recipe
        self.spices = ["cardamom", "clove", "star_anise", "cinnamon", "bay_leaf"]
        self.staples = ["basmati_rice"]
        self.enemies = ["strawberry", "chocolate"]
        self.all_items = self.spices + self.staples + self.enemies

        # Image Loading
        self.images = {}
        for item in self.all_items:
            path = os.path.join("assets", "images", f"{item}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                self.images[item] = pygame.transform.scale(img, (60, 60))
            except:
                self.images[item] = pygame.Surface((60, 60))
                self.images[item].fill((200, 200, 200))

        # Basket Setup
        try:
            self.basket_img = pygame.image.load(os.path.join("assets", "images", "basket.png")).convert_alpha()
            self.basket_img = pygame.transform.scale(self.basket_img, (130, 80))
        except:
            self.basket_img = pygame.Surface((130, 80))
            self.basket_img.fill((139, 69, 19))
            
        self.basket_rect = self.basket_img.get_rect(midbottom=(400, 580))

        self.falling_items = []
        self.spawn_timer = 0
        self.message = "Collect Cardamom, Cloves & Rice!"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # FIX: Only listen for SPACE if self.done is True (Overlay is visible)
            if self.done:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.score >= SPICE_GOAL: # Only advance if they actually won
                        self.ready_to_move = True
                    else: # If they lost all lives, restart the level
                        self.__init__() 

    def update(self):
        # Stop item movement if the result screen is showing
        if self.done:
            return

        if self.score >= SPICE_GOAL or self.lives <= 0:
            self.done = True
            return

        self.basket_rect.centerx = pygame.mouse.get_pos()[0]

        self.spawn_timer += 1
        if self.spawn_timer > 35:
            name = random.choice(self.all_items)
            is_good = name in self.spices or name in self.staples
            rect = self.images[name].get_rect(center=(random.randint(50, 750), -50))
            self.falling_items.append({"rect": rect, "name": name, "is_good": is_good})
            self.spawn_timer = 0

        for item in self.falling_items[:]:
            item["rect"].y += 5
            
            if item["rect"].colliderect(self.basket_rect):
                if item["is_good"]:
                    self.score += 1
                    display_name = item['name'].replace('_', ' ').title()
                    self.message = f"Perfect! Added {display_name}."
                else:
                    self.lives -= 1
                    self.message = "Wait! Sweets are not for Biryani!"
                self.falling_items.remove(item)
            elif item["rect"].y > 600:
                self.falling_items.remove(item)

    def draw(self, screen):
        screen.fill((255, 250, 240)) 
        
        # HUD Area
        pygame.draw.rect(screen, (46, 139, 87), [0, 0, 800, 90]) 
        title = self.font_main.render("LEVEL 1: PANTRY GATHERING", True, (255, 255, 255))
        stats = self.font_info.render(f"Ingredients: {self.score}/{SPICE_GOAL} | Lives: {self.lives}", True, (255, 255, 255))
        msg = self.font_info.render(self.message, True, (255, 255, 0))
        
        screen.blit(title, (20, 10))
        screen.blit(stats, (20, 45))
        screen.blit(msg, (400, 45))

        screen.blit(self.basket_img, self.basket_rect)
        for item in self.falling_items:
            screen.blit(self.images[item["name"]], item["rect"])
            label = self.font_info.render(item["name"].replace("_", " ").title(), True, (50, 50, 50))
            screen.blit(label, (item["rect"].x, item["rect"].y + 65))

        # IMPORTANT: Draw overlay if self.done is True
        if self.done:
            self.draw_result(screen)

    def draw_result(self, screen):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        if self.score >= SPICE_GOAL:
            txt, col = "CHEF'S TIP: AROMATICS", (50, 255, 50)
            fact = "Whole spices infuse the oil with flavor without adding heat."
            sub_fact = "Aged rice is used so the grains stay separate and firm!"
            action_text = "Press SPACE to Rinse Rice"
        else:
            txt, col = "PANTRY REFILL", (255, 50, 50)
            fact = "The recipe requires aged basmati rice and whole spices."
            sub_fact = "Avoid sweets like strawberries in savory biryani!"
            action_text = "Press SPACE to Try Again"

        screen.blit(self.font_main.render(txt, True, col), (200, 250))
        screen.blit(self.font_info.render(fact, True, (200, 200, 200)), (120, 310))
        screen.blit(self.font_info.render(sub_fact, True, (200, 200, 200)), (120, 340))
        screen.blit(self.font_info.render(action_text, True, (255, 255, 255)), (280, 420))