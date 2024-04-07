from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import rockVideo
from .forms import RockVideoForm
# Create your views here.
def index(request): 
    # Get all active rock climbing videos
    active_rockVideos = rockVideo.objects.filter(is_active=True)
    # Render index.html with the active rock climbing videos in the context
    return render(request, 'rockclimb_app/index.html', {'rockVideos': active_rockVideos})
def rockVideo_detail(request, pk):
    rockvideo = get_object_or_404(rockVideo, pk=pk)
    return render(request, 'rockclimb_app/rockVideo_detail.html', {'rockVideo': rockvideo})
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


 
def upload_video(request):
    if request.method == 'POST':
        form = RockVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('some-view-name')
    else:
        form = RockVideoForm()
    return render(request, 'upload.html', {'form': form})
