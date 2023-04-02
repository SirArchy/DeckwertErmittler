import re
import tkinter as tk
from tkinter import ttk
import threading
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog as fd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


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
        lbl_id = ttk.Label(self, text="ID: ", font = "Verdana 10 bold")
        self.defaultID = tk.StringVar(value='MagicNerdism')
        self.defaultPW = tk.StringVar(value='Test1234')
        ent_id = ttk.Entry(self, textvariable=self.defaultID, font = "Verdana 10")
        lbl_pw = ttk.Label(self, text="Password: ", font = "Verdana 10 bold")
        ent_pw = ttk.Entry(self, textvariable=self.defaultPW, show="•", font = "Verdana 10")
        btn_submit1 = ttk.Button(
            self, text="Weiter", command=lambda: self.master.switch_frame(UploadPage))
        lbl_id.grid(row=0, column=0, padx='5', pady='5', sticky='ew')
        ent_id.grid(row=0, column=1, padx='5', pady='5', ipadx=25, sticky='ew')
        lbl_pw.grid(row=1, column=0, padx='5', pady='5', sticky='ew')
        ent_pw.grid(row=1, column=1, padx='5', pady='5', ipadx=25, sticky='ew')
        btn_submit1.grid(row=0, column=2, rowspan=2, sticky=tk.N+tk.S)
        id = ent_id.get()
        pw = ent_pw.get()



class UploadPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lbl_insert_file = ttk.Label(self, text="Deckliste", font = "Verdana 10 bold")
        self.txt_decklist = tk.Text(self, height=18, width=15)
        btn_open_file = ttk.Button(
            self, text='Deckliste auswählen', command= self.open_text_file)
        btn_calculate_price = ttk.Button(self, text='Preis ausrechnen', command= self.calculate_price)
        lbl_insert_file.grid(row=0, column=0, columnspan=2, padx='5', pady='5')
        self.txt_decklist.grid(row=1, column=0, columnspan=2, padx='5', pady='5', sticky='ew')
        btn_open_file.grid(row=2, column=0, padx='5', pady='5', ipady=10, ipadx=41, sticky='ew')
        btn_calculate_price.grid(row=2, column=1, padx='5', pady='5', ipady=10, ipadx=41, sticky='ew')

    def calculate_price(self):
        # Throw error when no file selected
        if deckPath == "":
            messagebox.showerror('Python Error', 'Error: Keine Deckliste ausgewählt! Bitte wähle zuerst eine Deckliste aus.')
        else:
            self.show_gif()
            self.save_text_file()
            # Run deckwert_ermittlung function in a separate thread
            t = threading.Thread(target=self.deckwert_ermittlung)
            t.start()

    def open_text_file(self): #✔️
        global deckPath
        global deckContent
        # show the open file dialog
        f = fd.askopenfile(initialdir="C:/Users/MainFrame/Desktop/",
                            title="Open Text file",
                            filetypes=(("Text Files", "*.txt"),))
        # read the text file and show its content on the Text
        if self.txt_decklist.get("1.0", tk.END) != "\n":
            self.txt_decklist.delete('1.0', tk.END)
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
        self.gif_viewer.wm_iconbitmap("money-icon.ico")
        lbl_text = tk.Label(self.gif_viewer, text="Deckwerte werden ermittelt...")
        lbl_text.grid(row=0, column=0)
        GifViewer(self.gif_viewer, "loading.gif")


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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('window-size=1920x1080')
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
        WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[normalize-space()='Paste/upload list']]"))
        )
        driver.find_element(
            By.XPATH, "//span[text()[normalize-space()='Paste/upload list']]").click()
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "html[1]/body[1]/div[19]"))
        )
        driver.find_element(
            By.ID, 'deckbuilder_upload_list_dialog_textarea').send_keys(deckContent.replace('\t',' ').replace('//Sidedeck','//Sideboard').replace('//Maindeck','//Mainboard').replace('Sidedeck','//Sideboard').replace('Maindeck','//Mainboard'))
        WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'button_primary ui-button')]//span)[3]"))
        )
        driver.find_element(By.XPATH, "(//button[contains(@class,'button_primary ui-button')]//span)[3]").click()
        WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()[normalize-space()='Speichern']]"))
        )
        driver.find_element(By.XPATH, "//span[text()[normalize-space()='Speichern']]").click()
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "ncmp__tool"))
        )
        driver.find_element(By.XPATH, "//*[@id='ncmp__tool']/div/div/div[3]/div[1]/button[2]").click()
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "html[1]/body[1]/div[13]"))
        )
        driver.find_element(By.XPATH, "(//span[text()='OK'])[2]").click()
        driver.find_element(By.ID, 'ui-id-14').click()
        mainboardPrice = driver.find_element(
            By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[1]").get_attribute("innerHTML")
        try: 
            sideboardPrice = driver.find_element(
                By.XPATH, "(//td[@title='Total price on Cardmarket for the card versions listed'])[2]").get_attribute("innerHTML")
            totalPrice = str(float(mainboardPrice.replace('€',''))+float(sideboardPrice.replace('€','')))
            totalPrice = "{:.2f}".format(float(totalPrice))
            StrVar_mainboardPrice.set(mainboardPrice)
            StrVar_sideboardPrice.set(sideboardPrice)
            StrVar_totalPrice.set(totalPrice + " €")
            StrVar_deckname.set(deckName)
            self.master.switch_frame(DeckValuePage)      
        except NoSuchElementException:     
            messagebox.showerror('Python Error', 'Deck hat kein Sideboard. Bitte fügen sie dieses hinzu.') 
        driver.quit()
        self.gif_viewer.destroy()
        


class DeckValuePage(Page):
    def __init__(self, *args, **kwargs):
        global mainboardPrice
        global sideboardPrice
        global totalPrice
        Page.__init__(self, *args, **kwargs)
        deckname_frame = ttk.Frame(self)
        deckname_frame.grid(row=0, column=0, columnspan=2)
        lbl_deckname = ttk.Label(deckname_frame, textvariable=StrVar_deckname, font = "Verdana 20 bold")
        lbl_deckname.grid()
        
        mainboard_frame = ttk.Frame(self)
        mainboard_frame.grid(row=1, column=0, sticky='ew', padx='10')
        lbl_mainboard = ttk.Label(mainboard_frame, text="Mainboard Preis: ", font = "Verdana 20")
        lbl_mainboard.grid()
        mainboard_frame_prices = ttk.Frame(self)
        mainboard_frame_prices.grid(row=1, column=1, sticky='ew', padx='10')
        lbl_mainboard_price = ttk.Label(mainboard_frame_prices, textvariable=StrVar_mainboardPrice, font = "Verdana 20 bold")
        lbl_mainboard_price.grid()
        
        sideboard_frame = ttk.Frame(self)
        sideboard_frame.grid(row=2, column=0, sticky='ew', padx='10')
        lbl_sideboard = ttk.Label(sideboard_frame, text="Sideboard Preis: ", font = "Verdana 20")
        lbl_sideboard.grid()
        sideboard_frame_prices = ttk.Frame(self)
        sideboard_frame_prices.grid(row=2, column=1, sticky='ew', padx='10')
        lbl_sideboard_price = ttk.Label(sideboard_frame_prices, textvariable=StrVar_sideboardPrice, font = "Verdana 20 bold")
        lbl_sideboard_price.grid()
        
        totalprice_frame = ttk.Frame(self)
        totalprice_frame.grid(row=3, column=0, sticky='ew', padx='10')
        lbl_totalprice = ttk.Label(totalprice_frame, text="Gesamtpreis: ", font = "Verdana 20")
        lbl_totalprice.grid()
        totalprice_frame_prices = ttk.Frame(self)
        totalprice_frame_prices.grid(row=3, column=1, sticky='ew', padx='10')
        lbl_total_price = ttk.Label(totalprice_frame_prices, textvariable=StrVar_totalPrice, font = "Verdana 20 bold")
        lbl_total_price.grid()
        
        btn_submit3 = ttk.Button(self, text="Preise zwischenspeichern & nächstes Deck", command=lambda: [self.save_prices_in_str(), self.master.switch_frame(UploadPage)])
        btn_submit4 = ttk.Button(self, text="Alle Preise als Datei abspeichern", command= lambda: [self.save_prices_in_str(), self.save_prices_in_file()])
        btn_submit3.grid(row=4, column=0, columnspan=2, padx='5', pady='5', ipadx=30, ipady=10, sticky='ew')
        btn_submit4.grid(row=5, column=0, columnspan=2, padx='5', pady='5', ipadx=30, ipady=10, sticky='ew')
        
    def save_prices_in_str(self):
        global saved_prices
        global prices_str
        prices_str = deckName + "\n" + mainboardPrice + "\n" + sideboardPrice + "\n" + totalPrice + " €"
        if saved_prices == "":
            saved_prices = prices_str
        else:    
            saved_prices = saved_prices + "\n" + "\n" + prices_str 
    
    def save_prices_in_file(self):
        global saved_prices
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
        self.canvas.grid(row=1, column=0)
        
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
        self.master.after(20, self.animate_gif)



class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.pages = {}
        for F in (LoginPage, UploadPage, DeckValuePage):
            page = F(self)
            self.pages[F] = page
            page.grid(row=0, column=0, sticky="nsew")
        
        # Add row and column configuration to the main frame
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

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
    StrVar_deckname = tk.StringVar(root)
    mainboardPrice = ""
    StrVar_mainboardPrice = tk.StringVar(root)
    sideboardPrice = ""
    StrVar_sideboardPrice = tk.StringVar(root)
    totalPrice = ""
    StrVar_totalPrice = tk.StringVar(root)
    saved_prices = ""
    prices_str = ""
    main = MainView(root)
    main.grid(row=0, column=0, sticky="nsew") # Use grid instead of pack
    root.wm_geometry("400x400")
    root.mainloop()

