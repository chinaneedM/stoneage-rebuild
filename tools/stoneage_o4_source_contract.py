"""Public/source-only finite map observation contract for the PRIVATE O4 viewer.

This is a deterministic research navigation simulator, NOT a reconstructed
original server, client movement algorithm, or NPC runtime. The actual original
graphics and CP950 text remain in the user's private Library, never in CI.
"""
from dataclasses import dataclass
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R15=ROOT/'research/recovered/STONEAGE-SCENE15-DOORWAY-SOURCE-R1.json'
R21=ROOT/'research/recovered/STONEAGE-SCENE21-TOWN1000-SOURCE-R1.json'
R22=ROOT/'research/recovered/STONEAGE-SCENE22-NPC-ARGUMENT-R1.json'
O4=ROOT/'research/recovered/STONEAGE-O4-TWO-SCENE-PRIVATE-ACTUAL-ACCEPTANCE-R1.json'
START=(1001,11,15)
EXPECTED_DOORS=(
    ((1001,10,15),(1000,63,99)),
    ((1000,63,99),(1001,10,15)),
)
NPC=(1000,63,103)


def require(ok,message):
    if not ok:raise ValueError(message)


def evidence():
    r15,r21,r22,w=(json.loads(p.read_bytes()) for p in (R15,R21,R22,O4))
    require(r15['scope']=='PRESERVED_MIXED25_STATIC_DOORWAY_PLUS_MODERN_OFFLINE_OBSERVER_NOT_ORIGINAL_GAME','R15 source provenance changed')
    require(r21['floor']==1000 and not r21['same_official_deployed_build_authenticated'],'R21 original map has not been authenticated as TW1')
    require(r15['views'][1]['source_DAT_sha256']==r21['source_map_sha256'],'two archived original map byte witnesses disagree')
    require(r15['views'][0]['source_DAT_sha256']==w['original_map_dat_sha256']['floor_1001'],'room1001 DAT identity drift')
    require(r21['source_map_sha256']==w['original_map_dat_sha256']['floor_1000'],'town1000 DAT identity drift')
    require(r21['expanded_bounds']==[60,96,66,106],'town bounded source window drift')
    require(r15['views'][0]['inclusive_viewport']==[7,12,13,18],'room bounded source window drift')
    left={(tuple(p['source_xy']),p['layer'],p['map_id']) for p in r15['views'][1]['placements']}
    right={(tuple(p['xy']),p['layer'],p['image_key']) for p in r21['placements'] if p['xy'][1]<=102}
    require(len(left)==len(right)==54 and left==right,'old 1000 overlap no longer identical')
    common=set(r15['resources']) & set(r21['resources'])
    require(len(common)==36,'shared source original-PNG image set changed')
    require(all(r15['resources'][k]['PNG_sha256']==r21['resources'][k]['PNG_sha256'] for k in common),'same original sprite palette/render hashes disagree')
    require(len(r15['views'][0]['placements'])==w['exact_legacy_original_map_source_overlap']['scene15_room_1001_source_tile_and_parts_occurrences']==27,'room input coverage changed')
    require(len(r21['placements'])==w['exact_legacy_original_map_source_overlap']['scene21_town_1000_7x11_source_tile_and_parts_occurrences']==85,'town input coverage changed')
    require(w['exact_legacy_original_map_source_overlap']['exact_placement_triples_equal'] is True and w['exact_legacy_original_map_source_overlap']['all_common_source_image_png_sha256_equal'] is True,'immutable O4 overlap predicate downgraded')
    doors=r15['doorway_pair']
    require(len(doors)==2,'only these two original source links have been qualified')
    require(tuple((d['source_floor'],*d['source_xy']) for d in doors)==tuple(a for a,b in EXPECTED_DOORS),'original source door coordinate drift')
    require(tuple((d['destination_floor'],*d['destination_xy']) for d in doors)==tuple(b for a,b in EXPECTED_DOORS),'original target coordinate drift')
    for i,d in enumerate(doors):
        wd=w['source_create_blocks'][i]
        require(wd['from']==list(EXPECTED_DOORS[i][0]) and wd['to']==list(EXPECTED_DOORS[i][1]) and wd['byte_sha256']==d['source_block']['block_sha256'],'original create span fingerprint conflict')
    require(r22['target']['floor']==NPC[0] and tuple(r22['target']['xy'])==NPC[1:],'NPC source placement changed')
    require(r22['target']['graphic']==16048 and r22['target']['functionset']=='TownPeople','original NPC source identity mismatch')
    require(r22['message']['bytes']==143 and r22['message']['sha256']==w['original_npc_static']['source_message_sha256'],'static original message SHA changed')
    require(w['original_npc_static']['dialogue_game_runtime_executed'] is False,'no original NPC runtime may be inferred from static text')
    require(w['independent_actual_pixel_replay']['total_pixels_compared']==1442557 and w['independent_actual_pixel_replay']['pixels_diff_gt1']==0,'O4 independent browser/Pillow acceptance tampered')
    require(w['source_actual_replay']['original_image_subresources_loaded_in_Chromium']==67,'original viewer image coverage drift')
    require(w['source_actual_replay']['external_http_requests']==0 and w['source_actual_replay']['js_errors']==0,'original private browser safety contract drift')
    require(w['private_output']['original_png_dat_rd_or_script_text_in_git'] is False and w['ci_public_gate_never_reads_private_originals'] is True,'copyright/privacy boundary drift')
    require(all(v is False for v in w['historical_limits'].values()),'historical claim promoted without a new source')
    require(w['overall_percent'] is None and w['stage_a']=='7 PARTIAL + 2 OPEN','restoration stage must remain unknown')
    return r15,r21,r22,w


