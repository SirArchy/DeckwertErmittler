from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

"""
This program is used to display the deck value of the selected .txt file containing a magic the gathering deck.
It logs into the given deckstats.net account, adds the deck and then displays the deck's values. 
"""


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_id = ttk.Label(self, text="ID: ")
        self.defaultID = tk.StringVar(value='MagicNerdism')
        self.defaultPW = tk.StringVar(value='Test1234')
        ent_id = ttk.Entry(self, textvariable = self.defaultID)
        lbl_pw = ttk.Label(self, text="Password: ")
        ent_pw = ttk.Entry(self, textvariable = self.defaultPW, show="•")
        btn_submit1 = ttk.Button(self, text="Weiter", command=lambda: self.master.switch_frame(UploadPage))
        lbl_id.pack(fill=tk.X, side=tk.LEFT)
        ent_id.pack(fill=tk.X, side=tk.LEFT)
        lbl_pw.pack(fill=tk.X, side=tk.LEFT)
        ent_pw.pack(fill=tk.X, side=tk.LEFT)
        btn_submit1.pack(fill=tk.X, side=tk.LEFT)
        self.id = tk.StringVar(value=ent_id.get())
        self.pw = tk.StringVar(value=ent_pw.get())

class UploadPage(Page):
    parent = LoginPage
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_insert_file = ttk.Label(self, text="Deckliste",width=20)
        txt_decklist = tk.Text(self, height=12)
        btn_open_file = ttk.Button(self, text='Deckliste auswählen', command=lambda: self.open_text_file()) #this function should open the file, save it's location and it's contents + display it in textfield
        btn_calculate_price = ttk.Button(self, text='Preis ausrechnen', command=lambda: [self.deckwert_ermittlung('INSERT FILE LOCATION',  self.parent.id, self.parent.pw), self.master.switch_frame(UploadPage)])
        lbl_insert_file.pack(fill=tk.BOTH, side=tk.TOP)
        txt_decklist.pack(fill=tk.BOTH, side=tk.TOP)
        btn_open_file.pack(fill=tk.BOTH, side=tk.LEFT)
        btn_calculate_price.pack(fill=tk.BOTH, side=tk.LEFT)
    def open_text_file(self):
        # file type
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
            )
        # show the open file dialog
        f = fd.askopenfile(filetypes=filetypes)
        # read the text file and show its content on the Text
        self.txt_decklist.insert('1.0', f.readlines())
    def textdateiEinlesen(textfile_location):
        # open textfile and save as string
        with open(textfile_location, 'r') as file:
            textfile_content = file.read().replace('\t',' ')
        # read deck name
        textfile_name = re.search("[ \w-]+?(?=\.)", textfile_location).group()
        textfile_data = [textfile_content, textfile_name]
        return textfile_data
    def deckwert_ermittlung(self, textfile_location, id, pw):
        # Create the webdriver object
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        prefs = {'download.default_directory': ''}  # enter your download directory here
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # get website link
        driver.get('https://deckstats.net')

        # get deckname and decklist
        deckdata = self.textdateiEinlesen(textfile_location)

        # Obtain buttons by class name and click all of them
        driver.find_element(By.NAME, 'user').send_keys(id)
        driver.find_element(By.NAME, 'passwrd').send_keys(pw)
        driver.find_element(By.ID, 'user_login_segment').click()
        time.sleep(1) #maybe there is a way to wait if the page has loaded correctly
        driver.find_element(By.LINK_TEXT,'Okay!').click()
        driver.find_element(By.XPATH, "(//i[@class='fa fa-plus'])[1]").click()
        driver.find_element(By.ID, 'deckbuilder_new_deck_dialog_name').send_keys(deckdata[0])
        format_selecter = Select(driver.find_element(By.ID, 'deckbuilder_new_deck_dialog_format'))
        format_selecter.select_by_value('3')
        driver.find_element(By.ID, 'deckbuilder_new_deck_dialog_is_public').click()
        driver.find_element(By.XPATH, "(//span[text()='OK'])[1]").click()
        time.sleep(1) #maybe there is a way to wait if the page has loaded correctly
        driver.find_element(By.XPATH, "//span[text()[normalize-space()='Paste/upload list']]").click()
        time.sleep(1) #maybe there is a way to wait if the page has loaded correctly
        driver.find_element(By.ID, 'deckbuilder_upload_list_dialog_textarea').send_keys(deckdata[1])
        time.sleep(1)
        driver.find_element(By.XPATH, "(//span[text()='OK'])[5]").click()
        driver.find_element(By.XPATH, "//span[text()[normalize-space()='Speichern']]").click()
        driver.find_element(By.XPATH, "(//span[text()='OK'])[2]").click()
        driver.find_element(By.ID, 'ui-id-14').click()
        mainboardPrice.set(value=driver.find_element(By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[1]").getText())
        sideboardPrice.set(value=driver.find_element(By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[2]").getText())
        totalPrice.set(str(int(mainboardPrice)+int(sideboardPrice)))
        driver.quit()


class DeckValuePage(Page):
    parent = UploadPage
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_mainboard_price = ttk.Label(self, text="Mainboard Preis: " + str(mainboardPrice), width=20)
        lbl_sideboard_price = ttk.Label(self, text="Sideboard Preis: " + str(sideboardPrice), width=20)
        lbl_total_price = ttk.Label(self, text="Gesamtpreis: " + str(totalPrice), width=20)
        btn_submit3 = ttk.Button(self, text="Nächstes Deck", width=20, command=lambda: self.master.switch_frame(UploadPage))
        btn_submit3.bind('<Button-1>', self.pack_forget())
        lbl_mainboard_price.pack(fill=tk.BOTH, side=tk.LEFT)
        lbl_sideboard_price.pack(fill=tk.BOTH, side=tk.LEFT)
        lbl_total_price.pack(fill=tk.BOTH, side=tk.LEFT)
        btn_submit3.pack(fill=tk.BOTH, side=tk.BOTTOM)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.pages = {}
        for F in (LoginPage, UploadPage, DeckValuePage):
            page = F(self)
            self.pages[F] = page
            page.grid(row=0, column=0, sticky="nsew")
        self.switch_frame(LoginPage)
        
    def switch_frame(self, frame_class):
        page = self.pages[frame_class]
        page.show()

<<<<<<< HEAD
if __name__ == "__main__":
    root = tk.Tk()
    root.wm_iconbitmap("money-icon.ico")
    mainboardPrice = tk.StringVar()
    sideboardPrice = tk.StringVar()
    totalPrice = tk.StringVar()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
=======
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
mainboardPrice, sideboardPrice = deckwert_ermittlung('C:/Users/Fabian/Desktop/SampleDeckliste.txt', id, pw)

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
>>>>>>> f85dfd95dbf55cb9c8c6152bb93e476cfa0343e6
