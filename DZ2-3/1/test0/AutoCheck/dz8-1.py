from datetime import datetime
date = '2020-10-09'

def get_days_from_today(date):
    ldt = date.split('-')
    dt = datetime(year=int(ldt[0]), month=int(ldt[1]), day=int(ldt[2])).date()
    cdt = datetime.now().date()
    rdt = (dt - cdt)
    return rdt.days

print(get_days_from_today(date))
