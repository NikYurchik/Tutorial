def is_spam_words(text, spam_words, space_around=False):
    txt = text.replace('.',' ').lower().split()
    for v in spam_words:
        v1 = v.lower()
        for s in txt:
            if space_around:
                res = (s == v1)
            else:
                 res = (s.find(v1) >= 0)
            if res:
                return res
    return False
            
print(is_spam_words("Молох", ["лох"]))  # True
print(is_spam_words("Молох", ["лох"], True))  # False
