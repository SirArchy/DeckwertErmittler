from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert



def deck_löscher(): #✔️
    # THROW ERROR MESSAGE WHEN NO FILE SELECTED
    global id
    global pw
    global deckContent
    global mainboardPrice
    global sideboardPrice
    global totalPrice
    global deckName
    # Create the webdriver object
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument('window-size=1920x1080')
    # enter your download directory here
    prefs = {'download.default_directory': ''}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # get website link
    driver.get('https://deckstats.net')
    # Obtain buttons by class name and click all of them
    alert = Alert(driver)
    driver.find_element(By.NAME, 'user').send_keys("MagicNerdism")
    driver.find_element(By.NAME, 'passwrd').send_keys("Test1234")
    driver.find_element(By.ID, 'user_login_segment').click()
    driver.find_element(By.LINK_TEXT, "Your Decks").click()
    WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "(//a[@class='deck_list_name_link'])[1]")))
    driver.find_element(By.XPATH, "//*[@id='deck_list_table_decks']/div[2]/div[1]/div[1]/div[2]").click()
    driver.find_element(By.XPATH, "//li[@id='ui-id-19']//a[1]").click()
    alert.accept()
    driver.quit()

for i in range(100):
    deck_löscher()