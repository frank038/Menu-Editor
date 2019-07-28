#!/usr/bin/env python3

"""
 by frank38
 V. 0.0.1
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
import os
#import sys
#import shutil
#import time
#import subprocess
import glob
import collections
from xdg import DesktopEntry
from xdg import IconTheme
#IconTheme.getIconPath("qterminal")
#'/usr/share/icons/hicolor/64x64/apps/qterminal.png'

# font size
font_size = 20

# window width and height
app_width = 1200
app_height = 900

# stampa la home dir + .local/share 
#print(os.environ.get('XDG_DATA_HOME'))

# directory in cui si trova questo script
#scriptDirectory = os.path.dirname(os.path.realpath(__file__))

# directory in cui si trovano i file .desktop
app_dirs = [os.environ.get("XDG_DATA_HOME")+"/applications", "/usr/share/applications"]
#app_dirs = ["/home/linux10/Desktop/os-monitor-master/tkmenu/desktop"]
app_dirs_user = [os.environ.get("XDG_DATA_HOME")+"/applications"]
app_dirs_system = ["/usr/share/applications"]

#######################
# principali categorie freedesktop
# tolti "Audio" e "Video" come categorie separate
freedesktop_main_categories = ["AudioVideo","Development",
                              "Education","Game","Graphics","Network",
                              "Office","Settings","System","Utility"]

development_extended_categories = ["Building","Debugger","IDE","GUIDesigner",
                                  "Profiling","RevisionControl","Translation",
                                  "Database","WebDevelopment"]

office_extended_categories = ["Calendar","ContanctManagement","Office",
                             "Dictionary","Chart","Email","Finance","FlowChart",
                             "PDA","ProjectManagement","Presentation","Spreadsheet",
                             "WordProcessor","Engineering"]

graphics_extended_categories = ["2DGraphics","VectorGraphics","RasterGraphics",
                               "3DGraphics","Scanning","OCR","Photography",
                               "Publishing","Viewer"]

utility_extended_categories = ["TextTools","TelephonyTools","Compression",
                              "FileTools","Calculator","Clock","TextEditor",
                              "Documentation"]

settings_extended_categories = ["DesktopSettings","HardwareSettings",
                               "Printing","PackageManager","Security",
                               "Accessibility"]

network_extended_categories = ["Dialup","InstantMessaging","Chat","IIRCClient",
                              "FileTransfer","HamRadio","News","P2P","RemoteAccess",
                              "Telephony","VideoConference","WebBrowser"]

# aggiunte le categorie main "Audio" e "Video"
audiovideo_extended_categories = ["Audio","Video","Midi","Mixer","Sequencer","Tuner","TV",
                                 "AudioVideoEditing","Player","Recorder",
                                 "DiscBurning"]

game_extended_categories = ["ActionGame","AdventureGame","ArcadeGame",
                           "BoardGame","BlockGame","CardGame","KidsGame",
                           "LogicGame","RolePlaying","Simulation","SportGame",
                           "StrategyGame","Amusement","Emulator"]

education_extended_categories = ["Art","Construction","Music","Languages",
                                "Science","ArtificialIntelligence","Astronomy",
                                "Biology","Chemistry","ComputerScience","DataVisualization",
                                "Economy","Electricity","Geography","Geology","Geoscience",
                                "History","ImageProcessing","Literature","Math","NumericAnalysis",
                                "MedicalSoftware","Physics","Robots","Sports","ParallelComputing",
                                "Electronics"]

system_extended_categories = ["FileManager","TerminalEmulator","FileSystem",
                             "Monitor","Core"]

## lista di tutte le categorie estese
#all_ext_cat = [development_extended_categories,office_extended_categories,graphics_extended_categories,utility_extended_categories,settings_extended_categories,network_extended_categories,audiovideo_extended_categories,game_extended_categories,education_extended_categories,system_extended_categories]

# named tuple
nt_ext_categ = collections.namedtuple("List", "main list", rename=False)

development_ext = nt_ext_categ("Development", development_extended_categories)
office_ext = nt_ext_categ("Office", office_extended_categories)
graphics_ext = nt_ext_categ("Graphics", graphics_extended_categories)
utility_ext = nt_ext_categ("Utility", utility_extended_categories)
settings_ext = nt_ext_categ("Settings", settings_extended_categories)
network_ext = nt_ext_categ("Network", network_extended_categories)
audiovideo_ext = nt_ext_categ("AudioVideo", audiovideo_extended_categories)
game_ext = nt_ext_categ("Game", game_extended_categories)
education_ext = nt_ext_categ("Education", education_extended_categories)
system_ext = nt_ext_categ("System", system_extended_categories)
# tutte le sotto categorie in una lista
all_extend_list = [development_ext,office_ext,graphics_ext,utility_ext,
                  settings_ext,network_ext,audiovideo_ext,game_ext,
                  education_ext,system_ext]

# sottocategorie rimanenti
# KDE (QT), GNOME (GTK), GTK, Qt, Motif, Java, ConsoleOnly
# categorie riservate, da usare con OnlyShowIn= entry
# Screensaver, TrayIcon, Applet, Shell
# OnlyShowIn Value:
# GNOME, KDE, ROX, XFCE, Old
######################


# /usr/share/desktop-directories

## per ottenere la lingua
#import locale
## con locale.getlocale() ottengo ('it_IT', 'UTF-8')
#llang = locale.getlocale()[0].split("_")[0] # ottengo it
#print("llang::", llang)

## usare questo
print(os.environ["LANG"].split("_")[0])

###############

# dove vengono memorizzati i file con le categorie
# serve per creare una lista
class catDesktop():
    name = ""
    categories = ""
    path = ""
    

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.pack(fill="both", expand=True)
        self.master.update_idletasks()
        
        # per settare l altezza di ogni row in treeview - workaround
        ffont = font.Font(family='', size=font_size)
        #print(ffont.metrics("linespace"))
        self.tv_row_height = ffont.metrics("linespace")
        
        self.create_widgets()
        
    def create_widgets(self):
        # font family and size
        self.s = ttk.Style(self.master)
        self.s.configure('.', font=('', font_size))
        ###
        ###############
        # lista per ogni elemento file desktop
        self.info_desktop = []
        #self.file_list = self.list_app(app_dirs_user)
        self.file_list = []
        # funzione che sostituisce i tre successivi
        # popola self.info_desktop
        self.fpop(app_dirs_user)
        ##############
        # ottengo la lista dei file desktop
        ##self.file_list = self.list_app(app_dirs_user)
        #self.file_list = []
        #
        #
        ## lista per ogni elemento file desktop
        #self.info_desktop = []
        #
        ## popolo la lista - funzione
        #self.pop_info_desktop()
        #
        ## stampo il contenuto della lista - OK
        #print("self.info_desktop::", self.info_desktop[0].categories)
        #
        ############### creo la struttura grafica
        #### buttons
        self.frame_btn = ttk.Frame(self, width=app_width)
        self.frame_btn.grid(column=0, row=0, columnspan=10)#, sticky="nw")
        # button
        self.btn1 = ttk.Button(self.frame_btn, text="User/System", command=self.fswitch)
        self.btn1.grid(column=0, row=0, sticky="nw")
        # button
        self.btn2 = ttk.Button(self.frame_btn, text="Modify")
        self.btn2.grid(column=2, row=0, sticky="nw")
        # button
        self.btn3 = ttk.Button(self.frame_btn, text="New")
        self.btn3.grid(column=3, row=0, sticky="nw")
        # quit button
        quit_btn = ttk.Button(self.frame_btn, text="Exit", command=quit)
        quit_btn.grid(column=9, row=0, sticky="ne")
        # frame per treeview e scrollbar
        self.tv_frame = ttk.Frame(self)
        self.tv_frame.grid(column=0, row=4, rowspan=20)
        self.tv = ttk.Treeview(self.tv_frame, selectmode="browse", height=25)#, show="tree")
        #self.tv.grid(column=0, row=4, rowspan=20, sticky="nw")
        self.tv.pack(side="left", fill="y", expand=True)
        # larghezza della colonna
        self.tv.column("#0", width=350)
        # instestazione della colonna - anche per cambiarla in seguito
        self.tv.heading("#0", text="User")
        # soluzione per aumentare l altezza di ogni row - workaround
        self.s.configure('Treeview', rowheight=self.tv_row_height+2)
        #
        # scrollbar 
        self.vscrollbar = ttk.Scrollbar(self.tv_frame, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=self.vscrollbar.set)
        #self.vsb.grid(column=1, row=4, rowspan=20, sticky="nw")
        self.vscrollbar.pack(fill="y", expand=True)
        #
        ### parte destra
        # stile bold per i label
        bold_style = ttk.Style ()
        bold_style.configure("Bold.TLabel", font=("", font_size, "bold"))
        #bold_style = font.Font(family="Sans", size=font_size, weight="bold")
        # stile corsivo per i label
        italic_style = ttk.Style()
        italic_style.configure("Italic.TLabel", font=("", font_size, "italic"))
        #
        #self.s.configure("TCombobox", font=("", 24))
        # per incrementare la dimensione dei font di combobox
        bigfont = font.Font(family="",size=font_size)
        ## questo lo applica a tutti - funziona
        #self.master.option_add("*Font", bigfont)
        ## non funziona
        #self.master.option_add("*TCombobox*Listbox*Font", bigfont)
        # FUNZIONA SOLO CON QUESTO
        self.master.option_add("*TCombobox*Font", bigfont)
        ## frame
        self.d_frame = ttk.Frame(self)
        self.d_frame.grid(column=1, row=4, rowspan=20)
        # image - solo png in hicolor theme
        self.iimage = tk.PhotoImage(file="ag.png")
        self.image_lbl = ttk.Label(self.d_frame, text="", image=self.iimage)
        self.image_lbl.grid(column=0, row=4, rowspan=3)#, sticky="nw")
        # name
        self.pname_lbl = ttk.Label(self.d_frame, text="", style="Bold.TLabel")
        self.pname_lbl.grid(column=1, row=4, sticky="w")
        # generic name
        self.generic_name_lbl = ttk.Label(self.d_frame, text="", style="Italic.TLabel")
        self.generic_name_lbl.grid(column=1,row=5, sticky="w")
        # comment
        self.comment_lbl = ttk.Label(self.d_frame, text="")
        self.comment_lbl.grid(column=1,row=6, sticky="w")
        ############# APPLICATION DETAILS
        # Applications Details line
        self.blank_lbl = ttk.Label(self.d_frame, text="\nApplication Details", style="Bold.TLabel")
        self.blank_lbl.grid(column=0, row=7)
        #
        # exec
        self.exec_lbl = ttk.Label(self.d_frame, text="  Command: ")
        self.exec_lbl.grid(column=0, row=8, sticky="w")
        #
        self.exec_lbl2 = ttk.Label(self.d_frame, text="")
        self.exec_lbl2.grid(column=1, row=8, sticky="w")
        # try exec
        self.tryexec_lbl = ttk.Label(self.d_frame, text="  TryExec: ")
        self.tryexec_lbl.grid(column=0, row=9, sticky="w")
        #
        self.tryexec_lbl2 = ttk.Label(self.d_frame, text="")
        self.tryexec_lbl2.grid(column=1, row=9, sticky="w")
        # categories
        self.categories_lbl = ttk.Label(self.d_frame, text="  Categories: ")
        self.categories_lbl.grid(column=0, row=10, sticky="w")
        #
        #self.categories_lbl2 = ttk.Label(self.d_frame, text="")
        #self.categories_lbl2.grid(column=1, row=10, sticky="w")
        self.categories_cb2 = ttk.Combobox(self.d_frame)
        self.categories_cb2.grid(column=1, row=10, sticky="w")
        # mimetypes
        self.mime_lbl = ttk.Label(self.d_frame, text="  Mime Types: ")
        self.mime_lbl.grid(column=0, row=11, sticky="w")
        #
        self.mime_lbl2 = ttk.Label(self.d_frame, text="", width=30, wraplength=300)
        #self.mime_lbl2.grid(column=1, row=9, sticky="w")
        #
        self.mime_cb2 = ttk.Combobox(self.d_frame)
        self.mime_cb2.grid(column=1, row=11, sticky="w")
        # keywords
        self.keywords_lbl = ttk.Label(self.d_frame, text="  Keywords:")
        self.keywords_lbl.grid(column=0, row=12, sticky="w")
        #
        self.keywords_cb2 = ttk.Combobox(self.d_frame)
        self.keywords_cb2.grid(column=1, row=12, sticky="w")
        # URL
        self.url_lbl = ttk.Label(self.d_frame, text="  Url: ")
        self.url_lbl.grid(column=0, row=13, sticky="w")
        #
        self.url_lbl2 = ttk.Label(self.d_frame, text="")
        self.url_lbl2.grid(column=1, row=13, sticky="w")
        ###### OPTIONS
        # options
        self.options_lbl = ttk.Label(self.d_frame, text="Options", style="Bold.TLabel").grid(column=0, row=18, sticky="w")
        # terminal
        self.terminal_lbl = ttk.Label(self.d_frame, text="  Run in Terminal:")
        self.terminal_lbl.grid(column=0, row=19, sticky="w")
        # 
        self.terminal_lbl2 = ttk.Label(self.d_frame, text="")
        self.terminal_lbl2.grid(column=1, row=19, sticky="w")
        # hidden
        self.hidden_lbl = ttk.Label(self.d_frame, text="  Hidden:")
        self.hidden_lbl.grid(column=0, row=20, sticky="w")
        #
        self.hidden_lbl2 = ttk.Label(self.d_frame, text="")
        self.hidden_lbl2.grid(column=1, row=20, sticky="w")
        # nodisplay
        self.nodisplay_lbl = ttk.Label(self.d_frame, text="  No Display:")
        self.nodisplay_lbl.grid(column=0, row=21, sticky="w")
        #
        self.nodisplay_lbl2 = ttk.Label(self.d_frame, text="")
        self.nodisplay_lbl2.grid(column=1, row=21, sticky="w")
        # 
        
        ### primo elemento in radice
        #id = self.tv.insert("", 0, text="primo", tags="uno")
        #print("id::", id)
        ### inserisco come figlio di sopra
        #id2 = self.tv.insert(id, 0, text="secondo")
        #print("id2::", id2)
        ## nuovo elemento in radice
        #
        ## immagine deve essere self
        #self.iimage = tk.PhotoImage(file="ag.png")
        #
        #self.tv.insert("", index=1, text="terzo", image=self.iimage, tags=("tag_terzo",))
        #
        # virtual event <<TreeviewSelect>> - elemento selezionato
        self.tv.bind("<<TreeviewSelect>>", self.ftv)
        #
        # freedesktop_main_categories
        # all_ext_cat
        # popolo treeview con le categorie principali
        self.id_list = []
        # aggiungo categoria dei dispersi
        id = self.tv.insert("", 0, text="Missed", tags=("Missed","C"))
        self.id_list.append(id) #([id,ccat])
        self.id_list.append("Missed")
        # categorie principali
        for ccat in reversed(freedesktop_main_categories):
            id = self.tv.insert("", 0, text=ccat, tags=(ccat,"C"))
            self.id_list.append(id) #([id,ccat])
            self.id_list.append(ccat)
        #
        # con ([id,ccat]) ottengo: [['I002', 'Utility'], ['I003', 'System'], ['I004', 'Settings'], ['I005', 'Office'], ['I006', 'Network'], ['I007', 'Graphics'], ['I008', 'Game'], ['I009', 'Education'], ['I00A', 'Development'], ['I00B', 'AudioVideo']]
        #print("self.id_list::", self.id_list)
        # popolo treeview
        self.fpop_treeview()
    
    
    #### POPOLO TREEVIEW 
    def fpop_treeview(self):
        #### POPOLO TREEVIEW 
        #
        for item in  self.info_desktop:
            print("* item::", item.name, item.categories)
            #
            ret = 0
            # categoria principale - prima passata
            ret = self.item_in_main(item)
            print("ret main::", ret)
            # direttamente categoria principale
            if ret:
                #pass
                # lo inserisco come figlio
                # trovo id della categoria
                idx_cat = self.id_list.index(ret)
                # id della categoria trovata
                idx = self.id_list[idx_cat-1]
                self.tv.insert(idx, 0, text=item.name, tags=(item.path,"E"))
            else:
                # direttamente categoria principale - seconda passata
                #print("NO MAIN")
                ret = self.item_in_main2(item)
                print("ret main2::", ret)
                #
                if ret:
                    #pass
                    # lo inserisco come figlio
                    # trovo id della categoria
                    idx_cat = self.id_list.index(ret)
                    # id della categoria trovata
                    idx = self.id_list[idx_cat-1]
                    self.tv.insert(idx, 0, text=item.name, tags=(item.path,"E"))
                else:
                    # indirettamene categoria principale
                    #print("NO MAIN 2")
                    ret = self.item_in_ext(item)
                    #print("ret ext::", ret)
                    if ret:
                        # lo inserisco come figlio
                        # trovo id della categoria
                        idx_cat = self.id_list.index(ret)
                        # id della categoria trovata
                        idx = self.id_list[idx_cat-1]
                        self.tv.insert(idx, 0, text=item.name, tags=(item.path,"E"))
                    else:
                        # categoria Missed
                        # lo inserisco come figlio
                        # trovo id della categoria
                        idx_cat = self.id_list.index("Missed")
                        # id della categoria trovata
                        idx = self.id_list[idx_cat-1]
                        self.tv.insert(idx, 0, text=item.name, tags=(item.path,"E"))
    
    # commuta da user a system
    def fswitch(self):
        print("fswitch")
        # azzero dei widgets
        # il primo per la parte entry 
        self.categories_cb2.set("")
        # il secondo per la parte listbox widget
        self.categories_cb2.configure(values="")
        self.keywords_cb2.set("")
        self.keywords_cb2.configure(values="")
        self.mime_cb2.set("")
        self.mime_cb2.configure(values="")
        # anche la icona
        self.iimage = tk.PhotoImage(file="ag.png")
        self.image_lbl.configure(image=self.iimage)
        # anche i label
        self.pname_lbl.configure(text="")
        self.generic_name_lbl.configure(text="")
        self.comment_lbl.configure(text="")
        self.exec_lbl2.configure(text="")
        self.tryexec_lbl2.configure(text="")
        self.url_lbl2.configure(text="")
        self.terminal_lbl2.configure(text="")
        self.hidden_lbl2.configure(text="")
        self.nodisplay_lbl2.configure(text="")
        #
        # svuoto self.tv
        # per ogni entry
        for id in self.tv.get_children():
            #self.tv.delete(id)
            #print(id)
            ##print(self.tv.item(id))
            #print(self.tv.get_children(id))
            # per ogni children in entry
            for idd in self.tv.get_children(id):
                # cancello i children
                self.tv.delete(idd)
        #
        # setto il nuovo heading
        # instestazione della colonna - anche per cambiarla in seguito
        # stampo l attuale intestazione
        #print("HEADING::", self.tv.heading("#0", option="text"))
        # da User a System e viceversa
        if self.tv.heading("#0", option="text") == "User":
            # testo pulsante 1
            #self.btn1.configure(text="System")
            #
            self.tv.heading("#0", text="System")
            # ripopolo self.info_desktop
            self.fpop(app_dirs_system)
        else:
            # testo pulsante 1
            #self.btn1.configure(text="User")
            #
            self.tv.heading("#0", text="User")
            # ripopolo self.info_desktop
            self.fpop(app_dirs_user)
        # ripopolo treeview
        self.fpop_treeview()
    
    ######
    def fpop(self, ap_dir):
        #print("PPPPPPPP::", ap_dir)
        # ottengo la lista dei file desktop
        self.file_list = self.list_app(ap_dir)
        #
        # svuoto lista per ogni elemento file desktop
        self.info_desktop = []
        # popolo la lista - funzione
        self.pop_info_desktop()
        # stampo il contenuto della lista - OK
        #print("self.info_desktop::", self.info_desktop[0].category)
    
    ## elenca i file desktop in app_dirs
    ## popola self.file_list
    #def list_app22(self):
    #    # lista di tutti i file desktop trovati
    #    file_lista = []
    #    for ddir in app_dirs:
    #        file_lista += glob.glob(ddir+"/*.desktop")
    #    #print("file_list::", file_lista)
    #    return file_lista
    
    # elenca i file desktop in app_dirs
    # popola self.file_list
    def list_app(self, llist):
        # lista di tutti i file desktop trovati
        file_lista = []
        for ddir in llist:
            file_lista += glob.glob(ddir+"/*.desktop")
        #print("file_list::", file_lista)
        return file_lista
    
    # popolo la lista self.info_desktop
    def pop_info_desktop(self):
        # per ogni file in self.file_list popolo self.info_desktop
        for ffile in self.file_list:
            print("File::", ffile)
            #
            # controlla anche che sia un file desktop valido
            try:
                entry = DesktopEntry.DesktopEntry(ffile)
                fname = entry.getName()
                fcategory = entry.getCategories()
                ftype = entry.getType()

                # creo elemento della lista self.info_desktop
                # se esistono entrambi
                if ftype == "Application" and fcategory != "":
                    dentry = catDesktop()
                    dentry.name = fname
                    dentry.categories = fcategory
                    dentry.path = ffile
                    # aggiungo dentry alla lista
                    #print("dentry::", dentry)
                    self.info_desktop.append(dentry)
            except Exception as E:
                #pass
                print("Exdception::", str(E))
    
#############################

    # se categoria principale - prima passata
    def item_in_main(self, item):
        # check if the first entry is in main list
        try:
            if item.categories[0] in freedesktop_main_categories:
                #print("1: ITEM", item.name, "IN MAIN", item.categories[0])
                #
                return item.categories[0]
        except:
            return 0
        else:
            return 0
    
    # categoria principale - seconda passata
    def item_in_main2(self, item):
        # iitem is ogni categoria delle categorie della entry desktop iitem
        try:
            for iitem in item.categories:
                #print("AAAAAAAA:::", iitem, item.categories)
                # se in categoria principale
                if iitem in freedesktop_main_categories:
                    #print("2: ITEM", item.name, "IN MAIN:", iitem)
                    return iitem
                #else:
                    #return 0
                    #continue
            return 0
        except:
            return 0
    
    # categoria estesa - terza passata
    def item_in_ext(self, item):
        # all_extended_list is named tuple
        # ccat is la singola named tuple
        try:
            for ccat in all_extend_list:
                #print("TTT::", "Audio" in ccat.list)
                # 
                # iitem is ogni categoria delle categorie della entry desktop iitem
                for iitem in item.categories:
                    #print("3::", iitem, ccat.list)
                    if iitem in ccat.list:
                        #print("3: ITEM", item.name, "IN SUBMAIN:", ccat.main)
                        return ccat.main
            #
            return 0
        except:
            return 0
        
##########################
    
    # quando seleziono un elemento in treeview
    def ftv(self, event):
        #print("TV::", event)
        #
        # azzero dei widgets
        self.categories_cb2.set("")
        self.categories_cb2.configure(values="")
        self.keywords_cb2.set("")
        self.keywords_cb2.configure(values="")
        self.mime_cb2.set("")
        self.mime_cb2.configure(values="")
        # anche la icona
        self.iimage = tk.PhotoImage(file="ag.png")
        self.image_lbl.configure(image=self.iimage)
        # anche i label
        self.pname_lbl.configure(text="")
        self.generic_name_lbl.configure(text="")
        self.comment_lbl.configure(text="")
        self.exec_lbl2.configure(text="")
        self.tryexec_lbl2.configure(text="")
        self.url_lbl2.configure(text="")
        self.terminal_lbl2.configure(text="")
        self.hidden_lbl2.configure(text="")
        self.nodisplay_lbl2.configure(text="")
        #
        item = self.tv.selection()[0]
        # disponibili {'text': 'secondo', 'image': '', 'values': '', 'open': 0, 'tags': ''}
        print("you clicked on::", self.tv.item(item,"tags"))#[0])
        # ottengo i tags
        item_tags = self.tv.item(item,"tags")
        # E per file - C per categoria
        if item_tags[1] == 'E':
            # self.name_lbl2
            entry = DesktopEntry.DesktopEntry(item_tags[0])
            #print("Selected::", entry.getName())
            # name
            self.pname_lbl.configure(text=entry.getName())
            # generic name
            self.generic_name_lbl.configure(text=entry.getGenericName())
            # comment
            self.comment_lbl.configure(text=entry.getComment())
            # image
            # IconTheme.getIconPath("system-lock-screen")
            img = entry.getIcon()
            #print("IMG::", img)
            # ottengo il path dell icona usata - png - hicolor theme
            img_path = IconTheme.getIconPath(img)
            #img_path = "/usr/share/icons/Papirus/48x48/apps/"+img
            try:
                if img_path:
                    self.iimage = tk.PhotoImage(file=img_path)
                else:
                    self.iimage = tk.PhotoImage(file="ag.png")
            except:
                self.iimage = tk.PhotoImage(file="ag.png")
            self.image_lbl.configure(image=self.iimage)
            # command
            self.exec_lbl2.configure(text=entry.getExec())
            # tryexec
            self.tryexec_lbl2.configure(text=entry.getTryExec())
            # categories
            #self.categories_lbl2.configure(text=entry.getCategories())
            self.categories_cb2.configure(values=entry.getCategories())
            try:
                self.categories_cb2.current(0)
            except:
                pass
            # mimetypes
            #self.mime_lbl2.configure(text=entry.getMimeTypes())
            self.mime_cb2.configure(values=entry.getMimeTypes())
            try:
                self.mime_cb2.current(0)
            except:
                pass
            # keywords
            self.keywords_cb2.configure(values=self.ffind_action(item_tags[0], "Keywords"))
            try:
                self.keywords_cb2.current(0)
            except:
                pass
            # URL
            self.url_lbl2.configure(text=entry.getURL())
            ##### options
            # terminal
            self.terminal_lbl2.configure(text=self.fbool(entry.getTerminal()))
            # hidden
            self.hidden_lbl2.configure(text=self.fbool(entry.getHidden()))
            # nodisplay
            self.nodisplay_lbl2.configure(text=self.fbool(entry.getNoDisplay()))
            
        # funzione che riordina - vedo sotto
        #self.tv.heading("#0", text="#0", command=lambda c="#0": treeview_sort_column(self.tv, c, False))
    
    # vedo sopra
    def treeview_sort_column(self, col, reverse):
        tv = self.tv
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(key=lambda t: int(t[0]), reverse=reverse)
        #      ^^^^^^^^^^^^^^^^^^^^^^^

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
    
    # find an action in the desktop file
    def ffind_action(self, ffile, aaction):
        kws = []
        with open(ffile, 'r') as f:
            for line in f:
                if aaction+"=" in line:
                    #print("Keywords::", line)
                    kws = line.split("=")[1].split(";")[:-1]
                    #print("kws::", kws)
        return kws
    
    
    # da bool a yes/no
    def fbool(self, n):
        if n:
            return "Yes"
        else:
            return "No"
        
    
###########
def main():
    root = tk.Tk()
    root.title("Menu editor")
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    width = app_width
    height = app_height
    root.geometry('{}x{}'.format(width, height))
    
    # style
    s = ttk.Style()
    # uno tra: clam alt default classic
    s.theme_use("clam")
    
    app = Application(master=root)
    app.mainloop()
    
if __name__ == "__main__":
    main()

""" NAMED TUPLE
>>> import collections
>>> persona = collections.namedtuple("list", 'main lista')
>>> tizio = persona("utility", [11,22])
>>> caio = persona("graphics", [33,44])
>>> sempronio = persona("office", [55,66])
>>> caio
list(main='graphics', lista=[33, 44])
>>> all_lista = [tizio, caio, sempronio]
>>> for item in all_lista:
...     print(item.main)
... 
utility
graphics
office
>>> for item in all_lista:
...   if 33 in item.lista:
...     print(item.main)
...   else:
...     print("non valido:", item)
... 
non valido: list(main='utility', lista=[11, 22])
graphics
non valido: list(main='office', lista=[55, 66])

