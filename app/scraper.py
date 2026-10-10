
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
TZ=ZoneInfo("America/Sao_Paulo")
MONEY=re.compile(r"R\$\s*([\d\.]+,\d{2})")
COUNT=re.compile(r"Histórico de lances\s*\((\d+)\)",re.I)
INC=re.compile(r"Lance\s*\(incremento:\s*R\$\s*([\d\.]+,\d{2})\)",re.I)
END=re.compile(r"Encerramento\s+(\d{1,2})\s+([a-zç]+)\.?\s+a partir das\s+(\d{1,2}):(\d{2})(?::(\d{2}))?",re.I)
MONTHS={"jan":1,"fev":2,"mar":3,"abr":4,"mai":5,"jun":6,"jul":7,"ago":8,"set":9,"out":10,"nov":11,"dez":12}
def br_money(s): return float(s.replace(".","").replace(",", ".")) if s else None
def after(text,label):
    m=re.search(re.escape(label)+r".{0,140}?R\$\s*([\d\.]+,\d{2})",text,re.I|re.S)
    return br_money(m.group(1)) if m else None
def end_at(text):
    m=END.search(text)
    if not m:return None
    d,mon,h,mi,s=m.groups(); month=MONTHS.get(mon[:3].lower())
    if not month:return None
    now=datetime.now(TZ); dt=datetime(now.year,month,int(d),int(h),int(mi),int(s or 0),tzinfo=TZ)
    if (now-dt).days>180:dt=dt.replace(year=now.year+1)
    return dt.isoformat()
async def scrape_lot(page,cfg):
    await page.goto(cfg["url"],wait_until="domcontentloaded",timeout=60000)
    try: await page.wait_for_load_state("networkidle",timeout=10000)
    except Exception: pass
    try: await page.get_by_text(re.compile(r"Valor (atual|inicial)",re.I)).first.wait_for(timeout=15000)
    except Exception: pass
    text=(await page.locator("body").inner_text(timeout=30000)).replace("\r","")
    typ="Atual" if re.search(r"Valor atual",text,re.I) else "Inicial"
    cur=after(text,"Valor atual") or after(text,"Valor inicial")
    m=COUNT.search(text); bids=int(m.group(1)) if m else 0
    m=INC.search(text); inc=br_money(m.group(1)) if m else None
    nxt=None
    block=re.search(r"Lance\s*\(incremento:.*?(?=Total com despesas e comissão:|$)",text,re.I|re.S)
    if block:
        vals=[br_money(v) for v in MONEY.findall(block.group(0))]
        if vals:nxt=vals[-1]
    if nxt is None:nxt=cur
    disp=after(text,"Total com despesas e comissão:")
    rem=None
    m=re.search(r"Tempo restante\s*[•·]?\s*(.+?)(?:\n|Encerramento)",text,re.I)
    if m:rem=" ".join(m.group(1).split())
    return dict(captured_at=datetime.now(timezone.utc).isoformat(),lot=cfg["lot"],ref=cfg.get("ref"),title=cfg.get("title"),
                value_type=typ,current_value=cur,bid_count=bids,increment=inc,next_bid=nxt,displayed_total=disp,
                end_at=end_at(text),remaining_text=rem,raw_excerpt="\n".join(text.splitlines()[:120])[:7000],
                parse_ok=int(cur is not None and nxt is not None),error=None)
