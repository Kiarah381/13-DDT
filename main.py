#IMPORTS
import tkinter as tk 
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import sqlite3

class PrepWiseApp:
    def __init__(self, root): #This line "init" is used to give each object its own starting traits like colour and size
        self.root = root #This line "self" is used to keep track of which specific object you are changing 
        self.root.title("PrepWise - Meal Prep Assistant")
        self.root.geometry("1000x750")
        self.root.configure(bg="#f5f5f5")

        self.current_user_id = None
        self.current_username = None
        self.meals = {} #This creates an empty list or contianer that will store my food items
        self.selected_date = None


# SQLite Database section
        self.prepwise_database = sqlite3.connect("prepwise.database")
        self.database_cursor = self.prepwise_database.cursor()

        self.database_cursor.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                meal TEXT
            )
        """)

        self.prepwise_database.commit()

        self.database_cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                ingredients TEXT,
                instructions TEXT
            )
        """)

        self.prepwise_database.commit()

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
    
 # Add Meal section
        meal_section = tk.Frame(
            self.root,
            bg="white",
            bd=2,
            relief="groove"
        )
        meal_section.pack(
            side="right",
            padx=20,
            pady=10
        )

        meal_title = tk.Label(
            meal_section,
            text="Add Meal",
            font=("Lexend", 16, "bold"),
            bg="white"
        )
        meal_title.pack(pady=10)
        self.selected_date_label = tk.Label(
            meal_section,
            text="Select a date",
            font=("Lexend", 11),
            bg="white"
        )
        self.selected_date_label.pack(pady=5)

        meal_label = tk.Label(
            meal_section,
            text="Meal:",
            font=("Lexend", 11),
            bg="white"
        )
        meal_label.pack()

        self.meal_entry = tk.Entry(
            meal_section,
            font=("Lexend", 11),
            width=20
        )
        self.meal_entry.pack(pady=5)

        add_button = tk.Button(
            meal_section,
            text="Add",
            font=("Lexend", 11),
            width=10,
            command=self.add_meal #This tells my program to reun the add meal function when triggered/clicked on
        )
        add_button.pack(pady=10)


