import json

users = {
    'users': [
        {
            'login': 'oskar',
            'password': 'qwerty'
        },
        {
            'login': 'admin',
            'password': 'admin'
        }
    ],
    'books':[
        {
            "title": 'book1',
            'author': 'asd',
            'pages': 123
        }
    ]
}
json_object = json.dumps(users, indent = 4)
print(json_object)

with open("users.json", "w") as outfile:
    outfile.write(json_object)


with open('users.json', 'r') as f:
    data = f.read()
    data = json.loads(data)

print(data['books'])
