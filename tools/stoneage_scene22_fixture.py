"""Append synthetic NPC text to an existing synthetic SCENE21 UI fixture."""
from pathlib import Path
import sys
from tools.stoneage_scene22_npc_argument import append_reader
p=Path(sys.argv[1]);s=p.read_text();assert '"synthetic_fixture":true' in s
s=append_reader(s,'合成NPC <test>','合成说明甲，乙。\nASCII,separator <script>safe</script>')
p.write_text(s)
