import pygame
import os

class Level7:
    def __init__(self):
        self.done = False          
        self.ready_to_move = False 
        self.next_level = "QUIZ_LEVEL"
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_info = pygame.font.SysFont("Verdana", 18)
        
        # Difficulty Logic
        self.required_order = ["gravy", "rice", "onions", "nuts", "paneer"]
        self.current_layer = 0
        self.pressure_meter = 0 # If this hits 100, the pot "explodes" (fail)
        self.is_sealing = False
        self.seal_progress = 0
        
        # Drag and Drop Logic
        self.dragging = None
        self.drag_offset = (0, 0)
        
        self.assets = self.load_assets()
        self.ingredients = []
        for i, name in enumerate(self.required_order):
            # Scatter ingredients on the table
            self.ingredients.append({
                "name": name, 
                "rect": pygame.Rect(50, 110 + (i * 95), 100, 80),
                "in_pot": False,
                "original_pos": (50, 110 + (i * 95))
            })
            
        self.pot_rect = pygame.Rect(350, 200, 400, 400)
        self.layers_in_pot = []
        self.message = "DRAG the ingredients in order into the pot (gravy, rice, onions, nuts, paneer)!"
    def load_assets(self):
        loaded = {}
        # Map the Level 7 logic names to your actual filenames
        file_map = {
            "gravy": "gravy.png",
            "rice": "basmati_rice.png", 
            "onions": "onions.png",
            "nuts": "cashew.png",       
            "paneer": "paneer.png"
        }

        for name, filename in file_map.items():
            path = os.path.join("assets", "images", filename)
            try:
                # Load and scale for the side menu
                img = pygame.image.load(path).convert_alpha()
                loaded[name] = pygame.transform.scale(img, (100, 80))
                
                # Load and scale for the pot (the stacked layers)
                loaded[f"{name}_big"] = pygame.transform.scale(img, (350, 250))
                print(f"Loaded {filename} successfully.")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                # Fallback to colored surfaces if images still fail
                fallback_cols = {
                    "gravy": (150, 50, 0),
                    "rice": (255, 255, 255),
                    "onions": (101, 67, 33),
                    "nuts": (210, 180, 140),
                    "paneer": (255, 250, 240)
                }
                surf = pygame.Surface((100, 80))
                surf.fill(fallback_cols.get(name, (200, 200, 200)))
                loaded[name] = surf
                
                big_surf = pygame.Surface((350, 250), pygame.SRCALPHA)
                big_surf.fill((*fallback_cols.get(name, (200, 200, 200)), 180))
                loaded[f"{name}_big"] = big_surf
        return loaded

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return

            # 1. START DRAGGING
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_sealing:
                    # Seal mini-game (Click the pot rim)
                    if self.pot_rect.collidepoint(event.pos):
                        self.seal_progress += 10
                else:
                    # Check if clicking on an ingredient that hasn't been added yet
                    for ing in self.ingredients:
                        if ing["rect"].collidepoint(event.pos) and not ing["in_pot"]:
                            self.dragging = ing
                            # Calculate offset so the item doesn't "snap" its corner to the mouse
                            self.drag_offset = (ing["rect"].x - event.pos[0], ing["rect"].y - event.pos[1])
                            break # Only drag one item at a time

            # 2. DROP INGREDIENT
            if event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    # Check if the ingredient was dropped over the pot
                    # Use a slightly larger collision area for the pot to make it easier
                    if self.pot_rect.inflate(50, 50).collidepoint(event.pos):
                        self.attempt_drop()
                    else:
                        # Snap back to original side-menu position
                        self.dragging["rect"].topleft = self.dragging["original_pos"]
                    self.dragging = None

            if self.done and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Level 7 Complete. Transitioning to Quiz...") # Debug check
                    self.ready_to_move = True

    def update(self):
        # 3. UPDATE POSITION WHILE DRAGGING
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.dragging["rect"].x = mouse_x + self.drag_offset[0]
            self.dragging["rect"].y = mouse_y + self.drag_offset[1]
        
        # Steam Pressure Timer
        if not self.done:
            self.pressure_meter += 0.05
            if self.pressure_meter >= 100:
                self.done = True

    def attempt_drop(self):
        if self.dragging["name"] == self.required_order[self.current_layer]:
            self.dragging["in_pot"] = True
            self.layers_in_pot.append(self.dragging["name"])
            self.current_layer += 1
            if self.current_layer == len(self.required_order):
                self.is_sealing = True
                self.message = "ALL IN! CLICK THE RIM RAPIDLY TO SEAL WITH DOUGH!"
        else:
            self.pressure_meter += 20 # Penalty for wrong order
            self.dragging["rect"].topleft = self.dragging["original_pos"]
            self.message = "Wrong Layer! The steam is leaking!"



    def draw(self, screen):
        screen.fill((255, 248, 230))
        
        # Draw HUD & Pressure Meter
        pygame.draw.rect(screen, (101, 67, 33), [0, 0, 800, 100])
        p_col = (255, 255, 0) if self.pressure_meter < 70 else (255, 0, 0)
        pygame.draw.rect(screen, (50, 50, 50), [550, 40, 200, 20])
        pygame.draw.rect(screen, p_col, [550, 40, self.pressure_meter * 2, 20])
        screen.blit(self.font_info.render("STEAM PRESSURE", True, (255, 255, 255)), (550, 15))
        
        screen.blit(self.font_info.render(self.message, True, (255, 255, 0)), (20, 60))

        # Pot
        pygame.draw.circle(screen, (50, 50, 50), (500, 380), 200)
        
        # Draw stacked layers
        for i, layer in enumerate(self.layers_in_pot):
            screen.blit(self.assets[f"{layer}_big"], (325, 300 - (i * 15)))

        # Draw Ingredients on table
        for ing in self.ingredients:
            if not ing["in_pot"]:
                screen.blit(self.assets[ing["name"]], ing["rect"])

        # Dragging item
        if self.dragging:
            self.dragging["rect"].topleft = (pygame.mouse.get_pos()[0] + self.drag_offset[0], 
                                            pygame.mouse.get_pos()[1] + self.drag_offset[1])

        # Sealing visual (Dough ring)
        # Sealing visual (Dough ring)
        if self.is_sealing:
            # Create a surface for the dough
            dough_surf = pygame.Surface((420, 420), pygame.SRCALPHA)
            
            # 1. Draw with 3 RGB values (No alpha here)
            pygame.draw.circle(dough_surf, (245, 245, 220), (210, 210), 200, 15)
            
            # 2. Set the transparency of the whole surface separately
            alpha = int((self.seal_progress / 100) * 255)
            dough_surf.set_alpha(alpha)
            
            # 3. Blit it to the main screen
            screen.blit(dough_surf, (290, 170))

        if self.done: self.draw_result(screen)

    def draw_result(self, screen):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        screen.blit(overlay, (0, 0))
        
        if self.seal_progress >= 100:
            txt, col = "BIRYANI PERFECTED!", (50, 255, 50)
            fact = "The dough seal (Purdah) creates a pressure-cooker effect."
        else:
            txt, col = "POT EXPLODED!", (255, 50, 50)
            fact = "The steam pressure was too high. You lost the flavor!"
            
        screen.blit(self.font_main.render(txt, True, col), (270, 250))
        screen.blit(self.font_info.render(fact, True, (200, 200, 200)), (120, 310))
        screen.blit(self.font_info.render("Press SPACE to answer some questions and GET YOUR CERTIFICATE!!", True, (255, 255, 255)), (230, 400))