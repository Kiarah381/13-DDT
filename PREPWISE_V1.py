#IMPORTS
import tkinter as tk 
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
# from sqlite import database as db
# import auth

class PrepWiseApp:
    def __init__(self, root): #This line "init" is used to give each object its own starting traits like colour and size
        self.root = root #This line "self" is used to keep track of which specific object you are changing 
        self.root.title("PrepWise - Meal Prep Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")

        self.current_user_id = None
        self.current_username = None

        self.style = ttk.Style() #Style is a variable i created to keep track of the formatting and design of my different items
        self.style.configure("TFrame", background= "#f5f5f5")
        self.style.configure("TLabel", background= "#f5f5f5", font=("Lexend", 10))
        self.style.configure("Header.TLabel", font=("Lexend", 18, "bold"))
        self.style.configure("Card.TFrame", background="white")

        #Dashboard
        self.create_dashboard()
    def create_dashboard(self):
        title = tk.Label(
                self.root, #"root" is a variable name I created to represent my base or starting point for this section
                text="PrepWise Dashboard",
                font=("Lexend", 24, "bold"),
                bg="#f5f5f5"
    )
        title.pack(pady=30)
        tk.Button(
                self.root,
                text="Monthly Meal Calender",
                width=30,
                command=self.monthly_calendar #"command" is used to link a button to a function
            ).pack(pady=10)
        tk.Button(
                self.root,
                text="Meal Reminders",
                width=30,
                command=self.meal_reminders
            ).pack(pady=10)
        tk.Button(
                self.root,
                text="AI Recipe Generator",
                width=30,
                command=self.recipe_generator
            ).pack(pady=10)
        tk.Button(
                self.root,
                text="My Cookbook",
                width=30,
                command=self.cookbook
            ).pack(pady=10)
        tk.Button(
                self.root,
                text="Logout",
                width=30,
                command=self.logout
            ).pack(pady=20)

    #Navigation between windows
    def clear_window(self):
            for widget in self.root.winfo_children():
                widget.destroy()
    def show_dashboard(self):
            self.clear_window()
            self.create_dashboard()  

    def monthly_calendar(self):
        self.clear_window()
        self.current_date = datetime.now()
        self.create_calendar()

    def create_calendar(self):
        self.clear_window()
        header = tk.Frame(
                self.root,
                bg="#f5f5f5"
            )
        header.pack(pady=20)
    #Back button to scroll to the previous dates
        previous_button = tk.Button(
                header,
                text="<",
                command=self.previous_month
            )
        previous_button.grid(row=0, column=0, padx=20)
    #Displays the current date
        self.month_label = tk.Label(
                header,
                text=self.current_date.strftime("%B %Y"),#This displays the current date and time "%B %Y" inserts the month and year
                font=("Lexend", 24, "bold"),
                bg="#f5f5f5"
            )
        self.month_label.grid(row=0, column=1)
    #Next month button
        next_button = tk.Button(
                header,
                text=">",
                command=self.next_month
            )
        next_button.grid(row=0, column=2, padx=20)

        self.calendar_frame = tk.Frame(
                    self.root,
                    bg="#f5f5f5"
             )
        self.calendar_frame.pack()
        self.display_calendar() 
            
        back_button = tk.Button(
                self.root,
                text="Back",
                command=self.show_dashboard
            )
        back_button.pack(pady=20)      
#Displays the calender 
    def display_calendar(self):
        import calendar

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for col, day in enumerate(days): #'enumerate' means that it is organising the days by numbers
            tk.Label(
            self.calendar_frame,
            text=day,
            font=("Lexend", 12, "bold"),
            bg="#f5f5f5"
        ).grid(row=0, column=col)


        month = calendar.monthcalendar(
        self.current_date.year,
        self.current_date.month
    )

        for row, week in enumerate(month, start=1):
            for col, day in enumerate(week):

                tk.Button(
                self.calendar_frame,
                text=day if day != 0 else "",
                width=10,
                height=4
            ).grid(
                row=row,
                column=col,
                padx=2,
                pady=2
            )

    def previous_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(
            year=self.current_date.year-1,
            month=12
        )
        else:
            self.current_date = self.current_date.replace(
            month=self.current_date.month-1
        )

        self.create_calendar()         
    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(
            year=self.current_date.year+1,
            month=1
        )
        else:
            self.current_date = self.current_date.replace(
            month=self.current_date.month+1
        )

        self.create_calendar()      

#-Verion one calender ends here-





    def meal_reminders(self):
                self.clear_window()

    def recipe_generator(self):
                self.clear_window()

    def cookbook(self):
                self.clear_window()

    def logout(self):
                self.clear_window()
                Login_System(self.root)

# Login screen 
class Login_System:
    def __init__(self, root):#This line is used to give each object its own starting traits like colour and size
        self.root=root #This line "self" is used to keep track of which specific object you are changing
        self.root.title("Login Page")
        self.root.geometry("1350x700+0+0")
        self.root.configure(bg="#f5f5f5")

        #Title
        title = tk.Label(
        self.root,
        text="PrepWise Login Page",
        font=("Lexend", 24, "bold"),
        bg="#f5f5f5"
    )
        title.pack(pady=20) #This line "pack" tells the system how to organise everything in the window
 #Username
        username_label = tk.Label(
         self.root,
         text="Username:",
         font=("Lexend", 12),
         bg="#f5f5f5"
     )
        username_label.pack()
        self.username_entry = tk.Entry(
        self.root,
        font=("Lexend", 12)
    )
        self.username_entry.pack(pady=10) #This line "pack" tells the system how to organise everything in the window
 #Password
        password_label = tk.Label(
        self.root,
        text="Password:",
        font=("Lexend", 12),
        bg="#f5f5f5"
    )
        password_label.pack()
        self.password_entry = tk.Entry(
        self.root,
        font=("Lexend", 12),
    )
        self.password_entry.pack(pady=10)#This line "pack" tells the system how to organise everything in the window
#Login Button
        login_button = tk.Button(
            self.root,
            text="Login",
            font=("Lexend", 11),
            width=15,
            command=self.login
     )
        login_button.pack(pady=20)
#Login Actual Function/Authorisation
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get() #This line allows the user to type inside the username textbox
        if username == "admin" and password == "3344": #This line does the same thing but for the passwordbox
            messagebox.showinfo(
            "Login was successful",
            "Welcome buddy to PrepWise!!"
        )
        #Removes everything from the login page
            for widget in self.root.winfo_children():
                widget.destroy()

        #Opens the dashboard
            PrepWiseApp(self.root)
        else:
             messagebox.showerror(
            "Login has failed",
            "Incorrect username or password"
        )
root = tk.Tk()
obj=Login_System(root)
root.mainloop() #This keeps the window of the program open