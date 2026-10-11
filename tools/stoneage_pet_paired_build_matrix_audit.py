"""Exact pinned client/server PET build-entrypoint audit; source-only, NOT a compiled binary."""
import argparse
from pathlib import Path
import re
import subprocess

COMMIT="999ffdf1d220ec6666eb65339180689c9caf1876"
PINS={
"client/build-client.ps1":"7045da30a9e54a3ffba997069bb32cc2f9112e18",
"client/stoneage.sln":"7dd2bf48f50aa3bd3439a6b1848088934cc0a9db",
"client/stoneage.vcxproj":"373c0699a5df017f53e4ab7a7d64c3d6280a8578",
"client/resources/version.h":"35bd4446a740a189c1ad9439e30e61fe169d5f46",
"server/CMakeLists.txt":"1523d12c3543e3d2a8c3a1401f92d79d11d85413",
"server/scripts/build-linux.sh":"17a6c21ad76634a4141383960549121bf76a1724",
"server/scripts/build-windows.ps1":"b9357b25a1cb5a0fd041d4c8a1b55ec53c2978ca",
"server/gmsv/makefile":"8afd1f288a1d07a5cf0075af04e51e64741dcc81",
"server/common/makefile":"263ef622f4c0c3ac495d783ff35b078277984d43",
"server/gmsv/include/version.h":"b3fc0c80705973bc8d088287c98a5d66171bb6c2",
}
RESOLUTION="RESOLUTION|PET_PAIR_BUILD_DEFAULT_DISABLED_SOURCE_ONLY_PASS"
NAMES=("client_header","client_special","client_version80_forced","server_header","server_pet_forced")

def demand(ok,why):
    if not ok:raise ValueError(why)

def pinned(root):
    def git(*args):return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()
    demand(git("rev-parse","HEAD")==COMMIT,"wrong pinned commit")
    result={}
    for path,sha in PINS.items():
        demand(git("hash-object",path)==sha,"pinned file changed "+path)
        result[path]=(root/path).read_text(encoding="utf-8-sig",errors="replace")
    return result

def macros(root,header,compiler,*args):
    command=[compiler,"-dM","-E","-x","c++" if compiler=="g++" else "c",
             "-I",str(root/"server/gmsv/include"),
             "-I",str(root/"server/common"),
             "-I",str(root/"server/common/utils"),
             "-I",str(root/"shared/lua51"),
             *args,"-include",str(root/header),"-"]
    out=subprocess.run(command,input="",text=True,capture_output=True,check=True,timeout=40).stdout
    return set(re.findall(r"(?m)^#define\s+([A-Za-z_]\w*)\b",out))

