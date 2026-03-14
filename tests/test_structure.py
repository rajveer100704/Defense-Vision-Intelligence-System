import os

required_dirs = [
    "datasets",
    "models",
    "pipelines",
    "tracking",
    "geospatial",
    "api",
    "dashboard",
    "configs",
    "experiments",
    "tests",
    "logs",
]

def check_structure():
    missing = []
    
    # Check if we are in the correct directory (defense_ai_system)
    # If not, try to append it to the path
    root = "."
    if not os.path.exists("datasets") and os.path.basename(os.getcwd()) != "defense_ai_system":
       print("Warning: datasets directory not found. Are you in defense_ai_system root?")

    for d in required_dirs:
        if not os.path.isdir(os.path.join(root, d)):
            missing.append(d)

    if missing:
        print("Missing directories:", missing)
    else:
        print("All directories verified!")

if __name__ == "__main__":
    check_structure()
