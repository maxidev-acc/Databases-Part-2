userIn = [{"name":"Maximilian", "email": "admin@test.at","sex": "M", "birthDate": "1999/03/20", "origin": "AT", "SVN": "5039 290399","role": "T"}]
print(type(userIn))

for k in userIn:
    print(k["role"])