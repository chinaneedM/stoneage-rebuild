import unittest
from pathlib import Path
from types import MappingProxyType

from tools.stoneage_local_runtime_core import (
    LocalRuntimeSessionState,
    ResolvedTransitionBinding,
    WorldRegionRequest,
    load_runtime_bootstrap_file,
)
from tools.stoneage_recovered25_world_profile_adapter import (
    HOMETOWN_TRANSITION_IDS,
    SHADOWED_BRANCH_TRANSITION_ID,
    Recovered25FreshStartFactory,
    Recovered25TransitionGateEvaluator,
    Recovered25WorldProfileAdapter,
)
from tools.stoneage_singleplayer_domain import (
    InventoryItem,
    InventorySlot,
    ItemTemplateId,
    MapPosition,
    PersistentPlayerState,
    PlayerState,
)
from tools.stoneage_singleplayer_world import LATER_RECOVERED

ROOT=Path(__file__).resolve().parents[1]
BOOTSTRAP=ROOT/"game"/"RUNTIME-BOOTSTRAP-RECOVERED25-R1.json"


def _state(ordinal:int)->PersistentPlayerState:
    return PersistentPlayerState(
        character=PlayerState(
            MappingProxyType({"name":f"seed-{ordinal}","level":1})
        )
    )


class Recovered25WorldProfileAdapterTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile=load_runtime_bootstrap_file(BOOTSTRAP)
        cls.adapter=Recovered25WorldProfileAdapter.from_repository(cls.profile)

    def test_real_adapter_exposes_closed_826_floor_ordered_topology(self):
        self.assertEqual(len(self.adapter.topology.maps),826)
        self.assertEqual(len(self.adapter.topology.legacy_warps),2724)
        self.assertEqual(
            set(self.adapter.topology.maps),
            set(self.adapter.runtime.base.extension.materializable_floor_ids),
        )
        self.assertTrue(
            all(
                definition.provenance is not None
                and definition.provenance.content_role==LATER_RECOVERED
                and not definition.provenance.claims_early_membership
                for definition in self.adapter.topology.maps.values()
            )
        )

    def test_region_materialization_is_provenance_descriptor_not_fake_cache(self):
        floor_id=min(self.adapter.topology.maps)
        definition=self.adapter.topology.maps[floor_id]
        region=self.adapter.materialize_region(WorldRegionRequest(
            floor_id=floor_id,
            x1=0,y1=0,x2=0,y2=0,
            world_profile="recovered25",
        ))
        self.assertEqual(region.payload.floor_id,floor_id)
        self.assertEqual(region.payload.width,definition.width)
        self.assertEqual(region.provenance["content_role"],LATER_RECOVERED)
        self.assertEqual(
            region.provenance["payload_kind"],
            "PROVENANCE_MAP_REGION_DESCRIPTOR",
        )
        with self.assertRaises(ValueError):
            self.adapter.materialize_region(WorldRegionRequest(
                floor_id=floor_id,
                x1=0,y1=0,x2=definition.width,y2=0,
                world_profile="recovered25",
            ))

    def test_all_four_hometown_positions_are_preserved_and_materializable(self):
        positions=self.adapter.hometown_positions()
        self.assertEqual(set(positions),{1,2,3,4})
        self.assertEqual(
            [(p.floor_id,p.x,p.y) for p in positions.values()],
            [(1006,15,22),(2006,20,16),(3006,21,16),(4006,14,20)],
        )
        self.assertTrue(
            all(self.adapter.topology.is_valid_position(p) for p in positions.values())
        )

    def test_fresh_start_factory_binds_hometown_without_inventing_player_state(self):
        factory=Recovered25FreshStartFactory(self.adapter,_state)
        seeds=[factory.create_fresh_start(self.profile,i) for i in range(1,5)]
        self.assertEqual([seed.hometown_ordinal for seed in seeds],[1,2,3,4])
        self.assertEqual(
            [seed.player_state.character.fields["name"] for seed in seeds],
            ["seed-1","seed-2","seed-3","seed-4"],
        )
        self.assertEqual(
            [seed.position for seed in seeds],
            list(self.adapter.hometown_positions().values()),
        )

    def test_item_gate_evaluator_requires_bound_recovered_item(self):
        contract=self.profile.transitions[HOMETOWN_TRANSITION_IDS[3]]
        binding=ResolvedTransitionBinding(
            transition_id=contract.transition_id,
            source=self.adapter.hometown_positions()[3],
            destination=self.adapter.hometown_positions()[1],
            predicate_payload={
                "gate_kind":"FREE_CLAUSES",
                "free_clauses":(({"key":"ITEM","operator":"=","operand":12345},),),
                "item_template_id":12345,
            },
            provenance={"source_profile":"recovered25"},
        )
        state=_state(3)
        session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile="recovered25",
            hometown_ordinal=3,
            player_position=self.adapter.hometown_positions()[3],
            player_state=state,
        )
        evaluator=Recovered25TransitionGateEvaluator(self.profile)
        denied_decision=evaluator.evaluate_transition(contract,binding,session)
        self.assertFalse(denied_decision.allowed)
        self.assertEqual(dict(denied_decision.consumed_state),{})
        state.inventory[InventorySlot(0)]=InventoryItem(
            slot=InventorySlot(0),
            template_id=ItemTemplateId(12345),
            view=MappingProxyType({}),
        )
        allowed_decision=evaluator.evaluate_transition(contract,binding,session)
        self.assertTrue(allowed_decision.allowed)
        self.assertEqual(dict(allowed_decision.consumed_state),{})

    def test_progression_gate_rechecks_current_level_and_item(self):
        contract=self.profile.transitions[SHADOWED_BRANCH_TRANSITION_ID]
        binding=ResolvedTransitionBinding(
            transition_id=contract.transition_id,
            source=MapPosition(811,0,0),
            destination=MapPosition(820,0,0),
            predicate_payload={
                "gate_kind":"FREE_CLAUSES",
                "free_clauses":((
                    {"key":"LV","operator":">","operand":10},
                    {"key":"LV","operator":"<","operand":20},
                    {"key":"ITEM","operator":"=","operand":12345},
                ),),
            },
            provenance={"source_profile":"recovered25"},
        )
        evaluator=Recovered25TransitionGateEvaluator(self.profile)

        missing_item=PersistentPlayerState(
            character=PlayerState(MappingProxyType({"level":15}))
        )
        denied=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile="recovered25",
            hometown_ordinal=1,
            player_position=self.adapter.hometown_positions()[1],
            player_state=missing_item,
        )
        denied_decision=evaluator.evaluate_transition(contract,binding,denied)
        self.assertFalse(denied_decision.allowed)
        self.assertEqual(dict(denied_decision.consumed_state),{})

        slot=InventorySlot(0)
        missing_item.inventory[slot]=InventoryItem(
            slot=slot,template_id=ItemTemplateId(12345),view=MappingProxyType({})
        )
        allowed_decision=evaluator.evaluate_transition(contract,binding,denied)
        self.assertTrue(allowed_decision.allowed)
        self.assertEqual(dict(allowed_decision.consumed_state),{})

        too_high=PersistentPlayerState(
            character=PlayerState(MappingProxyType({"level":25})),
            inventory=dict(missing_item.inventory),
        )
        high_session=LocalRuntimeSessionState(
            contract_id=self.profile.contract_id,
            world_profile="recovered25",
            hometown_ordinal=1,
            player_position=self.adapter.hometown_positions()[1],
            player_state=too_high,
        )
        high_decision=evaluator.evaluate_transition(contract,binding,high_session)
        self.assertFalse(high_decision.allowed)
        self.assertEqual(dict(high_decision.consumed_state),{})


if __name__=="__main__":
    unittest.main()
