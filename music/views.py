from django.views.generic import DetailView, ListView, View
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserForm


class IndexView(ListView):
    template_name = 'music/index.html'
    context_object_name = 'albums'

    def get_queryset(self):
        return Album.objects.all()


class SongIndexView(ListView):
    template_name = 'music/all_songs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        return Song.objects.all()


class SongsView(ListView):
    template_name = 'music/all_songs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        return Song.objects.all()


class DetailView(DetailView):
    template_name = 'music/detail.html'
    model = Album


class AlbumCreateView(CreateView):
    model = Album
    fields = ['album_title', 'artist', 'genre', 'album_logo']


def favorite(request, redirect_page, song_id):
    selected_song = get_object_or_404(Song, pk=song_id)
    try:
        if selected_song.is_favorite:
            selected_song.is_favorite = False
        else:
            selected_song.is_favorite = True
        selected_song.save()
    except (KeyError, Song.DoesNotExist):
        if redirect_page == 'detail_page':
            return redirect('music:index')
        elif redirect_page == 'songs_page':
            return redirect('music:view-songs')
    else:
        if redirect_page == 'detail_page':
            return redirect('music:detail', pk=selected_song.album.pk)
        elif redirect_page == 'songs_page':
            return redirect('music:view-songs')


class AlbumUpdateView(UpdateView):
    model = Album
    fields = ['album_title', 'artist', 'genre', 'album_logo']


class AlbumDeleteView(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


def delete_song(self, redirect_page, song_id):
    song = Song.objects.get(pk=song_id)
    song.delete()
    if redirect_page == 'detail_page':
        return redirect('music:detail', pk=song.album.pk)
    elif redirect_page == 'songs_page':
        return redirect('music:view-songs')


class SongCreateView(CreateView):
    model = Song
    fields = ['song_title', 'song_file']

    def form_valid(self, form):
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        form.instance.album = album
        return super(SongCreateView, self).form_valid(form)


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # render blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # submit form
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized data)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            form.save()

            # returns user object if user is authenticated
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
        return render(request, self.template_name, {'form': form})