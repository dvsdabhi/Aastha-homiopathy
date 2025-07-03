from django.urls import path
from .import views

urlpatterns = [
    path('', views.index,name='index'),
    path('register/', views.patient_register, name='patient_register'),
    path('login/', views.patient_login, name='patient_login'),
    path('logout/', views.patient_logout, name='patient_logout'),
    path('about/', views.about,name='about'),
    path('appointment/', views.appointment,name='appointment'),
    path('view_appointments/', views.my_appointments,name='my_appointments'),
    path('contact/', views.contact,name='contact'),
    path('feature/', views.feature,name='feature'),
    path('treatment/', views.treatment,name='treatment'),
    path('treatment/<slug:slug>/', views.treatment_detail_view, name='treatment_detail'),
    path('team/', views.team,name='team'),
    path('testimonial/', views.testimonial,name='testimonial'),
    path('404/', views.not_found,name='404'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]