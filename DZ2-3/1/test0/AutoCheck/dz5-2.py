articles_dict = [
    {
        "title": "Endless ocean waters.",
        "author": "Jhon Stark",
        "year": 2019,
    },
    {
        "title": "Oceans of other planets are full of silver",
        "author": "Artur Clark",
        "year": 2020,
    },
    {
        "title": "An ocean that cannot be crossed.",
        "author": "Silver Name",
        "year": 2021,
    },
    {
        "title": "The ocean that you love.",
        "author": "Golden Gun",
        "year": 2021,
    },
]


def find_articles(key, letter_case=False):
    res = []
    k = key if letter_case else key.lower()
    for dc in articles_dict:
        tl = dc["title"] if letter_case else dc["title"].lower()
        au = dc["author"] if letter_case else dc["author"].lower()
        if (tl.find(k) >= 0) or (au.find(k) >= 0):
            res.append(dc)
    return res
        
print(find_articles("Silver",True))        
        
            
        
        
            
        
        
            
        
        
            
        
            
    