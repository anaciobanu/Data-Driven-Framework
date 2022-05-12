from urllib import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import pytest
#import urllib.request
from time import sleep
from get_db_data import login_form_parameters
#from get_excel_data import login_form_parameters
import logging

####### Common functions #####

logging.basicConfig(filename='C:\Data Driven Framework\logs\info.log', 
                    encoding='utf-8', 
                    level=logging.INFO, 
                    force=True,
                    format='%(asctime)s %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')

def launch_swaglabs():
    logging.info('Launching the swaglabs page')
    global driver
    driver = webdriver.Firefox()
    driver.maximize_window()
    logging.info('Maximizing the window')
    driver.get('https://www.saucedemo.com/')


def valid_login_swaglabs():
    logging.info('Loggin in')
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By. NAME, 'password').send_keys('secret_sauce')
    driver.find_element(By.CLASS_NAME, 'submit-button ').click() 

def capture_evidence():
    image_name = fr"C:\Data Driven Framework\tests\evidence\image-{datetime.today().strftime('%m%d%y-%H%M%S')}.png"
    driver.save_screenshot(image_name)

def text_is_displayed(text):
    logging.info(f'Checking if [{text}] exists on the page')
    return text.lower() in driver.page_source.lower()
##### Test cases #####  

def test_launch_login_page():
    launch_swaglabs()
    assert driver.title == 'Swag Labs'
    capture_evidence()
    driver.quit()
  
#login_form_parameters = [
   ## ('standard_user',	'secret_sauce', 'Products')			
  #  ('locked_out_user', 'secret_sauce', 'Sorry, this user has been locked out')	
   # ('problem_user',	'secret_sauce', 'Products')			
 #   ('test', 'test', 'Username and password do not match any user in this service')		
  #  ('standard_user', ' ', 'Password is required')			
 #   (' ', 'secret_sauce' 'Username is required')			
  #  (' ', ' ', 'Username is required')
 #   ]

@pytest.mark.parametrize("username, password, checkpoint", 'login_form_parameter')
def test_login_invalid_credentials(username, password, checkpoint):
    launch_swaglabs()
    if username != None: driver.find_element(By.ID, 'user-name').send_keys(username)
    if password != None: driver.find_element(By. NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'submit-button ').click() 
    sleep(5)
    assert checkpoint.lower() in driver.page_source.lower()   
    capture_evidence()
    driver.quit()  

##### Below Test cases has setup and teardown #####  

@pytest.fixture()
def setup(request):
    #the following code runs before each test
    launch_swaglabs()
    valid_login_swaglabs()

#the following code runs after each test
def teardown():
        capture_evidence()
        driver.quit()
request.addfinalizer(teardown)    


@pytest.mark.reg
def test_login_valid_credentials(setup):
    assert 'products' in driver.page_source.lower()   

def test_view_product_details(setup):
    logging.info('View product details on the page')
    product_names = driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
    product_names[0].click()
    assert 'back to products' in driver.page_source.lower()

def test_item_price(setup):
    price_element=driver.find_element(By.CSS_SELECTOR,'.inventory_item_price')
    print(price_element.text)
    assert 'products' in driver.page_source.lower()     

def test_add_item_to_cart(setup):
    driver.find_element(By. CSS_SELECTOR, '#add-to-cart-sauce-labs-backpack').click()
    assert 'products' in driver.page_source.lower() 

def test_remove_item_from_cart(setup):
    driver.find_element(By. CSS_SELECTOR, '#add-to-cart-sauce-labs-backpack').click()
    driver.find_element(By.CSS_SELECTOR, '.shopping_cart_badge').click()
    driver.find_element(By. CSS_SELECTOR, '#remove-sauce-labs-backpack').click()
    assert 'your cart' in driver.page_source.lower() 








