import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import calendar
import sqlite3


class PrepWiseApp:
    def __init__(self, root):
        self.root = root #Sets the text for my title at the top of my apps window
        self.root.title("PrepWise - Meal Prep Assistant")
        self.root.geometry("1000x750") #Sets the strating width and height of my application 
        self.root.minsize(700, 600) #Sets the smallest width and height that the user is allowed to chnage the size too 

        self.selected_date = None #This tells my program what the exact date and time it is today so that it can use it
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

        self.bg_colour = "#f4f6f8"
        self.card_colour = "#ffffff"
        self.green = "#4caf50"
        self.dark_green = "#388e3c"
        self.light_green = "#e8f5e9"
        self.text_colour = "#333333"
        self.grey = "#666666"
        self.red = "#d9534f"
        self.border_colour = "#dfe4e8"

        self.root.configure(bg=self.bg_colour)

        # ------------------------------------------------------
        # Frames
        # ------------------------------------------------------

        style.configure(
            "TFrame",
            background=self.bg_colour
        )

        style.configure(
            "Card.TFrame",
            background=self.card_colour
        )

        # ------------------------------------------------------
        # Labels
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # Buttons
        # ------------------------------------------------------

        # All application buttons use the same padding.
        style.configure(
            "Green.TButton",
            font=("Lexend", 10, "bold"),
            padding=(16, 10),
            foreground="white",
            background=self.green
        )

        style.map(
            "Green.TButton",
            background=[
                ("active", self.dark_green),
                ("pressed", self.dark_green)
            ],
            foreground=[
                ("disabled", "#aaaaaa")
            ]
        )

        style.configure(
            "App.TButton",
            font=("Lexend", 10),
            padding=(16, 10)
        )

        style.configure(
            "Danger.TButton",
            font=("Lexend", 10, "bold"),
            padding=(16, 10),
            foreground="white",
            background=self.red
        )

        style.map(
            "Danger.TButton",
            background=[
                ("active", "#b52b27"),
                ("pressed", "#b52b27")
            ]
        )

        # ------------------------------------------------------
        # Calendar
        # ------------------------------------------------------

        style.configure(
            "Calendar.TButton",
            font=("Lexend", 10),
            padding=(8, 10)
        )

        style.configure(
            "Today.TButton",
            font=("Lexend", 10, "bold"),
            padding=(8, 10),
            foreground=self.dark_green
        )

        # ------------------------------------------------------
        # Entry
        # ------------------------------------------------------

        style.configure(
            "TEntry",
            padding=8,
            font=("Lexend", 10)
        )

        # ------------------------------------------------------
        # Treeview
        # ------------------------------------------------------

        style.configure(
            "Treeview",
            font=("Lexend", 10),
            rowheight=32,
            background="white",
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            font=("Lexend", 10, "bold")
        )

        # ------------------------------------------------------
        # Labels frame
        # ------------------------------------------------------

        style.configure(
            "TLabelframe",
            background=self.card_colour
        )

        style.configure(
            "TLabelframe.Label",
            background=self.card_colour,
            foreground=self.text_colour,
            font=("Lexend", 11, "bold")
        )

    def create_button(
        self,
        parent,
        text,
        command,
        style="App.TButton"
    ):
        """
        Creates a standardised button.

        All buttons use the same height/padding and can expand
        horizontally when their parent allows it.
        """
        return ttk.Button(
            parent,
            text=text,
            command=command,
            style=style
        )

    def configure_responsive_columns(self, widget, columns):
        """
        Gives columns equal responsive weight.
        """
        for column in range(columns):
            widget.columnconfigure(
                column,
                weight=1,
                uniform="responsive"
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
        main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        content = ttk.Frame(main_frame)

        content.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        content.columnconfigure(0, weight=1)

        # ------------------------------------------------------
        # Header
        # ------------------------------------------------------

        ttk.Label(
            content,
            text="PrepWise Dashboard",
            style="Title.TLabel",
            anchor="center"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(40, 8)
        )

        ttk.Label(
            content,
            text="Welcome to PrepWise!",
            style="Subtitle.TLabel",
            anchor="center"
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            pady=4
        )

        ttk.Label(
            content,
            text="Your simple meal planning assistant",
            style="Subtitle.TLabel",
            anchor="center"
        ).grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 35)
        )

        # ------------------------------------------------------
        # Dashboard buttons
        # ------------------------------------------------------

        button_frame = ttk.Frame(content)

        button_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=50
        )

        button_frame.columnconfigure(
            0,
            weight=1
        )

        dashboard_buttons = [
            (
                "Monthly Meal Calendar",
                self.monthly_calendar,
                "Green.TButton"
            ),
            (
                "Meal Reminders",
                self.meal_reminders,
                "Green.TButton"
            ),
            (
                "My Cookbook",
                self.cookbook,
                "Green.TButton"
            ),
            (
                "Logout",
                self.logout,
                "App.TButton"
            )
        ]

        for row, (text, command, style) in enumerate(
            dashboard_buttons
        ):
            button = self.create_button(
                button_frame,
                text,
                command,
                style
            )

            button.grid(
                row=row,
                column=0,
                sticky="ew",
                pady=6
            )

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

        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # ------------------------------------------------------
        # Header
        # ------------------------------------------------------

        header = ttk.Frame(main_frame)

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        header.columnconfigure(1, weight=1)

        self.create_button(
            header,
            "◀",
            self.previous_month
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.month_label = ttk.Label(
            header,
            text=self.current_date.strftime("%B %Y"),
            style="Title.TLabel",
            anchor="center"
        )

        self.month_label.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        self.create_button(
            header,
            "▶",
            self.next_month
        ).grid(
            row=0,
            column=2,
            sticky="e"
        )

        # ------------------------------------------------------
        # Content
        # ------------------------------------------------------

        content = ttk.Frame(main_frame)

        content.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        # ------------------------------------------------------
        # Calendar Card
        # ------------------------------------------------------

        calendar_card = ttk.LabelFrame(
            content,
            text="Calendar",
            padding=15
        )

        calendar_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        calendar_card.columnconfigure(
            0,
            weight=1
        )

        calendar_card.rowconfigure(
            0,
            weight=1
        )

        self.calendar_frame = ttk.Frame(
            calendar_card
        )

        self.calendar_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.display_calendar()

        # ------------------------------------------------------
        # Meal Card
        # ------------------------------------------------------

        meal_card = ttk.LabelFrame(
            content,
            text="Meals",
            padding=15
        )

        meal_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        meal_card.columnconfigure(
            0,
            weight=1
        )

        meal_card.rowconfigure(
            4,
            weight=1
        )

        self.selected_date_label = ttk.Label(
            meal_card,
            text="Select a date",
            font=("Lexend", 10, "bold"),
            anchor="center"
        )

        self.selected_date_label.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(5, 15)
        )

        ttk.Label(
            meal_card,
            text="Meal name:"
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.meal_entry = ttk.Entry(
            meal_card
        )

        self.meal_entry.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=5
        )

        self.create_button(
            meal_card,
            "Add Meal",
            self.add_meal,
            "Green.TButton"
        ).grid(
            row=3,
            column=0,
            sticky="ew",
            pady=10
        )

        ttk.Label(
            meal_card,
            text="Saved meals",
            font=("Lexend", 11, "bold")
        ).grid(
            row=4,
            column=0,
            sticky="nw",
            pady=(15, 5)
        )

        self.meal_tree = ttk.Treeview(
            meal_card,
            columns=("meal",),
            show="headings"
        )

        self.meal_tree.heading(
            "meal",
            text="Meal"
        )

        self.meal_tree.column(
            "meal",
            anchor="w"
        )

        self.meal_tree.grid(
            row=5,
            column=0,
            sticky="nsew"
        )

        meal_card.rowconfigure(
            5,
            weight=1
        )

        # ------------------------------------------------------
        # Back Button
        # ------------------------------------------------------

        self.create_button(
            main_frame,
            "Back",
            self.show_dashboard
        ).grid(
            row=2,
            column=0,
            pady=(15, 0)
        )

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

        # Seven equal-width columns
        for column in range(7):
            self.calendar_frame.columnconfigure(
                column,
                weight=1,
                uniform="calendar"
            )

        for row in range(7):
            self.calendar_frame.rowconfigure(
                row,
                weight=1
            )

        for column, day in enumerate(days):
            ttk.Label(
                self.calendar_frame,
                text=day,
                font=("Lexend", 10, "bold"),
                anchor="center"
            ).grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=2,
                pady=5
            )

        month = calendar.monthcalendar(
            self.current_date.year,
            self.current_date.month
        )

        today = datetime.now()

        for row, week in enumerate(
            month,
            start=1
        ):

            for column, day in enumerate(week):

                if day == 0:
                    continue

                date = self.current_date.replace(
                    day=day
                )

                date_string = date.strftime(
                    "%Y-%m-%d"
                )

                self.cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM meals
                    WHERE date = ?
                    """,
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
                    style=button_style,
                    command=lambda d=day: self.select_date(d)
                ).grid(
                    row=row,
                    column=column,
                    sticky="nsew",
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

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # ------------------------------------------------------
        # Title
        # ------------------------------------------------------

        ttk.Label(
            main_frame,
            text="Meal Reminders",
            style="Title.TLabel",
            anchor="center"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 20)
        )

        # ------------------------------------------------------
        # Add Reminder Card
        # ------------------------------------------------------

        reminder_card = ttk.LabelFrame(
            main_frame,
            text="Add Reminder",
            padding=15
        )

        reminder_card.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.configure_responsive_columns(
            reminder_card,
            4
        )

        # Date

        ttk.Label(
            reminder_card,
            text="Date (DD/MM/YYYY)"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.reminder_date_entry = ttk.Entry(
            reminder_card
        )

        self.reminder_date_entry.grid(
            row=1,
            column=0,
            sticky="ew",
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
            sticky="w",
            padx=5,
            pady=5
        )

        self.reminder_time_entry = ttk.Entry(
            reminder_card
        )

        self.reminder_time_entry.grid(
            row=1,
            column=1,
            sticky="ew",
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
            sticky="w",
            padx=5,
            pady=5
        )

        self.reminder_entry = ttk.Entry(
            reminder_card
        )

        self.reminder_entry.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=5,
            pady=5
        )

        # Add button

        self.create_button(
            reminder_card,
            "Add Reminder",
            self.add_reminder,
            "Green.TButton"
        ).grid(
            row=1,
            column=3,
            sticky="ew",
            padx=5,
            pady=5
        )

        # ------------------------------------------------------
        # Saved reminders
        # ------------------------------------------------------

        ttk.Label(
            main_frame,
            text="Saved Reminders",
            font=("Lexend", 14, "bold")
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=(25, 8)
        )

        tree_frame = ttk.Frame(main_frame)

        tree_frame.grid(
            row=4,
            column=0,
            sticky="nsew"
        )

        tree_frame.columnconfigure(
            0,
            weight=1
        )

        tree_frame.rowconfigure(
            0,
            weight=1
        )

        main_frame.rowconfigure(
            4,
            weight=1
        )

        self.reminder_tree = ttk.Treeview(
            tree_frame,
            columns=("date", "time", "reminder"),
            show="headings"
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
            width=130,
            minwidth=100,
            stretch=False
        )

        self.reminder_tree.column(
            "time",
            width=100,
            minwidth=80,
            stretch=False
        )

        self.reminder_tree.column(
            "reminder",
            minwidth=200,
            stretch=True
        )

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.reminder_tree.yview
        )

        self.reminder_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.reminder_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        # ------------------------------------------------------
        # Bottom buttons
        # ------------------------------------------------------

        button_frame = ttk.Frame(main_frame)

        button_frame.grid(
            row=5,
            column=0,
            pady=15
        )

        self.create_button(
            button_frame,
            "Delete Reminder",
            self.delete_reminder,
            "Danger.TButton"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.create_button(
            button_frame,
            "Back",
            self.show_dashboard
        ).grid(
            row=0,
            column=1,
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

        main_frame.columnconfigure(
            0,
            weight=1
        )

        main_frame.rowconfigure(
            2,
            weight=1
        )

        # ------------------------------------------------------
        # Title
        # ------------------------------------------------------

        ttk.Label(
            main_frame,
            text="My Cookbook",
            style="Title.TLabel",
            anchor="center"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # Add Recipe
        # ------------------------------------------------------

        add_frame = ttk.LabelFrame(
            main_frame,
            text="Add Recipe",
            padding=15
        )

        add_frame.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.configure_responsive_columns(
            add_frame,
            3
        )

        # Recipe Name

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
            add_frame
        )

        self.recipe_name_entry.grid(
            row=1,
            column=0,
            sticky="ew",
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
            height=5,
            font=("Lexend", 10),
            wrap=tk.WORD
        )

        self.ingredients_entry.grid(
            row=1,
            column=1,
            sticky="nsew",
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
            height=5,
            font=("Lexend", 10),
            wrap=tk.WORD
        )

        self.instructions_entry.grid(
            row=1,
            column=2,
            sticky="nsew",
            padx=5,
            pady=5
        )

        # Save

        save_button = self.create_button(
            add_frame,
            "Save Recipe",
            self.save_recipe,
            "Green.TButton"
        )

        save_button.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=5,
            pady=10
        )

        # ------------------------------------------------------
        # Cookbook area
        # ------------------------------------------------------

        cookbook_frame = ttk.Frame(
            main_frame
        )

        cookbook_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=(20, 0)
        )

        cookbook_frame.columnconfigure(
            0,
            weight=1
        )

        cookbook_frame.columnconfigure(
            1,
            weight=3
        )

        cookbook_frame.rowconfigure(
            0,
            weight=1
        )

        # ------------------------------------------------------
        # Recipe List
        # ------------------------------------------------------

        list_frame = ttk.LabelFrame(
            cookbook_frame,
            text="Saved Recipes",
            padding=10
        )

        list_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        list_frame.columnconfigure(
            0,
            weight=1
        )

        list_frame.rowconfigure(
            0,
            weight=1
        )

        self.recipe_tree = ttk.Treeview(
            list_frame,
            columns=("name",),
            show="headings"
        )

        self.recipe_tree.heading(
            "name",
            text="Recipe"
        )

        self.recipe_tree.column(
            "name",
            stretch=True
        )

        self.recipe_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.recipe_tree.bind(
            "<<TreeviewSelect>>",
            self.show_recipe
        )

        self.create_button(
            list_frame,
            "Delete Recipe",
            self.delete_recipe,
            "Danger.TButton"
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            pady=10
        )

        # ------------------------------------------------------
        # Recipe Details
        # ------------------------------------------------------

        display_frame = ttk.LabelFrame(
            cookbook_frame,
            text="Recipe Details",
            padding=10
        )

        display_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        display_frame.columnconfigure(
            0,
            weight=1
        )

        display_frame.rowconfigure(
            2,
            weight=1
        )

        display_frame.rowconfigure(
            4,
            weight=1
        )

        self.recipe_display_title = ttk.Label(
            display_frame,
            text="Select a recipe",
            font=("Lexend", 17, "bold"),
            anchor="center"
        )

        self.recipe_display_title.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=5
        )

        ttk.Label(
            display_frame,
            text="Ingredients",
            font=("Lexend", 11, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.recipe_ingredients = scrolledtext.ScrolledText(
            display_frame,
            height=6,
            font=("Lexend", 10),
            wrap=tk.WORD
        )

        self.recipe_ingredients.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=5
        )

        self.recipe_ingredients.config(
            state="disabled"
        )

        ttk.Label(
            display_frame,
            text="Instructions",
            font=("Lexend", 11, "bold")
        ).grid(
            row=3,
            column=0,
            sticky="w"
        )

        self.recipe_instructions = scrolledtext.ScrolledText(
            display_frame,
            height=6,
            font=("Lexend", 10),
            wrap=tk.WORD
        )

        self.recipe_instructions.grid(
            row=4,
            column=0,
            sticky="nsew",
            pady=5
        )

        self.recipe_instructions.config(
            state="disabled"
        )

        # ------------------------------------------------------
        # Back
        # ------------------------------------------------------

        self.create_button(
            main_frame,
            "Back",
            self.show_dashboard
        ).grid(
            row=3,
            column=0,
            pady=10
        )

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

        # Database connection for registered accounts
        self.database = sqlite3.connect("prepwise.db")
        self.cursor = self.database.cursor()

        # Make sure the users table exists
        self.create_users_table()

        self.setup_style()
        self.create_login()

    # Creates a table to store registered usernames and passwords
    def create_users_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS simple_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

        self.database.commit()

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.bg_colour = "#f4f6f8"
        self.green = "#388e3c"
        self.dark_green = "#2e7d32"
        self.text_colour = "#333333"
        self.grey = "#666666"

        self.root.configure(
            bg=self.bg_colour
        )

        style.configure(
            "TFrame",
            background=self.bg_colour
        )

        style.configure(
            "TLabel",
            background=self.bg_colour,
            foreground=self.text_colour,
            font=("Lexend", 10)
        )

        style.configure(
            "LoginTitle.TLabel",
            background=self.bg_colour,
            foreground=self.green,
            font=("Lexend", 30, "bold")
        )

        style.configure(
            "LoginSubtitle.TLabel",
            background=self.bg_colour,
            foreground=self.grey,
            font=("Lexend", 12)
        )

        style.configure(
            "Login.TButton",
            font=("Lexend", 10, "bold"),
            padding=(16, 10)
        )

    def create_login(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root)

        main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        main_frame.columnconfigure(
            0,
            weight=1
        )

        main_frame.rowconfigure(
            0,
            weight=1
        )

        login_frame = ttk.Frame(
            main_frame
        )

        login_frame.grid(
            row=0,
            column=0,
            sticky=""
        )

        login_frame.columnconfigure(
            0,
            weight=1
        )

        # ------------------------------------------------------
        # Header
        # ------------------------------------------------------

        ttk.Label(
            login_frame,
            text="PrepWise",
            style="LoginTitle.TLabel",
            anchor="center"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 5)
        )

        ttk.Label(
            login_frame,
            text="Login Page",
            style="LoginSubtitle.TLabel",
            anchor="center"
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 30)
        )

        # ------------------------------------------------------
        # Username
        # ------------------------------------------------------

        ttk.Label(
            login_frame,
            text="Username"
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )

        self.username_entry = ttk.Entry(
            login_frame
        )

        self.username_entry.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(5, 15)
        )

        # ------------------------------------------------------
        # Password
        # ------------------------------------------------------

        ttk.Label(
            login_frame,
            text="Password"
        ).grid(
            row=4,
            column=0,
            sticky="w"
        )

        self.password_entry = ttk.Entry(
            login_frame,
            show="*"
        )

        self.password_entry.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(5, 15)
        )

        # ------------------------------------------------------
        # Buttons
        # ------------------------------------------------------

        ttk.Button(
            login_frame,
            text="Login",
            style="Login.TButton",
            command=self.login
        ).grid(
            row=6,
            column=0,
            sticky="ew",
            pady=5
        )

        ttk.Button(
            login_frame,
            text="Create Account",
            style="Login.TButton",
            command=self.create_registration
        ).grid(
            row=7,
            column=0,
            sticky="ew",
            pady=5
        )

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # Validation check - both fields must be completed
        if not username or not password:
            messagebox.showerror(
                "Login Failed",
                "Please enter your username and password."
            )
            return

        # Check whether the entered details belong to a registered user
        self.cursor.execute(
            "SELECT id FROM simple_users WHERE username = ? AND password = ?",
            (username, password)
        )

        registered_user = self.cursor.fetchone()

        if registered_user:
            for widget in self.root.winfo_children():
                widget.destroy()

            PrepWiseApp(self.root)
            return

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
    # Registration
    # ==========================================================

    def create_registration(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self.root)

        main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

        main_frame.columnconfigure(
            0,
            weight=1
        )

        main_frame.rowconfigure(
            0,
            weight=1
        )

        registration_frame = ttk.Frame(
            main_frame
        )

        registration_frame.grid(
            row=0,
            column=0
        )

        registration_frame.columnconfigure(
            0,
            weight=1
        )

        # ------------------------------------------------------
        # Header
        # ------------------------------------------------------

        ttk.Label(
            registration_frame,
            text="PrepWise",
            style="LoginTitle.TLabel",
            anchor="center"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 5)
        )

        ttk.Label(
            registration_frame,
            text="Create Account",
            style="LoginSubtitle.TLabel",
            anchor="center"
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 30)
        )

        # ------------------------------------------------------
        # Username
        # ------------------------------------------------------

        ttk.Label(
            registration_frame,
            text="Username"
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )

        self.register_username_entry = ttk.Entry(
            registration_frame
        )

        self.register_username_entry.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(5, 15)
        )

        # ------------------------------------------------------
        # Password
        # ------------------------------------------------------

        ttk.Label(
            registration_frame,
            text="Password"
        ).grid(
            row=4,
            column=0,
            sticky="w"
        )

        self.register_password_entry = ttk.Entry(
            registration_frame,
            show="*"
        )

        self.register_password_entry.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(5, 15)
        )

        # ------------------------------------------------------
        # Confirm password
        # ------------------------------------------------------

        ttk.Label(
            registration_frame,
            text="Confirm Password"
        ).grid(
            row=6,
            column=0,
            sticky="w"
        )

        self.confirm_password_entry = ttk.Entry(
            registration_frame,
            show="*"
        )

        self.confirm_password_entry.grid(
            row=7,
            column=0,
            sticky="ew",
            pady=(5, 15)
        )

        # ------------------------------------------------------
        # Buttons
        # ------------------------------------------------------

        ttk.Button(
            registration_frame,
            text="Register",
            style="Login.TButton",
            command=self.register
        ).grid(
            row=8,
            column=0,
            sticky="ew",
            pady=5
        )

        ttk.Button(
            registration_frame,
            text="Back to Login",
            style="Login.TButton",
            command=self.create_login
        ).grid(
            row=9,
            column=0,
            sticky="ew",
            pady=5
        )

        self.register_username_entry.focus()

    def register(self):
        username = self.register_username_entry.get().strip()
        password = self.register_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Check that every field has been completed
        if not username or not password or not confirm_password:
            messagebox.showerror(
                "Registration Error",
                "Please complete all fields."
            )
            return

        # Check that the username is long enough
        if len(username) < 3:
            messagebox.showerror(
                "Registration Error",
                "Username must be at least 3 characters."
            )
            return

        # Check that the username only contains letters and numbers
        if not username.isalnum():
            messagebox.showerror(
                "Registration Error",
                "Username can only contain letters and numbers."
            )
            return

        # Check that the password is long enough
        if len(password) < 4:
            messagebox.showerror(
                "Registration Error",
                "Password must be at least 4 characters."
            )
            return

        # Check that both passwords match
        if password != confirm_password:
            messagebox.showerror(
                "Registration Error",
                "Passwords do not match."
            )
            return

        # Check whether the username already exists
        self.cursor.execute(
            "SELECT username FROM simple_users WHERE username = ?",
            (username,)
        )

        existing_user = self.cursor.fetchone()

        if existing_user:
            messagebox.showerror(
                "Registration Error",
                "That username already exists."
            )
            return

        # Save the new account to the database
        self.cursor.execute(
            "INSERT INTO simple_users (username, password) VALUES (?, ?)",
            (username, password)
        )

        self.database.commit()

        messagebox.showinfo(
            "Account Created",
            "Your PrepWise account has been created successfully."
        )

        self.create_login()


# ==========================================================
# Starts program
# ==========================================================

if __name__ == "__main__":
    root = tk.Tk()
    LoginSystem(root)
    root.mainloop()