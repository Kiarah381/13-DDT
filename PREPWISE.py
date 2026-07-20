import tkinter as tk 
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import database as db
import auth
class PrepWiseApp:
    def_init_(self, root):
    self.root = root
    self.root.title("PrepWise - Meal Prep Assistant")
    self.root.geometry("1000x700")
    self.root.configure(bg="#f5f5f5")

    self.current_user_id = None
    self.current_username = None

    db.init_db()

    self.style = ttk.Style()
    self.style.configure("TFreame", background= "#f5f5f5")
    self.style.configure("TLabel", background= "#f5f5f5", front=(Segoe UI, 10))
    self.style.configure("Header.TLabel", front=("Segoe UI", 18, "bold"))
    self.style.configure("Card.TFrame", background="white")

def show_login_screen(self):
    self.clear_window ()
    

        