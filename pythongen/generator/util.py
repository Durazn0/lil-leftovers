from typing import Union, Optional

def generic(name: str, value: Union[int, float], addition: bool = False) -> dict:
    """Used in origins:attribute type of power for generic minecraft attributes"""
    return {
        "name": "@s",
        "attribute": f"minecraft:generic.{name}",
        "operation": "multiply_total" if not addition else "addition",
        "value": round(value, 6)
    }

def command(command: str, value: Optional[Union[int, float]] = None) -> dict:
    """Used in origins:execute_command and selects the entity that does have the power"""
    return {
        "type": "origins:execute_command",
        "command": command + f" {round(value, 6)} @s" if value else " @s"
    }

