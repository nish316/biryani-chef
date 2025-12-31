import os

def create_structure():
    # Get the absolute path where the script is running
    base_path = os.getcwd()
    print(f"Installing project at: {base_path}\n")

    dirs = [
        "assets/images", "assets/sounds", "assets/fonts",
        "src/levels", "data"
    ]

    files = {
        "src/main.py": "import pygame\nprint('Game Starting...')",
        "src/engine.py": "class StateMachine:\n    pass",
        "data/facts.json": '{"level1": "Spices are seeds, fruits, or bark!"}',
        "requirements.txt": "pygame-ce",
        "README.md": "# Biryani Chef\n7 Levels of Culinary Coding",
        ".gitignore": "__pycache__/\n.venv/\n*.pyc"
    }

    # Add Level files
    for i in range(1, 8):
        files[f"src/levels/level{i}.py"] = f"class Level{i}:\n    def __init__(self): pass"

    # Create Directories
    for d in dirs:
        path = os.path.join(base_path, d)
        os.makedirs(path, exist_ok=True)
        print(f"Verified Directory: {d}")

    # Create Files
    for filename, content in files.items():
        file_path = os.path.join(base_path, filename)
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Created File: {filename}")

if __name__ == "__main__":
    create_structure()
    print("\n[SUCCESS] If you don't see files, restart VS Code or refresh the Explorer (icon at top left).")