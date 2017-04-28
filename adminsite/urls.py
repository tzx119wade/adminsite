from django.conf.urls import url
from .views import *
from .api import *

urlpatterns = [
    url(r'^m/userdetail/',userdetail,name='userdetail'),
    url(r'^m/userlistpanel/login',userListLogin,name='userListLogin'),
    url(r'^m/userlistpanel/$',userListPanel,name='userListPanel'),



    # api部分
    url(r'^api/login/',login),# 登录
    url(r'^api/user/',user),# 获取用户列表
    url(r'^api/adduser/',adduser),# 添加用户
    url(r'^api/deleteuser/(?P<id>\d+)',deleteuser),# 删除用户
    url(r'^api/inviteduser/(?P<id>\d+)',invited),# invited user
    url(r'^api/banuser/(?P<id>\d+)',ban_user), # 禁止用户登录
    url(r'^api/detail/(?P<id>\d+)',user_detail),# 获取用户详情
    url(r'^api/changeuserinfo/(?P<id>\d+)',change_user_info), # 修改用户名及密码
    url(r'^api/logout/',logout),# 退出登录

]
