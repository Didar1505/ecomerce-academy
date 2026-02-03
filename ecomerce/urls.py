from django.urls import path
from . import  views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.profile, name="profile"),
    path("profile/update", views.update_profile, name="update_profile"),
    path("orders", views.my_orders, name="my_orders"),
    path("add_order_item/<int:id>", views.add_order_item, name="add_order_item"),
    path("confirm_order/<int:order_id>", views.confirm_order, name="confirm_order"),
]