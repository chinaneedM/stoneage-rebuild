"""R73: documentary family/host narrative and two separately qualified cave quests."""
import argparse
import hashlib
import json
import re
import urllib.request
from pathlib import Path
from tools.stoneage_five_brothers_source import Article

ROOT=Path(__file__).resolve().parents[1]
STEM='STONEAGE-CN2003-LIULI-CAVE'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
PROFILE='CN2003_SINA_LIULI_CAVE_EXACT_BUILD_UNKNOWN'
URLS={'S1':'https://games.sina.com.cn/zhqu/sta/article/2003-06-06/11290.shtml',
      'S2':'https://web.archive.org/web/20031204051540id_/http://games.sina.com.cn:80/zhqu/sta/article/2003-06-06/11290.shtml'}
PARSER_PATH='tools/stoneage_five_brothers_source.py'
BOUNDARIES={k:False for k in ('official_authorship_verified','current_raw_is_historical_raw',
    'same_build_tw10_membership_verified','original_server_runtime_verified','original_ids_recovered',
    'father_death_account_is_final_narrative_truth','family_reunion_completed',
    'diary_age_is_son_age','eight_positions_are_eight_npc_instances','drop_means_logout_or_disconnect',
    'side_quest_is_rebirth_required','caption_washing_stone_is_guaranteed_reward',
    'monster_labels_are_complete_pet_roster','original_html_or_assets_committed','stage_b_started')}


def require(ok,message):
    if not ok:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()

def compact(text):return re.sub(r'\s+','',text)


def one(pattern,text):
    matches=re.findall(pattern,text)
    require(len(matches)==1,'Missing/duplicate scoped evidence: '+pattern)
    return matches[0]


def coordinates(text):return [[int(x),int(y)] for x,y in re.findall(r'（东(\d+)，南(\d+)）',text)]


def article(raw):
    text=raw.decode('gb18030',errors='strict')
    require(re.search(r'charset=["\x27]?gb2312',text,re.I),'Declared charset changed')
    date=one(r'<!-- include 发布时间 begin -->(.*?)<!-- include 发布时间 end -->',text)
    require(compact(date)=='2003-06-0614:55','Visible publication changed')
    p=Article();p.feed(text)
    require(p.roots==1 and p.active is None,'Article absent/duplicate/unclosed')
    require(compact(''.join(p.visible)).count('《石器时代》任务功略-琉璃洞窟')==1,'Visible title missing/ambiguous')
    return compact(''.join(p.parts))


