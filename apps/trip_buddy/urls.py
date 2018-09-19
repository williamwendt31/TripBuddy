from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('travels', views.travels),
    path('view/<int:id>', views.show),
    path('addtrip', views.addtrip),
    path('processadd', views.processadd),
    path('join/<int:id>', views.join),
    path('delete/<int:id>', views.delete),
    path('cancel/<int:id>', views.cancel),
    path('logout', views.logout),
]