#################
# popolo la lista self.info_desktop
    def pop_info_desktop2(self):
        # per ogni file in self.file_list popolo self.info_desktop
        for ffile in self.file_list:
            #print("File::", ffile)
            with open(ffile, 'r') as f:
                for line in f:
                    if "Type=" in line:
                        if not "MimeType=" in line:
                            #print("Type::", line.split("=")[1].strip())
                            ftype = line.split("=")[1].strip("\n")
                    elif "Categories=" in line:
                        #print("Category::", line.split("=")[1].strip())
                        # [:-1] per rimuovere la entry vuota ''
                        fcategory = line.split("=")[1].strip("\n").split(";")[:-1]
                    elif "Name=" in line:
                        fname = line.split("=")[1].strip("\n")
            # creo elemento della lista self.info_desktop
            # se esistono entrambi
            if ftype == "Application" and fcategory != "":
                dentry = catDesktop()
                dentry.name = fname
                dentry.categories = fcategory
                dentry.path = ffile
                # aggiungo dentry alla lista
                #print("dentry::", dentry)
                self.info_desktop.append(dentry)
        
##################
    # funzione fasulla
    def aaa(self):
        # per ogni elemento desktop
        for iitem in self.info_desktop:
            print("* iitem::", iitem.name, iitem.categories)
            #self.tv.insert("", 0, text=iitem.name, tags=iitem.path)
            # check if the first entry is in main list
            if iitem.categories[0] in freedesktop_main_categories:
                print("1: ITEM", iitem.categories[0], "IN MAIN:", iitem.categories[0])
                # lo inserisco come figlio
                # trovo id della categoria
                idx_cat = self.id_list.index(iitem.categories[0])
                # id della categoria trovata
                idx = self.id_list[idx_cat-1]
                self.tv.insert(idx, 0, text=iitem.name, tags=(iitem.path,"E"))
                # continuo col prossimo 
                continue
            # altrimenti ciclo su tutti
            else:
                # item is ogni categoria delle categorie della entry desktop iitem
                for item in iitem.categories:
                    # se in categoria principale
                    if item in freedesktop_main_categories:
                        print("2: ITEM", item, "IN MAIN:", item)
                        # lo inserisco come figlio
                        # trovo id della categoria
                        idx_cat = self.id_list.index(item)
                        print(idx_cat)
                        # id della categoria trovata
                        idx = self.id_list[idx_cat-1]
                        self.tv.insert(idx, 0, text=iitem.name, tags=(iitem.path,"E"))
                        # interrompo
                        break
                    # cerco di trovare la categoria main da una sottocategoria
                    else:
                        ret = self.faa(item)
                        #print("ret::", ret)
                        ## all_extended_list is named tuple
                        ## ccat is la singola named tuple
                        #for ccat in all_extend_list:
                        #    #print("ccat3::", ccat)
                        #    # item is categoria della lista freedesktop_main_categories
                        #    if item in ccat.list:
                        #        print("3: ITEM", item, "IN SUBMAIN:", ccat.main)
                        #        # dopo il primo interrompo
                        #        break
                        #        #continue
                        #    #else:
                        #    elif item not in ccat.list:
                        #        print("Missed::", iitem.name, item)
                        #        #break
                        #        continue
#####################

#
    def faa(self, item):
        print("faa::", item)
        # all_extended_list is named tuple
        # ccat is la singola named tuple
        for ccat in all_extend_list:
            #print("ccat3::", ccat)
            # item is categoria della lista freedesktop_main_categories
            if item in ccat.list:
                print("3: ITEM", item, "IN SUBMAIN:", ccat.main)
                return ccat.main
                # dopo il primo interrompo
                #break
        #        #continue
            else:
        #    elif item not in ccat.list:
                print("Missed::", item)
                return "00"
        #        #break
        #        continue
#####################


"""