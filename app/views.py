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
    show_player_id = request.GET.get('show_player')


    if show_player_id and not request.session.get('already_played') == show_player_id:
        try:
            song = Song.objects.get(id=show_player_id)
            song.play_count += 1
            song.save()
            request.session['already_played'] = show_player_id
        except Song.DoesNotExist:
            pass

    songs = Song.objects.all()
    if genre_id:
        songs = songs.filter(genre_id=genre_id)
    if query:
        songs = songs.filter(
            Q(title__icontains=query) |
            Q(artist__name__icontains=query)
        )

    top_song = Song.objects.order_by('-play_count').first()

    return render(request, 'main.html', {
        'songs': songs,
        'genres': genres,
        'selected_genre': genre_id,
        'top_song': top_song,
        'show_player_id': show_player_id,
    })