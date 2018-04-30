from django.db import models
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta: 
        db_table = "res_user"

    def __str__(self):
        return json.dumps({'username': self.username, 'password': self.password, "first_name": self.first_name, "last_name": self.last_name}, sort_keys=True,indent=4, separators=(',', ': '))


@csrf_exempt
def create_user(request):
    print("Reached create_request")
    print('Reached create_user')
    
    # print(json.loads(request.body))
    print(request.body)
    if request.method == 'POST':
        json_obj = json.loads(request.body)
        username = json_obj.get('username', '')
        password = json_obj.get('password', '')
        first_name = json_obj.get('first_name', '')
        last_name = json_obj.get('last_name', '')
        a = User(username=username, password = password, first_name = first_name, last_name = last_name)
        a.save()
        return JsonResponse(a)

def get_user(request):
    print("Reached get_user")
    if request.method == 'GET':
        user = User.objects.all()
        print(user)
        # return HttpResponse(json.dumps(list(user)))
        # return JsonResponse({'results': list(user)})
        return HttpResponse(serializers.serialize("json", user), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error": "Invalid request type"}, sort_keys=True,indent=4, separators=(',', ': ')), content_type="application/json")

def delete_user(request):
    print("Reached delete user")
    try:
        if(request.method == 'DELETE'):
            body = json.loads(request.body)
            user = User.objects.get(id=body.get("id", '')).delete()
            return HttpResponse(user)
        else:
            return HttpResponse("Invalid request type.")
    except Exception as e:
        return HttpResponse(e)


class Comment(models.Model):
    class Meta:
        db_table = "comment"

    user_id = models.ForeignKey(User, on_delete=models.PROTECT, db_column = 'user_id')
    parent_comment_id = models.ForeignKey("Comment", on_delete=models.CASCADE, db_column = 'parent_comment_id', blank=True, null=True)
    comment_message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    # def __str__(self):
        # json.dumps({'id': self.id, 'parent_comment_id': self.parent_comment_id, 'user_id': self.user_id, "comment_message": self.comment_message}, sort_keys=True,indent=4, separators=(',', ': '))

@csrf_exempt
def create_comment(request):
    print("Reached create_comment")
    if(request.method == 'POST'):
        data = json.loads(request.body)
        comment_data = data
        print(data.get('parent_comment_id'))
        if "parent_comment_id" in data:
            try:
                parent = Comment.objects.get(id=data.get('parent_comment_id'))
                comment_data["parent_comment_id"] = parent
            except:
                pass
        if "user_id" in data:
            try:
                user = User.objects.get(id=data.get('user_id'))
                print(type(user))
                comment_data["user_id"] = user
            except:
                pass
        print("Commnet data user_id", comment_data.get('user_id', ''))
        comment = Comment(user_id = comment_data.get('user_id', None),
                          parent_comment_id = comment_data.get('parent_comment_id', None),
                          comment_message = comment_data.get('comment_message', ''),
                          created_at = comment_data.get('created_at', None),
                          modified_at = comment_data.get('modified_at', None)) 
        comment.save()
        return HttpResponse(comment)
    else:
        return HttpResponse("Invalid request type")

@csrf_exempt
def delete_comment(request):
    print("Reached delete_comment")
    if request.method == "DELETE":
        data = json.loads(request.body)
        comment = Comment.objects.get(id=data.get('comment_id'))
        return HttpResponse(comment.delete())
    else:
        return HttpResponse("Invalid request type.")

@csrf_exempt
def get_comments(request):
    print(request.GET)
    print("Reached get_comments")
    if request.GET != None:
        print('query in request')
        return HttpResponse('query in request')
    return HttpResponse(request)
    # data = json.loads(request.query)


@csrf_exempt
def get_user_comments(request):
    if request.method == "GET" and request.GET != None:
        bfs_query = str("WITH RECURSIVE CommentCTE AS (") + \
                str("SELECT id, parent_comment_id, user_id ") + \
                str("FROM comment ") + \
                str("WHERE parent_comment_id is NULL AND user_id=") + request.GET.get('user_id', None) + \
                str("") + \
                str("UNION ALL ") + \
                str("") + \
                str("SELECT child.id, child.parent_comment_id, child.user_id ") + \
                str("FROM comment child ") + \
                str("JOIN CommentCTE ") + \
                str("ON child.parent_comment_id = CommentCTE.id ") + \
                str(") ") + \
                str("SELECT * FROM CommentCTE") \

        dfs_query = str("WITH RECURSIVE comment_cte(level,path,id, parent_comment_id, user_id) as (") + \
            str("       select 0,id::text, id, parent_comment_id,user_id from comment where parent_comment_id is null") + \
            str("   union all") + \
            str("       select")+ \
            str("           level + 1,") + \
            str("           path::text || ' > ' || child.id::text,") + \
            str("           child.id , child.parent_comment_id, child.user_id") + \
            str("       from ") + \
            str("           comment child") + \
            str("           inner join comment_cte on child.parent_comment_id = comment_cte.id ") + \
            str(") select * from comment_cte order by path;")
        user_comments = Comment.objects.raw(dfs_query)

        return HttpResponse(serializers.serialize("json", user_comments), content_type="application/json")
    return HttpResponse("Invalid request type")
    # data = json.loads(request.query)