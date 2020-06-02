from django.urls import path
from . import views

app_name = 'music'
urlpatterns = [
    # music/
    path('', views.IndexView.as_view(), name="index"),

    # music/songs/
    path('songs/', views.SongsView.as_view(), name="view-songs"),

    # music/register/
    path('register/', views.UserFormView.as_view(), name="register"),

    # music/album_id/
    path('<pk>/', views.DetailView.as_view(), name="detail"),

    # music/album/add/
    path('album/add/', views.AlbumCreateView.as_view(), name="add-album"),

    # music/album/song/favorite/
    path('album/song/favorite/<redirect_page>/<song_id>/', views.favorite, name="favorite"),

    # music/album/update/album_id
    path('album/update/<pk>/', views.AlbumUpdateView.as_view(), name="update-album"),

    # music/album/delete/album_id
    path('album/delete/<pk>/', views.AlbumDeleteView.as_view(), name="delete-album"),

    # music/album/addsong/album_id
    path('album/addsong/<pk>/', views.SongCreateView.as_view(), name="add-song"),

    # music/album/song/delete/song_id
    path('album/song/delete/<redirect_page>/<song_id>/', views.delete_song, name="delete-song"),


]