@dataclass(frozen=True)
class Cursor:
    """Modern manually driven view. Not historical client state."""
    floor:int=START[0]
    x:int=START[1]
    y:int=START[2]
    journal:tuple=()

    @property
    def location(self):
        return (self.floor,self.x,self.y)


def manual_step(c,dx,dy):
    """One orthogonal source-coordinate step; refuses unobserved pixel windows."""
    require(type(dx) is int and type(dy) is int and abs(dx)+abs(dy)==1,'only modern single-grid orthogonal control')
    if c.floor==1001: bounds=(7,12,13,18)
    elif c.floor==1000: bounds=(60,96,66,106)
    else:raise ValueError('unsourced floor')
    x,y=c.x+dx,c.y+dy
    require(bounds[0]<=x<=bounds[2] and bounds[1]<=y<=bounds[3],'original image sample window limit, not historical collision')
    return Cursor(c.floor,x,y,c.journal)


def manual_warp(c):
    """Only manual application of two exact original create target tuples."""
    if c.location==EXPECTED_DOORS[0][0]:dest=EXPECTED_DOORS[0][1]
    elif c.location==EXPECTED_DOORS[1][0]:dest=EXPECTED_DOORS[1][1]
    else:raise ValueError('no certified source doorway at coordinate')
    return Cursor(*dest,c.journal+((c.location,dest,'MANUAL_APPLICATION_NOT_ORIGINAL_GAMEPLAY'),))


def can_inspect_original_document(c):
    """Expose a source-original static NPC document, never execute a dialogue."""
    return c.location==NPC


def sample_tour():
    c=Cursor()
    c=manual_step(c,-1,0)
    c=manual_warp(c)
    for _ in range(4):c=manual_step(c,0,1)
    require(can_inspect_original_document(c),'NPC originally sourced position inaccessible')
    for _ in range(4):c=manual_step(c,0,-1)
    c=manual_warp(c)
    return c


def main():
    _,_,_,w=evidence()
    c=sample_tour()
    require(c.location==(1001,10,15) and len(c.journal)==2,'two-way sourced observation route incomplete')
    print(json.dumps({'O4_PUBLIC_ORIGINAL_DERIVED_CROSSSOURCE_GATE':'PASS',
      'original_image_map_overlap_triples':54,'shared_identical_source_PNGs':36,
      'private_real_browser_decoded_original_images_from_receipt':w['source_actual_replay']['original_image_subresources_loaded_in_Chromium'],
      'private_pixel_replay_checked_from_receipt':w['independent_actual_pixel_replay']['total_pixels_compared'],
      'private_pixel_replay_mismatch_from_receipt':w['independent_actual_pixel_replay']['pixels_diff_gt1'],
      'synthetic_manually_applied_original_doorway_links':2,
      'source_original_NPC_document_coordinate':list(NPC),
      'proprietary_source_executed_in_this_CI':False,'original_game_world_entered':False},
      ensure_ascii=False,sort_keys=True))

if __name__=='__main__':main()
