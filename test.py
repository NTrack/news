import  jwt
from  news.news.settings import SECRET_KEY
encoded_jwt = jwt.encode({'username':'运维咖啡吧','site':'https://ops-coffee.cn'},SECRET_KEY,algorithm='HS256')
print(encoded_jwt)
print(jwt.decode(encoded_jwt,SECRET_KEY,algorithms=['HS256']))