
from app import Person, db

newperson = Person(
            svn = '848392493',
            first_name = 'Maximilian',
            email = "newtest@admin.com",
            sex = "m",
                birthDate = '17.04.1999',
                origin = "AT"
                    )
db.session.add(newperson)
db.session.commit()
