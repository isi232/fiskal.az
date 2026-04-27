from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('qeydiyyat/', views.register_view, name='register'),
    path('giris/', views.login_view, name='login'),
    path('cixis/', views.logout_view, name='logout'),

    # Main pages
    path('', views.home, name='home'),
    path('sikayet/', views.complaint_view, name='complaint'),
    path('analitika/', views.analytics, name='analytics'),
    path('xerite/', views.map_view, name='map'),
    path('profil/', views.profile, name='profile'),
    path('kart-elave-et/', views.add_card, name='add_card'),
]