#Displays saved meals section
        meal_display = tk.Frame(
            self.root,
            bg="white",
            bd=2,
            relief="groove"
        )
        meal_display.pack(
            side="left",
            padx=20,
            pady=10
        )

        meal_display_title = tk.Label(
            meal_display,
            text="Meals for Selected Date",
            font=("Lexend", 16, "bold"),
            bg="white"
        )
        meal_display_title.pack(pady=10)

        self.meal_list = tk.Listbox(
            meal_display,
            width=25,
            height=8,
            font=("Lexend", 11)
        )
        self.meal_list.pack(padx=10, pady=10)
   
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
            for col, day in enumerate(week): # "enumerate" used here draws the calender grid and places my days of the week into the right place 

                if day != 0:

                    today = datetime.now()

    # Check if this is today's date
                    is_today = (
                        day == today.day
                        and self.current_date.month == today.month
                        and self.current_date.year == today.year
                    )

                    if is_today:
                        button_bg = "#c8e6c9"
                        button_relief = "solid"
                        button_border = 3
                    else:
                        button_bg = "white"
                        button_relief = "raised"
                        button_border = 1

                    tk.Button(
                        self.calendar_frame,
                        text=self.meals.get(
                            self.current_date.replace(day=day).strftime("%Y-%m-%d"),
                            day, #Allows my program to know exactly which day was selected
                        ),
                        width=10,
                        height=3,
                        bg=button_bg,
                        relief=button_relief,
                        bd=button_border,
                        #"lambda" is a throw away function that makes my code more concise and the "d=day" allows python to lock in the correct day for each button during creation
                        command=lambda d=day: self.select_date(d),
                    ).grid(
                    row=row,
                    column=col,
                    padx=2,
                    pady=2
                    )
    def select_date(self, day):
        selected_date = self.current_date.replace(day=day)
        self.selected_date = selected_date

        if (
                day == datetime.now().day
                and self.current_date.month == datetime.now().month
                and self.current_date.year == datetime.now().year
        ):
                self.selected_date_label.config(
                    text="Today"
        )
        else:
            self.selected_date_label.config(
            text=selected_date.strftime("%d %B %Y")  # "strftime" is an abbreviate for string fortmat time which is a tool that converts dates into text. 
        )               
        self.show_meals() #This tells python that the user just clicked a date, so it has to now show the meals that were saved for that date

    def show_meals(self):

        self.meal_list.delete(0, tk.END)

        date = self.selected_date.strftime("%Y-%m-%d")

        self.database_cursor.execute(
            "SELECT meal FROM meals WHERE date = ?",
            (date,)
        )

        meals = self.database_cursor.fetchall()

        for meal in meals:
            self.meal_list.insert(tk.END, meal[0])

    def previous_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(
            year=self.current_date.year-1, # Helps my program navagate between the years so if we go back from january to 2025 it will reset and make the year 2025 aswell as December
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
        
#Fucntion that adds my meals to my calendar   
    def add_meal(self):
        meal = self.meal_entry.get()

        if meal == "":
            messagebox.showerror(
            "Error",
            "Please enter a meal."
            )
            return

        if self.selected_date == None:
            messagebox.showerror(
            "Error",
            "Please select a date first."
            )
            return

        date = self.selected_date.strftime("%Y-%m-%d")

        self.database_cursor.execute(
            "INSERT INTO meals (date, meal) VALUES (?, ?)",
            (date, meal)
        )
        self.prepwise_database.commit()
        self.meal_entry.delete(0, tk.END) #This tells my program from what character the user entred till the end to wipe it all away
        self.show_meals()
        messagebox.showinfo(
            "Meal Added",
            "Your meal has been added!"
        )

#-Verion two calender ends here-

    def meal_reminders(self):
                self.clear_window()

    def recipe_generator(self):
                self.clear_window()

    def cookbook(self):
                self.clear_window()

                # My Cookbook Title 
                title = tk.Label(
                    self.root,
                    text="My Cookbook",
                    font=("Lexend", 24, "bold"),
                    bg="#f5f5f5"
                )
                title.pack(pady=20)

                # Recipe name
                name_label = tk.Label(
                    self.root,
                    text="Recipe Name:",
                    font=("Lexend", 11),
                    bg="#f5f5f5"
                )
                name_label.pack()

                self.recipe_name_entry = tk.Entry(
                    self.root,
                    font=("Lexend", 11),
                    width=50
                )
                self.recipe_name_entry.pack(pady=5)

                # Ingredients
                ingredients_label = tk.Label(
                    self.root,
                    text="Ingredients:",
                    font=("Lexend", 11),
                    bg="#f5f5f5"
                )
                ingredients_label.pack()

                self.ingredients_entry = scrolledtext.ScrolledText(
                    self.root,
                    width=55,
                    height=5,
                    font=("Lexend", 11)
                )
                self.ingredients_entry.pack(pady=5)

                # Instructions
                instructions_label = tk.Label(
                    self.root,
                    text="Instructions:",
                    font=("Lexend", 11),
                    bg="#f5f5f5"
                )
                instructions_label.pack()

                self.instructions_entry = scrolledtext.ScrolledText(
                    self.root,
                    width=55,
                    height=5,
                    font=("Lexend", 11)
                )
                self.instructions_entry.pack(pady=5)

                 # Save button
                save_button = tk.Button(
                    self.root,
                    text="Save Recipe",
                    font=("Lexend", 11),
                    width=15,
                    command=self.save_recipe
                )
                save_button.pack(pady=10)

                # Saved recipes heading
                saved_label = tk.Label(
                    self.root,
                    text="Saved Recipes",
                    font=("Lexend", 16, "bold"),
                    bg="#f5f5f5"
                )
                saved_label.pack(pady=10)

                # Recipe area
                recipe_area = tk.Frame(
                    self.root,
                    bg="#f5f5f5"
                )
                recipe_area.pack(pady=5)

                # List of saved recipes
                self.recipe_list = tk.Listbox(
                    recipe_area,
                    width=30,
                    height=8,
                    font=("Lexend", 11)
                )
                self.recipe_list.grid(
                    row=0,
                    column=0,
                    padx=10,
                    pady=10
                )

                self.recipe_list.bind(
                    "<<ListboxSelect>>",
                    self.show_recipe
                )
                # Recipe display section
                recipe_display = tk.Frame(
                    recipe_area,
                    bg="white",
                    bd=2,
                    relief="groove",
                    width=400,
                    height=300
                )
                recipe_display.grid(
                    row=0,
                    column=1,
                    padx=10,
                    pady=10
                )
                # Recipe title
                self.recipe_display_title = tk.Label(
                    recipe_display,
                    text="Select a recipe",
                    font=("Lexend", 18, "bold"),
                    bg="white"
                )
                self.recipe_display_title.pack(pady=10)

                # Ingredients heading
                ingredients_label = tk.Label(
                    recipe_display,
                    text="Ingredients",
                    font=("Lexend", 13, "bold"),
                    bg="white"
                )
                ingredients_label.pack()
                # Ingredients box
                self.recipe_ingredients = scrolledtext.ScrolledText(
                    recipe_display,
                    width=35,
                    height=5,
                    font=("Lexend", 10)
                )
                self.recipe_ingredients.pack(
                    padx=10,
                    pady=5
                )

                # Instructions heading
                instructions_label = tk.Label(
                    recipe_display,
                    text="Instructions",
                    font=("Lexend", 13, "bold"),
                    bg="white"
                )
                instructions_label.pack()

                # Instructions box
                self.recipe_instructions = scrolledtext.ScrolledText(
                    recipe_display,
                    width=35,
                    height=5,
                    font=("Lexend", 10)
                )
                self.recipe_instructions.pack(
                    padx=10,
                    pady=5
                )
                # Back button
                back_button = tk.Button(
                    self.root,
                    text="Back",
                    command=self.show_dashboard
                )
                back_button.pack(pady=15)
                # Load recipes already stored in database
                self.load_recipes()

    def load_recipes(self):
        self.recipe_list.delete(0, tk.END)

        self.database_cursor.execute(
            "SELECT name FROM recipes ORDER BY name"
        )

        recipes = self.database_cursor.fetchall()

        for recipe in recipes:
            self.recipe_list.insert(tk.END, recipe[0])

    def show_recipe(self, event):
        selected = self.recipe_list.curselection()

        if not selected:
            return

        recipe_name = self.recipe_list.get(selected[0])

        self.database_cursor.execute(
            """
            SELECT ingredients, instructions
            FROM recipes
            WHERE name = ?
            """,
            (recipe_name,)
        )

        recipe = self.database_cursor.fetchone()

        if recipe:
            ingredients = recipe[0]
            instructions = recipe[1]

        # Display recipe name
        self.recipe_display_title.config(
            text=recipe_name
        )

        # Display ingredients
        self.recipe_ingredients.delete("1.0", tk.END)
        self.recipe_ingredients.insert(
            tk.END,
            ingredients
        )

        # Display instructions
        self.recipe_instructions.delete("1.0", tk.END)
        self.recipe_instructions.insert(
            tk.END,
            instructions
        )
    def view_recipe(self, recipe_id):
        self.clear_window()

    # Get the selected recipe from the database
        self.database_cursor.execute(
            "SELECT name, ingredients, instructions FROM recipes WHERE id = ?",
            (recipe_id,)
        )

        recipe = self.database_cursor.fetchone()

    # Recipe name
        title = tk.Label(
            self.root,
            text=recipe[0],
            font=("Lexend", 24, "bold"),
            bg="#f5f5f5"
        )
        title.pack(pady=20)           

    # Ingredients
        ingredients_label = tk.Label(
            self.root,
            text="Ingredients",
            font=("Lexend", 16, "bold"),
            bg="#f5f5f5"
        )
        ingredients_label.pack(pady=5)

        ingredients_text = scrolledtext.ScrolledText(
            self.root,
            width=50,
            height=8,
            font=("Lexend", 11)
        )
        ingredients_text.pack(pady=5)

        ingredients_text.insert(
            tk.END,
            recipe[1]
        )

        ingredients_text.config(state="disabled")

    # Instructions
        instructions_label = tk.Label(
            self.root,
            text="Instructions",
            font=("Lexend", 16, "bold"),
            bg="#f5f5f5"
        )
        instructions_label.pack(pady=5)

        instructions_text = scrolledtext.ScrolledText(
            self.root,
            width=50,
            height=8,
            font=("Lexend", 11)
        )
        instructions_text.pack(pady=5)

        instructions_text.insert(
            tk.END,
            recipe[2]
        )

        instructions_text.config(state="disabled")

    # Back button
        back_button = tk.Button(
            self.root,
            text="Back",
            font=("Lexend", 11),
            width=15,
            command=self.cookbook
        )
        back_button.pack(pady=15)

    def add_recipe(self):
        self.clear_window()

        # Title
        title = tk.Label(
            self.root,
            text="Add Recipe",
            font=("Lexend", 24, "bold"),
            bg="#f5f5f5"
        )
        title.pack(pady=20)

        # Recipe name
        name_label = tk.Label(
            self.root,
            text="Recipe Name:",
            font=("Lexend", 11),
            bg="#f5f5f5"
        )
        name_label.pack()

        self.recipe_name_entry = tk.Entry(
            self.root,
            font=("Lexend", 11),
            width=40
        )
        self.recipe_name_entry.pack(pady=5)

        # Ingredients
        ingredients_label = tk.Label(
            self.root,
            text="Ingredients:",
            font=("Lexend", 11),
            bg="#f5f5f5"
        )
        ingredients_label.pack()

        self.ingredients_entry = scrolledtext.ScrolledText(
            self.root,
            width=40,
            height=8,
            font=("Lexend", 11)
        )
        self.ingredients_entry.pack(pady=5)

        # Instructions
        instructions_label = tk.Label(
            self.root,
            text="Instructions:",
            font=("Lexend", 11),
            bg="#f5f5f5"
        )
        instructions_label.pack()

        self.instructions_entry = scrolledtext.ScrolledText(
            self.root,
            width=40,
            height=8,
            font=("Lexend", 11)
        )
        self.instructions_entry.pack(pady=5)

        # Save button
        save_button = tk.Button(
            self.root,
            text="Save Recipe",
            font=("Lexend", 11),
            width=20,
            command=self.save_recipe
        )
        save_button.pack(pady=10)

        # Back button
        back_button = tk.Button(
            self.root,
            text="Back",
            font=("Lexend", 11),
            width=15,
            command=self.cookbook
        )
        back_button.pack(pady=5)

    def save_recipe(self):
        recipe_name = self.recipe_name_entry.get()
        ingredients = self.ingredients_entry.get("1.0", tk.END).strip()
        instructions = self.instructions_entry.get("1.0", tk.END).strip()

        if recipe_name == "":
            messagebox.showerror("Error", "Please enter a recipe name.")
            return

        if ingredients == "":
            messagebox.showerror("Error", "Please enter the ingredients.")
            return

        if instructions == "":
            messagebox.showerror("Error", "Please enter the instructions.")
            return

        self.database_cursor.execute(
            """
            INSERT INTO recipes (name, ingredients, instructions)
            VALUES (?, ?, ?)
            """,
            (recipe_name, ingredients, instructions)
        )

        self.prepwise_database.commit()

        messagebox.showinfo(
        "Recipe Saved",
        "Your recipe has been saved!"
        )

        self.recipe_name_entry.delete(0, tk.END)
        self.ingredients_entry.delete("1.0", tk.END)
        self.instructions_entry.delete("1.0", tk.END)

        self.load_recipes()
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
        show="*" #This hides the password to give users privacy
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