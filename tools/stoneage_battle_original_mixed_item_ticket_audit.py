"""Original mixed valid/invalid tickets: all three slot positions and aliases."""
import hashlib
import resource
from tools import stoneage_battle_original_invalid_item_ticket_audit as prior

attack = prior.attack
replace_once = prior.replace_once
INVALID = (249, 256, 2147483647, -2, -2147483648, -1)


def mixed_controls(profile):
    c = prior.prior.prior.NEGATIVE.replace('negative_', 'mixed_')
    c = replace_once(c, 'static BATTLE mixed_saved_arena,mixed_expected_arena;',
                     'static BATTLE mixed_saved_arena,mixed_expected_arena;char mixed_baseline_rs[1024];')
    c = replace_once(c, ' for(int mixed_case=0;mixed_case<4;mixed_case++){', '''
 for(int kind=0;kind<2;kind++){
 for(int bad=0;bad<(kind?5:6);bad++){
 for(int position=0;position<3;position++){
  int invalids[6]={249,256,2147483647,-2,(-2147483647-1),-1};
  int pattern[3],mask=0,awards=kind+1;
  for(int k=0;k<3;k++){pattern[k]=kind?(k==position?invalids[bad]:3):(k==position?3:invalids[bad]);if(pattern[k]==3)mask|=1<<k;}
''')
    c = replace_once(c, '\n memcpy(reward_items,mixed_saved_items', '\n }\n }\n memcpy(reward_items,mixed_saved_items')
    c = replace_once(c, 'int recipient=mixed_case==1?2:mixed_case==2?-1:0;', 'int recipient=0;')
    c = replace_once(c, 'arena->use=1;', '''ITEM_SIZE=256;
   demand(GETITEM_MAX==3&&!ITEM_CHECKINDEX(249)&&ITEM_CHECKINDEX(3),"original three-slot active/inactive mixed inputs");
   demand(ITEM_getInt(3,ITEM_LEAKLEVEL)==LEAK_EXPECTED&&!strcmp(ITEM_getAppropriateName(3),DISPLAY_NAME)&&!strcmp(ITEM_getChar(3,ITEM_SECRETNAME),""),"original factory identification/name profile preserved");
   arena->use=1;''')
    c = replace_once(c, '    arena->Side[0].Entry[0].getitem[0]=3;\n    if(mixed_case==3)arena->Side[0].Entry[0].getitem[1]=3;',
                     '    for(int k=0;k<GETITEM_MAX;k++)arena->Side[0].Entry[0].getitem[k]=pattern[k];')
    c = replace_once(c, 'CHAR_setFlg(0,CHAR_ISDIE,mixed_case==0);', 'CHAR_setFlg(0,CHAR_ISDIE,FALSE);')
    c = c.replace('mixed_case==0||mixed_case==3', '1')
    c = replace_once(c, 'reward_phase=mixed_case==3?3:2;', 'reward_phase=kind?3:2;')
    c = replace_once(c, '    mixed_expected_arena=*arena;expected_count=ITEM_COUNT;', '''    mixed_expected_arena=*arena;expected_count=ITEM_COUNT;
    demand(finish_rs_count==1&&finish_rs_fd[0]==7&&strlen(finish_rs_text[0])>=3&&
           !strcmp(finish_rs_text[0]+strlen(finish_rs_text[0])-3,"|||"),"one original no-ticket RS and empty slot suffix");
    strcpy(mixed_baseline_rs,finish_rs_text[0]);mixed_baseline_rs[strlen(mixed_baseline_rs)-3]=0;''')
    start=c.index('    if(mixed_case==3){')
    end=c.index('    demand(!memcmp(mixed_expected_items',start)
    c=c[:start]+'''    mixed_expected_items[3].ITEM_FIELD.workint[ITEM_WORKCHARAINDEX]=0;
    mixed_expected_items[3].ITEM_FIELD.workint[ITEM_WORKOBJINDEX]=-1;
    for(int k=0;k<awards;k++)mixed_expected_actors[0].indexOfExistItems[first_slot+k]=3;
'''+c[end:]
    c=c.replace('(mixed_case==3?2:0)', 'awards').replace('(mixed_case==3?1:0)', '1')
    start=c.index('    printf("REAL_HEADER_TICKET_CLEANUP|')
    end=c.index('   }\n   reward_phase=0;',start)
    c=c[:start]+r'''    char mixed_expected_rs[1024];strcpy(mixed_expected_rs,mixed_baseline_rs);
    for(int k=0;k<3;k++){if(pattern[k]==3)strcat(mixed_expected_rs,DISPLAY_NAME);strcat(mixed_expected_rs,"|");}
    if(strcmp(finish_rs_text[0],mixed_expected_rs))printf("MIXED_RS_MISMATCH|actual=%s|expected=%s\n",finish_rs_text[0],mixed_expected_rs);fflush(stdout);
    demand(finish_rs_count==1&&finish_rs_fd[0]==7&&!strcmp(finish_rs_text[0],mixed_expected_rs),
           "original RS complete no-ticket prefix plus exact ordered three-slot item suffix");
    for(int actor=0;actor<7;actor++)for(int box=0;box<CHAR_MAXITEMHAVE;box++)
     demand(slots[actor].indexOfExistItems[box]!=invalids[bad]||invalids[bad]==-1,"no carried reference to invalid mixed ticket");
    printf("REAL_HEADER_MIXED_ITEM_TICKET|kind=%d|bad=%d|position=%d|invalid=%d|valid_mask=%d|awards=%d|named_items=NAMED_ITEMS|leak=LEAK_EXPECTED|secret_empty=1|item=3|live=1|owner=0|pool_size=256|count_unchanged=1|references=%d|logs=%d|data=%d|one=%d|rs=1|packet_oracle=1|second_loop=1|arena_released=1|tickets_cleared=1|whole_items=1|whole_actors=1|whole_arena=1|whole_connections=1|original_timer=1\n",
           kind,bad,position,invalids[bad],mask,awards,references,reward_log_count,reward_data_count,reward_one_count);
'''+c[end:]
    c=prior.prior.prior.capacity.prior.payout.ticket.drop.factory.allocator.item.substitutions(profile,c)
    return (c.replace('ENTRY_FIELD','char_index' if profile=='bismarck' else 'charaindex')
            .replace('WIN_SIDE','-1' if profile=='bismarck' else '0')
            .replace('ONE_EXPECTED','awards' if profile=='bismarck' else '0')
            .replace('CONNECTION_TYPE','GmsvSession' if profile=='bismarck' else 'CONNECT')
            .replace('TIMER_EXPECTED','1005' if profile=='bismarck' else '1000')
            .replace('TIMER_DRAWS','1').replace('TIMER_SENDS','1' if profile=='bismarck' else '0')
            .replace('DISPLAY_NAME','"Factory"' if profile=='bismarck' else '""')
            .replace('NAMED_ITEMS','%d').replace('LEAK_EXPECTED','0' if profile=='bismarck' else '1')
            .replace('mask,awards,references','mask,awards,'+('awards' if profile=='bismarck' else '0')+',references'))


