import debug_toolbar
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path, include

from app.views import register_view, main_view, play_song_view
from musicPortal import settings

urlpatterns = [
    path('', main_view, name='main'),
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('play/<int:song_id>/', play_song_view, name='play_song'),
    path('debug/', include(debug_toolbar.urls)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)