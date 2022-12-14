from django.http import HttpResponse
from django.template import loader

from mongoDB.mongoDB_manager import MongoDBManager

COLLECTION_NAME = "SmartHomeService"

def specific_user(request, username):
    def get():
        user_data = MongoDBManager().get_data({'name': username}, COLLECTION_NAME)
        user = user_data[0]
        del user['_id']

        template = loader.get_template('User.html')
        return HttpResponse(template.render({'userData' : [user]}, request))

    if(request.method == "GET"):
        return get()
    
    else:
        return HttpResponse(status = 405)

def all_users(request):
    def get():
        user_data = MongoDBManager().get_data({}, COLLECTION_NAME)

        users = []
        for user in user_data:
            del user['_id']
            users.append(user)
        
        template = loader.get_template('User.html')
        return HttpResponse(template.render({'userData' : users}, request))

    if(request.method == "GET"):
        return get()
    else:
        return HttpResponse(status=405)