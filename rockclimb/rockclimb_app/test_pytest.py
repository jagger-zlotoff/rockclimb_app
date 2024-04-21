import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from .models import rockVideo, Vote
from .forms import RockVideoForm, VoteForm
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def user(db):
    return User.objects.create_user(username='user', password='password')

@pytest.fixture
def rock_video(db, user):
    return rockVideo.objects.create(title='Climbing Video', user=user, is_active=True)

@pytest.fixture
def vote(db, rock_video):
    return Vote.objects.create(rockVideo=rock_video, grade='5.10')


#Testing my index
#Ensure the view renders correctly with active rock videos
#The videos and their most voted grades are correctly passed to the template
def test_index_view(client, rock_video, vote):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Climbing Video' in response.content.decode()

#Testing my details
#Test GET request: Check if the page loads correctly with the form
def test_rock_video_detail_view_get(client, rock_video):
    url = reverse('rockVideo-detail', kwargs={'pk': rock_video.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], VoteForm)
    
#Test POST request (valid data): Submit a valid form and check redirection
@pytest.mark.django_db
def test_rock_video_detail_view_post_valid(client, rock_video):
    url = reverse('rockVideo-detail', kwargs={'pk': rock_video.pk})
    response = client.post(url, {'grade': '5.10'})
    assert response.status_code == 302  # Redirection to index
    
#Test POST request (invalid data): Submit an invalid form and ensure it doesn't redirect
def test_rock_video_detail_view_post_invalid(client, rock_video):
    url = reverse('rockVideo-detail', kwargs={'pk': rock_video.pk})
    response = client.post(url, {'grade': ''})  # Invalid data
    assert response.status_code == 200

#The following views will all follow a similar format
#active_rockvideos, update_rockVideo, delete_rockVideo_confirm, add_rockVideo, upload_video, home, register
#Will test both GET and POST request
#Test form validation
#Test permissions and redirections
#Test session adn authentication

def test_add_rock_video_get(client):
    url = reverse('rockVideo-add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], RockVideoForm)

@pytest.mark.django_db
def test_add_rock_video_post_valid(client, user):
    client.force_login(user)
    url = reverse('rockVideo-add')
    response = client.post(url, {'name': 'New Climbing Video', 'is_active': True}, follow=True)
    assert response.status_code == 200
    assert rockVideo.objects.filter(is_active=True).count() == 1

@pytest.mark.django_db
def test_active_rockvideos_view(client):
    url = reverse('active_rockvideos')
    response = client.get(url, {'is_active': True}, follow=True)
    assert response.status_code == 200
    assert "Climbing Video" in response.content.decode()

@pytest.mark.django_db
def test_update_rockVideo_get(client, user, rock_video):
    client.force_login(user)
    url = reverse('rockVideo-update', kwargs={'pk': rock_video.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert "Update Rock Video" in response.content.decode()  
    
@pytest.mark.django_db
def test_update_rockVideo_post(client, user, rock_video):
    client.force_login(user)
    url = reverse('rockVideo-update', kwargs={'pk': rock_video.pk})
    response = client.post(url, {'name': 'Updated Name', 'is_active': True})
    assert response.status_code == 302  
    
@pytest.mark.django_db
def test_delete_rockVideo_confirm(client, user, rock_video):
    client.force_login(user)
    url = reverse('rockVideo-delete-confirm', kwargs={'pk': rock_video.pk})
    response = client.post(url)  
    assert response.status_code == 302
    assert rockVideo.objects.filter(pk=rock_video.pk).exists() is False

@pytest.mark.django_db
def test_home(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assert "Welcome" in response.content.decode()  

@pytest.mark.django_db
def test_register(client):
    url = reverse('register')
    response = client.post(url, {'username': 'newuser', 'password1': 'newpassword123', 'password2': 'newpassword123'})
    assert response.status_code == 302  
    assert User.objects.filter(username='newuser').exists()
    