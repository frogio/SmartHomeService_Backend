from django.http import HttpResponse
import json

from mongoDB.mongoDB_manager import MongoDBManager

COLLECTION_NAME = "SmartHomeService"

def specific_user(request, username):

    def get():                                     # DB 내용 조회
        users = MongoDBManager().get_data({'name' : username}, COLLECTION_NAME)            # MongoDB는 싱글톤 클래스
        response = users[0]
        del response['_id']

        return HttpResponse(json.dumps(response), status = 200)
    
    def post():                                     # DB 내용 추가
        try:
            age, job = request.POST['age'], request.POST['job']
        except:
            return HttpResponse(status= 400)

        user = {
            'name' : username,
            'age' : age,
            'job' : job
        }                                           # json으로 데이터를 덤프한 뒤

        result = MongoDBManager().add_data(user, COLLECTION_NAME)    # data를 add한다.

    if(request.method == "GET"):                    # 요청이 GET 일 때
        return get()

    elif(request.method == "POST"):                 # 요청이 POST 일 때
        return post()

    else:
        return HttpResponse(status = 405)

def all_users(request):
    def get():
        users= MongoDBManager().get_data({}, COLLECTION_NAME)
        response = []
        for user in users:
            del user['_id']
            response.append(user)

        return HttpResponse(json.dumps(response), status = 200)

    if(request.method == "GET"):
        return get()
    
    else:
        return HttpResponse(status=405)
        