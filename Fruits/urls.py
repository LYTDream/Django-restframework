from django.conf.urls import url

from Fruits import views

urlpatterns = [
    url(r'^users/$', views.UsersApiView.as_view(actions={
        'post': 'handle_post',
        'get': 'handle_get',
    })),
    url(r'^user/(?P<pk>\d+)/$', views.UserApiView.as_view()),
    url(r'^carts/$', views.CartsApiView.as_view(
        actions={
            'post': 'handle_post',
            # 'get': 'handle_get',
            'delete': 'handle_delete',
        })),
    url(r'^cart/(?P<pk>\d+)/$', views.CartApiView.as_view(actions={
        'get': 'retrieve',
        'post': 'handle_post',
        'delete': 'destroy',
    })),
    url(r'^order/$', views.OrderApiView.as_view(actions={
        'post': 'handle_post',
        'delete': 'handle_delete',
        'get': 'handle_get',
        'patch': 'handle_update',
    })),
    url(r'^pay/', views.pay),

]
