from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# Create your tests here.
class PlayerFormTest(LiveServerTestCase):

  def testform(self):
    selenium = webdriver.Chrome()
    #Choose your url to visit
    selenium.get('http://localhost:8000/login/?next=/')
    #find the elements you need to submit form
    user = selenium.find_element(By.ID, 'id_username')
    password = selenium.find_element(By.ID, 'id_password')


    submit = selenium.find_element(By.ID, 'submit')

    #populate the form with data
    user.send_keys('test_user')
    password.send_keys('Pass2rock')

    #submit form
    submit.send_keys(Keys.RETURN)

    #check result; page source looks at entire html document
    assert 'test_user' in selenium.page_source