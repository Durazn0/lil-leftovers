from pathlib import Path
from typing import List
from attribute_split import attributes
import json
DATA_NAMESPACE = 'lil'
PROJECT_DIR = Path(__file__).parent.parent.parent.resolve() / "origindatapack"
DATAPACK = PROJECT_DIR / "generated" / "data"

class Character:
    power_dest = DATAPACK / DATA_NAMESPACE / "powers"
    origin_dest = DATAPACK / DATA_NAMESPACE / "origins"
    power_dest.mkdir(parents=True, exist_ok=True)
    origin_dest.mkdir(parents=True, exist_ok=True)

    def __init__(self, char_file: Path):
        try:
            with open(char_file, 'r') as file:
                self.data = json.load(file)

            self.origin = char_file.name[:-5]  # Get rid of the .json
            self.powers = self.data["powers"]
            self.upgrades = []

            # Read to check the values
            self.data["name"]
            self.data["last"]
            self.data["meta"]["goal"]
            self.data["attributes"]
            self.data["description"]
            self.data["attributes"]["height"]

        except json.decoder.JSONDecodeError:
            print(f"Failed to parse {char_file.name}")
        except KeyError as e:
            print(f"Missing {e} in {char_file.name}")


    def generate_attributes(self):
        """Genereate the main attributes file for each character"""
        attrpower = f'{self.origin}_attributes'
        self.powers += [f'{DATA_NAMESPACE}:{attrpower}']
        with open(self.power_dest / f"{attrpower}.json", "w") as file:
            power = {
                "type": "origins:multiple",
                "name": self.data["name"] + "attributes",
                "description": self.data["meta"]["goal"]
            }
            # Implement attributes in the multiple
            power |= attributes(self.data["attributes"])

            json.dump(power, file, indent=2)

    def generate_origin(self):
        # TODO: IMPLEMENT ALL THE DATA INTO THE ORIGIN
        with open(self.origin_dest / f"{self.origin}.json", "w") as file:
            origin = {
                "powers": self.powers,
                "icon": f'kubejs:{self.data["name"].lower()}',
                "order": int(self.origin[:3]),
                "impact": 0,
                "name": f'{self.data["name"]} {self.data["last"]}',
                "description": self.data["description"],
                # "upgrades": self.upgrades + ["001_sensei"] if self.data["name"] != "Sensei" else self.upgrades
                # TODO: Make and include the achievement to get the origin
            }
            origin["unchoosable"] = (origin["order"] > 21)

            json.dump(origin, file, indent=2)


class Layer():
    def __init__(self, namespace: str, description: str):
        self.namespace = namespace
        self.description = description
        self.origins: List[Character] = []

    def get_origins(self, character_path: Path):
        self.origins = [Character(character_file) for character_file in (character_path).glob("*")]
    
    
    # NOTE: molo stands for main origins layer overide
    def generate(self, molo: bool):
        origins = []
        for character in self.origins:
            name = character.data["name"].lower
            # if name in character_mapping:
            #     character.upgrades += character_mapping["name"]

            character.generate_attributes()
            character.generate_origin()
            origins.append(f"{self.namespace}:{character.origin}")

        data = {
            "gui_title": {"choose_origin": self.description},
            "origins": origins,
        }
        data |= {"replace": True} if molo else {}
        layer_namespace = "origins" if molo else self.namespace
        layer_path = DATAPACK / layer_namespace / "origin_layers" 
        layer_path.mkdir(parents=True, exist_ok=True)
        layer_path /= "origins.json" 
        
        with open(layer_path, 'w') as file:
            json.dump(data, file, indent=2)


# TODO: Create non-numbered characters
character_mapping = {
    "ami": ["sekai"],
    "ayane": ["031_osako", "todd", "himawari"],
    "chika": ["025_chinami", "chiaki"],
    "chinami": ["chiaki", "010_chika"],
    "chiaki": ["025_chinami", "010_chika"],
    "futaba": ["034_imani"],
    "makoto": ["027_maki"],
    "rin": ["035_rika", "023_haruka"],
    "sana": ["022_sara"],
    "yumi": ["028_yuki", "024_kaori"],
    "kaori": ["036_nao", "john"],
    "nao": ["frog"],
    "osako": ["030_wakana"],
    "kirin": ["026_karin"],
    "molly": ["023_haruka"],
    "noriko": ["029_niki"],
    "otoha": ["029_niki"],
    "touka": ["032_tsubasa", "033_tsukasa"],
    "tsubasa": ["032_tsubasa", "014_touka"],
    "tsukasa": ["014_touka", "033_tsukasa"],
    "tsuneyo": ["noodles"]
}
