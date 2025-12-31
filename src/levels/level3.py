import pygame
import os
import random

class Level3:
    def __init__(self):
        self.done = False          # Shows the Result Overlay
        self.ready_to_move = False # Signals Engine to change levels
        self.next_level = "LEVEL4"
        
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_info = pygame.font.SysFont("Verdana", 18)
        
        # Steps: 0: Paneer, 1: Nuts, 2: Wipe Pan
        self.step = 0
        self.progress = 0
        self.images = self.load_assets()
        self.fry_items = []
        self.burnt_bits = []
        self.message = "Step 1: Fry Paneer! Click the blocks to turn them golden."

    def load_assets(self):
        assets = ["paneer", "cashew", "raisin"]
        loaded = {}
        for item in assets:
            path = os.path.join("assets", "images", f"{item}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                loaded[item] = pygame.transform.scale(img, (80, 80))
            except:
                surf = pygame.Surface((80, 80), pygame.SRCALPHA)
                surf.fill((255, 250, 205)) 
                loaded[item] = surf
        return loaded

    def start_step_1(self):
        self.fry_items = []
        positions = [(320, 270), (410, 270), (320, 360), (410, 360)]
        for pos in positions:
            self.fry_items.append({
                "img": self.images["paneer"].copy(), 
                "pos": list(pos), 
                "clicks": 0,
                "type": "paneer"
            })

    def start_step_2(self):
        self.fry_items = []
        for _ in range(4):
            c_pos = [random.randint(300, 430), random.randint(280, 400)]
            r_pos = [random.randint(300, 430), random.randint(280, 400)]
            self.fry_items.append({"img": self.images["cashew"].copy(), "pos": c_pos, "type": "cashew", "clicks": 0})
            self.fry_items.append({"img": self.images["raisin"].copy(), "pos": r_pos, "type": "raisin", "clicks": 0})

    def start_step_3(self):
        self.burnt_bits = []
        for _ in range(20):
            self.burnt_bits.append(pygame.Rect(random.randint(280, 520), random.randint(230, 470), 10, 10))

    def handle_events(self, events):
        for event in events:
            # Result Screen Logic: Check for SPACE to advance
            if self.done:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.ready_to_move = True
                continue

            # Gameplay Logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.step < 2:
                    for item in self.fry_items:
                        rect = item["img"].get_rect(topleft=item["pos"])
                        if rect.collidepoint(mouse_pos):
                            if item["clicks"] < 3:
                                item["clicks"] += 1
                                self.progress += 8.34 
                                
                                # Apply tint without going black
                                if item["type"] == "paneer":
                                    base_img = self.images["paneer"].copy()
                                    target_color = (139, 69, 19) # Golden Brown
                                    item["img"] = self.get_cooked_surf(base_img, target_color, item["clicks"])
                                elif item["type"] == "cashew":
                                    base_img = self.images["cashew"].copy()
                                    target_color = (218, 165, 32) # Light Golden
                                    item["img"] = self.get_cooked_surf(base_img, target_color, item["clicks"])
                                elif item["type"] == "raisin":
                                    new_size = 80 + (item["clicks"] * 3)
                                    item["img"] = pygame.transform.scale(self.images["raisin"], (new_size, new_size))

    def get_cooked_surf(self, base_surf, color, clicks):
        overlay = pygame.Surface(base_surf.get_size(), pygame.SRCALPHA)
        # Apply tint twice per click to hit 12-click target
        alpha = min(clicks * 20, 140) 
        overlay.fill((*color, alpha))
        result = base_surf.copy()
        result.blit(overlay, (0, 0))
        return result

    def update(self):
        if self.done: return

        if not self.fry_items and self.step == 0: self.start_step_1()

        # Step 3 Wipe logic
        if self.step == 2:
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                for bit in self.burnt_bits[:]:
                    tissue_rect = pygame.Rect(mouse_pos[0]-25, mouse_pos[1]-25, 50, 50)
                    if tissue_rect.colliderect(bit):
                        self.burnt_bits.remove(bit)
                        self.progress += 5

        if self.progress >= 100:
            self.progress = 0
            self.step += 1
            if self.step == 1:
                self.start_step_2()
                self.message = "Step 2: Fry Cashews (golden) & Raisins until plump!"
            elif self.step == 2:
                self.fry_items = []
                self.start_step_3()
                self.message = "Step 3: Wipe pan with tissue to remove burnt bits!"
            elif self.step == 3:
                self.done = True # Triggers Result Screen

    def draw(self, screen):
        screen.fill((255, 245, 230))
        pygame.draw.circle(screen, (30, 30, 30), (400, 350), 220) 
        pygame.draw.circle(screen, (70, 70, 70), (400, 350), 200) 
        pygame.draw.rect(screen, (101, 67, 33), [0, 0, 800, 85])
        msg_surf = self.font_info.render(self.message, True, (255, 255, 255))
        screen.blit(msg_surf, (20, 30))
        
        pygame.draw.rect(screen, (150, 150, 150), [200, 540, 400, 20])
        pygame.draw.rect(screen, (255, 215, 0), [200, 540, self.progress * 4, 20])
        
        for bit in self.burnt_bits:
            pygame.draw.rect(screen, (30, 15, 0), bit)
        for item in self.fry_items:
            screen.blit(item["img"], item["pos"])
        
        if self.step == 2:
            m_pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, (240, 240, 240), [m_pos[0]-25, m_pos[1]-25, 50, 50], border_radius=5)
            
        if self.done:
            self.draw_result(screen)

    def draw_result(self, screen):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        txt, col = "FRYING COMPLETE!", (50, 255, 50)
        # Educational Facts
        fact1 = "Paneer is fried first to give it a restaurant-style golden crust."
        fact2 = "Raisins are fried until 'plump' to release sweetness."
        fact3 = "Wiping the pan removes burnt bits so they don't bitter the gravy."
        
        screen.blit(self.font_main.render(txt, True, col), (280, 200))
        screen.blit(self.font_info.render(fact1, True, (200, 200, 200)), (130, 280))
        screen.blit(self.font_info.render(fact2, True, (200, 200, 200)), (130, 310))
        screen.blit(self.font_info.render(fact3, True, (200, 200, 200)), (130, 340))
        
        screen.blit(self.font_info.render("Press SPACE to start the Onion Birista", True, (255, 255, 255)), (230, 430))