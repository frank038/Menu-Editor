# Menu-Editor
by frank038

v. 0.8.0

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY. Anyone can use and modified it for any purpose. Just remember the author (in case of modification).

A simple menu editor for Linux written in Python3/tkinter.

Requirements: python3, python3-xdg.

This program uses customs file and directory dialogs instead of the default tkinter dialogs. They are a slightly modified version of the project by Juliette Monsel (j_4321).

This program try to follow the freedesktop directives about the desktop file as possible.
It will never manage submenu items.
To date this program can list the applications it found in the system default directory and in the user default directory, delete them (only the user files), modify them (always saved in the user folder) and create new ones (in the user folder).

Limitations: a few categories has been merged into other main categories (e.g. Audio and Video are simply links to AudioVideo category); the icons in the main program are taken from Hicolor icon theme, so it cannot match the real icon the user can see in its menu (tkinter cannot handle svg files; the xdg python module has some limitations).

![My image](https://github.com/frank038/Menu-Editor/blob/master/img1.png)

![My image](https://github.com/frank038/Menu-Editor/blob/master/img2.png)
