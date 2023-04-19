from datetime import datetime, timedelta


users = ({'name': 'Bill', 'birthday': datetime(year=1988, month=4, day=19)},
         {'name': 'Jill', 'birthday': datetime(year=2001, month=4, day=19)},
         {'name': 'Kim', 'birthday': datetime(year=1999, month=4, day=20)},
         {'name': 'Kate', 'birthday': datetime(year=2007, month=4, day=25)},
         {'name': 'Jan', 'birthday': datetime(year=1988, month=4, day=23)}
        )

def get_birthdays_per_week(users):
    weekdays = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    listdays = [[], [], [], [], []]
    res = []

    def add_name(weekday, name):
        wd = weekday if weekday <= 4 else 0
        listdays[wd].append(name)

    def get_str(weekday):
        wd = weekday if weekday <= 4 else 0
        st = ''
        t = weekdays[wd] + ': '
        for s in listdays[wd]:
            st = st + t + s
            t = ', '
        return st

    curdate = datetime.now().date()
    nextdate = curdate + timedelta(days=1)
    nextweek = curdate + timedelta(days=7)

    for m in users:
        n = m["name"]
        d = m["birthday"].date()
        dt = datetime(year=curdate.year, month=d.month, day=d.day).date()

        if dt > curdate and dt <= nextweek:
            wd = dt.weekday()
            add_name(wd, n)
    
    for i in range(7):
        wd = nextdate.weekday()
        if ((wd + i) % 7) <= 4:
            st = get_str((wd + i) % 7)
            if len(st) > 0:
                res.append(st)
    return res

print(get_birthdays_per_week(users))
