from tkinter.messagebox import showinfo
import pkg_resources.py2_warn
from firebase import firebase
from tkinter import *


def focusin(event):
    url.config(fg="black")
    url.delete(0, END)


def focusout(event):
    if url.get() == "" or url.get() is None:
        url.config(fg="grey")
        url.insert(0, "Examination Url")


def submit(event):
    link = url_var.get()

    auth = firebase.FirebaseAuthentication("YJ6PEwgmdqmB1VxjDciddFOGNjRlUCy4DprvRYcH",
                                           "raviprogrammingacademy@gmail.com")
    con = firebase.FirebaseApplication("https://course-students.firebaseio.com/", auth)

    con.put("/", "link", link)
    showinfo("Ravi Programming Academy Examination", "Examination link uploaded successfully!")
    root.destroy()


root = Tk()
root.resizable(False, False)

container = LabelFrame(root, bg="black", text="Ravi Programming Academy Examination", fg="red",
                       font=("Helvetica", 21, "bold"), bd=5)
container.pack(fill=BOTH, expand=True)

url_var = StringVar()
url = Entry(container, textvariable=url_var, font=("Ariel", 13, "bold"), fg="grey")
url.insert(0, 'Examination Url')
url.bind("<FocusIn>", focusin)
url.bind("<FocusOut>", focusout)
url.bind("<Return>", submit)
url.pack(fill=X, expand=True, padx=25, pady=11)

submit_but = Button(container, text="Submit", bg="white", fg="black", bd=0)
submit_but.bind("<Button-1>", submit)
submit_but.bind("<Return>", submit)
submit_but.pack(anchor=SE, expand=True, padx=25, pady=7)


root.mainloop()