def mixed_native(profile, source, battle, event, root):
    native,has_lua=prior.invalid_native(profile,source,battle,event,root)
    old=prior.invalid_controls(profile)
    native=replace_once(native,old,old+'\n'+mixed_controls(profile))
    for name in ('BATTLE_GetExpGold','BATTLE_DeleteItem','BATTLE_DeleteBattle','ITEM_getAppropriateName'):
        body=attack.definition(native,name)
        original_source=attack.pp_file(profile,root,attack.LAYOUTS[profile]/'item/item.c') if name=='ITEM_getAppropriateName' else battle
        if body!=attack.definition(original_source,name):raise ValueError('original mixed-ticket body drift '+name)
        print(f'MIXED_TICKET_SOURCE|{profile}|{name}|sha256={hashlib.sha256(body.encode()).hexdigest()}',flush=True)
    return native,has_lua


def validate_report(report):
    prior.validate_report(report)
    rows={}
    for line in report.splitlines():
        if not line.startswith('ACTUAL|') or '|REAL_HEADER_MIXED_ITEM_TICKET|' not in line:continue
        parts=line.split('|');profile=parts[1]
        try:
            f=dict(p.split('=',1) for p in parts[3:]);kind=int(f['kind']);bad=int(f['bad']);position=int(f['position']);key=profile,kind,bad,position
            if profile not in ('gavin','bismarck') or kind not in (0,1) or bad not in range(5 if kind else 6) or position not in range(3) or key in rows:
                raise ValueError('unknown/duplicate mixed-ticket witness')
            awards=kind+1
            expected=dict(invalid=INVALID[bad],valid_mask=7-(1<<position) if kind else 1<<position,
                          awards=awards,named_items=awards if profile=='bismarck' else 0,leak=0 if profile=='bismarck' else 1,secret_empty=1,item=3,live=1,owner=0,pool_size=256,references=awards,
                          logs=awards,data=1,one=awards if profile=='bismarck' else 0,rs=1)
            for n in ('count_unchanged','packet_oracle','second_loop','arena_released','tickets_cleared','whole_items','whole_actors','whole_arena','whole_connections','original_timer'):expected[n]=1
            if any(int(f[n])!=v for n,v in expected.items()):raise ValueError('mixed-ticket witness disagrees with ordered state oracle')
            rows[key]=f
        except (KeyError,TypeError) as exc:raise ValueError('incomplete mixed-ticket witness') from exc
    if set(rows)!={(p,k,b,s) for p in ('gavin','bismarck') for k in (0,1) for b in range(5 if k else 6) for s in range(3)}:
        raise ValueError('missing mixed-ticket profile/case/position')
    if 'RESOLUTION|ORIGINAL_REAL_HEADER_MIXED_ITEM_TICKET_BOUNDED_PASS' not in report.splitlines():raise ValueError('missing mixed-ticket resolution')
    return rows


def main():
    soft,hard=resource.getrlimit(resource.RLIMIT_STACK)
    if soft!=resource.RLIM_INFINITY and soft<64*1024*1024:resource.setrlimit(resource.RLIMIT_STACK,(64*1024*1024,hard))
    attack.main(native_builder=mixed_native,extra_markers=('REAL_HEADER_FINISH_DISPATCH|','REAL_HEADER_SAME_ITEM_CAPACITY|','REAL_HEADER_TICKET_CLEANUP|','REAL_HEADER_RECIPIENT_SIDE|','REAL_HEADER_INVALID_ITEM_TICKET|','REAL_HEADER_MIXED_ITEM_TICKET|'))
    print('BOUNDARY|explicit logical256 pool and ordered three-slot mixed tickets; original valid item3 aliases; exact typed RS suffix; no natural bad-ticket reachability, early server identity or modern ownership DESIGN')
    for gate in ('SAME_ITEM_CAPACITY','TICKET_CLEANUP','RECIPIENT_SIDE','INVALID_ITEM_TICKET','MIXED_ITEM_TICKET'):print('RESOLUTION|ORIGINAL_REAL_HEADER_'+gate+'_BOUNDED_PASS')


if __name__=='__main__':main()
