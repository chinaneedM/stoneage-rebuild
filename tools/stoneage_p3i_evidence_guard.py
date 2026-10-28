"""Evidence gate: an observed independent PRIMARY is not a private game backbuffer."""
import re
HEX=re.compile(r'^[0-9a-f]{64}$')
def require(ok,why):
    if not ok:raise ValueError(why)
def qualify_p3i(runtime):
    require(runtime.get('original_client_execution_attempted') is True,'original process')
    require(runtime.get('native_probe_attempted') is True,'probe on owned original window')
    obs=runtime.get('observations',[])
    require(len(obs)==3 and any(o.get('frame',{}).get('rgb_sha256') for o in obs),'paired GDI capture')
    probe=runtime.get('native_probe',{})
    require(probe.get('returncode')==0 and isinstance(probe.get('stdout'),dict),'native probe completed')
    p=probe['stdout']
    require(p.get('schema')=='stoneage.p3i.native_ddraw_primary.v1','source schema')
    require(p.get('target_owned_window_verified') is True and p.get('original_private_surface_read') is False,'window scope')
    require(p.get('sample_region')==[640,480],'limited owned rectangle')
    for n in ('ddraw_create_hr','cooperative_hr','primary_create_hr','primary_lock_hr'):
        require(re.fullmatch('0x[0-9a-fA-F]{8}',p.get(n,'')) is not None,'actual HRESULT '+n)
    if p.get('pixel_sha256'):
        require(HEX.fullmatch(p['pixel_sha256']) is not None,'pixel digest')
        require(p.get('surface_bpp') in (8,16,24,32),'bounded surface bitdepth')
        require(p.get('surface_pitch',0)>=640*(p['surface_bpp']//8),'valid read row length')
        if p['surface_bpp']==8:
            require(p.get('index_zero_pixels',-1)+p.get('index_nonzero_pixels',-1)==307200,'all indexed pixels')
            require(1<=p.get('index_distinct',0)<=256,'indexed distinct')
        else:
            require(all(p.get(k)==0 for k in ('index_zero_pixels','index_nonzero_pixels','index_distinct')),'not indexed palette')
        return 'PRIMARY_SURFACE_BYTES_READ_GAME_CONTENT_UNATTRIBUTED'
    if p.get('palette_read'):
        require(HEX.fullmatch(p.get('palette_sha256','')) is not None,'palette digest')
    return 'PRIMARY_DISPLAY_READ_UNAVAILABLE_GAME_RENDER_UNKNOWN'

def verify_actual_summary(r):
    """Permanent source-safe receipt; never accepts a world/visual promotion."""
    require(r.get('schema')=='stoneage.p3i.actual_primary_observation.r1','receipt schema')
    s=r['source_run'];require(s['conclusion']=='success' and s['id']==40640162726 and s['job_id']==122656198136,'actual source action')
    require(s['artifact_download_independently_verified'] is True and s['raw_source_report_extracted_and_hashed'] is True,'source zip independent')
    require(s['raw_source_report_bytes']==45308 and s['raw_source_report_sha256']=='be1cc255e05059518d90807f308ee4641700b176545a86ea262406e97ecdf534','source raw immutable digest')
    require(s['artifact_zip_sha256']=='d523e095168538938a6229cb81fc954e21a1034e325a07e8d6612f750f3344b8','source artifact zip')
    o=r['original_run']
    require(o['original_client_executed'] is True and o['real_original_640x480_window'] is True and o['actual_quit_exit_before_cleanup'] is True,'original live source')
    require(o['original_executable_modified'] is False and o['original_world_entered'] is False and o['original_server_contacted'] is False and o['account_or_password_entered'] is False and o['original_GetACP_directly_measured'] is False,'unproven original capability')
    q=r['probe']
    require(q['observed'] is True and q['returncode']==0 and q['window_id_qualified'] is True,'independent observer')
    require(q['independent_process_global_primary_only'] is True and q['original_private_surface_read'] is False,'primary not private game buffer')
    require(all(q[k]=='0x00000000' for k in ('ddraw_create_hr','cooperative_hr','primary_create_hr','primary_lock_hr')),'actual DD success')
    require(q['surface_width']==1024 and q['surface_height']==768 and q['surface_pitch']==4096 and q['surface_bpp']==32,'actual 32-bit primary')
    require(q['sample_region']==[640,480] and q['original_client_origin']==[3,26],'bounded original client crop')
    require(q['pixel_sha256']=='e76e2132c541303e27bf4653104b7eedf60c393524e6847ed9bcd257c61ce98b','actual primary pixel digest')
    require(q['native_pixel_color_classification_not_recorded'] is True,'no invented source RGB distribution')
    require(r['screen_capture']['all_original_art_unverified'] is True and len(r['screen_capture']['rgb_sha256'])==3,'Pillow art remains unqualified')
    require(r['retention']['plaintext_original_published'] is False and r['retention']['source_claim'].startswith('encrypted data delivered as 7-day'), 'private source bounded')
    require(r['assessment']=='PRIMARY_SURFACE_BYTES_READ_GAME_CONTENT_UNATTRIBUTED' and r['overall_restoration_percent'] is None,'no original world promotion')
    return r['assessment']
