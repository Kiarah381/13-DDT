import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import calendar
import sqlite3

# modified - reminderto add lots of comments
class PrepWiseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PrepWise - Meal Prep Assistant")
        self.root.geometry("900x650")
        self.root.minsize(800, 650)

        self.selected_date = None
        self.current_date = datetime.now()
        self.reminder_job = None

        # Database
        self.database = sqlite3.connect("prepwise.db")
        self.cursor = self.database.cursor()

        self.create_database()

        # Styling
        self.setup_style()

        # Start the dashboard
        self.create_dashboard()

        # Close database properly when window closes
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # ==========================================================
    # Database
    # ==========================================================

    def create_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                meal TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                reminder TEXT NOT NULL
            )
        """)

        self.database.commit()

    # ==========================================================
    # Style
    # ==========================================================

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Main colours
        self.bg_colour = "#f4f6f8"
        self.card_colour = "#ffffff"
        self.green = "#4caf50"
        self.dark_green = "#388e3c"
        self.light_green = "#e8f5e9"
        self.text_colour = "#333333"
        self.grey = "#666666"
        self.red = "#d9534f"

        self.root.configure(bg=self.bg_colour)

        # General widgets
        style.configure(
            "TFrame",
            background=self.bg_colour
        )

        style.configure(
            "Card.TFrame",
            background=self.card_colour
        )

        style.configure(
            "TLabel",
            background=self.bg_colour,
            foreground=self.text_colour,
            font=("Lexend", 10)
        )

        style.configure(
            "Title.TLabel",
            background=self.bg_colour,
            foreground=self.text_colour,
            font=("Lexend", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background=self.bg_colour,
            foreground=self.grey,
            font=("Lexend", 11)
        )

        style.configure(
            "CardTitle.TLabel",
            background=self.card_colour,
            foreground=self.text_colour,
            font=("Lexend", 15, "bold")
        )

        # Buttons
        style.configure(
            "Green.TButton",
            font=("Lexend", 10),
            padding=8
        )

        style.map(
            "Green.TButton",
            background=[
                ("active", self.dark_green)
            ]
        )

        # Calendar buttons
        style.configure(
            "Calendar.TButton",
            font=("Lexend", 10),
            padding=10
        )

        style.configure(
            "Today.TButton",
            font=("Lexend", 10, "bold"),
            padding=10
        )

        # Treeview
        style.configure(
            "Treeview",
            font=("Lexend", 10),
            rowheight=30
        )

        style.configure(
            "Treeview.Heading",
            font=("Lexend", 10, "bold")
        )

    # ==========================================================
    # General functions
    # ==========================================================

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.stop_reminder_checker()
        self.create_dashboard()

    def create_dashboard(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(
            main_frame,
            text="PrepWise Dashboard",
            style="Title.TLabel"
        )
        title.pack(pady=(70, 10))

        subtitle = ttk.Label(
            main_frame,
            text="Your simple meal planning assistant",
            style="Subtitle.TLabel"
        )
        subtitle.pack(pady=(0, 40))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack()

        ttk.Button(
            button_frame,
            text="Monthly Meal Calendar",
            width=30,
            style="Green.TButton",
            command=self.monthly_calendar
        ).pack(pady=8)

        ttk.Button(
            button_frame,
            text="Meal Reminders",
            width=30,
            style="Green.TButton",
            command=self.meal_reminders
        ).pack(pady=8)

        ttk.Button(
            button_frame,
            text="My Cookbook",
            width=30,
            style="Green.TButton",
            command=self.cookbook
        ).pack(pady=8)

        ttk.Button(
            button_frame,
            text="Logout",
            width=30,
            command=self.logout
        ).pack(pady=(25, 8))

    # ==========================================================
    # Calender
    # ==========================================================

    def monthly_calendar(self):
        self.current_date = datetime.now()
        self.selected_date = None
        self.create_calendar()

    def create_calendar(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill="x", pady=(0, 15))

        ttk.Button(
            header,
            text="◀",
            width=4,
            command=self.previous_month
        ).pack(side="left")

        self.month_label = ttk.Label(
            header,
            text=self.current_date.strftime("%B %Y"),# "strftime" is an abbreviate for string fortmat time which is a tool that converts dates into text. 
            style="Title.TLabel"
        )
        self.month_label.pack(side="left", expand=True)

        ttk.Button(
            header,
            text="▶",
            width=4,
            command=self.next_month
        ).pack(side="right")

        # Content
        content = ttk.Frame(main_frame)
        content.pack(fill="both", expand=True)

        # Calendar
        calendar_card = ttk.LabelFrame(
            content,
            text="Calendar",
            padding=10
        )
        calendar_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.calendar_frame = ttk.Frame(calendar_card)
        self.calendar_frame.pack()

        self.display_calendar()

        # Meal section
        meal_card = ttk.LabelFrame(
            content,
            text="Meals",
            padding=15
        )
        meal_card.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        self.selected_date_label = ttk.Label(
            meal_card,
            text="Select a date",
            font=("Lexend", 10, "bold")
        )
        self.selected_date_label.pack(pady=(5, 15))

        ttk.Label(
            meal_card,
            text="Meal name:"
        ).pack(anchor="w")

        self.meal_entry = ttk.Entry(
            meal_card,
            width=25
        )
        self.meal_entry.pack(pady=5)

        ttk.Button(
            meal_card,
            text="Add Meal",
            style="Green.TButton",
            command=self.add_meal
        ).pack(fill="x", pady=10)

        ttk.Label(
            meal_card,
            text="Saved meals",
            font=("Lexend", 11, "bold")
        ).pack(anchor="w", pady=(15, 5))

        self.meal_tree = ttk.Treeview(
            meal_card,
            columns=("meal",),
            show="headings",
            height=8
        )

        self.meal_tree.heading(
            "meal",
            text="Meal"
        )

        self.meal_tree.column(
            "meal",
            width=190
        )

        self.meal_tree.pack()

        ttk.Button(
            main_frame,
            text="Back",
            command=self.show_dashboard
        ).pack(pady=(15, 0))

    def display_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun"
        ]

        for column, day in enumerate(days):
            ttk.Label(
                self.calendar_frame,
                text=day,
                font=("Lexend", 10, "bold"),
                anchor="center",
                width=9
            ).grid(
                row=0,
                column=column,
                padx=2,
                pady=5
            )

        month = calendar.monthcalendar(
            self.current_date.year,
            self.current_date.month
        )

        today = datetime.now()

        for row, week in enumerate(month, start=1):
            for column, day in enumerate(week):

                if day == 0:
                    continue

                date = self.current_date.replace(day=day)
                date_string = date.strftime("%Y-%m-%d")

                # Check whether this date has meals
                self.cursor.execute(
                    "SELECT COUNT(*) FROM meals WHERE date = ?",
                    (date_string,)
                )

                meal_count = self.cursor.fetchone()[0]

                button_text = str(day)

                if meal_count > 0:
                    button_text += f"\n{meal_count} meal"

                    if meal_count != 1:
                        button_text += "s"

                is_today = (
                    day == today.day
                    and self.current_date.month == today.month
                    and self.current_date.year == today.year
                )

                button_style = (
                    "Today.TButton"
                    if is_today
                    else "Calendar.TButton"
                )

                ttk.Button(
                    self.calendar_frame,
                    text=button_text,
                    width=9,
                    style=button_style,
                     #"lambda" is a throw away function that makes my code more concise and the "d=day" allows python to lock in the correct day for each button during creation                                
                    command=lambda d=day: self.select_date(d)
                ).grid(
                    row=row,
                    column=column,
                    padx=2,
                    pady=2
                )

    def select_date(self, day):
        self.selected_date = self.current_date.replace(day=day)

        today = datetime.now()

        if self.selected_date.date() == today.date():
            self.selected_date_label.config(
                text="Today"
            )
        else:
            self.selected_date_label.config(
                text=self.selected_date.strftime("%d %B %Y")
            )

        self.show_meals() #This tells python that the user just clicked a date, so it has to now show the meals that were saved for that date

    def show_meals(self):
        for item in self.meal_tree.get_children():
            self.meal_tree.delete(item)

        if self.selected_date is None:
            return

        date = self.selected_date.strftime("%Y-%m-%d")

        self.cursor.execute(
            """
            SELECT meal
            FROM meals
            WHERE date = ?
            ORDER BY id
            """,
            (date,)
        )

        meals = self.cursor.fetchall()

        for meal in meals:
            self.meal_tree.insert(
                "",
                "end",
                values=(meal[0],)
            )

    def add_meal(self):
        meal = self.meal_entry.get().strip()

        if not meal:
            messagebox.showerror(
                "Error",
                "Please enter a meal."
            )
            return

        if self.selected_date is None:
            messagebox.showerror(
                "Error",
                "Please select a date first."
            )
            return

        date = self.selected_date.strftime("%Y-%m-%d")

        self.cursor.execute(
            """
            INSERT INTO meals (date, meal)
            VALUES (?, ?)
            """,
            (date, meal)
        )

        self.database.commit()

        self.meal_entry.delete(0, tk.END)

        self.show_meals()
        self.display_calendar()

        messagebox.showinfo(
            "Meal Added",
            "Your meal has been added."
        )

    def previous_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(
                year=self.current_date.year - 1, # Helps my program navagate between the years so if we go back from january to 2025 it will reset and make the year 2025 aswell as December
                month=12
            )
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month - 1
            )

        self.selected_date = None
        self.create_calendar()

    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(
                year=self.current_date.year + 1,
                month=1
            )
        else:
            self.current_date = self.current_date.replace(
                month=self.current_date.month + 1
            )

        self.selected_date = None
        self.create_calendar()

    # ==========================================================
    # Reminders
    # ==========================================================

    def meal_reminders(self):
        self.stop_reminder_checker()
        self.clear_window()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        ttk.Label(
            main_frame,
            text="Meal Reminders",
            style="Title.TLabel"
        ).pack(pady=(0, 20))

        # Add reminder section
        reminder_card = ttk.LabelFrame(
            main_frame,
            text="Add Reminder",
            padding=15
        )
        reminder_card.pack(fill="x")

        # Date
        ttk.Label(
            reminder_card,
            text="Date (DD/MM/YYYY)"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.reminder_date_entry = ttk.Entry(
            reminder_card,
            width=20
        )
        self.reminder_date_entry.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        # Time
        ttk.Label(
            reminder_card,
            text="Time (HH:MM)"
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.reminder_time_entry = ttk.Entry(
            reminder_card,
            width=15
        )
        self.reminder_time_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # Reminder
        ttk.Label(
            reminder_card,
            text="Reminder"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.reminder_entry = ttk.Entry(
            reminder_card,
            width=40
        )
        self.reminder_entry.grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

        ttk.Button(
            reminder_card,
            text="Add Reminder",
            style="Green.TButton",
            command=self.add_reminder
        ).grid(
            row=1,
            column=3,
            padx=10,
            pady=5
        )

        # Saved reminders
        ttk.Label(
            main_frame,
            text="Saved Reminders",
            font=("Lexend", 14, "bold")
        ).pack(
            anchor="w",
            pady=(25, 8)
        )

        self.reminder_tree = ttk.Treeview(
            main_frame,
            columns=("date", "time", "reminder"),
            show="headings",
            height=10
        )

        self.reminder_tree.heading(
            "date",
            text="Date"
        )

        self.reminder_tree.heading(
            "time",
            text="Time"
        )

        self.reminder_tree.heading(
            "reminder",
            text="Reminder"
        )

        self.reminder_tree.column(
            "date",
            width=120
        )

        self.reminder_tree.column(
            "time",
            width=100
        )

        self.reminder_tree.column(
            "reminder",
            width=500
        )

        self.reminder_tree.pack(
            fill="both",
            expand=True
        )

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Delete Reminder",
            command=self.delete_reminder
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Back",
            command=self.show_dashboard
        ).pack(
            side="left",
            padx=5
        )

        self.load_reminders()
        self.start_reminder_checker()

    def add_reminder(self):
        date = self.reminder_date_entry.get().strip()
        time = self.reminder_time_entry.get().strip()
        reminder = self.reminder_entry.get().strip()

        if not date or not time or not reminder:
            messagebox.showerror(
                "Error",
                "Please complete all reminder fields."
            )
            return

        try:
            datetime.strptime(
                f"{date} {time}",
                "%d/%m/%Y %H:%M"
            )
        except ValueError:
            messagebox.showerror(
                "Invalid Date or Time",
                "Please use DD/MM/YYYY and HH:MM."
            )
            return

        self.cursor.execute(
            """
            INSERT INTO reminders (date, time, reminder)
            VALUES (?, ?, ?)
            """,
            (date, time, reminder)
        )

        self.database.commit()

        self.reminder_date_entry.delete(0, tk.END)
        self.reminder_time_entry.delete(0, tk.END)
        self.reminder_entry.delete(0, tk.END)

        self.load_reminders()

        messagebox.showinfo(
            "Reminder Added",
            "Your reminder has been saved."
        )

    def load_reminders(self):
        if not hasattr(self, "reminder_tree"):
            return

        for item in self.reminder_tree.get_children():
            self.reminder_tree.delete(item)

        self.cursor.execute(
            """
            SELECT id, date, time, reminder
            FROM reminders
            ORDER BY date, time
            """
        )

        reminders = self.cursor.fetchall()

        for reminder_id, date, time, text in reminders:
            self.reminder_tree.insert(
                "",
                "end",
                iid=str(reminder_id),
                values=(date, time, text)
            )

    def delete_reminder(self):
        selected = self.reminder_tree.selection()

        if not selected:
            messagebox.showerror(
                "Error",
                "Please select a reminder first."
            )
            return

        confirm = messagebox.askyesno(
            "Delete Reminder",
            "Are you sure you want to delete this reminder?"
        )

        if not confirm:
            return

        reminder_id = selected[0]

        self.cursor.execute(
            "DELETE FROM reminders WHERE id = ?",
            (reminder_id,)
        )

        self.database.commit()

        self.load_reminders()

    def start_reminder_checker(self):
        self.stop_reminder_checker()
        self.check_notifications()

    def stop_reminder_checker(self):
        if self.reminder_job is not None:
            try:
                self.root.after_cancel(self.reminder_job)
            except tk.TclError:
                pass

            self.reminder_job = None

    def check_notifications(self):
        current_datetime = datetime.now()

        current_date = current_datetime.strftime("%d/%m/%Y")
        current_time = current_datetime.strftime("%H:%M")

        self.cursor.execute(
            """
            SELECT id, reminder
            FROM reminders
            WHERE date = ? AND time = ?
            """,
            (current_date, current_time)
        )

        reminders = self.cursor.fetchall()

        for reminder_id, reminder in reminders:
            messagebox.showinfo(
                "PrepWise Reminder",
                reminder
            )

            self.cursor.execute(
                "DELETE FROM reminders WHERE id = ?",
                (reminder_id,)
            )

        self.database.commit()

        if hasattr(self, "reminder_tree"):
            self.load_reminders()

        self.reminder_job = self.root.after(
            30000,
            self.check_notifications
        )

    # ==========================================================
    # Cookbook
    # ==========================================================

    def cookbook(self):
        self.stop_reminder_checker()
        self.clear_window()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        ttk.Label(
            main_frame,
            text="My Cookbook",
            style="Title.TLabel"
        ).pack(pady=(0, 15))

        # Add recipe section
        add_frame = ttk.LabelFrame(
            main_frame,
            text="Add Recipe",
            padding=15
        )
        add_frame.pack(fill="x")

        # Recipe name
        ttk.Label(
            add_frame,
            text="Recipe Name"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.recipe_name_entry = ttk.Entry(
            add_frame,
            width=45
        )
        self.recipe_name_entry.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        # Ingredients
        ttk.Label(
            add_frame,
            text="Ingredients"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        self.ingredients_entry = scrolledtext.ScrolledText(
            add_frame,
            width=35,
            height=5,
            font=("Lexend", 10),
            wrap=tk.WORD
        )
        self.ingredients_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # Instructions
        ttk.Label(
            add_frame,
            text="Instructions"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.instructions_entry = scrolledtext.ScrolledText(
            add_frame,
            width=35,
            height=5,
            font=("Lexend", 10),
            wrap=tk.WORD
        )
        self.instructions_entry.grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

        ttk.Button(
            add_frame,
            text="Save Recipe",
            style="Green.TButton",
            command=self.save_recipe
        ).grid(
            row=2,
            column=0,
            columnspan=3,
            pady=10
        )

        # Cookbook area
        cookbook_frame = ttk.Frame(main_frame)
        cookbook_frame.pack(
            fill="both",
            expand=True,
            pady=(20, 0)
        )

        # Recipe list
        list_frame = ttk.LabelFrame(
            cookbook_frame,
            text="Saved Recipes",
            padding=10
        )
        list_frame.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        self.recipe_tree = ttk.Treeview(
            list_frame,
            columns=("name",),
            show="headings",
            height=15
        )

        self.recipe_tree.heading(
            "name",
            text="Recipe"
        )

        self.recipe_tree.column(
            "name",
            width=220
        )

        self.recipe_tree.pack()

        self.recipe_tree.bind(
            "<<TreeviewSelect>>",
            self.show_recipe
        )

        ttk.Button(
            list_frame,
            text="Delete Recipe",
            command=self.delete_recipe
        ).pack(
            pady=10
        )

        # Recipe information
        display_frame = ttk.LabelFrame(
            cookbook_frame,
            text="Recipe Details",
            padding=10
        )
        display_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.recipe_display_title = ttk.Label(
            display_frame,
            text="Select a recipe",
            font=("Lexend", 17, "bold")
        )
        self.recipe_display_title.pack(pady=5)

        ttk.Label(
            display_frame,
            text="Ingredients",
            font=("Lexend", 11, "bold")
        ).pack(anchor="w")

        self.recipe_ingredients = scrolledtext.ScrolledText(
            display_frame,
            height=6,
            font=("Lexend", 10),
            wrap=tk.WORD
        )
        self.recipe_ingredients.pack(
            fill="both",
            expand=True,
            pady=5
        )

        self.recipe_ingredients.config(
            state="disabled"
        )

        ttk.Label(
            display_frame,
            text="Instructions",
            font=("Lexend", 11, "bold")
        ).pack(anchor="w")

        self.recipe_instructions = scrolledtext.ScrolledText(
            display_frame,
            height=6,
            font=("Lexend", 10),
            wrap=tk.WORD
        )
        self.recipe_instructions.pack(
            fill="both",
            expand=True,
            pady=5
        )

        self.recipe_instructions.config(
            state="disabled"
        )

        ttk.Button(
            main_frame,
            text="Back",
            command=self.show_dashboard
        ).pack(pady=10)

        self.load_recipes()

    def save_recipe(self):
        name = self.recipe_name_entry.get().strip()

        ingredients = self.ingredients_entry.get(
            "1.0",
            tk.END
        ).strip()

        instructions = self.instructions_entry.get(
            "1.0",
            tk.END
        ).strip()

        if not name:
            messagebox.showerror(
                "Error",
                "Please enter a recipe name."
            )
            return

        if not ingredients:
            messagebox.showerror(
                "Error",
                "Please enter the ingredients."
            )
            return

        if not instructions:
            messagebox.showerror(
                "Error",
                "Please enter the instructions."
            )
            return

        self.cursor.execute(
            """
            INSERT INTO recipes
            (name, ingredients, instructions)
            VALUES (?, ?, ?)
            """,
            (name, ingredients, instructions)
        )

        self.database.commit()

        self.recipe_name_entry.delete(
            0,
            tk.END
        )

        self.ingredients_entry.delete(
            "1.0",
            tk.END
        )

        self.instructions_entry.delete(
            "1.0",
            tk.END
        )

        self.load_recipes()

        messagebox.showinfo(
            "Recipe Saved",
            "Your recipe has been saved."
        )

    def load_recipes(self):
        if not hasattr(self, "recipe_tree"):
            return

        for item in self.recipe_tree.get_children():
            self.recipe_tree.delete(item)

        self.cursor.execute(
            """
            SELECT id, name
            FROM recipes
            ORDER BY name
            """
        )

        recipes = self.cursor.fetchall()

        for recipe_id, name in recipes:
            self.recipe_tree.insert(
                "",
                "end",
                iid=str(recipe_id),
                values=(name,)
            )

    def show_recipe(self, event=None):
        selected = self.recipe_tree.selection()

        if not selected:
            return

        recipe_id = selected[0]

        self.cursor.execute(
            """
            SELECT name, ingredients, instructions
            FROM recipes
            WHERE id = ?
            """,
            (recipe_id,)
        )

        recipe = self.cursor.fetchone()

        if recipe is None:
            return

        name, ingredients, instructions = recipe

        self.recipe_display_title.config(
            text=name
        )

        self.recipe_ingredients.config(
            state="normal"
        )

        self.recipe_ingredients.delete(
            "1.0",
            tk.END
        )

        self.recipe_ingredients.insert(
            tk.END,
            ingredients
        )

        self.recipe_ingredients.config(
            state="disabled"
        )

        self.recipe_instructions.config(
            state="normal"
        )

        self.recipe_instructions.delete(
            "1.0",
            tk.END
        )

        self.recipe_instructions.insert(
            tk.END,
            instructions
        )

        self.recipe_instructions.config(
            state="disabled"
        )

    def delete_recipe(self):
          # Get the recipe selected in the list
        selected = self.recipe_tree.selection()
          # Check if the user selected a recipe
        if not selected:
            messagebox.showerror(
                "Error",
                "Please select a recipe first."
            )
            return
         # Get the name of the selected recipe
        recipe_id = selected[0]
        recipe_name = self.recipe_tree.item(
            recipe_id,
            "values"
        )[0]
         # Ask the user to confirm the deletion
        confirm = messagebox.askyesno(
            "Delete Recipe",
            f"Are you sure you want to delete '{recipe_name}'?"
        )

        if not confirm:
            return
         # Delete the recipe from the database
        self.cursor.execute(
            "DELETE FROM recipes WHERE id = ?",
            (recipe_id,)
        )

        self.database.commit()
        # Remove the recipe from the Listbox
        self.load_recipes()
        # Clear the recipe display
        self.recipe_display_title.config(
            text="Select a recipe"
        )

        self.recipe_ingredients.config(
            state="normal"
        )

        self.recipe_ingredients.delete(
            "1.0",
            tk.END
        )

        self.recipe_ingredients.config(
            state="disabled"
        )

        self.recipe_instructions.config(
            state="normal"
        )

        self.recipe_instructions.delete(
            "1.0",
            tk.END
        )

        self.recipe_instructions.config(
            state="disabled"
        )
        # Tell the user the recipe was deleted
        messagebox.showinfo(
            "Recipe Deleted",
            "The recipe has been deleted."
        )

    # ==========================================================
    # Login / Logout
    # ==========================================================

    def logout(self):
        self.stop_reminder_checker()
        self.clear_window()
        LoginSystem(self.root)

    def close_app(self):
        self.stop_reminder_checker()
        self.database.close()
        self.root.destroy()


class LoginSystem:
    def __init__(self, root):
        self.root = root

        self.root.title("PrepWise - Login")
        self.root.geometry("1000x750")
        self.root.minsize(700, 500)

        self.setup_style()
        self.create_login()

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TFrame",
            background="#f4f6f8"
        )

        style.configure(
            "TLabel",
            background="#f4f6f8",
            foreground="#333333",
            font=("Lexend", 10)
        )

        style.configure(
            "LoginTitle.TLabel",
            background="#f4f6f8",
            foreground="#388e3c",
            font=("Lexend", 30, "bold")
        )

        style.configure(
            "LoginSubtitle.TLabel",
            background="#f4f6f8",
            foreground="#666666",
            font=("Lexend", 12)
        )

        style.configure(
            "Login.TButton",
            font=("Lexend", 10),
            padding=8
        )

    def create_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(
            fill="both",
            expand=True
        )

        login_frame = ttk.Frame(main_frame)
        login_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        ttk.Label(
            login_frame,
            text="PrepWise",
            style="LoginTitle.TLabel"
        ).pack(pady=(0, 5))

        ttk.Label(
            login_frame,
            text="Login Page",
            style="LoginSubtitle.TLabel"
        ).pack(pady=(0, 30))

        # Username
        ttk.Label(
            login_frame,
            text="Username"
        ).pack(anchor="w")

        self.username_entry = ttk.Entry(
            login_frame,
            width=30
        )
        self.username_entry.pack(
            pady=(5, 15)
        )

        # Password
        ttk.Label(
            login_frame,
            text="Password"
        ).pack(anchor="w")

        self.password_entry = ttk.Entry(
            login_frame,
            width=30,
            show="*"
        )
        self.password_entry.pack(
            pady=(5, 15)
        )

        ttk.Button(
            login_frame,
            text="Login",
            style="Login.TButton",
            width=25,
            command=self.login
        ).pack(pady=10)

        # Press Enter to login
        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # Simple login for the current project.

        if username == "admin" and password == "3344":
            for widget in self.root.winfo_children():
                widget.destroy()

            PrepWiseApp(self.root)

        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password."
            )


# ==========================================================
# Starts program
# ==========================================================

if __name__ == "__main__":
    root = tk.Tk()
    LoginSystem(root)
    root.mainloop()