# Python Tkinter Handbook

## import
```from tkinter import *
from tkinter import filedialog
from tkinter import messagebox      # Need for pop-up messagebox
from tkinter import ttk             # Need for combobox
```
## Display
```
root = Tk()                   # Main Window
root.title('Title')           # Main Window Title
root.resizable(False, False)  # Resize x,y
root.iconbitmap('icon.ico')   # Icon for Window
root.geometry("800x600")      # Window Size
root.grab_set()               # Focus On Window
root_second = Toplevel()      # Second Window

mainloop()                    # Loop In
```
## Widgets

### Frame
```
frame = LabelFrame(root, padx=1, pady=1, bg='#424242', relief="flat")
frame.grid(row=0, column=0, sticky=W+E)
frame.pack(side=RIGHT, fill=Y)
```
### Button
```
button = Button(frame, text="text", image=img, command=command_when_press, width=134,height=39, padx=8, pady=0, anchor=E, relief="flat", font=("Comic", "10", "bold"), fg="#10488d", activebackground ="#2c4c66")
button.grid(row=0, column=0)
button.pack(side=RIGHT)
```
### Label
```
label = Label(root, text="text", image=img, padx=5, pady=0, bg='#515A5A', fg="white", anchor=E, relief="flat",font=("Comic Sans MS", "8", "italic"),width=0,height=0)
label.grid(row=0, column=0, sticky=W+E)
label.pack(side=RIGHT, fill=Y)
```
### Scrollbar
```
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar.set)	# In List config
scrollbar.config(command=Listbox_name.yview)
```
    OR
```
def xview_scroll(*args):
	Listbox.yview(*args)

scrollbar = Scrollbar(frame, command=xview_scroll, relief='flat', orient=HORIZONTAL)
scrollbar.pack(side=BOTTOM, fill=X)
(yscrollcommand=scrollbar.set, xscrollcommand=scrollbar.set)	# In List config
scrollbar.config(command=Listbox_name.xview)
```
