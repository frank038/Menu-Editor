#!/usr/bin/env python3

"""
 by frank38
 V. 0.0.1
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
import os
import glob
import collections
from xdg import DesktopEntry
from xdg import IconTheme

# font size
font_size = 20

# window width and height
app_width = 1200
app_height = 900

app_dirs_user = [os.environ.get("XDG_DATA_HOME")+"/applications"]
app_dirs_system = ["/usr/share/applications"]

#######################
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

all_extend_list = [development_ext,office_ext,graphics_ext,utility_ext,
                  settings_ext,network_ext,audiovideo_ext,game_ext,
                  education_ext,system_ext]

###############

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
        
        ffont = font.Font(family='', size=font_size)
        self.tv_row_height = ffont.metrics("linespace")
        
        self.create_widgets()
        
    def create_widgets(self):
        # font family and size
        self.s = ttk.Style(self.master)
        self.s.configure('.', font=('', font_size))
        ###
        ###############
        self.info_desktop = []
        self.file_list = []
        self.fpop(app_dirs_user)
        ##############
        #
        ############### creo la struttura grafica
        #### buttons
        self.frame_btn = ttk.Frame(self, width=app_width)
        self.frame_btn.grid(column=0, row=0, columnspan=10)
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
        self.tv.pack(side="left", fill="y", expand=True)
        self.tv.column("#0", width=350)
        self.tv.heading("#0", text="User")
        self.s.configure('Treeview', rowheight=self.tv_row_height+2)
        #
        # scrollbar 
        self.vscrollbar = ttk.Scrollbar(self.tv_frame, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=self.vscrollbar.set)
        self.vscrollbar.pack(fill="y", expand=True)
        #
        ### 
        bold_style = ttk.Style ()
        bold_style.configure("Bold.TLabel", font=("", font_size, "bold"))
        italic_style = ttk.Style()
        italic_style.configure("Italic.TLabel", font=("", font_size, "italic"))
        #
        bigfont = font.Font(family="",size=font_size)
        self.master.option_add("*TCombobox*Font", bigfont)
        ## frame
        self.d_frame = ttk.Frame(self)
        self.d_frame.grid(column=1, row=4, rowspan=20)
        self.iimage = tk.PhotoImage(file="ag.png")
        self.image_lbl = ttk.Label(self.d_frame, text="", image=self.iimage)
        self.image_lbl.grid(column=0, row=4, rowspan=3)
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
        self.categories_cb2 = ttk.Combobox(self.d_frame)
        self.categories_cb2.grid(column=1, row=10, sticky="w")
        # mimetypes
        self.mime_lbl = ttk.Label(self.d_frame, text="  Mime Types: ")
        self.mime_lbl.grid(column=0, row=11, sticky="w")
        #
        self.mime_lbl2 = ttk.Label(self.d_frame, text="", width=30, wraplength=300)
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
        self.tv.bind("<<TreeviewSelect>>", self.ftv)
        #
        self.id_list = []
        #
        id = self.tv.insert("", 0, text="Missed", tags=("Missed","C"))
        self.id_list.append(id) #([id,ccat])
        self.id_list.append("Missed")
        #
        for ccat in reversed(freedesktop_main_categories):
            id = self.tv.insert("", 0, text=ccat, tags=(ccat,"C"))
            self.id_list.append(id)
            self.id_list.append(ccat)
        #
        self.fpop_treeview()
    
    
    def fpop_treeview(self):
        #
        for item in  self.info_desktop:
            print("* item::", item.name, item.categories)
            #
            ret = 0
            ret = self.item_in_main(item)
            if ret:
                idx_cat = self.id_list.index(ret)
                idx = self.id_list[idx_cat-1]
                self.tv.insert(idx, 0, text=item.name, tags=(item.path,"E"))
            else:
                ret = self.item_in_main2(item)
                #
                if ret:
                    idx_cat = self.id_list.index(ret)
                    idx = self.id_list[idx_cat-1]
                    self.tv.insert(idx, 0, text=item.name, tags=(item.path,"E"))
                else:
                    ret = self.item_in_ext(item)
                    if ret:
                        idx_cat = self.id_list.index(ret)
                        idx = self.id_list[idx_cat-1]
                        self.tv.insert(idx, 0, text=item.name, tags=(item.path,"E"))
                    else:
                        idx_cat = self.id_list.index("Missed")
                        idx = self.id_list[idx_cat-1]
                        self.tv.insert(idx, 0, text=item.name, tags=(item.path,"E"))
    
    def fswitch(self): 
        self.categories_cb2.set("")
        self.categories_cb2.configure(values="")
        self.keywords_cb2.set("")
        self.keywords_cb2.configure(values="")
        self.mime_cb2.set("")
        self.mime_cb2.configure(values="")
        self.iimage = tk.PhotoImage(file="ag.png")
        self.image_lbl.configure(image=self.iimage)
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
        for id in self.tv.get_children():
            for idd in self.tv.get_children(id):
                self.tv.delete(idd)
        #
        if self.tv.heading("#0", option="text") == "User":
            self.tv.heading("#0", text="System")
            self.fpop(app_dirs_system)
        else:
            self.tv.heading("#0", text="User")
            self.fpop(app_dirs_user)
        self.fpop_treeview()
    
    ######
    def fpop(self, ap_dir):
        self.file_list = self.list_app(ap_dir)
        self.info_desktop = []
        self.pop_info_desktop()
    
    
    def list_app(self, llist):
        file_lista = []
        for ddir in llist:
            file_lista += glob.glob(ddir+"/*.desktop")
        return file_lista
    
    def pop_info_desktop(self):
        for ffile in self.file_list:
            try:
                entry = DesktopEntry.DesktopEntry(ffile)
                fname = entry.getName()
                fcategory = entry.getCategories()
                ftype = entry.getType()
                
                if ftype == "Application" and fcategory != "":
                    dentry = catDesktop()
                    dentry.name = fname
                    dentry.categories = fcategory
                    dentry.path = ffile
                    self.info_desktop.append(dentry)
            except Exception as E:
                pass
    
#############################

    def item_in_main(self, item):
        # check if the first entry is in main list
        try:
            if item.categories[0] in freedesktop_main_categories:
                #
                return item.categories[0]
        except:
            return 0
        else:
            return 0
    
    def item_in_main2(self, item):
        try:
            for iitem in item.categories:
                if iitem in freedesktop_main_categories:
                    return iitem
            return 0
        except:
            return 0
    
    def item_in_ext(self, item):
        try:
            for ccat in all_extend_list:
                # 
                for iitem in item.categories:
                    if iitem in ccat.list:
                        return ccat.main
            #
            return 0
        except:
            return 0
        
##########################
    
    def ftv(self, event):
        self.categories_cb2.set("")
        self.categories_cb2.configure(values="")
        self.keywords_cb2.set("")
        self.keywords_cb2.configure(values="")
        self.mime_cb2.set("")
        self.mime_cb2.configure(values="")
        self.iimage = tk.PhotoImage(file="ag.png")
        self.image_lbl.configure(image=self.iimage)
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
        item_tags = self.tv.item(item,"tags")
        #
        if item_tags[1] == 'E':
            entry = DesktopEntry.DesktopEntry(item_tags[0])
            # name
            self.pname_lbl.configure(text=entry.getName())
            # generic name
            self.generic_name_lbl.configure(text=entry.getGenericName())
            # comment
            self.comment_lbl.configure(text=entry.getComment())
            # image
            img = entry.getIcon()
            img_path = IconTheme.getIconPath(img)
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
            self.categories_cb2.configure(values=entry.getCategories())
            try:
                self.categories_cb2.current(0)
            except:
                pass
            # mimetypes
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
            

    # find an action in the desktop file
    def ffind_action(self, ffile, aaction):
        kws = []
        with open(ffile, 'r') as f:
            for line in f:
                if aaction+"=" in line:
                    kws = line.split("=")[1].split(";")[:-1]
        return kws
    
    
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
    s.theme_use("clam")
    
    app = Application(master=root)
    app.mainloop()
    
if __name__ == "__main__":
    main()

