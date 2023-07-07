points = {
    (0, 1): 2,
    (0, 2): 3.8,
    (0, 3): 2.7,
    (1, 2): 2.5,
    (1, 3): 4.1,
    (2, 3): 3.9,
}


def calculate_distance(coordinates):
    n = 0
    k = 0
    s = 0.0
    i = 0
    if len(coordinates) <= 1:
        return 0.0
    while i < len(coordinates):
        if i == 0:
            k = coordinates[i]
        else:
            n = k
            k = coordinates[i]
        if n < k:
            if (n, k) in points:
                s = s + points[(n, k)]
            else:
                k = n
        elif n > k:
            if (k, n) in points:
                s = s + points[(k, n)]
            else:
                k = n
        i += 1
    return s

print(calculate_distance((0,1,3,2,0)))