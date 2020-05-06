from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from database import Database
import re
import smtplib
import email.mime.text
from hided import *


width = 600
pseudo = None

def launch(win):
    try:
        win.destroy()
    except:
        pass
    try:
        database = Database(mysql_config)
        database.connect()
        connected(database)
    except:
        error()


def connected(database):
    window = Tk()
    window.title("PyNetGames")
    window.geometry(f"{width}x{width}")
    window.configure(background="black")
    
    def login(*arg):
        global pseudo
        l_username = username.get()
        l_password = password.get()
        if l_username and l_password:
            if valid_username(l_username):
                if check_password(l_username, l_password):
                    pseudo = l_username
                    window.destroy()
                else:
                    error_login.config(text="Mot de passe incorrect")
            else:
                error_login.config(text="Cette utilisateur n'existe pas")
        else:
            error_login.config(text="Veuillez renseigner\ntout les champs")

    def valid_username(username):
        try:
            users = database.get("SELECT user_name FROM users")
            users = [user[0].replace(",","") for user in users]
            return username in users
        except:
            launch(window)

    def check_password(username, pass_word):
        try:
            password = database.get(f"SELECT user_password FROM users WHERE user_name = '{username}'")
            return password[0][0] == pass_word
        except:
            launch(window)

    def register():
        global pseudo
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        r_user_name = r_username.get()
        r_password1 = r_password.get()
        r_password2 = r_conf_password.get()
        r_email = mail_entry.get()
        if r_user_name and r_password1 and r_password2 and r_email:
            if r_valid_username(r_user_name):
                if valid_password(r_password1, r_password2):
                    if(re.search(regex,r_email)): 
                        inscription(r_user_name, r_password1, r_email)
                        pseudo = r_user_name
                        window.destroy()
                    else:
                        error_register.config(text="Email invalide")
            else:
                error_register.config(text="Ce nom est déjà pris")
        else:
            error_register.config(text="Veuillez renseigner\ntout les champs")

    def valid_password(password1, password2):
        if password1 == password2:
            if len(password1) >= 6:
                return True
            else:
                error_register.config(text="Votre mot de passe\ndoit faire au moins\nsix characteres")
        else:
            error_register.config(text="Les deux mots de passe\nne correspondent pas")
        return False

    def r_valid_username(username):
        try:
            users = database.get("SELECT user_name FROM users")
            try:
                users = [user[0].replace(",","") for user in users]
                return not username in users
            except:
                return True
        except:
            launch(window)

    def inscription(user_name, user_password, email):
        try:
            SQL_INSERT = "INSERT INTO {table}({columns}) VALUES ({placeholders})"
            colonne = ("user_name", "user_password", "email", "win_snake", "win_ttt", "win_pong")
            table = "users"
            query = SQL_INSERT.format(
                columns=",".join(colonne),
                table=table,
                placeholders=",".join(["%s" for i in range(len(colonne))]),
            )
            database.post(query, (user_name, user_password, email, 0, 0, 0),)
        except:
            launch(window)

    background_image=PhotoImage(file="menu_sprites/login_background.png")
    background_label = Label(window, image=background_image)
    background_label.place(x=0, y=0)
    error_login = Label(window, font=("PixelOperator8",15), text="", background ="black", foreground="#fe3a35")
    error_login.place(x=70, y=350)
    error_register = Label(window, font=("PixelOperator8",15), text="", background ="black", foreground="#fe3a35")
    error_register.place(x=370, y=350)
    window.bind('<Return>', login)
    login_image = PhotoImage(file="menu_sprites/login.png")
    register_image = PhotoImage(file="menu_sprites/register.png")
    mdp_image = PhotoImage(file="menu_sprites/mdp.png")
    
    #Username
    username = Entry(window, width=20)
    username.place(x=162, y=106)
    #Password
    password = Entry(window, show='*', width=20)
    password.place(x=162, y=154)
    #Bouton        
    login = Button(window, image=login_image, bg="black", border="0", command=login)
    login.place(x=50, y=430)
    #Bouton mdp oublié
    mdp_forgot = Button(window, image=mdp_image, bg="black", border="0", command= lambda data = database, win = window : mdp(data, win))
    mdp_forgot.place(x=175, y=423)

    #Username
    r_username = Entry(window, width=20)
    r_username.place(x=460, y=106)
    #Password
    r_password = Entry(window, show='*', width=20)
    r_password.place(x=460, y=156)
    #Confirm password
    r_conf_password = Entry(window, show='*', width=20)
    r_conf_password.place(x=460, y=215)
    #email
    mail_entry = Entry(window, width=20)
    mail_entry.place(x=460, y=285)
    #Bouton
    register = Button(window, image=register_image, bg="black", border="0", command=register)
    register.place(x=425, y=430)
    window.update()
    window.mainloop()

