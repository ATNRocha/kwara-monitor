
ADMIN_FEES=[(0.01,99.99,49),(100,199.99,65),(200,299.99,84),(300,399.99,110),(400,499.99,141),(500,649.99,182),(650,799.99,241),(800,999.99,317),(1000,1099.99,346),(1100,1999.99,484),(2000,3999.99,773),(4000,4999.99,963),(5000,6999.99,1100),(7000,9999.99,1360)]
def admin_fee(bid):
    for lo,hi,fee in ADMIN_FEES:
        if lo<=float(bid)<=hi:return float(fee)
    raise ValueError(f"Lance fora das faixas configuradas: {bid}")
def total_cost(bid): return round(float(bid)*1.05+admin_fee(bid),2)
def financial_status(next_bid,max_bid):
    if max_bid<=0:return "NÃO OFERTAR"
    if next_bid<=max_bid*.90:return "ATRATIVO"
    if next_bid<=max_bid:return "NO LIMITE"
    return "ACIMA DO TETO"
def cb_index(market,cost,tech,aesthetic):
    if not market:return 0.0
    margin=max(0.0,(market-cost)/market)
    fin=min(10.0,margin*15.0)
    return round(tech*.45+aesthetic*.15+fin*.40,2)
