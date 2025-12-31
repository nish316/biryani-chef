import pygame
import random

class QuizLevel:
    def __init__(self):
        self.done = False
        self.ready_to_move = False
        self.next_level = "WIN_SCREEN"
        
        self.font_main = pygame.font.SysFont("Verdana", 24, bold=True)
        self.font_info = pygame.font.SysFont("Verdana", 18)
        
        self.question_bank = [
            {"q": "Why rinse rice?", "a": "Remove Starch", "o": ["Remove Starch", "Add Salt", "Make it Soft"]},
            {"q": "What is 'Birista'?", "a": "Fried Onions", "o": ["Boiled Rice", "Fried Onions", "Spicy Sauce"]},
            {"q": "When does yogurt curdle?", "a": "On High Heat", "o": ["On Low Heat", "On High Heat", "When Cold"]},
            {"q": "What is 'Al Dente'?", "a": "95% Cooked", "o": ["50% Cooked", "100% Cooked", "95% Cooked"]},
            {"q": "Why use 'Dum'?", "a": "To Trap Steam", "o": ["To Trap Steam", "To Fry Rice", "To Cool Down"]},
            # ... add more from the list above here ...
        ]
        
        self.questions = random.sample(self.question_bank, 5)
        self.current_q_index = 0
        self.correct_count = 0
        self.message = "CHEF'S FINAL EXAM: Get 4/5 right to win!"
        self.show_feedback = False
        self.feedback_text = ""

    def check_answer(self, idx):
        q_data = self.questions[self.current_q_index]
        if q_data["o"][idx] == q_data["a"]:
            self.correct_count += 1
            self.feedback_text = "CORRECT!"
            self.feedback_color = (50, 255, 50)
        else:
            self.feedback_text = f"WRONG! It was: {q_data['a']}"
            self.feedback_color = (255, 50, 50)
        
        self.show_feedback = True
        self.feedback_timer = pygame.time.get_ticks() # Record the time of the click

    def update(self):
        # If we are showing feedback, wait 1.5 seconds then move to next question
        if self.show_feedback and not self.done:
            current_time = pygame.time.get_ticks()
            if current_time - self.feedback_timer > 1500: # 1500ms = 1.5 seconds
                self.show_feedback = False
                self.current_q_index += 1
                
                # Check if that was the last question
                if self.current_q_index >= 5:
                    print(f"Quiz Finished! Correct: {self.correct_count}") # Debug
                    self.done = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return
                
            if event.type == pygame.KEYDOWN:
                # ONLY listen for Space if the quiz is 100% finished
                if self.done:
                    if event.key == pygame.K_SPACE:
                        print("SPACE DETECTED - ATTEMPTING EXIT") # Debug
                        if self.correct_count >= 4:
                            self.ready_to_move = True
                        else:
                            self.__init__() # Reset if failed

                # ONLY listen for 1,2,3 if we are NOT showing feedback and NOT done
                elif not self.show_feedback:
                    if event.key == pygame.K_1: self.check_answer(0)
                    if event.key == pygame.K_2: self.check_answer(1)
                    if event.key == pygame.K_3: self.check_answer(2)

    def draw(self, screen):
        screen.fill((40, 20, 0))
        pygame.draw.rect(screen, (101, 67, 33), [50, 50, 700, 500], border_radius=15)
        
        if not self.done:
            q_data = self.questions[self.current_q_index]
            q_text = self.font_main.render(f"Q{self.current_q_index+1}: {q_data['q']}", True, (255, 255, 255))
            screen.blit(q_text, (80, 100))
            
            for i, option in enumerate(q_data["o"]):
                opt_text = self.font_info.render(f"{i+1}. {option}", True, (255, 215, 0))
                screen.blit(opt_text, (100, 200 + (i * 60)))
            
            score_text = self.font_info.render(f"Correct: {self.correct_count}/5", True, (255, 255, 255))
            screen.blit(score_text, (80, 500))
        else:
            result = "SUCCESS!" if self.correct_count >= 4 else "FAILED!"
            res_text = self.font_main.render(f"QUIZ {result} Score: {self.correct_count}/5", True, (255, 255, 255))
            screen.blit(res_text, (200, 250))
            prompt = "Press SPACE to finish" if self.correct_count >= 4 else "Press SPACE to retry"
            screen.blit(self.font_info.render(prompt, True, (200, 200, 200)), (280, 350))