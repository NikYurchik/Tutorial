from collections import Counter

IP = [
    "85.157.172.253",
    "85.157.172.253",
    "85.157.172.253",
    "185.157.172.253",
    "185.157.172.253",
    "115.157.172.253",
    "157.172.253.85",
    "157.172.253.90",
    "157.172.253.100",
]

def get_count_visits_from_ip(ips):
    return(dict(Counter(ips)))


def get_frequent_visit_from_ip(ips):
    return(Counter(ips).most_common(1)[0])

m = get_count_visits_from_ip(IP)
print(m)
n = get_frequent_visit_from_ip(IP)
print(n)
