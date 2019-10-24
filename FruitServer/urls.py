from django.conf.urls import url, include
from django.contrib import admin

from FruitServer import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    url(r'^goodstype/', views.GoodsTypeAPIView.as_view(
        actions={
            "get": "get_goodstypes",
        }
    )),
    url(r'^goods/', views.GoodsAPIView.as_view(
        actions={
            "get": "list",
        }
    )),

]
