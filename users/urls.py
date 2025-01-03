from django.urls import path
from .views import (
    signup, login_view, user_dash_view, about_us
)
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', user_dash_view, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='/menu/restaurants/'), name='logout'),
    path('about_us/', about_us, name='about_us'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
