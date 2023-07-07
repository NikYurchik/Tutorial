


def parse_url(next_url, data_lst=None, counter=None):
    if not data_lst:
        data_lst = []
    if not counter:
        counter = 1
    print(f"Do some work on page {next_url}{counter}")
    data_lst.append(f"{next_url}{counter}")
    counter += 1
    if counter > 10:  # тут умова коли кнопки NEXT немає, це вихід з рекурсії
        return data_lst
    else:
        lst = parse_url(next_url, data_lst, counter)
        return lst


if __name__ == "__main__":
    print(parse_url("www.some_site.com/"))
        