from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import rockVideo, Vote
from django.db.models import Count
from .forms import RockVideoForm, VoteForm
# Create your views here.
def index(request): 
    # Get all active rock climbing videos
    active_rockVideos = rockVideo.objects.filter(is_active=True)
    for video in active_rockVideos:
        votes = Vote.objects.filter(rockVideo=video).values('grade').annotate(vote_count=Count('grade')).order_by('-vote_count')
        video.most_voted_grade = votes[0]['grade'] if votes else 'No votes yet'

    # Render index.html with the active rock climbing videos in the context
    return render(request, 'rockclimb_app/index.html', {'rockVideos': active_rockVideos})

def rockVideo_detail(request, pk):
    # Retrieve the specific rockVideo instance
    rock_video_instance = get_object_or_404(rockVideo, pk=pk)

    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.rockVideo = rock_video_instance
            vote.save()
            return redirect('index')
    else:
        form = VoteForm()
    
    context = {
        'rockVideo': rock_video_instance,
        'form': form,
    }
    return render(request, 'rockclimb_app/rockVideo_detail.html', context)

def active_rockvideos(request):
    rockvideos = rockVideo.objects.filter(active=True)  # Get all active rock climbing videos
    return render(request, 'rockclimb_app/index.html', {'rockvideos': rockvideos})  

def update_rockVideo(request, pk):
    rockvideo = get_object_or_404(rockVideo, pk=pk)
    if request.method == 'POST':
        form = RockVideoForm(request.POST, request.FILES, instance=rockvideo)
        if form.is_valid():
            form.save()
            return redirect('rockVideo-detail', pk=rockvideo.pk)  # Redirect to the detail view or any other view
    else:
        form = RockVideoForm(instance=rockvideo)
    return render(request, 'rockclimb_app/update_rockVideo.html', {'form': form})

def delete_rockVideo_confirm(request, pk):
    rockvideo = get_object_or_404(rockVideo, pk=pk)
    if request.method == 'POST':
        rockvideo.delete()
        return redirect('index')  # Redirect to the list view after deletion
    return render(request, 'rockclimb_app/delete_route_confirm.html', {'rockVideo': rockvideo})

def add_rockVideo(request):
    if request.method == 'POST':
        form = RockVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RockVideoForm()
    return render(request, 'rockclimb_app/add_rockVideo.html', {'form': form})
 
def upload_video(request):
    if request.method == 'POST':
        form = RockVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('some-view-name')
    else:
        form = RockVideoForm()
    return render(request, 'upload.html', {'form': form})

def home(request):
    return render(request, 'rockclimb_app/home.html')
