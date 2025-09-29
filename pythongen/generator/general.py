"""Script that reads and actually runs the generation"""
from char_class import Layer, PROJECT_DIR

def main():
    layer = Layer("lil", "Choose your best girl")
    # INFO: Only json files are allowed in the characters/ directory.
    layer.get_origins(PROJECT_DIR / "characters")


    layer.generate(False)



if __name__ == "__main__":
    main()
    
