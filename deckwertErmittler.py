from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
import time
import tkinter as tk
from tkinter import filedialog as fd


def deckwert_ermittlung(textfile_location, id, pw):
    # Create the webdriver object
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': ''}  # enter your download directory here
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # get website link
    driver.get('https://deckstats.net')

    # get deckname and decklist
    decklist, deckname = textdateiEinlesen(textfile_location)

    # Obtain buttons by class name and click all of them
    driver.find_element(By.NAME, 'user').send_keys(id)
    driver.find_element(By.NAME, 'passwrd').send_keys(pw)
    driver.find_element(By.ID, 'user_login_segment').click()
    time.sleep(1) #schauen ob man auf richtige Webseite warten kann
    driver.find_element(By.LINK_TEXT,'Okay!').click()
    driver.find_element(By.XPATH, "(//i[@class='fa fa-plus'])[1]").click()
    driver.find_element(By.ID, 'deckbuilder_new_deck_dialog_name').send_keys(deckname)
    format_selecter = Select(driver.find_element(By.ID, 'deckbuilder_new_deck_dialog_format'))
    format_selecter.select_by_value('3')
    driver.find_element(By.ID, 'deckbuilder_new_deck_dialog_is_public').click()
    driver.find_element(By.XPATH, "(//span[text()='OK'])[1]").click()
    time.sleep(1) #schauen ob man auf richtige Webseite warten kann
    driver.find_element(By.XPATH, "//span[text()[normalize-space()='Paste/upload list']]").click()
    time.sleep(1) #schauen ob man auf richtige Webseite warten kann
    driver.find_element(By.ID, 'deckbuilder_upload_list_dialog_textarea').send_keys(decklist)
    time.sleep(1)
    driver.find_element(By.XPATH, "(//span[text()='OK'])[5]").click()
    driver.find_element(By.XPATH, "//span[text()[normalize-space()='Speichern']]").click()
    driver.find_element(By.XPATH, "(//span[text()='OK'])[2]").click()
    driver.find_element(By.ID, 'ui-id-14').click()
    mainboardPrice = driver.find_element(By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[1]").getText()
    sideboardPrice = driver.find_element(By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[2]").getText()
    driver.quit()
    return mainboardPrice, sideboardPrice


def textdateiEinlesen(textfile_location):
    # open textfile and save as string
    with open(textfile_location, 'r') as file:
        textfile_content = file.read().replace('\t',' ')

    # read deck name
    textfile_name = re.search("[ \w-]+?(?=\.)", textfile_location).group()

    return textfile_content, textfile_name


def open_text_file():
    # file type
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    # show the open file dialog
    f = fd.askopenfile(filetypes=filetypes)
    # read the text file and show its content on the Text
    txt_decklist.insert('1.0', f.readlines())


# create basic GUI
window = tk.Tk()
frm_login_data = tk.Frame()
frm_file_upload = tk.Frame()
frm_deckvalue = tk.Frame()
lbl_title = tk.Label(text="Deckwert Ermittler", width=20)

# create login screen
lbl_id = tk.Label(frm_login_data, text="ID: ")
ent_id = tk.Entry(frm_login_data, textvariable = tk.StringVar(window, value='MagicNerdism'))
lbl_pw = tk.Label(frm_login_data, text="Password: ")
ent_pw = tk.Entry(frm_login_data, textvariable = tk.StringVar(window, value='Test1234'), show="*")
btn_submit1 = tk.Button(frm_login_data, text="Weiter")
btn_submit1.bind('<Button-1>', frm_login_data.pack_forget())
lbl_title.pack(fill=tk.BOTH, side=tk.TOP)
lbl_id.pack(fill=tk.BOTH, side=tk.LEFT)
ent_id.pack(fill=tk.BOTH, side=tk.LEFT)
lbl_pw.pack(fill=tk.BOTH, side=tk.LEFT)
ent_pw.pack(fill=tk.BOTH, side=tk.LEFT)
btn_submit1.pack()
frm_login_data.pack()
id = ent_id.get()
pw = ent_pw.get()

# create file upload screen
lbl_insert_file = tk.Label(frm_file_upload, text="Deckliste",width=20, height=10)
txt_decklist = tk.Text(frm_file_upload, height=12)
btn_open_file = tk.Button(frm_file_upload, text='Deckliste auswählen', command=open_text_file)
btn_calculate_price = tk.Button(frm_file_upload, text='Preis ausrechnen', command=deckwert_ermittlung('C:/Users/Fabian/Desktop/SampleDeckliste.txt', id, pw))
btn_submit2 = tk.Button(frm_file_upload, text="Weiter",width=20, height=10)
btn_submit2.bind('<Button-1>', frm_file_upload.pack_forget()), 
lbl_insert_file.pack(fill=tk.BOTH, side=tk.TOP)
btn_open_file.pack(fill=tk.BOTH, side=tk.LEFT)
btn_submit2.pack(fill=tk.BOTH, side=tk.BOTTOM)
#mainboardPrice, sideboardPrice = deckwert_ermittlung('C:/Users/Fabian/Desktop/SampleDeckliste.txt', id, pw))

# create deck value screen
lbl_mainboard_price = tk.Label(frm_deckvalue, text="Mainboard Preis: " + mainboardPrice, width=20, height=10)
lbl_sideboard_price = tk.Label(frm_deckvalue, text="Sideboard Preis: " + sideboardPrice, width=20, height=10)
lbl_total_price = tk.Label(frm_deckvalue, text="Gesamtpreis: " + mainboardPrice + sideboardPrice, width=20, height=10)
btn_submit3 = tk.Button(frm_deckvalue, text="Nächstes Deck",width=20, height=10)
btn_submit3.bind('<Button-1>', frm_deckvalue.pack_forget())
lbl_mainboard_price.pack(fill=tk.BOTH, side=tk.LEFT)
lbl_sideboard_price.pack(fill=tk.BOTH, side=tk.LEFT)
lbl_total_price.pack(fill=tk.BOTH, side=tk.LEFT)
btn_submit3.pack(fill=tk.BOTH, side=tk.BOTTOM)
window.mainloop()