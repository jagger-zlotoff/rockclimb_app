from django.shortcuts import render
from django.http import HttpResponse
from .forms import RockVideoForm
# Create your views here.
def index(request):


# Render index.html
    return render( request, 'rockclimb_app/index.html')

def upload_video(request):
    if request.method == 'POST':
        form = RockVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('some-view-name')
    else:
        form = RockVideoForm()
    return render(request, 'upload.html', {'form': form})
