"""Test the actual file:// generated atlas in Chromium, not a synthetic page."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

path = Path(sys.argv[1]).resolve()
assert path.is_file()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(offline=True)
    errors, network = [], []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: network.append(r.url) if r.url.startswith(("http://", "https://")) else None)
    page.goto(path.as_uri())
    expect(page.locator("#summary")).to_contain_text("5924")
    expect(page.locator("#list button")).to_have_count(40)
    page.locator("#next").click()
    expect(page.locator("#page")).to_contain_text("2/")
    page.locator("#prev").click()
    expect(page.locator("#page")).to_contain_text("1/")
    page.locator("#source").select_option("tw10")
    page.locator("#query").fill("PET-000001")
    expect(page.locator("#list button")).to_have_count(1)
    page.locator("#list button").click()
    expect(page.locator("#detail h2")).to_have_text("烏力")
    expect(page.locator("#detail")).to_contain_text("100250")
    expect(page.locator("#detail")).to_contain_text("初始数值与区间")
    expect(page.locator("#detail")).to_contain_text("原零售档案编号与来源")
    expect(page.locator("#detail")).to_contain_text("私人观察凭证（本页不含原图）")
    page.locator("#source").select_option("tw75")
    page.locator("#query").fill("")
    expect(page.locator("#page")).to_contain_text("467")
    page.locator("#query").fill("TW75-TEMPLATE-1")
    expect(page.locator("#list button")).to_have_count(1)
    page.locator("#list button").click()
    expect(page.locator("#detail h2")).to_have_text("烏力")
    expect(page.locator("#detail")).to_contain_text("TW75-TEMPLATE-1")
    expect(page.locator("#detail")).to_contain_text("12–18")
    expect(page.locator("#detail")).to_contain_text("攻擊")
    expect(page.locator("#detail")).to_contain_text("坐标原范围")
    for heading in ("条件一级面板范围", "条件每级内部增量", "配置技能槽", "保存档取得"):
        expect(page.locator("#detail")).to_contain_text(heading)
    page.locator("#query").fill("NOT_A_HISTORICAL_PET_000")
    expect(page.locator("#list button")).to_have_count(0)
    assert not errors, errors
    assert not network, network
    browser.close()
print("PET_ATLAS_FILE_BROWSER_PASS: offline, pagination, source filter, Wuli profile, TW75 fields, negative query, zero external requests or page errors")
