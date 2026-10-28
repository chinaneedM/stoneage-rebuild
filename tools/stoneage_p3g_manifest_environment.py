"""One finite manifest-namespace experiment; self-authored x86 programs only."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
from tools.stoneage_p3f_manifest_probe import collect
from tools.stoneage_p3d_bench import run_case,evaluate_case

ROOT=Path(__file__).resolve().parents[1]
ASM1='urn:schemas-microsoft-com:asm.v1'
ASM3='urn:schemas-microsoft-com:asm.v3'
SETTINGS='http://schemas.microsoft.com/SMI/2019/WindowsSettings'
VARIANTS=('plain','wrong_namespace_zh_tw','correct_zh_tw','correct_utf8')
LAYERS=('DEFAULT','256COLOR')

def require(ok,message):
    if not ok:raise ValueError(message)

def manifest(locale,correct=True):
    require(locale in ('zh-TW','UTF-8'),'finite locale controls only')
    settings='asmv3:windowsSettings' if correct else 'windowsSettings'
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'<assembly xmlns="{ASM1}" xmlns:asmv3="{ASM3}" manifestVersion="1.0">\n'
        '<assemblyIdentity version="1.0.0.0" processorArchitecture="x86" name="StoneAgeP3GSynthetic.Namespace" type="win32"/>\n'
        f'<asmv3:application><{settings} xmlns="{SETTINGS}"><activeCodePage>{locale}</activeCodePage>'
        f'</{settings}></asmv3:application>\n</assembly>\n')

def inspect_manifest(raw):
    tree=ET.fromstring(raw)
    application=tree.find('{'+ASM3+'}application')
    require(application is not None,'asm.v3 application missing')
    require(len(application)==1,'single settings element required')
    settings=application[0];code=settings.find('{'+SETTINGS+'}activeCodePage')
    require(code is not None and code.text in ('zh-TW','UTF-8'),'code-page element missing')
    require(tree.find('{urn:schemas-microsoft-com:compatibility.v1}compatibility') is None,
            'supportedOS must not confound namespace-only comparison')
    return {'settings_namespace':settings.tag.rsplit('}',1)[0][1:],
            'active_codepage':code.text,'correct_settings_namespace':settings.tag=='{'+ASM3+'}windowsSettings'}

def paired_namespace_result(cases):
    return all(p['wrong_namespace_zh_tw']['acp_before']==p['plain']['acp_before'] and
               p['correct_zh_tw']['acp_before']==950 and p['correct_utf8']['acp_before']==65001
               for p in cases)

def simultaneous(c):
    a=evaluate_case(c);p=c['palette_state']
    return p['windows_acp']==950 and p['display_bpp']==8 and c['mode']=='ddraw' and all(
        a[k] for k in ('color_gate_passed','sendinput_gate_passed','foreground_gate_passed'))

def validate(r):
    require(r['schema']=='stoneage.p3g.manifest_namespace_environment.v1','schema')
    for k in ('original_client_downloaded','original_client_executed','original_world_entered',
              'original_process_isolation_qualified','original_server_contacted','usable_original_environment'):
        require(r[k] is False,'original capability promotion: '+k)
    require([p['layer'] for p in r['cases']]==list(LAYERS),'finite case order')
    for pair in r['cases']:
        for name in VARIANTS:
            d=pair[name]
            require(d['pointer_bytes']==4 and d['original_executed'] is False and
                    d['acp_before']==d['acp_after_console950'],'same x86 process ACP')
            require(d['ddraw_current_result']==0 and d['ddraw_create']==0 and
                    d['ddraw_current'][2]==d['display_bpp'],'same probe display state')
    require(r['namespace_effect_observed']==paired_namespace_result(r['cases']),'namespace effect')
    possible=any(simultaneous(c) for c in r['controls'])
    require(r['same_process_display_encoding_input_candidate']==possible,'same-process candidate')
    require(r['status']==('SYNTHETIC_CANDIDATE_ORIGINAL_ISOLATION_OPEN' if possible else
                          'BLOCKED_NO_SAME_PROCESS_CANDIDATE'),'status')
    require(r['original_ANSI_GDI_text_qualified'] is False,'ANSI text not measured')
    return possible

def run(directory,output):
    require(os.name=='nt','native Windows only')
    report={'schema':'stoneage.p3g.manifest_namespace_environment.v1',
        'original_client_downloaded':False,'original_client_executed':False,'original_world_entered':False,
        'original_process_isolation_qualified':False,'original_server_contacted':False,
        'original_ANSI_GDI_text_qualified':False,'usable_original_environment':False,
        'cases':[],'controls':[],'host_image_version':os.environ.get('ImageVersion'),
        'host_image_os':os.environ.get('ImageOS'),
        'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in (
            'tools/stoneage_p3g_manifest_environment.py','tools/stoneage_p3e_environment.c',
            'tools/stoneage_p3d_control.c','tools/stoneage_p3d_bench.py')},
        'embedded_manifest_readback':{}}
    try:
        for name in VARIANTS[1:]:
            raw=(directory/(name+'-readback.manifest')).read_bytes()
            report['embedded_manifest_readback'][name]=dict(inspect_manifest(raw),sha256=hashlib.sha256(raw).hexdigest())
        for layer in LAYERS:
            report['cases'].append(dict(layer=layer,**{name:collect(directory/(name+'.exe'),layer) for name in VARIANTS}))
        report['namespace_effect_observed']=paired_namespace_result(report['cases'])
        # Only spend GUI observation time if the corrected process has both prerequisites.
        row=report['cases'][1]['correct_zh_tw']
        if row['acp_before']==950 and row['display_bpp']==8 and row['ddraw_current'][2]==8:
            env=os.environ.copy();env['__COMPAT_LAYER']='256COLOR'
            for mode in ('gdi','ddraw'):
                report['controls'].append(run_case(directory/('control-'+mode),directory/'control-zh-tw.exe',env,mode,None,True))
        report['same_process_display_encoding_input_candidate']=any(simultaneous(c) for c in report['controls'])
        report['status']='SYNTHETIC_CANDIDATE_ORIGINAL_ISOLATION_OPEN' if report['same_process_display_encoding_input_candidate'] else 'BLOCKED_NO_SAME_PROCESS_CANDIDATE'
        validate(report)
    finally:
        output.write_text(json.dumps(report,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
    print('P3G_NAMESPACE_EFFECT',report['namespace_effect_observed'])
    for pair in report['cases']:
        print('P3G_CASE',pair['layer'],json.dumps({k:[pair[k]['acp_before'],pair[k]['display_bpp']] for k in VARIANTS}))
    print('P3G_STATUS',report['status'])

def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare',type=Path);p.add_argument('--directory',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--check',type=Path);a=p.parse_args()
    if a.prepare:
        a.prepare.mkdir(exist_ok=False)
        for name,locale,correct in ((VARIANTS[1],'zh-TW',False),(VARIANTS[2],'zh-TW',True),(VARIANTS[3],'UTF-8',True)):
            (a.prepare/(name+'.manifest')).write_text(manifest(locale,correct),encoding='utf-8')
    elif a.check:
        validate(json.loads(a.check.read_text()));print('P3G_ARCHIVED_SEMANTIC_REPLAY=PASS')
    else:run(a.directory,a.output)

if __name__=='__main__':main()