def derive(raw):
    body=article(raw)
    require(body.count('琉璃洞窟（二）')==1,'Two quest chapters required')
    main,rest=body.split('琉璃洞窟（二）')
    side,ecology=rest.split('7.琉璃的洞窟',1)
    recommended=int(one(r'1\.等级要求：建议等级(\d+)级',main))
    side_levels=[int(v) for v in one(r'1\.等级要求：(\d+)级，建议等级(\d+)级',side)]
    for chapter in (main,side):
        require('2.特殊要求：解过成人仪式。3.交通工具：步行或骑宠。4.精灵的羽毛：琉璃的羽毛。' in chapter,
                'Separate adulthood/travel/feather requirement changed')
    location=one(r'前往南岛奇喀喀村((?:（东\d+，南\d+）){2})东方「森林的独栋房屋"（东(\d+)，南(\d+)）',main)
    father=one(r'一位中年人「([^"]+)"',main)
    son=one(r'由于'+re.escape(father)+r'的儿子"([^"]+)"',main)
    mother=one(r'寻找母亲"([^"]+)"的行踪',main)
    diary_years=int(one(r'他母亲(\d+)年前所写的日记',main))
    require('在两个星期前整理房子时' in main and father+'只有跟'+son+'讲说他的母亲去世的事情' in main and
            son+'还没行成人仪式，因此不可能进入琉璃洞窟' in main,'Father/child/adulthood narrative changed')
    necklace=one(r'"([^"<>]+的项链)"（魅力([+-]\d+)回避率上升([+-]\d+)）',main)
    diary=one(r'交出"([^"<>]+的日记)"',main)
    require('项链与日记只要掉到地上便会马上消失不见' in main,'Drop-only item lifetime changed')
    search=coordinates(one(r'伊布所出现的坐标位置如下：((?:（东\d+，南\d+）[、。]){8})',main))
    require(len(search)==8 and len({tuple(x) for x in search})==8,'Eight distinct reported search positions required')
    cave_coord=[int(v) for v in one(r'前往琉璃洞窟（东(\d+)，南(\d+)）',main)]
    first=one(r'琉璃洞窟(\d+)楼时，勇者会遇到一只(\d+)级以上的"([^"]+)"',main)
    second=one(r'来到(\d+)楼后，勇者还会遇到一只(\d+)级以上的"([^"]+)"',main)
    guards=[{'floor_as_reported':int(f),'level_lower_word_以上':int(l),'name_as_written':n,
             'original_enemy_id':None,'stats':None} for f,l,n in [first,second]]
    require('击败9楼的"大地守护兽"才能继续前进' in main,'Main guard progression changed')
    onward=[int(v) for v in one(r'通往(\d+)楼的洞口在（东(\d+)，南(\d+)）',main)]
    require('到达11楼时' in main and '有些洞口通往死路，有些洞口会让勇者走回10楼' in main,
            'Limited floor/exit topology changed')
    goddess=one(r'在(\d+)楼看到"女神([^"]+)"',main)
    cycle=int(one(r'宿身是(\d+)年改变一次',main))
    require('此时的宿身正是'+father+'的妻子'+mother in main and
            '在宿身改变的那一年第一个生下小孩的母亲，就会被选为宿身' in main and
            mother+'在未完成使命前，是无法再次与'+father+'父子相会' in main and
            '一直等'+son+'来跟她相见' in main,'Host selection, duty or future reunion narrative changed')
    reward=one(r'6\.获得物品：([^（]+)（((?:[攻防敏魅][+-]\d+)+)([^）]+)）',main)
    require('此任务是四大属性洞窟之一，与转生任务相关，解过此任务才得以进入碧青的洞窟与漆黑的洞窟' in main and
            '收集四大洞窟的证明，就可以换取不错的宝物' in main,'Main follow-on prerequisite scope changed')
    side_start=one(r'前往南岛琉璃洞窟（东(\d+)，南(\d+)）(\d+)楼和"([^"]+)"（东(\d+)，南(\d+)）',side)
    require([int(x) for x in side_start[:2]]==cave_coord,'Cave coordinates disagree between branches')
    target=one(r'回到琉璃洞窟(\d+)楼打一只等级(\d+)几级的([^，]+)，打败[^，]+后就可获得"([^"]+)"',side)
    master=one(r'再向旁边「([^"]+)"说话，即可选择大袋或小袋的礼物',side)
    require('再次前往琉璃洞窟15楼，和女神'+goddess[1]+'说话' in side and
            '6.获得物品：随机。' in side and '玩家可以跟琉璃洞窟（一）一起解' in side and
            '由于跟转生没有相关，因此玩家可自行斟酌解或者不解' in side,'Optional/random reward scope changed')
    caption=one(r'哇~我得到了一块([^6]+)6\.获得物品',side)
    eco_coord=coordinates(one(r'坐标：((?:（东\d+，南\d+）)+)怪物等级',ecology))
    eco_levels=[int(v) for v in one(r'怪物等级：(\d+)~(\d+)级',ecology)]
    labels=one(r'怪物种类：(.+?)琉璃的洞窟1楼',ecology).split('、')
    require(len(labels)==9 and eco_coord==[cave_coord],'Ecology scope/entrance summary changed')
    npcs=[{'name':father,'role':'requesting_father','location':'森林的独栋房屋','coord':[int(v) for v in location[1:]],'floor':None,'npc_id':None},
          {'name':son,'role':'lost_son_diary_handoff','reported_search_positions':search,'spawn_selection':None,'npc_id':None},
          {'name':'女神'+goddess[1],'role':'mother_host_revelation_and_main_reward','floor':int(goddess[0]),'coord':None,'npc_id':None},
          {'name':side_start[3],'role':'optional_request','floor':int(side_start[2]),'coord':[int(v) for v in side_start[4:]],'npc_id':None},
          {'name':master,'role':'optional_bag_choice','floor':15,'coord':None,'npc_id':None}]
    items=[{'name':necklace[0],'role':'narrative_delivery','stats_as_written':{'魅力':int(necklace[1]),'回避率上升':int(necklace[2])},
            'drop_disappears_as_reported':True,'logout_behavior':None,'disconnect_behavior':None,'item_id':None},
           {'name':diary,'role':'narrative_delivery','caption_name_variant':mother+'日记',
            'drop_disappears_as_reported':True,'logout_behavior':None,'disconnect_behavior':None,'item_id':None},
           {'name':reward[0],'role':'main_quest_reward','stats_as_written':{k:int(v) for k,v in re.findall(r'([攻防敏魅])([+-]\d+)',reward[1])},
            'description_as_written':reward[2],'spirit_name':None,'item_id':None},
           {'name':target[3],'role':'optional_enemy_reward_to_bag_choice','item_id':None,'consumed_at_exchange':None}]
    return {'region_label':'南岛','village':'奇喀喀村','village_coordinate_literals':coordinates(location[0]),
        'village_coordinate_frames':None,'cave_entrance_as_reported':cave_coord,
        'main_quest':{'recommended_level':recommended,'hard_entry_level':None,'adult_completion_required_as_reported':True,
            'rebirth_related_as_reported':True,'follow_on_cave_names':['碧青的洞窟','漆黑的洞窟'],
            'four_cave_proofs_exchange_mentioned':True,'four_proofs_reward':None,'event_id':None},
        'side_quest':{'reported_level_requirement':side_levels[0],'recommended_level':side_levels[1],
            'adult_completion_required_as_reported':True,'server_level_gate_verified':False,
            'can_do_with_main_as_reported':True,'rebirth_required_as_reported':False,
            'target':{'name':target[2],'floor_as_reported':int(target[0]),'level_literal':target[1]+'几级',
                      'exact_level':None,'enemy_id':None},'reward_choices':['大袋','小袋'],'reward_selection':'RANDOM',
            'caption_example_reward':caption,'caption_is_guaranteed':False,'reward_pool':None,'event_id':None},
        'npc_occurrences':npcs,'delivery_and_reward_items':items,'guard_occurrences':guards,
        'limited_exit':{'from_floor_as_reported':11,'to_floor_as_reported':onward[0],'coord':onward[1:],
                        'other_exits_described_as':['DEAD_END','RETURN_FLOOR_10'],'map_ids':None},
        'narrative':{'father':father,'son':son,'mother_host':mother,'goddess_label':'女神'+goddess[1],
            'father_initial_account':'MOTHER_DIED_AS_TOLD_TO_SON','later_account':'MOTHER_SERVES_AS_GODDESS_HOST',
            'diary_written_years_before_as_reported':diary_years,'son_age':None,
            'discovery_two_weeks_before_as_narrated':True,'host_cycle_years_as_reported':cycle,
            'selection_condition':'FIRST_MOTHER_GIVING_BIRTH_IN_HOST_CHANGE_YEAR_AS_NARRATED',
            'requires_mothers_first_child':None,'mother_reunion_after_duty_not_completed':True,
            'npc_original_id_equivalence':None,'real_time_host_rotation_implemented':False,
            'relations':[{'subject':father,'relation':'father_of','object':son},
                         {'subject':mother,'relation':'mother_of','object':son},
                         {'subject':father,'relation':'spouse_of','object':mother},
                         {'subject':mother,'relation':'serves_as_host_for','object':'女神'+goddess[1]},
                         {'subject':'女神'+goddess[1],'relation':'awaits_future_visit_by','object':son}]},
        'ecology':{'map_label':'琉璃的洞窟','monster_levels_as_reported':eco_levels,'monster_labels_as_reported':labels,
            'encounter_weights':None,'capture_eligibility':None,'map_id':None},
        'original_server_runtime_verified':False,'exact_game_build':None,'quest_ids':None}


