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
