from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subscription', views.subscription_page, name='subscription'),
    path('no_subscription',views.no_subscription,name='no_subscription'),
    # path('subscription',views.SubscriptionCreateView.as_view(),name='subscription'),
]