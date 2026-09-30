import json
import unittest
from pathlib import Path
from types import MappingProxyType

from tools.stoneage_local_runtime_core import (
    BOOTSTRAP_SCHEMA,
    LOCAL_SESSION_SCHEMA,
    FreshStartRouteContract,
    LocalRuntimeSessionState,
    StateGatedTransitionContract,
    decode_local_runtime_session,
    encode_local_runtime_session,
    load_runtime_bootstrap_contract,
    load_runtime_bootstrap_file,
)
from tools.stoneage_singleplayer_domain import (
    MapPosition,
    PersistentPlayerState,
    PlayerState,
)

ROOT=Path(__file__).resolve().parents[1]
BOOTSTRAP=ROOT/"game"/"RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"


class LocalRuntimeCoreTests(unittest.TestCase):

    def test_real_bootstrap_contract_loads_and_preserves_provenance(self):
        profile=load_runtime_bootstrap_file(BOOTSTRAP)
        self.assertEqual(profile.schema_id,BOOTSTRAP_SCHEMA)
        self.assertEqual(profile.historical_foundation,"taiwan-v1.0")
        self.assertEqual(profile.runtime_world_profile,"recovered25")
        self.assertEqual(profile.runtime_world_evidence_role,"LATER_RECOVERED")
        self.assertEqual(profile.materializable_floor_count,826)
        self.assertEqual(profile.reachable_floor_count,826)
        self.assertEqual(profile.remaining_unreachable_floor_count,0)
        self.assertEqual(set(profile.routes),{1,2,3,4})
        self.assertEqual(
            profile.routes[3].milestones,
            ("COMBAT","SHOP","WARPMAN"),
        )
        self.assertEqual(
            profile.routes[4].milestones,
            ("SHOP","COMBAT","WARPMAN"),
        )
        self.assertTrue(all(not x.unconditional for x in profile.transitions.values()))

    def test_bootstrap_rejects_provenance_promotion(self):
        payload=json.loads(BOOTSTRAP.read_text(encoding="utf-8"))
        payload["runtime_world_profile"]["historical_membership_in_taiwan_v1"]="PROVEN"
        with self.assertRaises(ValueError):
            load_runtime_bootstrap_contract(payload)

        payload=json.loads(BOOTSTRAP.read_text(encoding="utf-8"))
        payload["runtime_world_profile"]["may_be_relabelled_as_taiwan_v1_content"]=True
        with self.assertRaises(ValueError):
            load_runtime_bootstrap_contract(payload)

    def test_state_gated_transition_cannot_be_unconditional(self):
        with self.assertRaises(ValueError):
            StateGatedTransitionContract(
                transition_id="x",
                kind="WARPMAN",
                unconditional=True,
                source_profile="recovered25",
                raw={},
            )

    def test_route_contract_requires_closed_ordered_state(self):
        with self.assertRaises(ValueError):
            FreshStartRouteContract(
                ordinal=1,
                route_class="CLASSIC",
                requires_shop=False,
                requires_warpman=False,
                milestones=("COMBAT",),
                ordered=False,
            )

    def test_local_session_roundtrip_wraps_existing_player_persistence(self):
        player=PersistentPlayerState(
            character=PlayerState(
                MappingProxyType({
                    "hp":100,
                    "max_hp":100,
                    "level":5,
                    "name":"Hero",
                })
            )
        )
        state=LocalRuntimeSessionState(
            contract_id="stoneage.recovered25.local-first-bootstrap.r1",
            world_profile="recovered25",
            hometown_ordinal=3,
            player_position=MapPosition(1000,10,11),
            player_state=player,
            world_flags=frozenset({"award_chain_open","bridge_item_bought"}),
        )
        encoded_a=encode_local_runtime_session(state)
        encoded_b=encode_local_runtime_session(state)
        self.assertEqual(encoded_a,encoded_b)
        payload=json.loads(encoded_a)
        self.assertEqual(payload["schema"],LOCAL_SESSION_SCHEMA)
        self.assertNotIn("runtime_object_id",encoded_a)

        restored=decode_local_runtime_session(
            encoded_a,
            expected_contract_id=state.contract_id,
            expected_world_profile="recovered25",
        )
        self.assertEqual(restored.player_position,MapPosition(1000,10,11))
        self.assertEqual(restored.hometown_ordinal,3)
        self.assertEqual(restored.world_flags,state.world_flags)
        self.assertEqual(restored.player_state.character.fields["name"],"Hero")

    def test_local_session_rejects_contract_or_profile_drift(self):
        state=LocalRuntimeSessionState(
            contract_id="c1",
            world_profile="recovered25",
            hometown_ordinal=1,
            player_position=MapPosition(1,2,3),
            player_state=PersistentPlayerState(),
        )
        encoded=encode_local_runtime_session(state)
        with self.assertRaises(ValueError):
            decode_local_runtime_session(encoded,expected_contract_id="c2")
        with self.assertRaises(ValueError):
            decode_local_runtime_session(encoded,expected_world_profile="taiwan-v1.0")


if __name__=="__main__":
    unittest.main()
