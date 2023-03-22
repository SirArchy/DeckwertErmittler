from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
import time
import tkinter as tk
from tkinter import filedialog as fd

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_id = tk.Label(self, text="ID: ")
        ent_id = tk.Entry(self, textvariable = tk.StringVar(self, value='MagicNerdism'))
        lbl_pw = tk.Label(self, text="Password: ")
        ent_pw = tk.Entry(self, textvariable = tk.StringVar(self, value='Test1234'), show="•")
        btn_submit1 = tk.Button(self, text="Weiter")
        btn_submit1.bind('<Button-1>', self.pack_forget())
        lbl_id.pack(fill=tk.X, side=tk.LEFT)
        ent_id.pack(fill=tk.X, side=tk.LEFT)
        lbl_pw.pack(fill=tk.X, side=tk.LEFT)
        ent_pw.pack(fill=tk.X, side=tk.LEFT)
        btn_submit1.pack(fill=tk.X, side=tk.LEFT)
        LoginPage.id = ent_id.get()
        LoginPage.pw = ent_pw.get()

class UploadPage(LoginPage):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_insert_file = tk.Label(self, text="Deckliste",width=20, height=10)
        txt_decklist = tk.Text(self, height=12)
        btn_open_file = tk.Button(self, text='Deckliste auswählen', command=self.open_text_file)
        btn_calculate_price = tk.Button(self, text='Preis ausrechnen', command=self.deckwert_ermittlung('C:/Users/Fabian/Desktop/SampleDeckliste.txt', LoginPage.id, LoginPage.pw))
        btn_submit2 = tk.Button(self, text="Weiter",width=20, height=10)
        btn_submit2.bind('<Button-1>', self.pack_forget()), 
        lbl_insert_file.pack(fill=tk.BOTH, side=tk.TOP)
        txt_decklist.pack(fill=tk.BOTH, side=tk.TOP)
        btn_open_file.pack(fill=tk.BOTH, side=tk.LEFT)
        btn_calculate_price.pack(fill=tk.BOTH, side=tk.LEFT)
        btn_submit2.pack(fill=tk.BOTH, side=tk.BOTTOM)
        #mainboardPrice, sideboardPrice = deckwert_ermittlung('C:/Users/Fabian/Desktop/SampleDeckliste.txt', id, pw))
    def open_text_file():
        # file type
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
            )
        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)
        # read the text file and show its content on the Text
        UploadPage.txt_decklist.insert('1.0', f.readlines())
    def deckwert_ermittlung(textfile_location, id, pw):
        # Create the webdriver object
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': ''}  # enter your download directory here
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # get website link
        driver.get('https://deckstats.net')

        # get deckname and decklist
        decklist, deckname = UploadPage.textdateiEinlesen(textfile_location)

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

class DeckValuePage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_mainboard_price = tk.Label(self, text="Mainboard Preis: " + UploadPage.mainboardPrice, width=20, height=10)
        lbl_sideboard_price = tk.Label(self, text="Sideboard Preis: " + UploadPage.sideboardPrice, width=20, height=10)
        lbl_total_price = tk.Label(self, text="Gesamtpreis: " + UploadPage.mainboardPrice + UploadPage.sideboardPrice, width=20, height=10)
        btn_submit3 = tk.Button(self, text="Nächstes Deck",width=20, height=10)
        btn_submit3.bind('<Button-1>', self.pack_forget())
        lbl_mainboard_price.pack(fill=tk.BOTH, side=tk.LEFT)
        lbl_sideboard_price.pack(fill=tk.BOTH, side=tk.LEFT)
        lbl_total_price.pack(fill=tk.BOTH, side=tk.LEFT)
        btn_submit3.pack(fill=tk.BOTH, side=tk.BOTTOM)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = LoginPage(self)
        p2 = UploadPage(self)
        p3 = DeckValuePage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Page 1", command=p1.show)
        b2 = tk.Button(buttonframe, text="Page 2", command=p2.show)
        b3 = tk.Button(buttonframe, text="Page 3", command=p3.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()