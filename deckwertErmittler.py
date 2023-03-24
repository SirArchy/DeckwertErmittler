import re
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

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
        ent_id = ttk.Entry(self, textvariable=self.defaultID)
        lbl_pw = ttk.Label(self, text="Password: ")
        ent_pw = ttk.Entry(self, textvariable=self.defaultPW, show="•")
        btn_submit1 = ttk.Button(
            self, text="Weiter", command=lambda: self.master.switch_frame(UploadPage))
        lbl_id.pack(fill=tk.X, side=tk.LEFT)
        ent_id.pack(fill=tk.X, side=tk.LEFT)
        lbl_pw.pack(fill=tk.X, side=tk.LEFT)
        ent_pw.pack(fill=tk.X, side=tk.LEFT)
        btn_submit1.pack(fill=tk.X, side=tk.LEFT)
        id.set(value=ent_id.get())
        pw.set(value=ent_pw.get())


class UploadPage(Page):
    parent = LoginPage

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_insert_file = ttk.Label(self, text="Deckliste", width=20)
        self.txt_decklist = tk.Text(self, height=12)
        # this function should open the file, save it's location and it's contents + display it in textfield
        btn_open_file = ttk.Button(
            self, text='Deckliste auswählen', command= lambda: self.open_text_file())
        btn_calculate_price = ttk.Button(self, text='Preis ausrechnen', command=lambda: [
                                         self.save_text_file(), self.deckwert_ermittlung(), self.master.switch_frame(UploadPage)])
        lbl_insert_file.pack(fill=tk.BOTH, side=tk.TOP)
        self.txt_decklist.pack(fill=tk.BOTH, side=tk.TOP)
        btn_open_file.pack(fill=tk.BOTH, side=tk.LEFT)
        btn_calculate_price.pack(fill=tk.BOTH, side=tk.LEFT)

    def open_text_file(self):
        # show the open file dialog
        f = fd.askopenfile(initialdir="C:/Users/MainFrame/Desktop/",
        title="Open Text file",
        filetypes=(("Text Files", "*.txt"),))
        # read the text file and show its content on the Text
        self.txt_decklist.insert('1.0', f.read())
        deckPath.set(value=f)
        deckContent.set(value=f.read())

    def save_text_file(self): #doesn't seem to work? maybe because webdriver doesn't work
        deckContent.set(self.txt_decklist.get(1.0, tk.END))
        print(deckPath.get())
        text_file = open(deckPath.get(), "w")
        text_file.write(self.txt_decklist.get(1.0, tk.END))
        text_file.close()

    def deckNameEinlesen(self):
        # read deck name
        print(deckPath.get())
        textfile_name = re.search("[ \w-]+?(?=\.)", deckPath.get()).group()
        return textfile_name

    def deckwert_ermittlung(self):
        # Create the webdriver object
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # enter your download directory here
        prefs = {'download.default_directory': ''}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # get website link
        driver.get('https://deckstats.net')

        # get deckname and decklist
        self.deckdata = self.deckNameEinlesen()

        # Obtain buttons by class name and click all of them
        driver.find_element(By.NAME, 'user').send_keys(str(id))
        driver.find_element(By.NAME, 'passwrd').send_keys(str(pw))
        driver.find_element(By.ID, 'user_login_segment').click()
        # maybe there is a way to wait if the page has loaded correctly
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, 'Okay!').click()
        driver.find_element(By.XPATH, "(//i[@class='fa fa-plus'])[1]").click()
        driver.find_element(
            By.ID, 'deckbuilder_new_deck_dialog_name').send_keys(str(self.deckdata))
        format_selecter = Select(driver.find_element(
            By.ID, 'deckbuilder_new_deck_dialog_format'))
        format_selecter.select_by_value('3')
        driver.find_element(
            By.ID, 'deckbuilder_new_deck_dialog_is_public').click()
        driver.find_element(By.XPATH, "(//span[text()='OK'])[1]").click()
        # maybe there is a way to wait if the page has loaded correctly
        time.sleep(1)
        driver.find_element(
            By.XPATH, "//span[text()[normalize-space()='Paste/upload list']]").click()
        # maybe there is a way to wait if the page has loaded correctly
        time.sleep(1)
        driver.find_element(
            By.ID, 'deckbuilder_upload_list_dialog_textarea').send_keys(str(deckContent))
        time.sleep(1)
        driver.find_element(By.XPATH, "(//span[text()='OK'])[5]").click()
        driver.find_element(
            By.XPATH, "//span[text()[normalize-space()='Speichern']]").click()
        driver.find_element(By.XPATH, "(//span[text()='OK'])[2]").click()
        driver.find_element(By.ID, 'ui-id-14').click()
        mainboardPrice.set(value=driver.find_element(
            By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[1]").getText())
        sideboardPrice.set(value=driver.find_element(
            By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[2]").getText())
        totalPrice.set(str(int(mainboardPrice)+int(sideboardPrice)))
        driver.quit()


class DeckValuePage(Page):
    parent = UploadPage

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_mainboard_price = ttk.Label(
            self, text="Mainboard Preis: " + str(mainboardPrice), width=20)
        lbl_sideboard_price = ttk.Label(
            self, text="Sideboard Preis: " + str(sideboardPrice), width=20)
        lbl_total_price = ttk.Label(
            self, text="Gesamtpreis: " + str(totalPrice), width=20)
        btn_submit3 = ttk.Button(self, text="Nächstes Deck", width=20,
                                 command=lambda: self.master.switch_frame(UploadPage))
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


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Deckwert Ermittler")
    root.wm_iconbitmap("money-icon.ico")
    #maybe make these global instead of stringvar
    id = tk.StringVar()
    pw = tk.StringVar()
    deckPath = tk.StringVar()
    deckContent = tk.StringVar()
    mainboardPrice = tk.StringVar()
    sideboardPrice = tk.StringVar()
    totalPrice = tk.StringVar()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
