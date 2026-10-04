"""Typed recovered25 ID-613 submission; historical numeric COM1 stays unassigned."""
from dataclasses import dataclass
from tools.stoneage_attack_crazed_model import CALLBACK_NAME, COMMAND_NAME, attack_crazed_callback_setup
from tools.stoneage_enemy_spawn_model import SpawnedEnemy
from tools.stoneage_recovered25_petskill_runtime import Recovered25PetSkillRuntime


@dataclass(frozen=True)
class EnemyAiAttackCrazedSubmission:
    participant_id: str
    skill_slot: int
    skill_id: int
    callback: str
    source_target_slot: int
    attack_count: int = 3
    semantic_command_name: str = COMMAND_NAME

    def __post_init__(self):
        if not str(self.participant_id) or not 0 <= int(self.skill_slot) < 7:
            raise ValueError('AttackCrazed participant/skill slot outside admitted domain')
        if int(self.skill_id) != 613 or self.callback != CALLBACK_NAME:
            raise ValueError('AttackCrazed recovered ID/callback drift')
        if not 0 <= int(self.source_target_slot) < 10 or int(self.attack_count) != 3:
            raise ValueError('AttackCrazed target/count outside recovered domain')
        if self.semantic_command_name != COMMAND_NAME:
            raise ValueError('AttackCrazed command symbol drift')
        for key in ('skill_slot','skill_id','source_target_slot','attack_count'):
            object.__setattr__(self,key,int(getattr(self,key)))
        object.__setattr__(self,'participant_id',str(self.participant_id))

    def callback_setup(self, *, fixed_strength, fixed_toughness):
        return attack_crazed_callback_setup(
            actor_kind='enemy',fixed_strength=fixed_strength,fixed_toughness=fixed_toughness,
            skill_array=0,submitted_target=self.source_target_slot,option=b'3',
        )


def resolve_enemy_ai_attack_crazed_submission(spawned: SpawnedEnemy, *, skill_slot: int,
                                             target_slot: int, petskill_runtime: Recovered25PetSkillRuntime):
    rows=tuple(sorted((e for e in petskill_runtime.skills.values() if e.function_name==CALLBACK_NAME),key=lambda e:e.skill_id))
    if tuple(e.skill_id for e in rows) != (613,):
        raise ValueError('AttackCrazed callback population must be exactly ID 613')
    slots=tuple(int(i) for i in spawned.template.skill_slot_ids)
    if len(slots)!=7 or not 0 <= int(skill_slot) < 7 or slots[int(skill_slot)]!=613:
        raise ValueError('AttackCrazed requires authoritative selected seven-slot identity')
    e=rows[0]
    if (e.field,e.target,e.cost,e.illegal,bytes(e.option_bytes))!=(1,1,2,0,b'3'):
        raise ValueError('AttackCrazed verified metadata/OPTION drift')
    return EnemyAiAttackCrazedSubmission(str(spawned.participant.participant_id),int(skill_slot),613,CALLBACK_NAME,int(target_slot))
