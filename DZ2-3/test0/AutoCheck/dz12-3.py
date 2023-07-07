import csv

contacts = [{'name': 'Allen Raymond',
             'email': 'nulla.ante@vestibul.co.uk', 
             'phone': '(992) 914-3792', 
             'favorite': False
            },
            {'name': 'Chaim Lewis', 
             'email': 'dui.in@egetlacus.ca', 
             'phone': '(294) 840-6685', 
             'favorite': True
            }
           ]

filename = 'contacts.csv'

def write_contacts_to_file(filename, contacts):
    print(contacts)
    with open(filename, 'w', newline='') as fh:
        head = []
        for key in contacts[0].keys():
            head.append(key)
        #print(head)
        writer = csv.DictWriter(fh, fieldnames=head)    # delimiter = ',' (default)
        writer.writeheader()
        for rec in contacts:
            #print(rec)
            writer.writerow(rec)
        print('--------------------------')

def read_contacts_from_file(filename):
    res = []
    with open(filename, 'r', newline='') as fh:
        reader = csv.DictReader(fh)                     # delimiter = ',' (default)
        for row in reader:
            print(row)
            print('--------------------------')
            for rk, rv in row.items():
                if rv == 'True':
                    row[rk] = True
                elif rv == 'False':
                    row[rk] = False
            #print(row)
            res.append(row)
    print(res)
    return res    

write_contacts_to_file(filename, contacts)
read_contacns = read_contacts_from_file(filename)
print(contacts == read_contacns)
