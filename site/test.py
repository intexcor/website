import jwt

# Your other code...

jwt_token = jwt.encode({'username': "1"}, 'SECRET_KEY', algorithm='HS256')
print(jwt_token)
