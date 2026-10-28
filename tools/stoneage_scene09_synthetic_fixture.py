"""Synthetic-only browser fixture for source-order switching. No original art."""
import json,sys,tempfile
from pathlib import Path
from tools.stoneage_scene08_synthetic_fixture import write as write_r8

def write(target):
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'synthetic.html';write_r8(p)
        pack=json.loads(p.read_text().split('<script id="evidence" type="application/json">')[1].split('</script>')[0])
    root=Path(__file__).resolve().parents[1]
    pack['actor_order_evidence']=json.loads((root/'research/recovered/STONEAGE-SCENE09-NATIVE-ORDER-R9.json').read_text())
    template=Path(__file__).with_name('scene-room-order-viewer-r9.html').read_text()
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(template.replace('"PRIVATE_PACK_PLACEHOLDER"',json.dumps(pack,ensure_ascii=False)))

if __name__=='__main__':write(sys.argv[1])
