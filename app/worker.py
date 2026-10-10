
import asyncio,json,signal
from datetime import datetime,timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from playwright.async_api import async_playwright
from .db import init_db,insert_snapshot,update_worker_status
from .pricing import total_cost,financial_status,cb_index
from .scraper import scrape_lot
BASE=Path(__file__).resolve().parents[1]; LOTS=BASE/"config/lots.json"; TZ=ZoneInfo("America/Sao_Paulo"); STOP=False
def load_lots(): return json.loads(LOTS.read_text(encoding="utf-8"))
def interval(end_times):
    now=datetime.now(TZ); nearest=None
    for v in end_times:
        if not v:continue
        try: secs=(datetime.fromisoformat(v).astimezone(TZ)-now).total_seconds()
        except Exception:continue
        if secs>0 and (nearest is None or secs<nearest):nearest=secs
    if nearest is None or nearest>86400:return 300
    if nearest>7200:return 120
    if nearest>900:return 60
    return 30
def stop(*_):
    global STOP; STOP=True
async def main():
    signal.signal(signal.SIGTERM,stop); signal.signal(signal.SIGINT,stop); init_db()
    lots=[x for x in load_lots() if x.get("enabled",True)]
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=["--disable-dev-shm-usage","--disable-gpu","--no-sandbox","--disable-extensions"])
        ctx=await browser.new_context(locale="pt-BR",timezone_id="America/Sao_Paulo",viewport={"width":1365,"height":900})
        page=await ctx.new_page()
        while not STOP:
            started=datetime.now(timezone.utc).isoformat(); ok=fail=0; ends=[]; last=None
            for cfg in lots:
                if STOP:break
                try:
                    row=await scrape_lot(page,cfg)
                    if row["next_bid"] is not None:
                        row["calculated_total"]=total_cost(row["next_bid"]); row["market_value"]=cfg["market_value"]; row["max_bid"]=cfg["max_bid"]
                        row["tech_score"]=cfg["tech_score"]; row["aesthetic_score"]=cfg["aesthetic_score"]
                        row["status"]=financial_status(row["next_bid"],cfg["max_bid"])
                        row["cb_index"]=cb_index(cfg["market_value"],row["calculated_total"],cfg["tech_score"],cfg["aesthetic_score"])
                    else:
                        row.update(calculated_total=None,market_value=cfg["market_value"],max_bid=cfg["max_bid"],tech_score=cfg["tech_score"],aesthetic_score=cfg["aesthetic_score"],status="ERRO DE COLETA",cb_index=0)
                    insert_snapshot(row); ends.append(row.get("end_at")); ok+=1
                except Exception as e:
                    fail+=1; last=f"Lote {cfg['lot']}: {type(e).__name__}: {e}"
                    insert_snapshot(dict(captured_at=datetime.now(timezone.utc).isoformat(),lot=cfg["lot"],ref=cfg.get("ref"),title=cfg.get("title"),
                        market_value=cfg.get("market_value"),max_bid=cfg.get("max_bid"),tech_score=cfg.get("tech_score"),aesthetic_score=cfg.get("aesthetic_score"),
                        status="ERRO DE COLETA",cb_index=0,parse_ok=0,error=last))
                await asyncio.sleep(2)
            finished=datetime.now(timezone.utc).isoformat()
            update_worker_status(updated_at=finished,cycle_started_at=started,cycle_finished_at=finished,enabled_lots=len(lots),successes=ok,failures=fail,last_error=last)
            for _ in range(interval(ends)):
                if STOP:break
                await asyncio.sleep(1)
        await ctx.close(); await browser.close()
if __name__=="__main__": asyncio.run(main())
