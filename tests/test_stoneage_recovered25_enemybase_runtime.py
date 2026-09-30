import tempfile
import unittest
from pathlib import Path
from types import MappingProxyType, SimpleNamespace

from tools.stoneage_recovered25_enemybase_runtime import (
    NAME_ENCODING_STATUS,
    load_recovered25_enemybase_runtime,
)
from tools.stoneage_tw10_25_encounter_bridge import (
    EncounterAreaBridge,
    EnemyVariantBridge,
    GroupBridge,
)


def _enemybase_row(tempno: int) -> str:
    chars = ["UnresolvedName", "", "", "", "", ""]
    vals = [0] * 33
    vals[0] = tempno
    vals[1] = 10
    vals[2] = "5.00"
    vals[3:7] = [10, 20, 30, 40]
    vals[7] = 4
    vals[9:13] = [50, 50, 0, 0]
    vals[26] = 2
    vals[29] = 4
    vals[30] = 1234
    vals[31] = 1
    vals[32] = 0
    return ",".join(chars + [str(x) for x in vals])


class Recovered25EnemybaseRuntimeTests(unittest.TestCase):

    def test_loader_keeps_name_unresolved_and_numeric_template_usable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            data = root / "data"
            data.mkdir()
            (data / "enemybase.txt").write_text(
                _enemybase_row(88) + "\n",
                encoding="ascii",
            )
            setup = root / "setup.cf"
            setup.write_text(
                "enemybasefile=./data/enemybase.txt\n",
                encoding="utf-8",
            )
            runtime = load_recovered25_enemybase_runtime(
                data_dir=data,
                setup=setup,
            )
            self.assertEqual(set(runtime.templates), {88})
            template = runtime.templates[88]
            self.assertIsNone(template.name)
            self.assertEqual(template.tempno, 88)
            self.assertEqual(template.level_up_point, 5)
            self.assertEqual(template.rare, 2)
            self.assertEqual(template.size_class, 0)
            self.assertEqual(runtime.name_encoding_status, NAME_ENCODING_STATUS)

    def test_stable_encounter_template_coverage_is_explicit(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "enemybase.txt").write_text(
                _enemybase_row(88) + "\n",
                encoding="ascii",
            )
            runtime = load_recovered25_enemybase_runtime(data_dir=data)

            area = EncounterAreaBridge.from_encount({
                "INDEX": 1,
                "FLOOR": 100,
                "X1": 0,
                "Y1": 0,
                "X2": 2,
                "Y2": 2,
                "PROB_MIN": 1,
                "PROB_MAX": 2,
                "ENEMY_MAX": 2,
                "ZORDER": 1,
                "GROUP_ID1": 7,
                "GROUP_PROB1": 100,
            })
            group = GroupBridge.from_group({
                "GROUP_ID": 7,
                "ENEMY_ID1": 700,
                "CREATE_PROB1": 100,
            })
            enemy = EnemyVariantBridge.from_enemy({
                "ID": 700,
                "TEMPNO": 88,
                "LV_MIN": 3,
                "LV_MAX": 5,
                "CREATEMAXNUM": 2,
                "CREATEMINNUM": 1,
                "TACTICS": 1,
                "EXP": 100,
                "DUELPOINT": 0,
                "STYLE": 0,
                "PETFLG": 1,
            })
            encounter = SimpleNamespace(
                encounter_areas=(area,),
                groups=MappingProxyType({7: group}),
                enemies=MappingProxyType({700: enemy}),
            )
            self.assertEqual(runtime.referenced_template_ids(encounter), (88,))
            self.assertEqual(runtime.unresolved_template_ids(encounter), ())


if __name__ == "__main__":
    unittest.main()
