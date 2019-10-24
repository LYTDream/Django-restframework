# FruitGP2

## 用户
- 字段
    - 用户名
    - 密码
    - 逻辑删除
    - 手机号
    - 邮箱
    - 是否激活
    - 注册日期
    - 是否禁用
    - 性别
    - 年龄

```
class FruitUser(models.Model):
    f_username = models.CharField(max_length=32)
    f_password = models.CharField(max_length=128, null=True)
    f_age = models.IntegerField(default=0)
    f_sex = models.BooleanField(default=False)
    f_phone = models.CharField(max_length=32)
    f_email = models.CharField(max_length=32)
    f_ctime = models.DateTimeField(auto_now_add=True, null=True)
    f_activated = models.BooleanField(default=False)
    f_disabled = models.BooleanField(default=False)
    f_delete = models.BooleanField(default=False)
```
# 商家服务端---- 水果设计
- 1
    - 一级分类
    - 水果
    - 蔬菜
    - 肉类
    - 饮品
- 2
    - 二级分类
    - 热带水果
    - 北方水果
    - 。。。
- 3
    -数据库设计
## 数据库关系
1. 第一分类为总类
2. 第二分类以第一类为外键（一对多）
3. 商品以第二分类为主键（一对多）



