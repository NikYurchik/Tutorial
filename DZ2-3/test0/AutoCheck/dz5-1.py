def real_len(text):
    s = ''
    for v in text:
        if v not in ['\n','\f','\r','\t','\v']:
            s = s + v
    print(s)
    print(len(s))
    return len(s)

real_len('Alex\nKdfe23\t\f\v.\r')
real_len('Al\nKdfe23\t\v.\r')