list_contacts = [
                    {
                        "name": "Allen",
                        "email": "Allen@vestibul.co.uk",
                        "phone": "(992) 914-3792",
                        "favorite": False,
                    },
                    {
                        "name": "Raymond",
                        "email": "Raymond@vestibul.co.uk",
                        "phone": "(992) 149-3792",
                        "favorite": True,
                    },
                    {
                        "name": "Willy",
                        "email": "Willy@vestibul.co.uk",
                        "phone": "(992) 491-3792",
                        "favorite": False,
                    }
                ]

res = []
for s in filter(lambda x: x["favorite"], list_contacts):
    res.append(s)
print(res)
