#!/usr/bin/env python3

"""
 by frank38
 V. 0.8.2
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
import os
import sys
import shutil
from xdg import DesktopEntry
from xdg import IconTheme

from tkfilebrowser import askopendirname, askopenfilename
from tkinter import messagebox

ccode = sys.argv[1]
dfilename = sys.argv[2]
font_size = sys.argv[3]


# window width and height
app_width = 1200
app_height = 950

# desktop file directories
if os.environ.get("XDG_DATA_HOME") != None:
    app_dirs_user = [os.environ.get("XDG_DATA_HOME")+"/applications"]
else:
    app_dirs_user = [os.getenv("HOME")+"/.local/share/applications"]

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
        self.lcr_name_ent = ttk.Entry(self, width=50)
        self.lcr_name_ent.grid(column=0, row=6, sticky="w")
        # generic name
        self.lcr_genericname_lbl = ttk.Label(self, text="Generic Name (optional)").grid(column=0, row=7, sticky="sw")
        self.lcr_genericname_ent = ttk.Entry(self, width=50)
        self.lcr_genericname_ent.grid(column=0, row=8, sticky="w")
        # executable
        self.lcr_exec_lbl = ttk.Label(self, text="Executable").grid(column=0, row=9, sticky="sw")
        self.lcr_exec_ent = ttk.Entry(self, width=50)
        self.lcr_exec_ent.grid(column=0, row=10, sticky="w")
        self.lcr_btn_exec = ttk.Button(self, text="Choose", command=self.fgetExec).grid(column=1, row=10, sticky="w")
        # tryexec
        self.lcr_tryexec_lbl = ttk.Label(self, text="TryExec (optional)").grid(column=0, row=11, sticky="sw")
        self.lcr_tryexec_ent = ttk.Entry(self, width=50)
        self.lcr_tryexec_ent.grid(column=0, row=12, sticky="w")
        self.lcr_btn_tryexec = ttk.Button(self, text="Choose", command=self.fgetTryExec).grid(column=1, row=12, sticky="w")
        # path
        self.lcr_dir_lbl = ttk.Label(self, text="Path (optional)").grid(column=0, row=13, sticky="sw")
        self.lcr_dir_ent = ttk.Entry(self, width=50)
        self.lcr_dir_ent.grid(column=0, row=14, sticky="w")
        self.lcr_btn_dir = ttk.Button(self, text="Choose", command=self.fgetDir).grid(column=1, row=14, sticky="w")
        # category
        self.lcr_category_lbl = ttk.Label(self, text="Category ")
        self.lcr_category_lbl.grid(column=0, row=15, sticky="sw")
        self.lcr_category_cb = ttk.Combobox(self, values=freedesktop_main_categories, width=50)
        self.lcr_category_cb.grid(column=0, row=16, sticky="w")
        # mimetypes
        self.lcr_keys_lbl = ttk.Label(self, text="Mimetypes (optional - separate with a space)").grid(column=0, row=17, sticky="sw")
        self.lcr_keys_ent = ttk.Entry(self, width=50)
        self.lcr_keys_ent.grid(column=0, row=18, sticky="w")
        # keywords
        self.lcr_keys_lbl = ttk.Label(self, text="Keywords (optional - separate with a space)").grid(column=0, row=19, sticky="sw")
        self.lcr_keys_ent2 = ttk.Entry(self, width=50)
        self.lcr_keys_ent2.grid(column=0, row=20, sticky="w")
        # icon
        self.lcr_icon_lbl = ttk.Label(self, text="Icon").grid(column=0, row=21, sticky="sw")
        self.lcr_icon_ent = ttk.Entry(self, width=50)
        self.lcr_icon_ent.grid(column=0, row=22, sticky="w")
        self.lcr_btn_icon = ttk.Button(self, text="Choose", command=self.fgetIcon).grid(column=1, row=22, sticky="w")
        # comment
        self.lcr_comment_lbl = ttk.Label(self, text="Comment (optional)").grid(column=0, row=23, sticky="sw")
        self.lcr_comment_ent = ttk.Entry(self, width=50)
        self.lcr_comment_ent.grid(column=0, row=24, sticky="w")
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
        self.lcr_name_ent.insert(0,dname)
        # generic name
        dgenericname = de.getGenericName()
        self.lcr_genericname_ent.insert(0,dgenericname)
        # executable
        dexec = de.getExec()
        self.lcr_exec_ent.insert(0,dexec)
        # tryexec
        dtryexec = de.getTryExec()
        self.lcr_tryexec_ent.insert(0,dtryexec)
        # path
        dpath = de.getPath()
        self.lcr_dir_ent.insert(0,dpath)
        # category - main only
        dcategories_temp = de.getCategories()
        for ccat in dcategories_temp:
             if ccat in freedesktop_main_categories:
                cat_idx = freedesktop_main_categories.index(ccat)
                self.lcr_category_cb.current(cat_idx)
                break
        # mimetypes
        dmime = de.getMimeTypes()
        self.lcr_keys_ent.insert(0,dmime)
        # keywords
        dkeywords = de.getKeywords()
        self.lcr_keys_ent2.insert(0,dkeywords)
        # icon
        dicon = de.getIcon()
        self.lcr_icon_ent.insert(0,dicon)
        # comment
        dcomment = de.getComment()
        self.lcr_comment_ent.insert(0,dcomment)
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
        dname = self.lcr_name_ent.get()
        # if empty
        if dname == "":
            messagebox.showerror("No", "Error: \nThe name is mandatory.")
            return
        # generic name
        dgenericname = self.lcr_genericname_ent.get()
        # executable
        dexec = self.lcr_exec_ent.get()
        # if empty
        if dexec == "":
            messagebox.showerror("No", "Error: \nThe executable is mandatory.")
            return
        # tryexec
        dtryexec = self.lcr_tryexec_ent.get()
        # path
        dpath = self.lcr_dir_ent.get()
        # category
        dcategories = self.lcr_category_cb.get()
        dcategories += ';'
        # mimetypes
        dmime = self.lcr_keys_ent.get()
        if dmime != "":
            dmime = dmime.replace(" ", ";")
            if dmime[-1] != ';':
                dmime += ';'
        # keywords
        dkeywords = self.lcr_keys_ent2.get()
        if dkeywords != "":
            dkeywords = dkeywords.replace(" ", ";")
            if dkeywords[-1] != ';':
                dkeywords += ';'
        # icon
        dicon = self.lcr_icon_ent.get()
        # comment
        dcomment = self.lcr_comment_ent.get()
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
        dhidden_temp = self.hidden_var.get()
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
        de.set("Version", "1.0", 'Desktop Entry')
        de.set("Type", "Application", 'Desktop Entry')
        de.set("Name", dname)
        de.set("GenericName", dgenericname, 'Desktop Entry')
        de.set("Exec", dexec, 'Desktop Entry')
        de.set("TryExec", dtryexec, 'Desktop Entry')
        de.set("Path", dpath, 'Desktop Entry')
        de.set("Categories", dcategories, 'Desktop Entry')
        de.set("MimeType", dmime, 'Desktop Entry')
        de.set("Keywords", dkeywords, 'Desktop Entry')
        de.set("Icon", dicon, 'Desktop Entry')
        de.set("Comment", dcomment, 'Desktop Entry')
        de.set("Terminal", dterminal, 'Desktop Entry')
        de.set("NoDisplay", dnodisplay, 'Desktop Entry')
        de.set("Hidden", dhidden, 'Desktop Entry')
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
        if filename:
            self.lcr_exec_ent.delete(0, 'end')
            self.lcr_dir_ent.delete(0, 'end')
            # if it is in path or not
            if shutil.which(os.path.basename(filename)):
                self.lcr_exec_ent.insert(0, os.path.basename(filename))
            else:
                self.lcr_exec_ent.insert(0, filename)
                self.lcr_dir_ent.insert(0, os.path.dirname(filename))
            # #
            # self.exec_ent_var.set(os.path.basename(filename))
            # if os.path.dirname(filename):
                # if os.path.dirname(filename) not in os.getenv("PATH").split(":"):
                    # self.dir_ent_var.set(os.path.dirname(filename))
    
    # get and set the executable chosen
    def fgetTryExec(self):
        filename = askopenfilename(parent=self.master, 
                           initialdir='/', 
                           initialfile='tmp',
                           filetypes=[("All files", "*")],
                           font_size=font_size)
        if filename:
            self.lcr_tryexec_ent.delete(0, 'end')
            # if it is in path or not
            if shutil.which(os.path.basename(filename)):
                self.lcr_tryexec_ent.insert(0, os.path.basename(filename))
            else:
                self.lcr_tryexec_ent.insert(0, filename)
    
    # get the path
    def fgetDir(self):
        dirname = askopendirname(parent=self.master, 
                         initialdir='/', 
                         initialfile='tmp', font_size=font_size)
        if dirname:
            self.lcr_dir_ent.delete(0, 'end')
            self.lcr_dir_ent.insert(0, dirname)
    
    # get the icon
    def fgetIcon(self):
        filename = askopenfilename(parent=self.master, 
                           initialdir='/', 
                           initialfile='tmp',
                           filetypes=[("All files", "*")],
                           font_size=font_size)
        if filename:
            self.lcr_icon_ent.delete(0, 'end')
            self.lcr_icon_ent.insert(0, filename)
        
###########
def main():
    root = tk.Tk()
    root.title("Editor")
    root.update_idletasks()
    
    # style
    s = ttk.Style()
    s.theme_use("clam")
    
    app = Application(master=root)
    app.mainloop()
    
if __name__ == "__main__":
    main()
