"""Pinned descendant enemy-slot and watcher-list lifecycle witnesses.

Only derived hashes/results leave transient source trees. Execute original
destruction/getter/party and Link/UnLink/Delete/Finish bodies; retain declared
symbolic structs and controlled item/network/Exit/Profit dependencies.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess

from tools.stoneage_guard_break2_source_audit import PINNED, LAYOUTS, _text, _compact
from tools.stoneage_mdfyattack_source_audit import _definition as inherited_definition
from tools.stoneage_becomepig_lookup_audit import numeric_initializer
from tools.stoneage_becomepig_restore_audit import run_native, original_functions
from tools.stoneage_becomepig_native_audit import _assert_rows

RESOLUTION = 'BOUNDED_ENEMY_SLOT_WATCH_LIST_LIFECYCLE_PASS_ZERO_RUNTIME_PROMOTIONS'
PIN_PATH = Path(__file__).resolve().parents[1] / 'research/recovered/STONEAGE-EXIT-LIFETIME-WATCH-SOURCE-DOMAINS-R1.json'


def _definition(text, name):
    # The inherited brace extractor searches a signature prefix. Start it at
    # the exact matched definition so getInt cannot select earlier getIntStrict.
    match = re.search(r'\b(?:static\s+)?(?:int|void|BOOL|float)\s+'+re.escape(name)+r'\s*\([^;{}]*\)\s*\{', text, re.S)
    if not match:
        raise ValueError('missing exact function '+name)
    return inherited_definition(text[match.start():], name)


def item_limit(expr):
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Mult)):
            a, b = visit(node.left), visit(node.right)
            return a+b if isinstance(node.op, ast.Add) else a*b
        raise ValueError('unsupported item cardinality expression')
    result = visit(ast.parse(expr.strip(), mode='eval').body)
    if not 0 < result < 512:
        raise ValueError('unsupported item cardinality bound')
    return result


def source_domain(profile, root):
    root = root.resolve()
    head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain'], text=True).strip()
    if head != PINNED[profile] or dirty:
        raise ValueError('pinned source tree drift')
    base = root / LAYOUTS[profile]
    inc = ['-I', str(base/'include')]
    if profile == 'bismarck':
        inc += ['-I', str(root/'server/common'), '-I', str(root/'shared/lua51')]
    def pp(text):
        text = re.sub(r'^\s*#\s*include[^\n]*', '', text, flags=re.M)
        return subprocess.run(['cpp', '-P', *inc, '-'], input='#include "version.h"\n'+text,
                              text=True, capture_output=True, check=True).stdout
    raw = {p: _text(base/p) for p in ('char/char_base.c', 'char/char.c', 'battle/battle.c')}
    charbase = pp(raw['char/char_base.c'])
    functions = {name: _definition(charbase, name) for name in (
        'CHAR_endCharData', 'CHAR_removeHaveItem', 'CHAR_removeHavePoolItem', '_CHAR_CHECKINDEX')}
    for label, names in (
        ('end_one', ('_CHAR_endCharOneArray', 'CHAR_endCharOneArray')),
        ('get_int', ('_CHAR_getInt', 'CHAR_getInt')),
        ('get_work', ('_CHAR_getWorkInt', 'CHAR_getWorkInt')),
    ):
        for name in names:
            try:
                functions[label] = _definition(charbase, name)
                break
            except ValueError:
                pass
        else:
            raise ValueError('missing default accessor '+label)
    functions['party'] = _definition(pp(raw['char/char.c']), 'CHAR_PartyUpdate')
    battle = pp(raw['battle/battle.c'])
    for name in ('BATTLE_WatchLink', 'BATTLE_WatchUnLink', 'BATTLE_DeleteBattle', 'BATTLE_Finish'):
        functions[name] = _definition(battle, name)
    if profile == 'bismarck':
        functions['CheckCharMaxItemChar'] = _definition(charbase, 'CheckCharMaxItemChar')
        functions['BATTLE_CHECKINDEX'] = _definition(battle, 'BATTLE_CHECKINDEX')
    header = pp(_text(base/'include/char_base.h')+'\nint lifecycle_n=CHAR_MAXITEMHAVE;\nint lifecycle_p=CHAR_MAXPOOLITEMHAVE;\n')
    equip_enum = next(body for body in re.findall(r'typedef\s+enum\s*\{([^{}]*)\}', header, re.S) if 'CHAR_EQUIPPLACENUM' in body)
    value = -1
    equip = None
    for entry in equip_enum.split(','):
        entry = entry.strip()
        if not entry:
            continue
        if '=' in entry:
            name, expr = entry.split('=', 1)
            value = numeric_initializer(expr.strip())
        else:
            name = entry
            value += 1
        if name.strip() == 'CHAR_EQUIPPLACENUM':
            equip = value
    if equip is None:
        raise ValueError('missing active equipment cardinality')
    limits = {key: item_limit(re.search(r'int lifecycle_'+mark+r'=(.*?);', header).group(1).replace('CHAR_EQUIPPLACENUM', str(equip)))
              for key,mark in (('items', 'n'), ('pool', 'p'))}
    # Expand Bismarck's actual item-limit helper expression with active header
    # constants, without expanding accessor macros in original C bodies.
    if profile == 'bismarck':
        functions['CheckCharMaxItemChar'] = _definition(pp(_text(base/'include/char_base.h')+'\n'+functions['CheckCharMaxItemChar']), 'CheckCharMaxItemChar')
        functions['CheckCharMaxItemChar'] = functions['CheckCharMaxItemChar'].replace('CHAR_EQUIPPLACENUM', str(equip))
    exit_body = original_functions(profile, root)[0][1]
    structural = contracts(profile, functions, exit_body)
    paths = (*raw, 'include/version.h', 'include/char_base.h', 'include/battle.h')
    identity = {'source_sha': head, 'files': {p: hashlib.sha256((base/p).read_bytes()).hexdigest() for p in paths},
                'functions': {name: hashlib.sha256(_compact(body).encode()).hexdigest() for name,body in functions.items()},
                'exit_sha256': hashlib.sha256(_compact(exit_body).encode()).hexdigest(),
                'limits': limits, 'contracts': structural}
    return functions, identity


def contracts(profile, functions, exit_body):
    f = {name: _compact(body) for name,body in functions.items()}
    end = f['CHAR_endCharData']
    if not (end.index('CHAR_removeHaveItem(ch)') < end.index('CHAR_removeHavePoolItem(ch)') < end.index('ch->use=')):
        raise ValueError('character destruction order drift')
    if re.search(r'\b(?:free|freeMemory|memset)\(', end):
        raise ValueError('character storage retention contract drift')
    for fn in ('CHAR_removeHaveItem', 'CHAR_removeHavePoolItem'):
        if f[fn].index('=-1;') > f[fn].index('ITEM_endExistItemsOne('):
            raise ValueError('item unlink-before-end drift')
    finish = f['BATTLE_Finish']
    if finish.count('pBattle=pBattle->pNext') != 2 or 'BATTLE_DeleteBattle(pBattle->battleindex);' not in finish:
        raise ValueError('watch deletion traversal drift')
    unlink = f['BATTLE_WatchUnLink']
    if not all(token in unlink for token in ('pTop->pNext=BattleArray[battleindex].pNext;', 'pNext->pBefore=pTop;', 'pBefore=', 'pNext=')):
        raise ValueError('watch link splice contract drift')
    delete = f['BATTLE_DeleteBattle']
    if not (delete.index('BATTLE_WatchUnLink(') < delete.index('pBattle->use=') < delete.index('BATTLE_DeleteItem(')):
        raise ValueError('battle unlink-before-invalidate drift')
    check = 'CHAR_CHECKINDEX' in f['get_work']
    partycheck = f['party'].find('CHAR_CHECKINDEX')
    partyread = f['party'].index('CHAR_getWorkInt')
    exit_compact = _compact(exit_body)
    after_party = exit_compact[exit_compact.index('CHAR_PartyUpdate('):]
    ticket_guard = 'CHAR_CHECKINDEX' in after_party[:after_party.index('CHAR_WORKTICKETTIME')]
    if check != (profile == 'bismarck') or (partycheck >= 0 and partycheck < partyread) != (profile == 'bismarck') or ticket_guard != (profile == 'bismarck'):
        raise ValueError('post-destroy accessor/party/ticket guard profile drift')
    return {'slot_use_false_after_item_cleanup': True, 'character_slot_not_freed_or_zeroed_in_end_data': True,
            'work_getter_checks_live_slot': check, 'party_checks_subject_before_read': partycheck >= 0 and partycheck < partyread,
            'exit_ticket_block_checks_live_slot': ticket_guard,
            'watch_delete_loop_reads_current_next_after_unlink': True}


def watch_vectors():
    # action0=Link new detached node,1=UnLink,2=Delete,3=Finish main.
    for count, slot in itertools.product(range(4), (0, 4, 9)):
        yield (0, count, count+1, slot)
        for action, target in itertools.product((1, 2), range(count+1)):
            yield (action, count, target, slot)
        yield (3, count, 0, slot)


def watch_oracle(case):
    action, count, target, slot = case
    links = list(range(count+1))
    use = [int(i <= count) for i in range(5)]
    if action == 0:
        use[target] = 1
        links.insert(1, target)
    elif action in (1, 2):
        links.remove(target)
        if action == 2:
            use[target] = 0
    else:
        # Exact original loop loses the first watch node's next after deletion.
        use[0] = 0
        if count:
            use[1] = 0
        links = list(range(2, count+1))
    rows = []
    for i in range(5):
        if i in links:
            p = links.index(i)
            before = links[p-1] if p else -1
            after = links[p+1] if p+1 < len(links) else -1
        else:
            before = after = -1
        rows.extend((use[i], before, after))
    # Deleted nodes clear entries; Exit stub removes all relevant live entries.
    entries = [i+1 if use[i] and action != 3 and i <= count else -1 for i in range(5)]
    total = count+1 + int(action == 0) - int(action == 2) - (1+int(count>0) if action == 3 else 0)
    profitmask = 1 if action == 3 else 0
    exitmask = (1 << (count+1))-1 if action == 3 else 0
    deletemask = (1 << target) if action == 2 else (1 | (2 if count else 0)) if action == 3 else 0
    return tuple([1 if action < 2 else 0, total, *rows, *entries, profitmask, exitmask, deletemask])


def watch_source(profile, functions):
    field = 'char_index' if profile == 'bismarck' else 'charaindex'
    text = '\n'.join(functions[name] for name in ('BATTLE_WatchLink', 'BATTLE_WatchUnLink', 'BATTLE_DeleteBattle', 'BATTLE_Finish'))
    symbols = sorted(set(re.findall(r'\b(?:CHAR|BATTLE)_[A-Z][A-Z0-9_]*\b', text)))
    constants = {name:j+10 for j,name in enumerate(symbols) if name not in ('CHAR_CHECKINDEX','BATTLE_CHECKINDEX','BATTLE_CHECKADDRESS','BATTLE_ENTRY')}
    constants.update({'BATTLE_ENTRY_MAX':10,'BATTLE_TYPE_P_vs_E':1,'BATTLE_TYPE_P_vs_P':2,'BATTLE_TYPE_WATCH':3,'BATTLE_CHARMODE_FINAL':2})
    head = '#include <stdio.h>\n#include <string.h>\n#define TRUE 1\n#define FALSE 0\n#define BOOL int\n'
    head += '\n'.join('#define '+k+' '+str(v) for k,v in constants.items())+'\n'
    head += r'''
typedef struct {int charaindex,char_index,escape;} BATTLE_ENTRY;
typedef struct BATTLE {int use,mode,battleindex,type,winside,createindex;void (*WinFunc)(int,int);struct BATTLE *pNext,*pBefore;struct {BATTLE_ENTRY Entry[10];} Side[2];} BATTLE;
static BATTLE BattleArray[5];static int BATTLE_battlenum=5,Total_BattleNum,profitmask,exitmask,deletemask;
#define BATTLE_CHECKADDRESS(a) ((&BattleArray[0])<=(a)&&(a)<=(&BattleArray[BATTLE_battlenum-1]))
int CHAR_CHECKINDEX(int i){return i>0&&i<6;}
void CHAR_setWorkInt(int i,int f,int v){(void)i;(void)f;(void)v;}
int CHAR_getInt(int i,int f){(void)i;(void)f;return 0;}
void CHAR_setInt(int i,int f,int v){(void)i;(void)f;(void)v;}
void NETWATCH_set(const char *s,int i,const char *v){(void)s;(void)i;(void)v;}
#define fprint(...) ((void)0)
void EntryInit(BATTLE_ENTRY *e){e->char_index=e->charaindex=-1;e->escape=0;}
void BATTLE_DeleteItem(int i){deletemask|=1<<i;}
void BATTLE_GetProfit(int b,int s,int p){(void)s;(void)p;profitmask|=1<<b;}
void BATTLE_Exit(int actor,int b){exitmask|=1<<b;for(int s=0;s<2;s++)for(int p=0;p<10;p++)if(BattleArray[b].Side[s].Entry[p].charaindex==actor)EntryInit(&BattleArray[b].Side[s].Entry[p]);}
'''
    if profile == 'bismarck':
        head += functions['BATTLE_CHECKINDEX']+'\n'
    else:
        head += '#define BATTLE_CHECKINDEX(a) (((a)>=BATTLE_battlenum||(a)<0)?FALSE:TRUE)\n'
    head += text+r'''
int main(void){int action,count,target,slot;while(scanf("%d%d%d%d",&action,&count,&target,&slot)==4){
 memset(BattleArray,0,sizeof(BattleArray));Total_BattleNum=count+1;profitmask=exitmask=deletemask=0;
 for(int b=0;b<5;b++){BattleArray[b].battleindex=b;BattleArray[b].use=b<=count;BattleArray[b].type=b?3:1;
 for(int s=0;s<2;s++)for(int p=0;p<10;p++)EntryInit(&BattleArray[b].Side[s].Entry[p]);
 if(b<=count){BattleArray[b].Side[0].Entry[slot].charaindex=b+1;BattleArray[b].Side[0].Entry[slot].char_index=b+1;
 BattleArray[b].pBefore=b?&BattleArray[b-1]:NULL;BattleArray[b].pNext=b<count?&BattleArray[b+1]:NULL;}}
 int ret;if(action==0){BattleArray[target].use=1;Total_BattleNum++;ret=BATTLE_WatchLink(0,target);}else if(action==1)ret=BATTLE_WatchUnLink(target);else if(action==2)ret=BATTLE_DeleteBattle(target);else ret=BATTLE_Finish(0);
 printf("%d %d",ret,Total_BattleNum);
 for(int b=0;b<5;b++)printf(" %d %d %d",BattleArray[b].use,BattleArray[b].pBefore?(int)(BattleArray[b].pBefore-BattleArray):-1,BattleArray[b].pNext?(int)(BattleArray[b].pNext-BattleArray):-1);
'''
    head += 'for(int b=0;b<5;b++)printf(" %d",BattleArray[b].Side[0].Entry[slot].'+field+');printf(" %d %d %d\\n",profitmask,exitmask,deletemask);}return 0;}\n'
    return head


def lifetime_vectors():
    return list(itertools.product((0,1), (0,1), (0,1,2)))  # live, pointer available, party mode


def lifetime_source(profile, functions, limits):
    head = r'''
#include <stdio.h>
#include <string.h>
#define BOOL int
#define TRUE 1
#define FALSE 0
#define INLINE
typedef int CHAR_DATAINT;typedef int CHAR_WORKDATAINT;
#define CHAR_DATAPLACENUMBER 0
#define CHAR_DATAINTNUM 64
#define CHAR_WORKDATAINTNUM 64
#define CHAR_WORKBATTLEMODE 0
#define CHAR_WORKPARTYMODE 1
#define CHAR_WORKPARTYINDEX1 10
#define CHAR_PARTY_NONE 0
#define CHAR_PARTY_LEADER 1
#define CHAR_PARTYMAX 5
#define CHAR_CDKEY 0
#define print(...) ((void)0)
#define fprintf(...) ((void)0)
'''
    head += f'#define CHAR_MAXITEMHAVE {limits["items"]}\n#define CHAR_MAXPOOLITEMHAVE {limits["pool"]}\n'
    head += r'''
typedef struct {int use,data[64],workint[64],indexOfExistItems[CHAR_MAXITEMHAVE],indexOfExistPoolItems[CHAR_MAXPOOLITEMHAVE];} Char;
static Char CHAR_chara[3];static int CHAR_charanum=3,pointer,ends,notifies,badorder;
void ITEM_endExistItemsOne(int i){ends++;if(!CHAR_chara[0].use)badorder++;if(i>=200){if(CHAR_chara[0].indexOfExistPoolItems[i-200]!=-1)badorder++;}else if(CHAR_chara[0].indexOfExistItems[i-100]!=-1)badorder++;}
char *CHAR_getChar(int i,int f){(void)i;(void)f;return "x";}
void CHAR_send_N_StatusString(int i,int p,int v){(void)i;(void)p;(void)v;notifies++;}
int getPartyNum(int i){(void)i;return CHAR_PARTYMAX;}
'''
    head += functions['_CHAR_CHECKINDEX']+'\n#define CHAR_CHECKINDEX(i) _CHAR_CHECKINDEX("w",0,i)\n'
    head += 'Char *CHAR_getCharPointer(int i){return pointer&&CHAR_CHECKINDEX(i)?&CHAR_chara[i]:NULL;}\n'
    head += functions['get_int']+'\n'+functions['get_work']+'\n'
    if '_CHAR_getInt(' in _compact(functions['get_int']):
        head += '#define CHAR_getInt(i,f) _CHAR_getInt("w",0,i,f)\n'
    if '_CHAR_getWorkInt(' in _compact(functions['get_work']):
        head += '#define CHAR_getWorkInt(i,f) _CHAR_getWorkInt("w",0,i,f)\n'
    if profile == 'bismarck':
        head += functions['CheckCharMaxItemChar']+'\n'
    for name in ('CHAR_removeHaveItem','CHAR_removeHavePoolItem','CHAR_endCharData','end_one','party'):
        head += functions[name]+'\n'
    call = '_CHAR_endCharOneArray(0,"w",0)' if profile == 'bismarck' else 'CHAR_endCharOneArray(0)'
    head += r'''
int main(void){int live,mode;while(scanf("%d%d%d",&live,&pointer,&mode)==3){memset(CHAR_chara,0,sizeof(CHAR_chara));ends=notifies=badorder=0;
 for(int a=0;a<3;a++){CHAR_chara[a].use=1;CHAR_chara[a].data[2]=73;CHAR_chara[a].workint[2]=73;
 for(int j=0;j<5;j++)CHAR_chara[a].workint[10+j]=j<3?j:-1;}
 CHAR_chara[0].use=live;CHAR_chara[0].workint[1]=mode;
 if(mode==2)CHAR_chara[0].workint[10]=1;
 for(int j=0;j<CHAR_MAXITEMHAVE;j++)CHAR_chara[0].indexOfExistItems[j]=j+100;
 for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)CHAR_chara[0].indexOfExistPoolItems[j]=j+200;
'''
    head += call+';int i=CHAR_getInt(0,2),w=CHAR_getWorkInt(0,2);CHAR_PartyUpdate(0,7);\n'
    head += r'''
 int cleared=0;for(int j=0;j<CHAR_MAXITEMHAVE;j++)cleared+=CHAR_chara[0].indexOfExistItems[j]==-1;
 for(int j=0;j<CHAR_MAXPOOLITEMHAVE;j++)cleared+=CHAR_chara[0].indexOfExistPoolItems[j]==-1;
 printf("%d %d %d %d %d %d %d %d\n",CHAR_chara[0].use,CHAR_CHECKINDEX(0),ends,cleared,i,w,notifies,badorder);
}return 0;}
'''
    return head


def lifetime_oracle(profile, limits, case):
    live, pointer, mode = case
    destroyed = live and pointer
    final_live = int(live and not pointer)
    cleared = limits['items']+limits['pool'] if destroyed else 0
    retained = profile != 'bismarck' or final_live
    return (final_live, final_live, cleared, cleared, 73 if retained else -1,
            73 if retained else -1, 2 if retained and mode else 0, 0)


def audit(profile, root):
    functions, identity = source_domain(profile, root)
    pinned = json.loads(PIN_PATH.read_text())['profiles'][profile]
    if identity != pinned:
        raise ValueError('lifetime/watch source-domain identity drift')
    watches = list(watch_vectors())
    life = lifetime_vectors()
    outputs = []
    for label, source, cases, expected in (
        ('watch', watch_source(profile, functions), watches, [watch_oracle(v) for v in watches]),
        ('lifetime', lifetime_source(profile, functions, identity['limits']), life,
         [lifetime_oracle(profile, identity['limits'], v) for v in life]),
    ):
        payload = ''.join(' '.join(map(str, v))+'\n' for v in cases)
        for opt in ('-O0','-O2'):
            _assert_rows(run_native(source,payload,opt),expected,profile+' '+label)
        outputs.extend(expected)
    return {'profile':profile,'source_sha':PINNED[profile],'watch_cases_per_optimization':len(watches),
            'lifetime_cases_per_optimization':len(life),'native_comparisons':2*(len(watches)+len(life)),
            'semantic_sha256':hashlib.sha256(json.dumps(outputs,separators=(',',':')).encode()).hexdigest()}


def main():
    parser=argparse.ArgumentParser()
    for profile in PINNED:
        parser.add_argument('--'+profile+'-dir',type=Path,required=True)
    args=parser.parse_args();total=0
    for profile in PINNED:
        row=audit(profile,getattr(args,profile+'_dir'));total+=row['native_comparisons']
        print('PROFILE|'+'|'.join(f'{k}={v}' for k,v in row.items()),flush=True)
    print(f'TOTAL|lifetime_watch_comparisons={total}|profiles=3')
    print('FACT|end_data_unlinks_items_before_ending_items_then_marks_use_false_character_slot_retained')
    print('FACT|gavin_iris_stale_slot_getters_and_party_reads_Bismarck_liveness_guards_preserved')
    print('FACT|Finish_exits_all_linked_watchers_but_deletes_only_first_watch_node_then_main_in_acyclic_chain')
    print('FACT|remaining_watch_nodes_stay_used_and_relinked_after_head_deletion_when_watch_count_exceeds_one')
    print('BOUNDARY|actual_default_bodies_symbolic_ABI_retained_fixed_array_item_end_Exit_Profit_network_entry_reset_stubs_valid_acyclic_nodes')
    print('OPEN|full_original_Exit_destroy_composition_item_end_semantics_watch_stop_task_cleanup_corrupt_cycles_invalid_pointers_runtime_original_build')
    print('RESOLUTION|'+RESOLUTION)


if __name__=='__main__':
    main()
