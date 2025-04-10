import tkinter
# pilow means python image in libary
from PIL import Image,ImageTk
 

jenish_root= tkinter.Tk()  # making instance of tk class that makes basic GUI that's why we call it's root beacuse we are forming base

# GUI logic here

# to give your size in  GUI use this method

jenish_root.geometry("444x43") # width x Height

# now user can resize the gui as he wants but if you want to lock your gui at min size
jenish_root.minsize(100 , 100) # width , height
jenish_root.maxsize(1200,998)


# to create label # lable means thing that user don't intreact with
kk=tkinter.Label(text="Jenish is good boy") # text or many para is there
kk.pack() # you need to pack it if you want to use this in your gui

# intrecat means , you can intreact with buttons , but can't intreact with labels
 # you can't intreact with images hence it is label so first you need to create object of your image than create it label and then pack it
 
# image1=tkinter.PhotoImage(file="D:\\2nd year\\Untitled.png") # dont support jpg and jpeg for this use pilow
# image1_label= tkinter.Label(image=image1)
# image1_label.pack()

# to work with the jpg images

# image1=tkinter.PhotoImage(file="D:\\2nd year\\Untitled.png") # dont support jpg and jpeg for this use pilow
pic=Image.open("E:\\Business\\Avadh\\drive-download-20241115T061402Z-001\\KT 109\\2.jpg")
image1=ImageTk.PhotoImage(pic)
image1_label= tkinter.Label(image=image1)
image1_label.pack()

#  to change the title

jenish_root.title("MY GUI jenish surani")

jenish_root.mainloop() # start the gui application and remember gui logic 



# buuttons kya plcae karvana che screen par tena mate methods:
#  for this geometiry managment we have following methods:

#  pac , greed, place
#   blockwise,excel greed banace, specific position ma button muke

