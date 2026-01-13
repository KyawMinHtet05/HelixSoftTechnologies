import tkinter as tk
from tkinter import messagebox

def check_credentials(username, password):
    # Dummy check for demonstration purposes
    return username == "admin" and password == "1234"

def login():
    user = entry_user.get()
    pwd = entry_pass.get()
    if check_credentials(user, pwd):
        messagebox.showinfo("Login", "Login Successful!")
    else:
        messagebox.showerror("Login", "Invalid Credentials")
        
if __name__ == "__main__":
    app = tk.Tk()
    app.title("Login App")

    tk.Label(app, text="Username:").pack()
    entry_user = tk.Entry(app)
    entry_user.pack()

    tk.Label(app, text="Password:").pack()
    entry_pass = tk.Entry(app, show="*") # Hide password input
    entry_pass.pack()

    login_button = tk.Button(app, text="Login", command=login)
    login_button.pack()

    app.mainloop()