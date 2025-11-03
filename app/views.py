from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from app.forms import RegisterForm
from app.models import Genre, Song


# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хэшируем пароль
            user.save()
            login(request, user)  # сразу авторизуем пользователя
            return redirect('main')  # редирект на главную
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def main_view(request):
    genres = Genre.objects.all()
    genre_id = request.GET.get('genre')
    query = request.GET.get('q')
    play_song_id = request.GET.get('play')

    if play_song_id:
        try:
            song = Song.objects.get(id=play_song_id)
            song.play_count += 1
            song.save()
        except Song.DoesNotExist:
            params = request.GET.copy()
            params.pop('play', None)
            return redirect(f"{request.path}?{params.urlencode()}")

    songs = Song.objects.all()
    if genre_id:
        songs = songs.filter(genre_id=genre_id)
    if query:
        songs = songs.filter(
            Q(title__icontains=query) |
            Q(artist__name__icontains=query)
        )

    return render(request, 'main.html', {
        'songs': songs,
        'genres': genres,
        'selected_genre': genre_id,
    })


def play_song_view(request, song_id):
    """Представление для проигрывания песни и увеличения счетчика"""
    try:
        song = Song.objects.get(id=song_id)
        song.play_count += 1
        song.save()
        return redirect('main')
    except Song.DoesNotExist:
        return redirect('main')