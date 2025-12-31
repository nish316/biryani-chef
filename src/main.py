import pygame
import sys
from src.engine import StateManager
from src.levels.level1 import Level1
from src.levels.level2 import Level2
from src.levels.level3 import Level3
from src.levels.level4 import Level4
from src.levels.level5 import Level5
from src.levels.level6 import Level6
from src.levels.level7 import Level7   
from src.levels.quizlevel import QuizLevel
from src.levels.winscreen import WinScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Biryani Chef Hackathon")
    clock = pygame.time.Clock()

    # Create the Manager
    manager = StateManager()
    
    # Initialize and Add Level 1
    lvl1 = Level1()
    manager.add_state("LEVEL1", Level1())
    manager.add_state("LEVEL2", Level2())
    manager.add_state("LEVEL3", Level3())
    manager.add_state("LEVEL4", Level4())
    manager.add_state("LEVEL5", Level5())
    manager.add_state("LEVEL6", Level6())
    manager.add_state("LEVEL7", Level7())
    manager.add_state("QUIZ_LEVEL", QuizLevel())
    manager.add_state("WIN_SCREEN", WinScreen())
    manager.set_state("LEVEL7")

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            manager.handle_events(events)

        manager.update()
        manager.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()