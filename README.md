
# Bombastic Biryani Chef by Nishka Komanduri

**Bombastic Biryani Chef** is an educational, state-based cooking simulator built with Python and Pygame. It takes players through the 7-stage process of creating a authentic Paneer Dum Biryani, concluding with a Final Chef's Exam and certificate.

## Architecture

The game is built using a **Custom State Machine Engine**. This allows for modular level design where each stage of the cooking process is isolated into its own logic class.

* **Engine:** `src/engine.py` manages the transition logic and event propagation.
* **State Contract:** Every level implements a standard interface:
* `handle_events()`: Manages user input (Mouse/Keyboard).
* `update()`: Handles physics, timers, and win/loss conditions.
* `draw()`: Renders the UI and ingredients (assets) to the screen.



## Gameplay Mechanics

| Level     | Name          | Mechanic           | Goal                                                     |
| --------- | --------------| ------------------ | -------------------------------------------------------- |
| **L1-L2** | The Gathering | Physics Collision  | Catch falling ingredients in the bowl.                   |
| **L3**    | Paneer Sear   | Precision Clicking | Click exactly 12 times for a perfect golden fry.         |
| **L4-L5** | The Masala    | Heat Management    | Balancing sautéing without burning the base.             |
| **L6**    | Al Dente Race | Timing/Precision   | Hit **SPACE** at exactly 95% rice doneness.              |
| **L7**    | The Assembly  | Logic & Pressure   | Layer ingredients correctly under rising steam pressure. |
| **Exam**  | Final Quiz    | Randomized QA.     | Score 4/5 on culinary theory to win.                     |

## Bug Log & Development Iterations

During this hackathon, the following critical issues were encountered and resolved by me:

1. **State Bleeding:** Fixed a transition "loop" where levels would skip instantly. Resolved by forcing a `ready_to_move` reset in the Engine.
2. **Asset Mapping:** Resolved "Black Box" errors by implementing a filename translation layer (e.g., mapping `rice` logic to `basmati_rice.png`).
3. **Visual Logic:** Fixed a `ValueError` in the dough seal rendering by utilizing `SRCALPHA` surfaces for transparency instead of RGBA tuples in draw calls.
4. **UX Balancing:** Re-engineered Level 3 from an infinite clicker to a precise 12-click mechanic based on user feedback.

## Installation & Running

1. **Requirements:**
* Python 3.10+
* Pygame Library (`pip install pygame`)


2. **Run the Game:**
Navigate to the root directory and run:
```bash
python3 -m src.main

```


3. **Controls:**
* **Mouse:** Drag/Click ingredients.
* **Space:** Advance levels / Precision timing.
* **1, 2, 3:** Quiz selection.
