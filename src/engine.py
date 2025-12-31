import pygame

class StateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.state_name = None

    def add_state(self, name, state_obj):
        self.states[name] = state_obj

    def set_state(self, name):
        self.state_name = name
        self.current_state = self.states[name]
        # Reset the level's 'done' flag when we enter it
        self.current_state.done = False 

    # Inside engine.py
    def update(self):
        if self.current_state and self.current_state.ready_to_move:
            # 1. Get the name of the next level
            next_state_name = self.current_state.next_level
            
            # 2. IMPORTANT: Reset the 'ready' flag of the level we are LEAVING
            self.current_state.ready_to_move = False 
            
            # 3. Switch to the new state
            self.current_state = self.states[next_state_name]
            
        if self.current_state:
            self.current_state.update()

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)