from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from photogur.models import Picture, Comment
from django.views.decorators.http import require_http_methods


def pictures(request):
    context = {'pictures': Picture.objects.all()}
    response = render(request, 'index.html', context)
    return HttpResponse(response)


def root(request):
    return HttpResponseRedirect('admin')


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
    user_name = request.POST['name']
    user_message = request.POST['message']
    user_select_picture = request.POST['picture']
    select_picture = Picture.objects.get(id=user_select_picture)
    comment = Comment(name=user_name, picture=select_picture, message=user_message)
    comment.save()
    return redirect("picture_show", id=user_select_picture)
# @require_http_methods(["POST"])
# def create_comment(request):
    # query = request.POST['query']
    # leave_comment = Comment.objects.filter(message=query)
    # context = {'comment': leave_comment, 'query': query}
    # response = render(request, 'search.html', context)
    # return HttpResponse(response)
