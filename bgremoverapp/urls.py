# from django.urls import path
# from . import views

# urlpatterns = [
#      path('', views.index, name='index'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.remove_background, name='remove_background'),
    path('change-background/', views.change_background, name='change_background'),
    path('result/', views.result, name='result'),  
]
