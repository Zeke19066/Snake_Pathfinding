people = [
{'name': "Tom", 'age': 10},
{'name': "Mark", 'age': 5},
{'name': "Pam", 'age': 7}
]

b = list(filter(lambda person: person['name'] == 'Pam', people))

if b != []:
    print(b)