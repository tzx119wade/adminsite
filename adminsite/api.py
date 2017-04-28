from .serializers import UserSerializers,UserProfileSerializers,GeneralSerializers, UserInfoSerializers
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import UserProfile
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


# 登录接口
@api_view(['POST'])
@csrf_exempt
def login(request):

    serializers = UserSerializers(data=request.data)
    # 数据验证是否成功
    if serializers.is_valid():
        username = serializers.initial_data['username']
        password = serializers.initial_data['password']

        # 查询有没有这个用户
        user = authenticate(username=username,password=password)
        if user is not None:
            # 查询是不是admin用户
            if user.username == 'tangzhenxing':
                # 生成token
                token = Token.objects.create(user=user)
                # 保存token返回给前台
                body = {
                    'success':1,
                    'token':token.key,
                    'msg':'welcome back,super admin',
                }
                return Response(body, status=status.HTTP_200_OK)
            else:
                body = {
                    'success':2,
                    'msg':'Sorry, You Cant Login This Site',
                }
                return Response(body, status=status.HTTP_403_FORBIDDEN)
        else:
            body = {
                'success':3,
                'msg':'user is ont exist,please try again',
            }
            return Response(body, status=status.HTTP_404_NOT_FOUND)
    # 如果验证失败
    else:
        body = {
            'success':4,
            'msg':serializers.errors,
        }
        return Response(body, status=status.HTTP_400_BAD_REQUEST)

# logout接口
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def logout(request):
    if request.auth :
        if request.method == "GET" :
            request.user.auth_token.delete()
            body = {
                'msg' : 'Token is delete',
            }
            return Response(body, status=status.HTTP_200_OK)
    else:
        body = {
            'msg' : 'something wrong',
        }
        return Response(body, status=status.HTTP_400_BAD_REQUEST)

# 获取用户列表的接口
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def user(request):
    print ('auth is :',request.auth)
    print ('user is :',request.user)
    if request.method == 'GET':
        if request.auth:
            queryset = UserProfile.objects.filter(is_admin=False).order_by('-id')
            serializers = UserProfileSerializers(queryset, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            body = {
                'msg':'Sorry,Please login first',
            }
            return Response(body, status=status.HTTP_403_FORBIDDEN)

# 添加用户的接口
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def adduser(request):
    print ('auth is :',request.auth)
    if request.auth:
        if request.method == 'POST':
            serializers = GeneralSerializers(data=request.data)
            if serializers.is_valid():
                # 取数据
                username = serializers.initial_data['username']
                password = serializers.initial_data['password']
                email = serializers.initial_data['email']
                identity = serializers.initial_data['identity']

                # 判断是否已有这个用户
                try:
                    user_is_exist = User.objects.get(username=username)
                except User.DoesNotExist:
                    # 创建user对象
                    user = User.objects.create_user(username=username, password=password, email=email)
                    # 创建 userprofile 对象
                    # 默认头像
                    profile_image = "https://cdn.sspai.com/user/725653_1488337112561.png?imageMogr2/quality/95/thumbnail/!120x120r/gravit"
                    userprofile = UserProfile.objects.create(belong_to=user,identity=identity,nick_name=username,profile_image=profile_image)
                    # 返回成功
                    return Response(serializers.data, status=status.HTTP_201_CREATED)

                # 如果这个用户已经存在
                body = {
                    'msg':'User is already exist'
                }
                return Response(body, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        body = {
            'msg':'Sorry,Please login first',
        }
        return Response(body, status=status.HTTP_403_FORBIDDEN)


# 删除用户的接口
@api_view(['DELETE'])
@authentication_classes((TokenAuthentication,))
def deleteuser(request,id):

    if request.auth :
        if request.method == 'DELETE':
            userprofile = UserProfile.objects.get(id=id)
            user = userprofile.belong_to
            user.delete()
            body = {
                'msg':'delete is ok',
            }
            return Response(body, status=status.HTTP_200_OK)
    else:

        body = {
            'msg':'sorry,you have no right to delete user',
        }
        return Response(body, status=status.HTTP_403_FORBIDDEN)

# invited user
@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
def invited(request,id):
    if request.auth :
        if request.method == 'PUT':
            userprofile = UserProfile.objects.get(id=id)
            userprofile.identity = 'author'
            userprofile.save()
            body = {
                'msg':'invited is success',
            }
            return Response(body, status=status.HTTP_200_OK)

    else:

        body = {
            'msg': 'sorry, you can not touch this user',
        }
        return Response(body, status=status.HTTP_403_FORBIDDEN)

# 禁止用户登录接口
@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
def ban_user(request,id):
    if request.auth :
        if request.method == 'PUT':
            userprofile = UserProfile.objects.get(id=id)
            user = userprofile.belong_to
            user.is_active = False
            user.save()

            body = {
                'msg':'ban is ok'
            }
            return Response(body, status=status.HTTP_200_OK)

    else:
        body = {
            'msg': 'sorry, you can not touch this user',
        }
        return Response(body, status=status.HTTP_403_FORBIDDEN)

# 获取用户详情接口
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def user_detail(request,id):
    if request.auth :
        if request.method == 'GET':
            # 获取数据
            userprofile = UserProfile.objects.get(id=id)
            # 序列化
            serializers = UserProfileSerializers(userprofile)
            return Response(serializers.data, status=status.HTTP_200_OK)
    else:
        body = {
            'msg':'BAD REQUEST',
        }
        return Response(body, status=status.HTTP_400_BAD_REQUEST)

# 修改用户详情接口
@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
def change_user_info(request,id):
    if request.auth :
        if request.method == 'PUT':
            userprofile = UserProfile.objects.get(id=id)
            user = userprofile.belong_to
            # 获取数据
            serializers = UserInfoSerializers(data=request.data)
            if serializers.is_valid():
                new_username = serializers.initial_data['username']
                new_password = serializers.initial_data['password']

                # 重新设置用户名及密码
                user.set_password(new_password)
                user.username = new_username
                user.save()
                # 返回成功
                body = {
                    'msg':'change is ok',
                }
                return Response(body, status=status.HTTP_201_CREATED)

            else:
                body = {
                    'msg':serializers.errors,
                }
                return Response(body, status=status.HTTP_400_BAD_REQUEST)
    else:
        body = {
            'msg' : 'you have no right to change',
        }
        return Response(body, status=status.HTTP_403_FORBIDDEN)
