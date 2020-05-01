from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from database import Database

pseudo = None

def connexion():
    width = 600         
    window = Tk()
    mysql_config = {
        "host": "mysql-sql-crackito.alwaysdata.net",
        "user": "204318",
        "passwd": "20102001Aa",
        "database": "sql-crackito_projetreseau",
    }
    database = Database(mysql_config)
    database.connect()

    def login():
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
        users = database.get("SELECT user_name FROM users")
        users = [user[0].replace(",","") for user in users]
        return username in users

    def check_password(username, pass_word):
        password = database.get(f"SELECT user_password FROM users WHERE user_name = '{username}'")
        return password[0][0] == pass_word

    def register():
        r_user_name = r_username.get()
        r_password1 = r_password.get()
        r_password2 = r_conf_password.get()
        if r_user_name and r_password1 and r_password2:
            if not valid_username(r_user_name):
                if valid_password(r_password1, r_password2):
                    inscription(r_user_name, r_password1)
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

    def inscription(user_name, user_password):
        SQL_INSERT = "INSERT INTO {table}({columns}) VALUES ({placeholders})"
        colonne = ("user_name", "user_password")
        table = "users"
        query = SQL_INSERT.format(
            columns=",".join(colonne),
            table=table,
            placeholders=",".join(["%s" for i in range(len(colonne))]),
        )
        database.post(query, (user_name, user_password,),)

    error_login = Label(window, font=("PixelOperator8",15), text="", background ="black")
    error_login.place(x=50, y=300)
    error_register = Label(window, font=("PixelOperator8",15), text="", background ="black")
    error_register.place(x=350, y=300)
        
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
    login.place(x=125, y=400)

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
    #Bouton
    register = Button(window, text="Register", command=register, width=10)
    register.place(x=425, y=400)


    window.title("PyNetGames")
    window.geometry(f"{width}x{width}")
    window.configure(background="black")
    window.iconbitmap("")
    window.update()
    window.mainloop()

connexion()
