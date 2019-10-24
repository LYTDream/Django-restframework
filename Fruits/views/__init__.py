from alipay import AliPay
from django.http import JsonResponse

from FruitShop.settings import app_private_key_string, alipay_public_key_string
from .userviews import UserApiView
from .userviews import UsersApiView
from .cartgoodsviews import CartsApiView
from .cartgoodsviews import CartApiView
from .order_views import OrderApiView


def pay(request, url, order):
    alipay = AliPay(
        appid="2016101200668958",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False,  # 默认False
    )
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order.id,
        total_amount=order.o_price,
        subject=order.o_user_id,
        return_url=url,
        notify_url="https://localhost:8000",  # 可选, 不填则使用默认notify url
    )
    url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
    return JsonResponse({'url': url})
