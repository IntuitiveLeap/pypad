import os
import sys
from tkinter import Menu, Tk
from tkinter.constants import BOTH, END
import tkinter.scrolledtext as scrltxt
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from tkinter import font
from tkinter.font import Font


# constants
APP_NAME = 'PyPad'
ICON = os.path.join(sys.path[0], 'pypad.ico')


# main App setup
class App(Tk):
    def __init__(self) -> None:
        super().__init__()

app = App()

# capture screen size at runtime
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# set initial size for the displayed App
scaling_factor = 0.8 
App_width = int(screen_width * scaling_factor)
App_height = int(screen_height * scaling_factor)

# calculate centered positioning of App on the display
app.update_idletasks()
center_X = int((screen_width / 2) - (App_width / 2))
center_Y = int((screen_height / 2) - (App_height / 2))

# set App title, icon and geometry
app.title(APP_NAME)
if os.path.isfile(ICON): # use icon if found on sys.path[0]
    app.iconbitmap(ICON)
print(f'window X,Y {screen_width, screen_height}\nApp WIDTH,HEIGHT {App_width,App_height}\ncenter X,Y {center_X,center_Y}')
app.geometry(f'{App_width}x{App_height}+0+0')

# capture available font-families from the system at runtime
fonts = font.families()

# set Calibri font to be used on this system, if available
if 'Calibri' in fonts:
    f = 'Calibri'
else:
    f = 'Arial'
font_used = Font(app, font=(f, 14))

# set up text content_area and add to App
content_area = scrltxt.ScrolledText(app, font=font_used)
content_area.pack(expand=True, fill=BOTH)

# set up menu area in App
menu_area = Menu(app)
app.config(menu=menu_area)

# create file menu and edit menu
file_menu = Menu(menu_area, tearoff=0)
edit_menu = Menu(menu_area, tearoff=0)

# add file_menu & edit_menu cascades to menu_area
menu_area.add_cascade(label='File', menu=file_menu)
menu_area.add_cascade(label='Edit', menu=edit_menu)

# handlers for File and Edit menus
file = None # initial file object - global

# File menu items
def new_file():
    global file
    app.title(f'{APP_NAME}: Untitled')
    content_area.delete(1.0, END)

def open_file():
    global file
    file = askopenfilename(
        defaultextension='.txt',
        filetypes=[('Text Documents', '*.txt')])
    if file == '':
        file = None
    else:
        app.title(f'{APP_NAME}: {os.path.basename(file)}')
        with open(file, 'r') as f:
            content_area.insert('1.0', f.read())

def save_file():
    global file
    if not file:
        file = None
        saveas_file()
    else:
        with open(file, 'w') as f:
            f.write(content_area.get('1.0', END))

def saveas_file():
    global file
    file = asksaveasfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')])
    if not file:
        file = None
    else:
        with open(file, 'w') as f:
            f.write(content_area.get('1.0', END))
        app.title(f'{APP_NAME}: {os.path.basename(file)}')

def exit_App():
    app.destroy()

# Edit menu items
def cut_text():
    content_area.event_generate(("<<Cut>>"))

def copy_text():
    content_area.event_generate(("<<Copy>>"))

def paste_text():
    content_area.event_generate(("<<Paste>>"))

def clear_text():
    content_area.delete("1.0", END)

# place File menu items into file_menu cascade
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_file)
file_menu.add_command(label='Save As', command=saveas_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=exit_App)

# place Edit menu items into edit_menu cascade
edit_menu.add_command(label='Cut', command=cut_text)
edit_menu.add_command(label='Copy', command=copy_text)
edit_menu.add_command(label='Paste', command=paste_text)
edit_menu.add_command(label='Clear', command=clear_text)



def main():
    app.mainloop()


if __name__ == '__main__':
    main()
