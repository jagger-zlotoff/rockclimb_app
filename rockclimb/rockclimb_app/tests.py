from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from django.test import TestCase, Client
from django.urls import reverse
from .models import rockVideo
from .forms import RockVideoForm
from django.contrib.auth.models import User

#These are all my selenium test cases
class UserAccountTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
            
    def test_login(self):
        time.sleep(3)
        #Choose your url to visit
        self.selenium.get(f'{self.live_server_url}/login/?next=/')
        #find the elements you need to submit form
        user = self.selenium.find_element(By.ID, 'id_username')
        password = self.selenium.find_element(By.ID, 'id_password')


        submit = self.selenium.find_element(By.ID, 'submit')

        #populate the form with data
        user.send_keys('test_user')
        password.send_keys('Pass2rock')

        #submit form
        submit.send_keys(Keys.RETURN)

        #check result; page source looks at entire html document
        assert 'test_user' in self.selenium.page_source
        
    
    def test_login_to_register_link(self):
        time.sleep(3)
        self.selenium.get(f'{self.live_server_url}/login/?next=/')
        #Finding the link on the login page that goes to the register page
        link = self.selenium.find_element(By.LINK_TEXT, 'Sign up')
        # Click the link
        link.click()
        # Wait for the new page to load
        WebDriverWait(self.selenium, 10).until(EC.url_changes(f'{self.live_server_url}/page-with-link/'))

        # Check the new URL
        new_url = self.selenium.current_url
        self.assertIn('register/', new_url)
        
        
    def test_register(self):
        time.sleep(3)
        self.selenium.get(f'{self.live_server_url}/register/')
        user = self.selenium.find_element(By.ID, 'id_username')
        password1 = self.selenium.find_element(By.ID, 'id_password1')
        password2 = self.selenium.find_element(By.ID, 'id_password2')
        submit = self.selenium.find_element(By.ID, 'submit')
        
        user.send_keys('test_user2')
        password1.send_keys('Pass2test')
        password2.send_keys('Pass2test')
        
        #submit form
        submit.send_keys(Keys.RETURN)

        #check result; page source looks at entire html document
        assert 'test_user2' in self.selenium.page_source
        
        
    def test_list_of_routes(self):
        time.sleep(3)
        self.selenium.get(f'{self.live_server_url}/routes/')
        link = self.selenium.find_element(By.LINK_TEXT, 'login')
        link.click()
        WebDriverWait(self.selenium, 10).until(EC.url_changes(f'{self.live_server_url}/page-with-link/'))
        new_url = self.selenium.current_url
        self.assertIn('login/', new_url)


#These are all my unit test cases.
#My test cases for my models
class RockVideoModelTests(TestCase):
    def test_is_active_rockvideo(self):
        # Happy path: Test that a rockVideo is active
        active_rockvideo = rockVideo.objects.create(title="A Climb", is_active=True)
        self.assertTrue(active_rockvideo.is_active) 
        
    def test_is_not_active_rockvideo(self):
        # Sad path: Test that a rockVideo is not active
        inactive_rockvideo = rockVideo.objects.create(title="A Climb", is_active=False)
        self.assertFalse(inactive_rockvideo.is_active)
        
#My test cases for my forms    
class RockVideoFormTest(TestCase):
    # Happy path: Test that the form is valid with data
    def test_valid_form(self):
        # Create dummy file data
        video = SimpleUploadedFile("video.mp4", b"file_content", content_type="video/mp4") 
        form_data = {
            'title': 'A Climb',
            'gym_name': 'Climb Gym',
            'contact_email': 'contact@climb.com',
            'gym_address': '123 Climb Street',
            'is_active': True,
            'file': video,
        }
        form = RockVideoForm(data=form_data, files={'file': video})  
        self.assertTrue(form.is_valid())
       
    def test_invalid_form(self):
        # Sad path: Test that the form is not valid with missing data
        #Title is requred but missing from the test
        form_data = {'is_active': True}  
        form = RockVideoForm(data=form_data)
        self.assertFalse(form.is_valid())
        print(form.errors)
          

