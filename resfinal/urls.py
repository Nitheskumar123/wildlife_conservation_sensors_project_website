from django.urls import path
from . import views 



urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.signup, name="register"),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),
    path("login", views.signin, name="signin"),
    path("logout", views.logout_page, name="logout"),
    path("profile/update", views.update_profile, name="update-profile"),
    path("profile", views.profile, name="profile"),
    path("about", views.about, name="about"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('pressure', views.pressure, name='pressure'),
    path('api/sensor-data/', views.get_sensor_data, name='get_sensor_data'),
    path('animal',views.animal,name='animal')
    
   
   
]


