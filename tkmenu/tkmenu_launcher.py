#!/usr/bin/env python3

"""
 by frank38
 V. 0.7
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
import os
import sys
import shutil
from xdg import DesktopEntry
from xdg import IconTheme
#from tkinter.filedialog import askopenfilename, askdirectory
from tkfilebrowser import askopendirname, askopenfilename
from tkinter import messagebox

# if a filename is passed to the program
dfilename = ""
if len(sys.argv) > 1:
    # 0 new - 1 modify
    ccode = sys.argv[1]
    dfilename = sys.argv[2]

# font size
font_size = 20

# window width and height
app_width = 1200
app_height = 950

# desktop file directories
app_dirs_user = [os.environ.get("XDG_DATA_HOME")+"/applications"]

# the dir of this script
this_dir = os.path.dirname(os.path.realpath(__file__))

#######################
# main categories
freedesktop_main_categories = ["AudioVideo","Development",
                              "Education","Game","Graphics","Network",
                              "Office","Settings","System","Utility"]

class MyDialog:
    
    def __init__(self, parent):
        
        self.top = tk.Toplevel(parent)
        self.lbl = ttk.Label(self.top, text="Filename:")
        self.lbl.pack()
        
        self.e_var = tk.StringVar()
        self.e = ttk.Entry(self.top, textvariable=self.e_var)
        self.e.pack(padx=5)
        # if a filename is passed as argument
        if dfilename != "":
            self.e_var.set(os.path.basename(dfilename).split('.')[0])

        b = ttk.Button(self.top, text="OK", command=self.ok)
        b.pack()
        
        cancel = ttk.Button(self.top, text="Cancel", command=self.cancel)
        cancel.pack()

    def ok(self):
        # the filename to pass
        self.filename = self.e.get() or "-1"
        # check if the filename is busy
        if os.path.exists(app_dirs_user[0]+"/"+self.filename+".desktop"):
            self.lbl.configure(text="Choose another name:")
        else:
            self.top.destroy()

    def cancel(self):
        self.filename = "-1"
        self.top.destroy()
            
class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.master.update_idletasks()
        
        # treeview: row height
        ffont = font.Font(family='', size=font_size)
        
        self.create_widgets()
        
    def create_widgets(self):
        # font family and size
        self.s = ttk.Style(self.master)
        self.s.configure('.', font=('', font_size))
        ########## GUI
        bigfont = font.Font(family="",size=font_size)
        self.master.option_add('*Font', bigfont)
        # name
        self.lcr_name_lbl = ttk.Label(self, text="Name").grid(column=0, row=5, sticky="sw")
        self.name_ent_var = tk.StringVar()
        self.lcr_name_ent = ttk.Entry(self, textvariable=self.name_ent_var, width=50).grid(column=0, row=6, sticky="w")
        # generic name
        self.lcr_genericname_lbl = ttk.Label(self, text="Generic Name (optional)").grid(column=0, row=7, sticky="sw")
        self.genericname_ent_var = tk.StringVar()
        self.lcr_genericname_ent = ttk.Entry(self, textvariable=self.genericname_ent_var, width=50).grid(column=0, row=8, sticky="w")
        # executable
        self.lcr_exec_lbl = ttk.Label(self, text="Executable").grid(column=0, row=9, sticky="sw")
        self.exec_ent_var = tk.StringVar()
        self.lcr_exec_ent = ttk.Entry(self, textvariable=self.exec_ent_var, width=50).grid(column=0, row=10, sticky="w")
        self.lcr_btn_exec = ttk.Button(self, text="Choose", command=self.fgetExec).grid(column=1, row=10, sticky="w")
        # tryexec
        self.lcr_tryexec_lbl = ttk.Label(self, text="TryExec (optional)").grid(column=0, row=11, sticky="sw")
        self.tryexec_ent_var = tk.StringVar()
        self.lcr_tryexec_ent = ttk.Entry(self, textvariable=self.tryexec_ent_var, width=50).grid(column=0, row=12, sticky="w")
        self.lcr_btn_tryexec = ttk.Button(self, text="Choose", command=self.fgetTryExec).grid(column=1, row=12, sticky="w")
        # path
        self.lcr_dir_lbl = ttk.Label(self, text="Path (optional)").grid(column=0, row=13, sticky="sw")
        self.dir_ent_var = tk.StringVar()
        self.lcr_dir_ent = ttk.Entry(self, textvariable=self.dir_ent_var, width=50).grid(column=0, row=14, sticky="w")
        self.lcr_btn_dir = ttk.Button(self, text="Choose", command=self.fgetDir).grid(column=1, row=14, sticky="w")
        # category
        self.lcr_category_lbl = ttk.Label(self, text="Category ")
        self.lcr_category_lbl.grid(column=0, row=15, sticky="sw")
        self.category_var = tk.StringVar()
        self.lcr_category_cb = ttk.Combobox(self, textvariable=self.category_var, values=freedesktop_main_categories, width=50)
        self.lcr_category_cb.grid(column=0, row=16, sticky="w")
        self.lcr_category_cb.current(0)
        # mimetypes
        self.lcr_keys_lbl = ttk.Label(self, text="Mimetypes (optional - separate with a semicolon)").grid(column=0, row=17, sticky="sw")
        self.mime_var = tk.StringVar()
        self.lcr_keys_ent = ttk.Entry(self, textvariable=self.mime_var, width=50).grid(column=0, row=18, sticky="w")
        # keywords
        self.lcr_keys_lbl = ttk.Label(self, text="Keywords (optional - separate with a semicolon)").grid(column=0, row=19, sticky="sw")
        self.keys_var = tk.StringVar()
        self.lcr_keys_ent = ttk.Entry(self, textvariable=self.keys_var, width=50).grid(column=0, row=20, sticky="w")
        # icon
        self.lcr_icon_lbl = ttk.Label(self, text="Icon").grid(column=0, row=21, sticky="sw")
        self.icon_var = tk.StringVar()
        self.lcr_icon_ent = ttk.Entry(self, textvariable=self.icon_var, width=50).grid(column=0, row=22, sticky="w")
        self.lcr_btn_icon = ttk.Button(self, text="Choose", command=self.fgetIcon).grid(column=1, row=22, sticky="w")
        # comment
        self.lcr_comment_lbl = ttk.Label(self, text="Comment (optional)").grid(column=0, row=23, sticky="sw")
        self.comment_var = tk.StringVar()
        self.lcr_comment_ent = ttk.Entry(self, textvariable=self.comment_var, width=50).grid(column=0, row=24, sticky="w")
        ### frame
        self.terminal_frame = ttk.Frame(self)
        self.terminal_frame.grid(column=0, row=25, columnspan=2, sticky="sw")
        # run in terminal
        self.terminal_var = tk.IntVar()
        self.lcr_terminal_chk = ttk.Checkbutton(self.terminal_frame, text="\n    Run in terminal    \n", variable=self.terminal_var, offvalue=0, onvalue=1).grid(column=0, row=0, sticky="sw")
        self.terminal_var.set(0)
        # no display
        self.nodisplay_var = tk.IntVar()
        self.lcr_nodisplay_chk = ttk.Checkbutton(self.terminal_frame, text="\n    No Display    \n", variable=self.nodisplay_var, offvalue=0, onvalue=1).grid(column=1, row=0, sticky="sw")
        self.nodisplay_var.set(0)
        # hidden
        self.hidden_var = tk.IntVar()
        self.lcr_hidden_chk = ttk.Checkbutton(self.terminal_frame, text="\n    Hidden    \n", variable=self.hidden_var, offvalue=0, onvalue=1).grid(column=2, row=0, sticky="sw")
        self.hidden_var.set(0)
        ####
        # save button
        self.save_button = ttk.Button(self, text="Save", command=self.fsave).grid(column=0, row=26, sticky="w")
        # quit button
        quit_btn = ttk.Button(self, text="Exit", command=quit).grid(column=1, row=26, sticky="e")
        # if a file desktop is passed to the program all the stuff are filled
        if dfilename != "":
            self.ffill()
    
    # fill all the entries
    def ffill(self):
        try:
            de = DesktopEntry.DesktopEntry(filename=dfilename)
        except Exception as E:
            messagebox.showerror("No", "Error with the file:\n" + str(E))
            return
        # check the consistency of the file
        try:
            de.parse(dfilename)
        except Exception as E:
            messagebox.showerror("No", "Error with the file:\n" + str(E))
            return
        #
        # name
        dname = de.getName()
        self.name_ent_var.set(dname)
        # generic name
        dgenericname = de.getGenericName()
        self.genericname_ent_var.set(dgenericname)
        # executable
        dexec = de.getExec()
        self.exec_ent_var.set(dexec)
        # tryexec
        dtryexec = de.getTryExec()
        self.tryexec_ent_var.set(dtryexec)
        # path
        dpath = de.getPath()
        self.dir_ent_var.set(dpath)
        # category - main only
        dcategories_temp = de.getCategories()
        for ccat in dcategories_temp:
            if ccat in freedesktop_main_categories:
                self.category_var.set(ccat)
                break
        # mimetypes
        dmime = de.getMimeTypes()
        self.mime_var.set(dmime)
        # keywords
        dkeywords = de.getKeywords()
        self.keys_var.set(dkeywords)
        # icon
        dicon = de.getIcon()
        self.icon_var.set(dicon)
        # comment
        dcomment = de.getComment()
        self.comment_var.set(dcomment)
        # run in terminal
        dterminal = de.getTerminal()
        self.terminal_var.set(dterminal)
        # no display
        dnodisplay = de.getNoDisplay()
        self.nodisplay_var.set(dnodisplay)
        # hidden
        dhidden = de.getHidden()
        self.hidden_var.set(dhidden)
    
    # save the file
    def fsave(self):
        # getting all the stuff
        # name
        dname = self.name_ent_var.get()
        # if empty
        if dname == "":
            messagebox.showerror("No", "Error: \nThe name is mandatory.")
            return
        # generic name
        dgenericname = self.genericname_ent_var.get()
        # executable
        dexec = self.exec_ent_var.get()
        # if empty
        if dexec == "":
            messagebox.showerror("No", "Error: \nThe executable is mandatory.")
            return
        # tryexec
        dtryexec = self.tryexec_ent_var.get()
        # path
        dpath = self.dir_ent_var.get()
        # category
        dcategories = self.category_var.get()
        dcategories += ';'
        # mimetypes
        dmime = self.mime_var.get()
        if dmime != "":
            if dmime[-1] != ';':
                dmime += ';'
        # keywords
        dkeywords = self.keys_var.get()
        if dkeywords != "":
            if dkeywords[-1] != ';' and dkeywords != "":
                dkeywords += ';'
        # icon
        dicon = self.icon_var.get()
        # comment
        dcomment = self.comment_var.get()
        # run in terminal
        dterminal_temp = self.terminal_var.get()
        if dterminal_temp == 0:
            dterminal = "false"
        else:
            dterminal = "true"
        # no display
        dnodisplay_temp = self.nodisplay_var.get()
        if dnodisplay_temp == 0:
            dnodisplay = "false"
        else:
            dnodisplay = "true"
        # hidden
        dhidden_temp = self.terminal_var.get()
        if dhidden_temp == 0:
            dhidden = "false"
        else:
            dhidden = "true"
        ######### creating and saving the desktop file
        pfilename = ""
        # new desktop file
        if ccode == "0":
            # getting the filename
            d = MyDialog(self.master)
            self.master.wait_window(d.top)
            if d.filename == "-1":
                return
            else:
                pfilename = d.filename+".desktop"
        ## modify the loaded desktop file
        elif ccode == "1":
            pfilename = os.path.basename(dfilename)
        #
        de = DesktopEntry.DesktopEntry()
        # file name
        de.new(filename=pfilename)
        # setting the actions
        de.set("Version", "1.0")
        de.set("Type", "Application")
        de.set("Name", dname)
        de.set("GenericName", dgenericname)
        de.set("Exec", dexec)
        de.set("TryExec", dtryexec)
        de.set("Path", dpath)
        de.set("Categories", dcategories)
        de.set("MimeType", dmime)
        de.set("Keywords", dkeywords)
        de.set("Icon", dicon)
        de.set("Comment", dcomment)
        de.set("Terminal", dterminal)
        de.set("NoDisplay", dnodisplay)
        de.set("Hidden", dhidden)
        #
        # to user defaul directory
        try:
            # to user defaul directory
            os.chdir(app_dirs_user[0])
            #  write the file
            de.write()
            # to the script directory
            os.chdir(this_dir)
        except Exception as E:
            messagebox.showerror("No", "Error: \n"+str(E))
        
    
    # get and set the executable chosen
    def fgetExec(self):
        filename = askopenfilename(parent=self.master, 
                           initialdir='/', 
                           initialfile='tmp',
                           filetypes=[("All files", "*")],
                           font_size=font_size)
        # if it is in path or not
        if shutil.which(os.path.basename(filename)):
            self.exec_ent_var.set(os.path.basename(filename))
        else:
            self.exec_ent_var.set(filename)
    
    # get and set the executable chosen
    def fgetTryExec(self):
        filename = askopenfilename(parent=self.master, 
                           initialdir='/', 
                           initialfile='tmp',
                           filetypes=[("All files", "*")],
                           font_size=font_size)
        # if it is in path or not
        if shutil.which(os.path.basename(filename)):
            self.tryexec_ent_var.set(os.path.basename(filename))
        else:
            self.tryexec_ent_var.set(filename)
    
    # get the path
    def fgetDir(self):
        dirname = askopendirname(parent=self.master, 
                         initialdir='/', 
                         initialfile='tmp', font_size=font_size)
        self.dir_ent_var.set(dirname)
    
    # get the icon
    def fgetIcon(self):
        filename = askopenfilename(parent=self.master, 
                           initialdir='/', 
                           initialfile='tmp',
                           filetypes=[("All files", "*")],
                           font_size=font_size)
        self.icon_var.set(filename)
        
###########
def main():
    root = tk.Tk()
    root.title("Editor")
    root.update_idletasks()
    
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
