from django.urls import path

from users import views

app_name = "users"
urlpatterns = [
    path("login", views.login.Login.as_view(), name="login"),
    path("logout", views.login.logout, name="logout"),
]
