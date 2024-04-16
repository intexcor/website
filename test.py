from requests import *
from data import db_session
from data.jobs import Jobs

print(get('http://localhost:5000/api/v2/jobs').json())


# print(post('http://localhost:5000/api/users',
#            json={'name': 'ЕГР',
#                  'surname': 'SERg',
#                  'age': 15,
#                  'position': 'владелец столовой',
#                  'speciality': 'повар, заведующий',
#                  'address': 'там где-то',
#                  'email': 'ivanivanov200857@mail.ru',
#                  'hashed_password': '57fivogi'}).json())
#
# # print(put('http://localhost:5000/api/jobs/2', json={'team_leader': 1}).json())
# print(put('http://localhost:5000/api/users/3', json={
#       'email': 'pespatron@mama.ua'
# }).json())