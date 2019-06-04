from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from photogur.models import Picture, Comment
from django.views.decorators.http import require_http_methods
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def pictures(request):
    context = {'pictures': Picture.objects.all()}
    response = render(request, 'index.html', context)
    return HttpResponse(response)


def root(request):
    return HttpResponseRedirect('pictures')


def picture_show(request, picture_id):
    picture = get_object_or_404(Picture, pk=picture_id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)


def picture_search(request):
    query = request.GET['query']
    search_results = Picture.objects.filter(artist=query)
    context = {'pictures': search_results, 'query': query}
    response = render(request, 'search.html', context)
    return HttpResponse(response)

@require_http_methods(['POST'])
def create_comment(request):
    pass


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/pictures')
    else:
        form = UserCreationForm
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)


def add(request):
    if request.method == 'POST':
        picture_form = PictureForm(request.POST)
        if picture_form.is_valid():
            new_pic = picture_form.save(commit=False)
            new_pic.user = request.user
            picture_form.save()
            return redirect('/pictures', id=new_pic.id)
    else:
        picture_form = PictureForm()
        return render(request, 'add.html', {'picture_form': picture_form})

