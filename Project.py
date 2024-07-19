from tkinter import *
from tkinter import filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import os

filename = None
secret = None

def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
        for j in range(8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode(image, data):
    newimg = image.copy()
    encode_enc(newimg, data)
    return newimg

def decode(image):
    data = ''
    imgdata = iter(image.getdata())
    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3] +
                                    imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return data



def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetypes=(("PNG file",".png"),
                                                     ("JPG file",".jpg"),
                                                     ("All file","*.txt")))
    if filename:
        img = Image.open(filename)
        img.thumbnail((400, 400))  
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img)
        lbl.image = img

def Hide():
    global secret, filename
    if not filename:
        messagebox.showerror("Error", "Please select an image first.")
        return
    message = text1.get(1.0, END).strip()
    if not message:
        messagebox.showerror("Error", "Please enter a message to hide.")
        return
    image = Image.open(filename)
    secret = encode(image, message)
    messagebox.showinfo("Success", "Message hidden successfully.")

def Show():
    global filename
    if not filename:
        messagebox.showerror("Error", "Please select an image first.")
        return
    image = Image.open(filename)
    clear_message = decode(image)
    text1.delete(1.0, END)
    text1.insert(END, clear_message)

def save():
    global secret
    if secret is None:
        messagebox.showerror("Error", "No hidden message to save. Please hide a message first.")
        return
    save_path = save_location_entry.get()
    save_name = save_name_entry.get()
    if not save_path:
        save_path = os.getcwd()
    if not save_name:
        save_name = "hidden.png"
    elif not save_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        save_name += '.png'
    
    full_path = os.path.join(save_path, save_name)
    secret.save(full_path)
    messagebox.showinfo("Success", f"Image saved as {full_path}")
    reset()

def browse_save_location():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        save_location_entry.delete(0, END)
        save_location_entry.insert(0, folder_selected)

def reset():
    global filename, secret
    filename = None
    secret = None
    lbl.configure(image='')
    text1.delete(1.0, END)
    save_location_entry.delete(0, END)
    save_name_entry.delete(0, END)
    messagebox.showinfo("Reset", "All fields have been reset.")

# GUI setup
root = Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("900x700+150+50")
root.resizable(False, False)
root.configure(bg="#2f4155")

# GUI elements
try:
    image_icon = PhotoImage(file="logo.jpg")
    root.iconphoto(False, image_icon)

    logo = PhotoImage(file="logo.png")
    Label(root, image=logo, bg="#2f4155").place(x=10, y=10)
except TclError:
    print("Warning: logo.jpg or logo.png not found. Skipping logo display.")

Label(root, text="CYBER SCIENCE", bg="#2f4155", fg="white", font="arial 25 bold").place(x=100, y=20)


f = Frame(root, bd=3, bg="white", width=420, height=420, relief=GROOVE)
f.place(x=10, y=80)
lbl = Label(f, bg="white")
lbl.place(x=0, y=0)


frame2 = Frame(root, bd=3, width=430, height=420, bg="white", relief=GROOVE)
frame2.place(x=460, y=80)

text1 = Text(frame2, font="Roboto 16", bg="white", fg="black", relief=GROOVE)
text1.place(x=0, y=0, width=420, height=395)

Scrollbar1 = Scrollbar(frame2)
Scrollbar1.place(x=420, y=0, height=395)
Scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=Scrollbar1.set)


frame3 = Frame(root, bd=3, bg="#2f4155", width=880, height=100, relief=GROOVE)
frame3.place(x=10, y=510)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)
Button(frame3, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=340, y=30)
Button(frame3, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=500, y=30)
Button(frame3, text="Reset", width=10, height=2, font="arial 14 bold", command=reset, bg="#ff3333", fg="white").place(x=660, y=30)


frame4 = Frame(root, bd=3, bg="#2f4155", width=880, height=70, relief=GROOVE)
frame4.place(x=10, y=620)

Label(frame4, text="Save Location:", bg="#2f4155", fg="white", font="arial 12 bold").place(x=10, y=10)
save_location_entry = Entry(frame4, width=50, font="arial 12")
save_location_entry.place(x=140, y=10)
Button(frame4, text="Browse", width=10, font="arial 10", command=browse_save_location).place(x=750, y=7)

Label(frame4, text="Save Name:", bg="#2f4155", fg="white", font="arial 12 bold").place(x=10, y=40)
save_name_entry = Entry(frame4, width=50, font="arial 12")
save_name_entry.place(x=140, y=40)
root.mainloop()