import sys

def parse_args():
    result = ""
    for i in range(len(sys.argv)):
        if i > 0:
            result = result + sys.argv[i] + " "
    #print(result)
    result = "'" + result.rstrip() + "'"
    return result

print(parse_args())