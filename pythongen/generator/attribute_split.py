"""Implementation of damage types rendered into functions that returns an Origin power"""

from util import command, generic
PEHKUI = "scale set pehkui:"

# TODO: Get modded damage names/tags (i.e. Create's crushing wheels)
# Hint: Find in generated/resources/data/... in most mods repos

# https://minecraft.wiki/w/Tag#Damage_type_tags
PHYSICAL_DAMAGE_TAGS = (
    "burn_from_stepping", 
    "damages_helmet", 
    "is_drowning",
    "is_fall"
)
MAGICAL_DAMAGE_TAGS = (
    "is_explosion",
    "is_fire",
    "is_freezing",
    "is_lightning"
)
# https://origins.readthedocs.io/en/latest/misc/extras/damage_source_names/
PHYSICAL_DAMAGE_NAMES = (
    "anvil",
    "anvil.player",
    "arrow",
    "arrow.item",
    "cactus",
    "cactus.player",
    "cramming",
    "cramming.player",
    "drown",
    "drown.player",
    "fall",
    "fall.player",
    "fallingBlock",
    "fallingBlock.player",
    "fallingStalactite",
    "fallingStalactite.player",
    "flyIntoWall",
    "flyIntoWall.player",
    "hotFloor",
    "hotFloor.player",
    "inWall",
    "lava",
    "lava.player",
    "mob", # I guess this stuff is physical with on hand objects
    "mob.item",
    "player", # Same idea
    "player.item",
    "stalagmite",
    "stalagmite.player",
    "sting",
    "sting.player",
    "sting.item",
    "sweetBerryBush",
    "sweetBerryBush.player",
    "thrown.item",
    "trident",
    "trident.item",
    "wither",
    "wither.player"
    "origins:no_water_for_gills",
    "origins:no_water_for_gills.player",
    "create:crush",
    "create:mechanical_drill",
    "create:mechanical_saw"
)
MAGICAL_DAMAGE_NAMES = (
    "badRespawnPoint",
    "dragonBreath",
    "dragonBreath.player",
    "explosion",
    "explosion.player",
    "fireball",
    "fireball.player",
    "fireworks",
    "fireworks.player",
    "fireworks.item",
    "freeze",
    "freeze.player",
    "indirectMagic",
    "indirectMagic.item",
    "inFire",
    "inFire.player",
    "lightningBolt",
    "lightningBolt.player",
    "magic",
    "magic.player",
    "onFire",
    "onFire.player",
    "sonic_boom",
    "sonic_boom.player",
    "sonic_boom.item",
    "thorns", # In this category because it is an enchantment
    "thorns.item",
    "witherSkull",
    "origins:genericDamageOverTime",
    "origins:genericDamageOverTime.player",
    "origins:hurt_by_water",
    "origins:hurt_by_water.player",
    "create:fan_fire",
    "create:fan_lava"
)
PHYSICAL_DTC = {
    "type": "origins:or",
    "conditions": [{"type": "origins:in_tag", "tag": tag} for tag in PHYSICAL_DAMAGE_TAGS] + [{"type": "origins:name", "name": name} for name in PHYSICAL_DAMAGE_NAMES] 
}
MAGICAL_DTC = {
    "type": "origins:or",
    "conditions": [{"type": "origins:in_tag", "tag": tag} for tag in MAGICAL_DAMAGE_TAGS] + [{"type": "origins:name", "name": name} for name in MAGICAL_DAMAGE_NAMES]
}

def attributes(bundle: dict) -> dict:
    """Takes the starting JSON file of the character and prepares it for a origins:multiple"""
    powers = {}
    
    # DAMAGE INCREASE
    if "pd" in bundle:
        powers["pd"] = {
            "type": "origins:modify_damage_dealt",
            "damage_condition": PHYSICAL_DTC,
            "modifier": {  # TODO: Check again, maybe too unbalanced
                "operation": "multiply_total_multiplicative",
                "value": bundle["pd"] / 100
            }
        }
    if "md" in bundle:
        powers["md"] = {
            "type": "origins:modify_damage_dealt",
            "damage_condition": MAGICAL_DTC,
            "modifier": {  # TODO: Check again, maybe too unbalanced
                "operation": "multiply_total_multiplicative",
                "value": bundle["md"] / 100
            }
        }

    # DAMAGE REDUCTION
    if "pr" in bundle:
        powers["pr"] = {
            "type": "origins:modify_damage_taken",
            "damage_condition": PHYSICAL_DTC,
            "modifier": {
                "operation": "multiply_total_multiplicative",
                "value": bundle["pr"] / 100
            }
        }
    if "mr" in bundle:
        powers["mr"] = {
            "type": "origins:modify_damage_taken",
            "damage_condition": MAGICAL_DTC,
            "modifier": {
                "operation": "multiply_total_multiplicative",
                "value": bundle["mr"] / 100
            }
        }
    # Generic minecraft attributes
    # https://minecraft.fandom.com/wiki/Attribute
    # https://origins.readthedocs.io/en/1.10.0/types/power_types/attribute/
    powers["generic"] = {
        "type": "origins:attribute",
        "modifiers": []
    }
    if "health" in bundle:
        powers["generic"]["modifiers"] += [generic("max_health", (bundle["health"] - 20) / 20)]
    if "attack_kb" in bundle:
        powers["generic"]["modifiers"] += [generic("attack_knockback", -bundle["kb_resist"], True)]
    if "kb_resist" in bundle:
        powers["generic"]["modifiers"] += [generic("knockback_resistance", bundle["kb_resist"], True)]
    if "speed" in bundle:
        powers["generic"]["modifiers"] += [generic("movement_speed", bundle["speed"])]
    if "attack" in bundle:
        powers["generic"]["modifiers"] += [generic("attack_damage", bundle["attack"])]  # NOTE: The default is 2

    # Pehkui commands and rtp
    # https://modrinth.com/mod/pehkui
    # height_comp = 195 / bundle["height"]
    # Height factor for shorter characters, commented because of the 1.6 factor
    powers["pehkui"] = {
        "type": "origins:action_on_callback",
            "entity_action_added": {
            "type": "origins:and",
            "actions": [
                # 1.6 factor to help with speed of the characters
                # Curanto: Changed to 1 lol
                # 185 is the visual default player size
                command(f"{PEHKUI}base", 1 * bundle["height"] / 185),
                # Normalization of reach
                command(f"{PEHKUI}reach 1"),
                # command(f"{PEHKUI}step_height", height_comp),
                # Random teleport
                # TODO: test command axis, make it work with all quarters
                command(f"execute at @s run spreadplayers ~ ~ 1450 1450 false")
            ]
        }
    }
        
    return powers


