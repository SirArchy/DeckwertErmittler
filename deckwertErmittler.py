import re
import tkinter as tk
from tkinter import ttk
import threading
from PIL import Image, ImageTk
from itertools import count, cycle
from tkinter import filedialog as fd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
This program is used to display the deck value of the selected .txt file containing a magic the gathering deck.
It logs into the given deckstats.net account, adds the deck and then displays the deck's values. 
✔️ ❌
"""


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        global id
        global pw
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
        id = ent_id.get()
        pw = ent_pw.get()


class UploadPage(Page):
    parent = LoginPage
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_insert_file = ttk.Label(self, text="Deckliste", width=20)
        self.txt_decklist = tk.Text(self, height=12)
        # this function should open the file, save it's location and it's contents + display it in textfield
        btn_open_file = ttk.Button(
            self, text='Deckliste auswählen', command= self.open_text_file)
        btn_calculate_price = ttk.Button(self, text='Preis ausrechnen')
        btn_calculate_price.bind("<Button-1>",  lambda :[
                                         self.show_gif, self.save_text_file, self.deckwert_ermittlung, self.master.switch_frame(DeckValuePage)])
        lbl_insert_file.pack(fill=tk.BOTH, side=tk.TOP)
        self.txt_decklist.pack(fill=tk.BOTH, side=tk.TOP)
        btn_open_file.pack(fill=tk.BOTH, side=tk.LEFT)
        btn_calculate_price.pack(fill=tk.BOTH, side=tk.LEFT)

    def open_text_file(self): #✔️
        global deckPath
        global deckContent
        # show the open file dialog
        f = fd.askopenfile(initialdir="C:/Users/MainFrame/Desktop/",
                            title="Open Text file",
                            filetypes=(("Text Files", "*.txt"),))
        # read the text file and show its content on the Text
        self.txt_decklist.insert('1.0', f.read())
        deckPath = f.name
        deckContent = f.read()

    def save_text_file(self): #✔️
        global deckPath
        global deckContent
        deckContent = self.txt_decklist.get(1.0, tk.END)
        text_file = open(deckPath, "w")
        text_file.write(deckContent)
        text_file.close()

    def deckNameEinlesen(self): #✔️
        global deckPath
        textfile_name = re.search("[ \w-]+?(?=\.)", deckPath).group()
        return textfile_name

    def show_gif(self):
        self.gif_viewer = tk.Toplevel(self)
        lbl_text = tk.Label(self.gif_viewer, text="Deckwerte werden ermittelt...")
        lbl_text.pack(fill=tk.BOTH, side=tk.TOP)
        GifViewer(self.gif_viewer, "loading.gif")
        t = threading.Thread(target=self.deckwert_ermittlung, args=(self.gif_viewer,))
        t.start()

    def deckwert_ermittlung(self): #✔️
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
        # get deckname and decklist
        deckName = UploadPage.deckNameEinlesen(self)
        # Obtain buttons by class name and click all of them
        driver.find_element(By.NAME, 'user').send_keys(id)
        driver.find_element(By.NAME, 'passwrd').send_keys(pw)
        driver.find_element(By.ID, 'user_login_segment').click()
        # maybe there is a way to wait if the page has loaded correctly
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Okay!'))
        )
        driver.find_element(By.LINK_TEXT, 'Okay!').click()
        driver.find_element(By.XPATH, "(//i[@class='fa fa-plus'])[1]").click()
        driver.find_element(
            By.ID, 'deckbuilder_new_deck_dialog_name').send_keys(deckName)
        format_selecter = Select(driver.find_element(
            By.ID, 'deckbuilder_new_deck_dialog_format'))
        format_selecter.select_by_value('3')
        driver.find_element(
            By.ID, 'deckbuilder_new_deck_dialog_is_public').click()
        driver.find_element(By.XPATH, "(//span[text()='OK'])[1]").click()
        # maybe there is a way to wait if the page has loaded correctly
        WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[normalize-space()='Paste/upload list']]"))
        )
        driver.find_element(
            By.XPATH, "//span[text()[normalize-space()='Paste/upload list']]").click()
        # maybe there is a way to wait if the page has loaded correctly
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "html[1]/body[1]/div[19]"))
        )
        driver.find_element(
            By.ID, 'deckbuilder_upload_list_dialog_textarea').send_keys(deckContent.replace('\t',' ').replace('Mainboard','').replace('Sideboard','').replace('Sidedeck','').replace('Maindeck',''))
        WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'button_primary ui-button')]//span)[3]"))
        )
        driver.find_element(By.XPATH, "(//button[contains(@class,'button_primary ui-button')]//span)[3]").click()
        WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[normalize-space()='Speichern']]"))
        )
        driver.find_element(By.XPATH, "//span[text()[normalize-space()='Speichern']]").click()
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "html[1]/body[1]/div[13]"))
        )
        driver.find_element(By.XPATH, "(//span[text()='OK'])[2]").click()
        driver.find_element(By.ID, 'ui-id-14').click()
        mainboardPrice = driver.find_element(
            By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[1]").get_attribute("innerHTML")
        sideboardPrice = driver.find_element(
            By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[2]").get_attribute("innerHTML")
        totalPrice = str(float(mainboardPrice.replace('€',''))+float(sideboardPrice.replace('€','')))
        driver.quit()


class DeckValuePage(Page):
    def __init__(self, *args, **kwargs):
        global mainboardPrice
        global sideboardPrice
        global totalPrice
        global saved_prices
        Page.__init__(self, *args, **kwargs)
        lbl_mainboard_price = ttk.Label(
            self, textvariable=StrVar_mainboardPrice, width=20) #❌
        lbl_sideboard_price = ttk.Label(
            self, textvariable=StrVar_sideboardPrice, width=20) #❌
        lbl_total_price = ttk.Label(
            self, textvariable=StrVar_totalPrice, width=20) #❌
        prices_str = deckName + "/n" + mainboardPrice + "/n" + sideboardPrice + "/n" + totalPrice
        btn_submit3 = ttk.Button(self, text="Preise sichern & nächstes Deck", width=20,
                                 command=lambda: [self.master.switch_frame(UploadPage), self.save_prices_in_str(prices_str)])
        btn_submit4 = ttk.Button(self, text="Alle Preise als Datei abspeichern", width=20, command= self.save_prices_in_file)
        btn_submit3.bind('<Button-1>', self.pack_forget())
        lbl_mainboard_price.pack(fill=tk.BOTH, side=tk.LEFT)
        lbl_sideboard_price.pack(fill=tk.BOTH, side=tk.LEFT)
        lbl_total_price.pack(fill=tk.BOTH, side=tk.LEFT)
        btn_submit3.pack(fill=tk.BOTH, side=tk.BOTTOM)
        btn_submit4.pack(fill=tk.BOTH, side=tk.BOTTOM)
    def save_prices_in_str(self, prices):
        saved_prices = saved_prices + "/n" + prices
    def save_prices_in_file(self):
        files = [('Text Document', '*.txt')]
        f = fd.asksaveasfile(filetypes = files, defaultextension = files)
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        f.write(saved_prices)
        f.close()

class GifViewer:
    def __init__(self, master, gif_path):
        self.master = master
        self.gif_path = gif_path
        self.gif_frames = []
        self.load_gif_frames()
        self.current_frame = 0
        
        self.canvas = tk.Canvas(self.master, height=140, width=130)
        self.canvas.pack(side=tk.BOTTOM)
        
        self.animate_gif()

    def load_gif_frames(self):
        gif_image = Image.open(self.gif_path)
        try:
            while True:
                gif_frame = gif_image.copy()
                self.gif_frames.append(ImageTk.PhotoImage(gif_frame))
                gif_image.seek(len(self.gif_frames))  # seek to next frame
        except EOFError:
            pass

    def animate_gif(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.gif_frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.master.after(20, self.animate_gif)  # call itself again after 100ms



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
    id = ""
    pw = ""
    deckPath = ""
    deckContent = ""
    deckName = ""
    mainboardPrice = ""
    StrVar_mainboardPrice = tk.StringVar(root, "Mainboard Preis: " + mainboardPrice)
    sideboardPrice = ""
    StrVar_sideboardPrice = tk.StringVar(root, "Sideboard Preis: " + mainboardPrice)
    totalPrice = ""
    StrVar_totalPrice = tk.StringVar(root, "Gesamtpreis: " + mainboardPrice + " €")
    saved_prices = ""
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
