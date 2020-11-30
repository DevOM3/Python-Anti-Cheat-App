from tkinter.messagebox import showinfo, showwarning, askyesno
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from PIL import ImageGrab
from firebase import firebase
from email import encoders
from tkinter import *
import subprocess
import webbrowser
import _thread
import smtplib
import shutil
import glob
import time
import os

stop = True
global student, end


def screenshot():
    t = 1
    while stop:
        im = ImageGrab.grab()
        os.system("mkdir exam_screenshot")
        im.save(f'exam_screenshot\\screenshot{t}.png')
        time.sleep(2)
        t = t + 1


def send_mail(link):
    email_user = 'raviprogrammingacademy@gmail.com'
    email_password = 'javatohbaaphein@2020'
    email_send = student

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = "Ravi Programming Academy Examination Link"

    body = f"Your link for Examination is given below\n\n" \
           f"Instructions:\n" \
           f"1] Do not close the Examination application\n" \
           f"2] Solve all questions within 90 mins.\n" \
           f"3] Close the application after you submit the Examination\n" \
           f"4] Closing the application may lead you to the Failure in Examination\n\n" \
           f"Examination Link:\n" \
           f"{link}\n\n\n" \
           f"All the Best!!!"
    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    server.quit()


def end_process():
    fromaddr = "raviprogrammingacademy@gmail.com"
    toaddr = "raviprogrammingacademy@gmail.com"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = f"Screenshots from {student}"

    body = "Screenshots :- \n"

    msg.attach(MIMEText(body, 'plain'))

    filename = "exam_screenshots.zip"
    attachment = open("exam_screenshots.zip", "rb")

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, "javatohbaaphein@2020")

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

    showinfo("Ravi Programming Academy Examination", "Verification successful ! \nSee you in the next Examination")

    root.destroy()


def end_exam(event):
    ans = askyesno("Ravi Programming Academy Examination", "Do you want to End Examination?")
    if ans == YES:
        global stop
        stop = False

        os.remove(r"exam_screenshots.zip")
        subprocess.call(["powershell.exe", "Compress-Archive -LiteralPath 'exam_screenshot' -DestinationPath "
                                           "'exam_screenshots.zip'"])

        # screenshots = glob.glob("exam_screenshot/*")
        # for f in screenshots:
        #     os.remove(f)
        shutil.rmtree("exam_screenshot")

        _thread.start_new_thread(end_process, ())

        showinfo("Ravi Programming Academy Examination", "Thank you ! for attending Examination...\n\n"
                                                         "Verification running........................\n"
                                                         "Don't disconnect your internet connection for 2-3 minutes")

        end.destroy()
        wait = Label(container, text="You must wait for Verification", font=("Ariel", 21, "bold"),
                     bg="black", fg="white")
        wait.pack(fill=X, expand=True, padx=25, pady=11)


def submit(event):

    def disable_event():
        pass

    def focus_in_end(eve):
        end.config(bg="red", fg="white", font=("Ariel", 18))

    def focus_out_end(eve):
        end.config(bg="white", fg="black", font=("Ariel", 15))

    global student
    student = mail.get()
    if not student.__contains__("@"):
        showwarning("Ravi Programming Academy Examination", "You must enter a valid E-mail ID")
    else:
        auth = firebase.FirebaseAuthentication("YJ6PEwgmdqmB1VxjDciddFOGNjRlUCy4DprvRYcH",
                                               "raviprogrammingacademy@gmail.com")
        con = firebase.FirebaseApplication("https://course-students.firebaseio.com/", auth)

        link = con.get("/link", '')

        showinfo("Ravi Programming Academy Examination", "Now go to your mail and click on the link that we sent you"
                                                         " and don't close this application "
                                                         "until you finish your exam. \nBut don't forget to close it "
                                                         "after Examination is finished or you will be failed!")

        send_mail(link)
        webbrowser.open_new_tab("https://mail.google.com/")

        email.destroy()
        submit_but.destroy()

        global end
        end = Button(container, text="End Examination", bg="white", fg="black", bd=2, font=("Ariel", 15))
        end.bind("<Enter>", focus_in_end)
        end.bind("<Leave>", focus_out_end)
        end.bind("<Button-1>", end_exam)
        end.bind("<Return>", end_exam)
        end.pack(side=TOP, expand=True, padx=25, pady=21)
        root.protocol("WM_DELETE_WINDOW", disable_event)

        _thread.start_new_thread(screenshot, ())


def focusin(event):
    email.config(fg="black")
    email.delete(0, END)


def focusout(event):
    if mail.get() == "" or mail.get() is None:
        email.config(fg="grey")
        email.insert(0, "E-mail")


root = Tk()
root.resizable(False, False)

container = LabelFrame(root, bg="black", text="Ravi Programming Academy Examination", fg="red",
                       font=("Helvetica", 21, "bold"), bd=5)
container.pack(fill=BOTH, expand=True)

mail = StringVar()
email = Entry(container, textvariable=mail, font=("Ariel", 13, "bold"), fg="grey")
email.insert(0, 'E-mail')
email.bind("<FocusIn>", focusin)
email.bind("<FocusOut>", focusout)
email.bind("<Return>", submit)
email.pack(fill=X, expand=True, padx=25, pady=11)

submit_but = Button(container, text="Submit", bg="white", fg="black", bd=0)
submit_but.bind("<Button-1>", submit)
submit_but.bind("<Return>", submit)
submit_but.pack(anchor=SE, expand=True, padx=25, pady=7)

root.mainloop()
