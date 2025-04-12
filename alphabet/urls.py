from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('letters/', views.letters, name='letters'),
    path('learn/<int:order>/', views.learn_letter, name='learn_letter'),  
    path('learn_stroke/<int:order>/', views.stroke_view, name='learn_stroke'),      
    path('test/', views.test, name='test'),
    path('test/<int:order>/', views.test_letter, name='test_letter'),
    path('flask/', views.redirect_to_flask, name='flask_redirect'),
    path('get_image_paths/<int:order>/', views.get_image_paths, name='get_image_paths'),
    path('letter_matching', views.letter_matching, name='letter_matching'),
    path('dashboard/', views.dashboard, name='dashboard'),

]