def catalog(ex):
    main_content={'requirements':ex['main_quest'],'narrative':ex['narrative'],
                  'delivery_item_names':[i['name'] for i in ex['delivery_and_reward_items'][:2]],
                  'reward_item_name':ex['delivery_and_reward_items'][2]['name'],
                  'original_script_recovered':False}
    rows=[('quests','documentary_main_quest',main_content),('quests','documentary_optional_quest',ex['side_quest'])]
    rows += [('npcs','documentary_npc_occurrence_not_original_population',n) for n in ex['npc_occurrences']]
    rows += [('items','documentary_delivery_or_reward_item',i) for i in ex['delivery_and_reward_items']]
    rows += [('maps','documentary_cave_ecology_not_original_geometry',ex['ecology'])]
    return [{'record_id':f'CN2003-LIULI-R73-{i:02d}','collection':c,'entity_type':t,'version_profile':PROFILE,
        'source_refs':['S1','S2'],'verification_status':'SOURCE_DESCRIPTION_NOT_RUNTIME',
        'rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED','record_revision':1,'game_ids':None,'content':v}
        for i,(c,t,v) in enumerate(rows,1)]


def pin(path):
    raw=(ROOT/path).read_bytes()
    return {'path':path,'bytes':len(raw),'sha256':sha(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


def verify_report(r):
    require(r['version_profile']==PROFILE and r['negative_boundaries']==BOUNDARIES,'Evidence boundaries changed')
    ex=r['extraction'];require(r['catalog_records']==catalog(ex),'Catalogue detached/promoted')
    require(r['original_html_or_assets_in_output'] is False and r['original_game_runtime_verified'] is False,
            'Original asset/runtime status promoted')
    require(ex['main_quest']['hard_entry_level'] is None and ex['main_quest']['four_proofs_reward'] is None and
            ex['main_quest']['event_id'] is None and ex['main_quest']['adult_completion_required_as_reported'] is True,
            'Main requirements/unknowns promoted')
    s=ex['side_quest'];require(s['target']['exact_level'] is s['target']['enemy_id'] is s['reward_pool'] is s['event_id'] is None and
        s['server_level_gate_verified'] is s['rebirth_required_as_reported'] is s['caption_is_guaranteed'] is False,
        'Side gate/reward/identity promoted')
    n=ex['narrative'];require(n['father_initial_account']=='MOTHER_DIED_AS_TOLD_TO_SON' and
        n['later_account']=='MOTHER_SERVES_AS_GODDESS_HOST' and
        n['selection_condition']=='FIRST_MOTHER_GIVING_BIRTH_IN_HOST_CHANGE_YEAR_AS_NARRATED',
        'Narrative account or host selection changed')
    require(n['son_age'] is n['requires_mothers_first_child'] is n['npc_original_id_equivalence'] is None and
        n['real_time_host_rotation_implemented'] is False and n['mother_reunion_after_duty_not_completed'] is True,
        'Narrative perspective/timing promoted')
    require(ex['quest_ids'] is ex['exact_game_build'] is ex['village_coordinate_frames'] is None and
            ex['original_server_runtime_verified'] is False,'Original build/runtime promoted')
    for npc in ex['npc_occurrences']:require(npc['npc_id'] is None,'Original NPC ID invented')
    require(ex['npc_occurrences'][1]['spawn_selection'] is None,'Eight positions turned into fixed spawns')
    for item in ex['delivery_and_reward_items']:require(item['item_id'] is None,'Original item ID invented')
    for item in ex['delivery_and_reward_items'][:2]:
        require(item['logout_behavior'] is item['disconnect_behavior'] is None and item['drop_disappears_as_reported'] is True,
                'Drop behavior widened')
    require(ex['delivery_and_reward_items'][2]['spirit_name'] is None and
            ex['delivery_and_reward_items'][3]['consumed_at_exchange'] is None,'Missing item semantics invented')
    require(all(g['original_enemy_id'] is g['stats'] is None for g in ex['guard_occurrences']) and
        ex['limited_exit']['map_ids'] is None and all(ex['ecology'][k] is None for k in ('encounter_weights','capture_eligibility','map_id')),
        'Original enemy/map identity invented')
    require([p['path'] for p in r['parent_pins']]==['research/recovered/STONEAGE-CN2003-DREAM-CAVE-SOURCE-R1.json',
        'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json'] and all(pin(p['path'])==p for p in r['parent_pins']),
        'Parent source bytes/identity changed')
    require(r['parser_dependency_pin']==pin(PARSER_PATH),'Shared bounded parser changed')
    parent=json.loads((ROOT/r['parent_pins'][0]['path']).read_text())['extraction']
    require(r['adult_comparison']=={'parent_adult_required_for_admission':parent['adult_required_for_admission'],
        'parent_adult_required_for_named_reward_sequence':parent['adult_required_for_named_reward_sequence'],
        'this_page_both_branches_require_adult_as_reported':True,'same_original_flag_id_verified':False},
        'Adult requirement categories conflated')
    h=r['historical_comparison'];require(h['reference_capture']=='20031204051540' and h['selected_full_visible_article_equal'] is True and
        h['independent_witness_count']==1 and h['first_publication_authenticated'] is h['current_raw_equals_archive_raw'] is False,
        'Historical authority promoted')
    require([(p['id'],p['url']) for p in r['source_pages']]==list(URLS.items()) and
            all(p['official_authorship_verified'] is False and p['exact_game_build'] is None for p in r['source_pages']),
            'Source detached or authority promoted')


MUTATIONS=(('2003-06-06 14:55','2003-06-07 14:55'),('建议等级80级','建议等级81级'),
 ('特殊要求：解过成人仪式','特殊要求：无需成人仪式'),('65级，建议等级80级','66级，建议等级80级'),
 ('东229，南988','东228，南988'),('东215，南1017','东216，南1017'),('14年前所写的日记','15年前所写的日记'),
 ('魅力+2 回避率上升+2','魅力+3 回避率上升+2'),('掉到地上便会马上消失','注销便会马上消失'),
 ('9楼时，勇者会遇到一只65级','9楼时，勇者会遇到一只66级'),('东5，南32','东5，南33'),
 ('宿身是50年改变一次','宿身是51年改变一次'),('那一年第一个生下小孩的母亲','那一年所有生下小孩的母亲'),
 ('无法再次与拉鲁父子相会','已经再次与拉鲁父子相会'),('攻-4防+5魅+3','攻-5防+5魅+3'),
 ('制服大地的证据','另一效果的精灵'),('东34，南10','东35，南10'),('等级50几级的鲁尼帖斯','等级60几级的鲁尼帖斯'),
 ('大袋或小袋','大袋和小袋'),('获得物品：随机','获得物品：固定'),('由于跟转生没有相关','由于跟转生密切相关'),
 ('怪物等级：53~75级','怪物等级：54~75级'),('洛奇安','其他怪物'))


def audit(raw,expected):
    text=raw.decode('gb18030')
    for old,new in MUTATIONS:
        require(old in text,'Real-source mutation absent: '+old)
        try:actual=derive(text.replace(old,new).encode('gb18030'))
        except ValueError:continue
        require(actual!=expected,'Semantic mutation accepted: '+old)
    require(derive(raw+b'<script>chrome=1</script>')==expected,'Peripheral script changed evidence')
    return {'semantic_mutations_rejected_without_digest_gate':len(MUTATIONS),'peripheral_script_positive':True}


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);args=p.parse_args()
    r=json.loads(REPORT.read_text());verify_report(r)
    inputs=[];extractions=[];bodies=[];audits=[]
    for sid,url in URLS.items():
        if args.fetch:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'StoneAge-research/1.0'}),timeout=45) as rs:
                require(rs.status==200 and rs.url==url,'HTTP identity changed');raw=rs.read(2_000_001)
        else:raw=(Path(args.input_dir)/('current.html' if sid=='S1' else 'archive.html')).read_bytes()
        require(0<len(raw)<=2_000_000,'Source size outside bound')
        ex=derive(raw);require(ex==r['extraction'],'Documentary semantics changed')
        inputs.append({'id':sid,'url':url,'bytes':len(raw),'sha256':sha(raw)});extractions.append(ex);bodies.append(article(raw));audits.append({'id':sid,**audit(raw,ex)})
    h=r['historical_comparison'];require(bodies[0]==bodies[1] and len(bodies[0])==h['visible_compact_characters'] and
        sha(bodies[0].encode())==h['visible_compact_utf8_sha256'],'Current/archive full visible article differs')
    out={'schema':'stoneage.liuli_cave.replay.r1','inputs':inputs,'extraction':extractions[0],
        'catalog_records':catalog(extractions[0]),'historical_comparison':h,'audit':audits,
        'original_html_or_assets_in_output':False,'original_game_runtime_verified':False}
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'inputs':inputs,'catalog_records':len(out['catalog_records']),'audit':audits}))


if __name__=='__main__':main()
