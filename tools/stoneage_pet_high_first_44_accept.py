"""Independent original member receipt and source-scoped reward controls verification."""
import collections, hashlib, json
from pathlib import Path
from tools import stoneage_pet_high_first_40_acquisition as r40
from tools.stoneage_pet_high_first_44_source import code_semantics
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'research/pets'
def read(path,pin):
    raw=path.read_bytes()
    assert r40.git_blob(raw)==pin,path
    return json.loads(raw)
def main():
    raw=(P/'PET-HIGH-FIRST-44-ORIGINAL-WINDOW-REWARD-R1.json').read_bytes()
    assert len(raw)==47046 and hashlib.sha256(raw).hexdigest()=='78b37e07efff1ab28ab997b6b28321bd43bb62cf9b3cc622845dbd38980e2dfc'
    assert r40.git_blob(raw)=='bc531842c068154e40b50658092fe553ff6173df'
    d=json.loads(raw);receipt=d['member_receipt'];rows=d['rows']
    assert receipt['headers_visited']==7954 and receipt['range_requests']==len(receipt['range_receipts'])==184
    assert receipt['actual_range_bytes']==sum(x['bytes'] for x in receipt['range_receipts'])==12013836
    assert not receipt['whole_archive_or_parts_rehashed'] and len(rows)==len(receipt['members'])==d['original_member_count']==4
    r43=read(P/'PET-HIGH-FIRST-43-ORIGINAL-EXCHANGE-SEMANTICS-R1.json','8ede61a53c670a883bb7824e1d5f410d0b76463a')
    r42=read(P/'PET-HIGH-FIRST-42-ORIGINAL-MEMBER-REPLAY-R1.json','779077c98b745f6045733d4ba1410768e989f73e')
    inv={x['path']:(x['size'],x['sha256']) for x in json.loads(r40.R18.read_bytes())['all_server_occurrences']}
    prior={x['path']:x for x in r43['member_receipt']['members']}
    m={}
    for x in receipt['members']:
        name=x['path'].split('/SA2.5服務端/gmsv/data/npc/',1)[1]
        assert name not in m and x['extractor']=='unar' and not x['flags']&(1|2|4|16)
        assert (x['bytes'],x['sha256'])==inv['npc/'+name]
        assert all(x[k]==prior[x['path']][k] for k in ('bytes','crc32','sha256','header_sha256','compressed_payload_sha256'))
        m[name]=x
    s43={s['path']:s for s in r43['projection']['scripts']}
    s42={s['path']:s for s in r42['scripts']}
    for row in rows:
        path=row['path'];(a,)=s43[path]['commands'];(b,)=s42[path]['commands']
        assert row['script_sha256']==m[path]['sha256']==s43[path]['script_sha256']
        assert row['getpet_line']==a['line']==b['line'] and row['block_end']==b['source_block_end']
        assert row['condition_fields']==a['fields']
        assert row['pet_slots']==a['numeric_literals']==b['numeric_literals']
        assert row['random_item_slots']==[int(n) for n in a['fields']['getranditem'][0].split(',')]
        for kind in ('pet','item'):
            slots=row['pet_slots' if kind=='pet' else 'random_item_slots']
            assert row[kind+'_slot_counts']=={str(k):v for k,v in collections.Counter(slots).items()}
        assert row['primary_window_present'] and not row['secondary_window_present']
        assert set(row['window_field_fingerprints'])=={'nomalwindowmsg'}
        (window,)=row['window_field_fingerprints']['nomalwindowmsg']
        assert row['block_start']<window['line']<row['getpet_line']
        assert row['later_code_route_candidate']=='LATER_DIRECT_ACCEPTDEL_CANDIDATE'
        assert not row['actual_award_verified'] and not row['official_probability_verified']
    assert set(m)=={x['path'] for x in rows}
    assert [len(x['pet_slots']) for x in rows]==[5,6,4,4]
    assert [x['window_field_fingerprints']['nomalwindowmsg'][0]['value_bytes'] for x in rows]==[135,135,119,120]
    assert rows[0]['window_field_fingerprints']['nomalwindowmsg'][0]['value_sha256']==rows[1]['window_field_fingerprints']['nomalwindowmsg'][0]['value_sha256']
    assert len({n for x in rows for n in x['pet_slots']})==15
    assert sum(len(x['pet_slot_counts']) for x in rows)==18
    assert rows[1]['pet_slot_counts']['482']==2 and rows[1]['item_slot_counts']['68']==rows[3]['item_slot_counts']['68']==2
    assert all(len(x['random_item_slots'])==10 for x in rows)
    assert d['code_semantics']==code_semantics()
    assert not any(d[k] for k in ('original_payload_published','runtime_executed','official_deployment_verified'))
    print('PET44: 4 members, 4 primary windows, 19 pet slots / 15 distinct instances, 40 item slots; no official execution or probability.')
if __name__=='__main__':main()
