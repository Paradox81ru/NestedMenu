from django.urls import path, include
from .views import MenuView

app_name = "menu"
urlpatterns = [
    path('', MenuView.as_view(), name='main'),
    path('<str:p>', MenuView.as_view()),
    path('<str:p>/<str:p1>', MenuView.as_view()),
    path('<str:p>/<str:p1>/<str:p2>', MenuView.as_view()),
    path('<str:p>/<str:p1>/<str:p2>/<str:p3>', MenuView.as_view()),
    path('<str:p>/<str:p1>/<str:p2>/<str:p3>/<str:p4>', MenuView.as_view())
]