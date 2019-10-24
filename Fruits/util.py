import uuid
from django.core.cache import cache
from django.core.mail import send_mail
from django.template import loader

from Fruits.models import Cart


def send_email(username, toemail):
    subject = '邮箱激活'
    print(username, toemail)
    from_email = toemail
    tem = loader.get_template('email.html')
    token = uuid.uuid4().hex
    cache.set(token, username, 60 * 60 * 5)
    url = 'http://127.0.0.1:8000/fruit/users/?action=activation&token=' + token
    html_message = tem.render({'username': username, 'url': url})

    send_mail(subject, '', '13465072090@163.com', [from_email, ], html_message=html_message)


def get_all_price(fu):
    carts = Cart.objects.filter(c_user_id=fu.id).filter(is_select=True)
    price = 0
    for cart in carts:
        price += cart.c_goods_num * cart.c_goods.g_price
    return price
