from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 登录功能
# 区分不同的账号

class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User,related_name='userprofile')
    profile_image = models.URLField('头像地址',max_length=100,blank=True,null=True)
    nick_name = models.CharField('昵称',max_length=100, blank=True, null=True,unique=True)
    is_admin = models.BooleanField('超级用户',default=False)

    CHOOOSE = (
        ('normal','normal'),
        ('author','author'),
    )
    identity = models.CharField('身份',choices=CHOOOSE,max_length=10,blank=True,null=True)

    def __str__(self):
        return self.nick_name
