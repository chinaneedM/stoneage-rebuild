#!/usr/bin/env python3
"""Reference model for the stable four-hometown StoneAge birth linkage."""

HOMETOWNS = (
    {
        "index": 0,
        "village": "萨姆吉尔村",
        "elder_floor": 1006,
        "elder_x": 15,
        "elder_y": 22,
        "starter_enemy_id": 1,
        "starter_pet_name_hint": "乌力",
    },
    {
        "index": 1,
        "village": "玛丽娜丝村",
        "elder_floor": 2006,
        "elder_x": 20,
        "elder_y": 16,
        "starter_enemy_id": 2,
        "starter_pet_name_hint": "凯比",
    },
    {
        "index": 2,
        "village": "加加村",
        "elder_floor": 3006,
        "elder_x": 21,
        "elder_y": 16,
        "starter_enemy_id": 3,
        "starter_pet_name_hint": "克克尔",
    },
    {
        "index": 3,
        "village": "卡鲁它那村",
        "elder_floor": 4006,
        "elder_x": 14,
        "elder_y": 20,
        "starter_enemy_id": 4,
        "starter_pet_name_hint": "威伯",
    },
)


def birth_state(hometown):
    """Return the stable ordinary four-village creation linkage."""
    hometown = int(hometown)
    if hometown < 0 or hometown >= len(HOMETOWNS):
        raise ValueError("hometown must be 0..3")
    row = dict(HOMETOWNS[hometown])
    row["last_talk_elder"] = hometown
    row["savepoint_bit"] = 1 << hometown
    row["starter_pet_level"] = 1
    return row


def unified_malinasi_spawn(hometown):
    """Later Bismarck `_UNIFIDE_MALINASI` location override only.

    This preserves the original hometown savepoint bit while forcing the
    initial elder/spawn index to 1. It intentionally does not alter starter
    pet choice because that belongs to a separate later configuration path.
    """
    base = birth_state(hometown)
    spawn = HOMETOWNS[1]
    base.update(
        {
            "elder_floor": spawn["elder_floor"],
            "elder_x": spawn["elder_x"],
            "elder_y": spawn["elder_y"],
            "last_talk_elder": 1,
        }
    )
    return base
