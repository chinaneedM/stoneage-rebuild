import struct
import tempfile
import unittest
from pathlib import Path

from tools.stoneage_itemset_schema_probe import INDEX, SCHEMA
from tools.stoneage_recovered25_attack_magic_runtime import (
    NONPLAYER_ITEM_ROLE,
    load_recovered25_attack_magic_runtime,
)


def petskill_row(skill_id, magic_id, item_id):
    chars = [
        "Display",
        "Comment",
        "PETSKILL_AttackMagic",
        f"magic={magic_id} item={item_id}",
        "",
        "",
    ]
    ints = [skill_id, 1, 3, 0, 0]
    return ",".join(chars + [str(x) for x in ints] + ["tail"])


def item_row(item_id, magic_id, magicusemp=5):
    row = [""] * len(SCHEMA)
    row[INDEX["id"]] = str(item_id)
    row[INDEX["magicid"]] = str(magic_id)
    row[INDEX["magicusemp"]] = str(magicusemp)
    for index, (_, kind) in enumerate(SCHEMA):
        if kind in {"int", "bool"} and row[index] == "":
            row[index] = "0"
    return ",".join(row)


def attmagic_record(matrix):
    values = [0] * 18 + [int(x) for row in matrix for x in row]
    return struct.pack("<33I", *values)


def write_fixture(root: Path, *, bad_item_magic=False):
    single = (
        (0, 0, 0, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 0, 0, 0),
    )
    whole = (
        (1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1),
        (0, 0, 0, 0, 0),
    )

    skills = []
    magics = []
    items = []
    matrices = {0: single, 1: single}
    for offset, magic_id in enumerate(range(301, 326)):
        skill_id = 1001 + offset
        item_id = 19647 + offset
        idx = 2 + offset
        skills.append(petskill_row(skill_id, magic_id, item_id))
        option = "地|100|1".encode("cp950")
        magics.append(
            b"D,C,MAGIC_AttMagic,"
            + option
            + f",{magic_id},1,1,0,{idx}\n".encode("ascii")
        )
        linked_magic = magic_id + 1 if bad_item_magic and magic_id == 301 else magic_id
        items.append(item_row(item_id, linked_magic))
        matrices[idx] = whole if magic_id == 305 else single

    (root / "petskill.txt").write_text(
        "\n".join(skills) + "\n",
        encoding="ascii",
    )
    (root / "magic.txt").write_bytes(b"".join(magics))
    (root / "itemset.txt").write_text(
        "\n".join(items) + "\n",
        encoding="ascii",
    )

    records = []
    for idx in range(27):
        matrix = matrices[idx]
        records.append(attmagic_record(matrix))
        records.append(attmagic_record(matrix))
    (root / "attmagic.bin").write_bytes(b"".join(records))


class Recovered25AttackMagicRuntimeTests(unittest.TestCase):
    def test_loader_closes_twenty_five_row_crosslink(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_fixture(root)
            runtime = load_recovered25_attack_magic_runtime(data_dir=root)
            self.assertEqual(len(runtime.entries), 25)
            self.assertEqual(
                {entry.magic_id for entry in runtime.entries.values()},
                set(range(301, 326)),
            )
            self.assertEqual(
                {entry.item_magicusemp for entry in runtime.entries.values()},
                {5},
            )
            self.assertEqual(runtime.nonplayer_item_role, NONPLAYER_ITEM_ROLE)

    def test_single_target_enemy_plan_has_exact_source_order(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_fixture(root)
            runtime = load_recovered25_attack_magic_runtime(data_dir=root)
            skill_id = runtime.skill_id_for_magic(301)
            plan = runtime.resolve_enemy_footprint(
                skill_id=skill_id,
                actor_slot=15,
                target_slot=0,
                alive_player_slots=range(10),
            )
            self.assertEqual(plan.magic_id, 301)
            self.assertEqual(plan.item_config_id, 19647)
            self.assertEqual(plan.target_membership, (0,))
            self.assertTrue(plan.source_sort_portable)
            self.assertEqual(plan.source_target_order, (0,))

    def test_multitarget_nonportable_plan_fails_closed_when_exact_required(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_fixture(root)
            runtime = load_recovered25_attack_magic_runtime(data_dir=root)
            skill_id = runtime.skill_id_for_magic(305)
            with self.assertRaisesRegex(ValueError, "SortLoc/qsort"):
                runtime.resolve_enemy_footprint(
                    skill_id=skill_id,
                    actor_slot=15,
                    target_slot=0,
                    alive_player_slots=range(10),
                )
            plan = runtime.resolve_enemy_footprint(
                skill_id=skill_id,
                actor_slot=15,
                target_slot=0,
                alive_player_slots=range(10),
                require_exact_source_order=False,
            )
            self.assertEqual(set(plan.target_membership), set(range(10)))
            self.assertFalse(plan.source_sort_portable)
            self.assertIsNone(plan.source_target_order)

    def test_multitarget_magic_can_become_portable_with_one_alive_target(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_fixture(root)
            runtime = load_recovered25_attack_magic_runtime(data_dir=root)
            skill_id = runtime.skill_id_for_magic(305)
            plan = runtime.resolve_enemy_footprint(
                skill_id=skill_id,
                actor_slot=15,
                target_slot=0,
                alive_player_slots=(0,),
            )
            self.assertEqual(plan.target_membership, (0,))
            self.assertEqual(plan.source_target_order, (0,))

    def test_item_magic_crosslink_drift_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_fixture(root, bad_item_magic=True)
            with self.assertRaisesRegex(ValueError, "magicid does not match"):
                load_recovered25_attack_magic_runtime(data_dir=root)


if __name__ == "__main__":
    unittest.main()
