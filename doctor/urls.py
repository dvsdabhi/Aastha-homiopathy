from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('appointments/', views.appointments, name='admin_appointments'),
    path('appointments/<int:id>/', views.confirm_appointment, name='confirm_appointment'),
    path('treatments/', views.treatments, name='admin_treatments'),
    path('treatments/add/', views.add_treatment, name='admin_add_treatment'),
    path('treatments/update/<int:id>/', views.update_treatment, name='update_treatment'),
    path('treatments/delete/<int:id>/', views.delete_treatment, name='admin_delete_treatment'),
    path('blogs/', views.blogs, name='admin_blogs'),
    path('blogs/add/', views.add_blog, name='admin_add_blog'),
    path('blogs/update/<int:id>/', views.update_blog, name='admin_edit_blog'),
    path('blogs/delete/<int:id>/', views.delete_blog, name='admin_delete_blog'),
    path('login/', views.login, name='admin_login'),
    path('register/', views.register, name='admin_register'),
    path('contact/', views.contact, name='admin_contact'),
    path('logout/', views.logout_view, name='admin_logout'),
]