def mdp(database, win):
    def check(*arg):
        pseudo = pseudo_entry.get()
        mail = email_entry.get()
        if pseudo and mail :
            if check_pseudo(pseudo):
                if check_mail(mail, pseudo): 
                    send_mail(mail, pseudo)
                    done = Label(window, font=("PixelOperator8",40), text="Mail envoyé", background="black", fg="white")
                    done.pack()
                    window.update()
                    done.place(x=300-(done.winfo_width()/2), y=350)
                else:                   
                    error_mail.config(text="Adresse mail non valide")
                    error_mail.pack()
                    window.update()
                    error_mail.place(x=300-(error_mail.winfo_width()/2), y=340)
            else:
                error_mail.config(text="Ce pseudo n'existe pas")
                error_mail.pack()
                window.update()
                error_mail.place(x=300-(error_mail.winfo_width()/2), y=340)
        else:
            error_mail.config(text="Veuillez renseigner tout les champs")
            error_mail.pack()
            window.update()
            error_mail.place(x=300-(error_mail.winfo_width()/2), y=340)
                    
    def send_mail(mail, pseudo):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        msg = email.mime.text.MIMEText(f'Une demande de réinitialisation du mot de passe pour le compte "{pseudo}" à été demandé.'
                                       + u'<br><a href="https://pynetgamechangepassword.000webhostapp.com?{}">Suivez ce lien pour le réinitialiser</a>'.format("pseudo="+pseudo+"&error=None"),'html')

        msg['Subject'] = 'Réinitialisation de votre mot de passe'
        msg['From'] = 'PyNetGame'
        msg['To'] = pseudo
        server.sendmail('PyNetGame@gmail.com', mail, msg.as_string())
        server.quit()
    
    def check_pseudo(pseudo):
        try:
            query = database.get(f"SELECT user_name FROM users")
            return (pseudo,) in query
        except:
            return False

    def check_mail(mail,pseudo):
        try:
            query = database.get(f"SELECT email FROM users WHERE user_name = '{pseudo}'")[0]
            return (mail,) == query
        except:
            return False
        
    win.destroy()
    window = Tk()
    bg = PhotoImage(file="menu_sprites/reinitialisation.png")
    bg_ = Label(window, image=bg)
    bg_.place(x=0,y=0)
    window.title("PyNetGames")
    window.geometry(f"{width}x{width}")
    window.configure(background="black")
    window.bind('<Return>', check)
    window.protocol("WM_DELETE_WINDOW", lambda win = window : launch(win))
    valider=PhotoImage(file="menu_sprites/valider.png")
    error_mail = Label(window, text="", font=("blabla", 20), background ="black", foreground="#fe3a35")
    error_mail.place(x=300, y=340)
     
    pseudo_entry = Entry(window, width=30)
    pseudo_entry.place(x=320, y=210)

    email_entry = Entry(window, width=30)
    email_entry.place(x=320, y=280)

    register = Button(window, image=valider, bg="black", border="0", command=check)
    register.place(x=140, y=400)
    
    window.mainloop()


def error():
    window = Tk()
    retry_button = PhotoImage(file="menu_sprites/retry.png")
    background_image=PhotoImage(file="menu_sprites/no_co.png")
    background_label = Label(window, image=background_image)
    background_label.place(x=0, y=0)
    window.title("PyNetGames")
    window.geometry(f"{width}x{width}")
    window.configure(background="black")
    retry = Button(window, image=retry_button, command= lambda win = window : launch(win), bg="black", border="0")
    retry.place(x=width/2-100, y=450)
    window.update()
    window.mainloop()
    
launch(None)