def check(root):
    f=pinned(root)
    m=re.search(r"GlobalSection\(SolutionConfigurationPlatforms\)(.*?)EndGlobalSection",
                f["client/stoneage.sln"],re.S)
    demand(m is not None,"client solution configs missing")
    solution=re.findall(r"(?m)^\s+([A-Za-z_0-9]+)\|Win32\s*=",m.group(1))
    demand(solution==["VER25_DEBUG","VER25_RELEASE"],
           "solution-selected names changed "+str(solution))
    xml=f["client/stoneage.vcxproj"]
    groups=re.findall(r"<ItemDefinitionGroup\b[^>]*Condition=\"([^\"]+)\"[^>]*>(.*?)</ItemDefinitionGroup>",
                      xml,re.S)
    profiles={}
    for condition,content in groups:
        name=re.search(r"==\'([^|']+)\|Win32\'",condition)
        if name:
            item=re.search(r"<PreprocessorDefinitions>(.*?)</PreprocessorDefinitions>",content,re.S)
            profiles[name.group(1)]=item.group(1).split(";") if item else []
    demand(all(k in profiles and "_SA_VERSION_SPECIAL" in profiles[k] for k in solution),
           "solution VER25 profiles no longer use special version")
    demand(all(not any("_SA_VERSION_80" in v or "_PET_ITEM" in v
                       for v in profiles[k]) for k in solution),
           "checked-in solution version80 PET feature unexpectedly enabled")
    demand("Debug" in profiles and "Release" in profiles
           and not profiles["Debug"] and not profiles["Release"],
           "standalone Debug/Release property groups changed")
    script=f["client/build-client.ps1"]
    demand("[ValidateSet('VER25_Release', 'VER25_Debug')]" in script
           and "[string]$Configuration = 'VER25_Release'" in script
           and '"/p:Configuration=$Configuration"' in script,
           "client build entrypoint default/arguments changed")
    ch=f["client/resources/version.h"]
    demand(re.search(r"(?m)^#define\s+_SA_VERSION_25\b",ch)
           and re.search(r"#ifdef\s+_SA_VERSION_80[\s\S]*?#define\s+_PET_ITEM\b",ch),
           "client PET macro conditional source drift")
    sh=f["server/gmsv/include/version.h"]
    demand(not re.search(r"(?m)^\s*#define\s+_PET_ITEM\b",sh),
           "server version.h default unexpectedly enables PET")
    cmake=f["server/CMakeLists.txt"]
    defs=re.search(r"set\(STONEAGE_WINDOWS_DEFINITIONS(.*?)\)",cmake,re.S)
    demand(defs and "_PET_ITEM" not in defs.group(1)
           and "target_compile_definitions(" in cmake
           and "STONEAGE_WINDOWS_DEFINITIONS" in cmake,
           "Windows CMake PET compile flag changed")
    win=f["server/scripts/build-windows.ps1"]
    linux=f["server/scripts/build-linux.sh"]
    demand("-DCMAKE_BUILD_TYPE=$Configuration" in win and "_PET_ITEM" not in win,
           "Windows server wrapper now mentions PET override")
    demand('BUILD_TYPE="release"' in linux and "_PET_ITEM" not in linux,
           "Linux server wrapper default PET flag drift")
    for p in ("server/gmsv/makefile","server/common/makefile"):
        demand("CFLAGS=" in f[p] and "_PET_ITEM" not in f[p],
               "checked-in GNU server compile flags now mention PET")
    ps={
      "client_header":macros(root,"client/resources/version.h","g++"),
      "client_special":macros(root,"client/resources/version.h","g++","-D_SA_VERSION_SPECIAL"),
      "client_version80_forced":macros(root,"client/resources/version.h","g++","-D_SA_VERSION_SPECIAL","-D_SA_VERSION_80"),
      "server_header":macros(root,"server/gmsv/include/version.h","gcc"),
      "server_pet_forced":macros(root,"server/gmsv/include/version.h","gcc","-D_PET_ITEM")}
    expected={"client_header":0,"client_special":0,"client_version80_forced":1,
              "server_header":0,"server_pet_forced":1}
    demand("_SA_VERSION_25" in ps["client_header"]
           and "_SA_VERSION_60" in ps["client_special"]
           and "_SA_VERSION_80" not in ps["client_special"]
           and "_SA_VERSION_80" in ps["client_version80_forced"],
           "client macro profile closure changed")
    for name,value in expected.items():
        demand(int("_PET_ITEM" in ps[name])==value, "PET macro profile "+name+" drift")
    kv={
      "pinned_commit":COMMIT,"source_blobs":"10",
      "sln_configs":"VER25_DEBUG,VER25_RELEASE",
      "script_default":"VER25_RELEASE","vs_solution_active_pet":"0",
      "server_make_default_pet":"0","server_windows_cmake_default_pet":"0",
      "paired_checked_in_default_pet":"0","client_forced_80_pet":"1",
      "server_forced_pet":"1","actual_enabled_pair_binaries":"0",
      "actual_network_packet":"0","original_early_feature_verified":"0"}
    return [
      "SOURCE_PET_PAIR_GATE|"+"|".join(f"{k}={v}" for k,v in kv.items()),
      *[f"SOURCE_PET_PAIR_PROFILE|name={name}|pet={expected[name]}" for name in NAMES],
      "BOUNDARY|Checked-in late-descendant solution VER25 profiles and GNU/MinGW server defaults have no PET gate; forcing both macro gates is a counterfactual preprocessor check, not a successful paired compile, link, deployed binary or historical 1999 feature",
      "CORRECTION|Prior prose identifying Debug and Release as the two solution-selected configurations was imprecise; actual solution selects VER25_DEBUG and VER25_RELEASE, while vcxproj also has standalone Debug/Release groups not selected by the solution",
      "OPEN|Any independently verified compiled PET-enabled pair; native client-server handshake, actual opcode127 packet, persistent item owner/unique-code lifecycle, early Japan/Taiwan version attribution",
      RESOLUTION]

def fields(line):
    a=[x.split("=",1) for x in line.split("|")[1:]]
    demand(all(len(x)==2 for x in a) and len(set(x[0] for x in a))==len(a),
           "malformed or repeated field")
    return dict(a)

def validate_report(raw):
    ls=raw.splitlines()
    demand(len(ls)==10 and ls[0].startswith("SOURCE_PET_PAIR_GATE|")
           and ls[-1]==RESOLUTION,"missing report boundaries")
    expected={"pinned_commit":COMMIT,"source_blobs":"10",
              "sln_configs":"VER25_DEBUG,VER25_RELEASE",
              "script_default":"VER25_RELEASE","vs_solution_active_pet":"0",
              "server_make_default_pet":"0","server_windows_cmake_default_pet":"0",
              "paired_checked_in_default_pet":"0","client_forced_80_pet":"1",
              "server_forced_pet":"1","actual_enabled_pair_binaries":"0",
              "actual_network_packet":"0","original_early_feature_verified":"0"}
    demand(fields(ls[0])==expected,"incorrect paired build or historical claim")
    for i,name in enumerate(NAMES,1):
        demand(ls[i].startswith("SOURCE_PET_PAIR_PROFILE|")
               and fields(ls[i])=={"name":name,"pet":"1" if name in
                        ("client_version80_forced","server_pet_forced") else "0"},
               "preprocessor row source scope changed")
    demand(ls[6].startswith("BOUNDARY|") and "counterfactual" in ls[6]
           and "not a successful paired compile" in ls[6]
           and ls[7].startswith("CORRECTION|") and "VER25_DEBUG" in ls[7]
           and ls[8].startswith("OPEN|"),"missing original-version boundary")
    return expected

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--checkout",type=Path,required=True)
    args=p.parse_args()
    s="\n".join(check(args.checkout))+"\n"
    validate_report(s)
    print(s,end="")
if __name__=="__main__":main()
