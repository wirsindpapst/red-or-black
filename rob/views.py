from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .modeldir.models import *
from django.core.exceptions import ObjectDoesNotExist
import random
from django.db.models import Count
from .forms import SelectionForm
# from django.db.models import F
# from django.db.models.expressions import CombinedExpression, Value

def home(request):
    expired_rounds = Game.objects.filter(ends_at__lte=datetime.now(), in_progress=True)
    for game in expired_rounds:
        choices = ["red", "black"]
        game.colour = random.choice(choices)
        game.previous_colours.append(game.colour)
        winners = Selection.objects.filter(game_id=game.id).filter(active=True).filter(colour=game.colour)
        losers = Selection.objects.filter(game_id=game.id).filter(active=True).exclude(colour=game.colour)
        for loser in losers:
            loser.active=False
            loser.lost_round = game.round_no
            loser.save()
        for winner in winners:
            winner.colour=""
            winner.active=True
            winner.save()
        if winners.count() > 1:
            game.round_no += 1
            start_time = datetime.now()
            game.started_at = start_time
            end_time = start_time + timedelta(minutes=1)
            game.ends_at = end_time
        else:
            game.in_progress=False
    first_games = Game.objects.first_round_games(request.user.id)
    second_games = Game.objects.filter(ends_at__gte=datetime.now(), selection__player_id=request.user.id, selection__active=True).exclude(selection__colour="").distinct()
    lost_games = Game.objects.filter(selection__player_id=request.user.id, selection__active=False, selection__viewable=True).distinct()
    won_games = Game.objects.filter(in_progess=False, selection__player_id=request.user.id, selection__active=True, selection__viewable=True).distinct()
    choose_games = Game.objects.filter(in_progress=True, selection__player_id=request.user.id, selection__active=True, selection__colour="").distinct()

    return render(request, 'home.html', { 'first_games': first_games, 'second_games': second_games, 'choose_games': choose_games, 'lost_games': lost_games, 'won_games': won_games })


def game_new(request):
    new_game = Game()
    player = get_object_or_404(Player, pk=request.user.id)
    new_game.create_game(player)
    return HttpResponseRedirect('/')

def view_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    end_time_string = game.return_end_time
    reds = Selection.objects.filter(active=True, game_id=pk, colour="red")
    blacks = Selection.objects.filter(active=True, game_id=pk, colour="black")
    if game.round_no > 1:
        losers_by_round = []
        counter = 1
        previous_colours = game.previous_colours
        previous_colours.pop(0)
        while counter <= game.round_no:
            this_round_losers = Selection.objects.filter(game_id=pk, active=False, lost_round=counter).count()
            losers_by_round.append(this_round_losers)
            counter+=1
    else:
        losers_by_round = []
        previous_colours = []
    try:
        selection = Selection.objects.get(player_id=request.user.id, game_id=pk, active=True)
    except Selection.DoesNotExist:
        selection = None
    game_data = zip(previous_colours, losers_by_round)
    return render(request, 'game/view.html', {'game': game, 'end_time_string': end_time_string, 'selection': selection, 'blacks': blacks, 'reds': reds, 'losers_by_round': losers_by_round, 'previous_colours': previous_colours, 'game_data': game_data})

def remove_game(request, pk):
    selection = get_object_or_404(Selection, game_id=pk, player_id=request.user.id)
    selection.viewable = False
    selection.save()
    return HttpResponseRedirect('/')

def set_stake(request, pk):
    if request.method == "POST":
        selection_form = SelectionForm(request.POST)
        if selection_form.is_valid():
            selection = selection_form.save(commit=False)
            # selection.choice = selection_form.cleaned_data['choice']
            selection.player_id = request.user.id
            selection.game_id=pk
            selection.active=True
            selection.save()
            return redirect(view_game, pk = pk)
    else:
        game = get_object_or_404(Game, pk=pk)
        selection_form = SelectionForm()
        end_time_string = game.return_end_time
        reds = Selection.objects.filter(active=True, game_id=pk, colour="red")
        blacks = Selection.objects.filter(active=True, game_id=pk, colour="black")
        selection = None
    return render(request, 'game/set_stake.html', {'game': game, 'end_time_string': end_time_string, 'selection': selection, 'blacks': blacks, 'reds': reds, 'selection_form': selection_form })



def join_game(request, pk, choice):
    game = get_object_or_404(Game, pk=pk)
    player = get_object_or_404(Player, pk=request.user.id)
    try:
        selection = Selection.objects.get(player_id=request.user.id, game_id=pk, active=True)
        selection.colour = choice
    except Selection.DoesNotExist:
        selection = Selection(game=game, player=player ,colour=choice)
    selection.save()
    end_time_string = game.return_end_time
    return redirect(view_game, pk = pk)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            player = Player()
            player.user = new_user
            player.save()
            return HttpResponseRedirect('/')

    else:
        form = RegistrationForm()

    token = {}
    token.update(csrf(request))
    token['form'] = form
    return render_to_response('registration/registration_form.html', token)

def registration_complete(request):
    return render_to_response('registration/registration_complete.html')
