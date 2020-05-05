from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from database import Database
import re
import smtplib
import email.mime.text

width = 600
mysql_config = {
    "host": "mysql-sql-crackito.alwaysdata.net",
    "user": "204318",
    "passwd": "20102001Aa",
    "database": "sql-crackito_projetreseau",
}
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
                    error_login.config(text="Mot de passe incorrect", background="grey")
            else:
                error_login.config(text="Cette utilisateur n'existe pas", background="grey")
        else:
            error_login.config(text="Veuillez renseigner\ntout les champs", background="grey")

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
                        error_register.config(text="Email invalide", background="grey")
            else:
                error_register.config(text="Ce nom est déjà pris", background="grey")
        else:
            error_register.config(text="Veuillez renseigner\ntout les champs", background="grey")

    def valid_password(password1, password2):
        if password1 == password2:
            if len(password1) >= 6:
                return True
            else:
                error_register.config(text="Votre mot de passe\ndoit faire au moins\nsix characteres", background="grey")
        else:
            error_register.config(text="Les deux mots de passe\nne correspondent pas", background="grey")
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


    error_login = Label(window, font=("PixelOperator8",15), text="", background ="black")
    error_login.place(x=70, y=350)
    error_register = Label(window, font=("PixelOperator8",15), text="", background ="black")
    error_register.place(x=370, y=350)
    window.bind('<Return>', login)
    ### Partie Login    
    log = Label(window, font=("PixelOperator8",40), text="Log In", width=7)
    log.place(x=38, y=50)
    #Username
    name = Label(window, font=("PixelOperator8",10), text="Username :", width=9)
    name.place(x=38, y=149)
    username = Entry(window, width=20)
    username.place(x=135, y=150)
    #Password
    passw = Label(window, font=("PixelOperator8",10), text="Password :", width=9)
    passw.place(x=38, y=189)
    password = Entry(window, show='*', width=20)
    password.place(x=135, y=190)
    #Bouton
    login = Button(window, text="Login", command=login, width=10)
    login.place(x=50, y=430)
    #Bouton mdp oublié
    login = Button(window, text="Mdp oublié ?", command= lambda data = database, win = window : mdp(data, win), width=10)
    login.place(x=175, y=430)

    ###Partie Register
    reg = Label(window, font=("PixelOperator8",40), text="Register", width=7)
    reg.place(x=338, y=50)
    #Username
    r_name = Label(window, font=("PixelOperator8",10), text="Username :", width=9)
    r_name.place(x=338, y=149)
    r_username = Entry(window, width=20)
    r_username.place(x=435, y=150)
    #Password
    r_passw = Label(window, font=("PixelOperator8",10), text="Password :", width=9)
    r_passw.place(x=338, y=189)
    r_password = Entry(window, show='*', width=20)
    r_password.place(x=435, y=190)
    #Confirm password
    r_conf_passw = Label(window, font=("PixelOperator8",10), text="Confirm\npassword :", width=9)
    r_conf_passw.place(x=338, y=229)
    r_conf_password = Entry(window, show='*', width=20)
    r_conf_password.place(x=435, y=237)
    #email
    mail = Label(window, font=("PixelOperator8",10), text="Adresse\nmail :", width=9)
    mail.place(x=338, y=283)
    mail_entry = Entry(window, width=20)
    mail_entry.place(x=435, y=290)
    #Bouton
    register = Button(window, text="Register", command=register, width=10)
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
                    print("Adresse mail non valide")
            else:
               print("Ce pseudo n'existe pas") 
        else:
            print("Veuillez renseigner tout les champs")
            
                    
    def send_mail(mail, pseudo):
        server = smtplib.SMTP('smtp.gmail.com:587')
        username = 'mat33360@@gmail.com'
        password = '20106969Aa'
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
    window.title("PyNetGames")
    window.geometry(f"{width}x{width}")
    window.configure(background="black")
    window.bind('<Return>', check)
    window.protocol("WM_DELETE_WINDOW", lambda win = window : launch(win))
  
    title = Label(window, font=("PixelOperator8",40), text="Réinitialisation du\nmot de passe", background="black", fg="white")
    title.pack()
    window.update()
    title.place(x=300-(title.winfo_width()/2), y=0)
    
    pseudo = Label(window, font=("PixelOperator8",10), text="Username :", width=9)
    pseudo.place(x=200, y=180)
    pseudo_entry = Entry(window, width=20)
    pseudo_entry.place(x=300, y=183)

    email_lab = Label(window, font=("PixelOperator8",10), text="Mail :", width=9)
    email_lab.place(x=200, y=230)
    email_entry = Entry(window, width=20)
    email_entry.place(x=300, y=233)

    confirm = Button(window, text="Confirm", command=check, width=10)
    confirm.pack()
    window.update()
    confirm.place(x=300-(confirm.winfo_width()/2), y=283)

def error():
    window = Tk()
    window.title("PyNetGames")
    window.geometry(f"{width}x{width}")
    window.configure(background="black")
    error = Label(window, font=("PixelOperator8",40), text="No Internet Connexion")
    error.place(x=35, y=width/2-50)
    retry = Button(window, text="Retry", command= lambda win = window : launch(win), width=10)
    retry.place(x=width/2-40, y=400)
    window.update()
    window.mainloop()
    
launch(None)
