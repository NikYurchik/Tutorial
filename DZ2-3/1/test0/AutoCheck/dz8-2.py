from datetime import date

#date = '2020-10-09'
month1 = 2
year1 = 2021
def get_days_in_month(month, year):
    dt1 = date(day=1, month=month, year=year)
    month2 = month+1 if month < 12 else 1
    year2 = year + (month+1)//12
    dt2 = date(day=1, month=month2, year=year2)
    print(dt1, dt2, (dt2-dt1).days)
    return (dt2-dt1).days
print(get_days_in_month(month1, year1))
