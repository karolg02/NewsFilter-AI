import customtkinter as ctk
from PIL import Image
from config.appearance import COLORS, FONTS, configure_theme


class BaseApp(ctk.CTk):
    def __init__(self):
        """Inicjalizacja aplikacji"""
        super().__init__()
        
        if not hasattr(Image, 'antialias'): 
            Image.antialias = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.Resampling.LANCZOS
            
        configure_theme()
        
        self.title("NewsFilter AI")
        self.geometry("1280x800")
        self.configure(fg_color=COLORS['bg_primary'])
        
        self.current_feed_name = None
        self.current_df = None

        self.main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_primary'])
        self.main_container.pack(fill='both', expand=True)
        
        # Dodajemy pasek statusu
        self.status_bar = ctk.CTkFrame(
            self, 
            fg_color=COLORS['bg_secondary'],
            height=24,
            corner_radius=0
        )
        self.status_bar.pack(fill='x', side='bottom')
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="NewsFilter AI v1.0",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        self.status_label.pack(side='right', padx=10)
        
    def _clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
        self.main_container.configure(fg_color=COLORS['bg_primary'])
        
    def show_message(self, title, message, message_type="info"):
        from tkinter import messagebox
        
        if message_type == "info":
            messagebox.showinfo(title, message)
        elif message_type == "warning":
            messagebox.showwarning(title, message)
        elif message_type == "error":
            messagebox.showerror(title, message)
            
    def animate_transition(self, new_scene_function, *args, **kwargs):
        old_container = self.main_container

        self.main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_primary'])
        self.main_container.place(relx=1.0, rely=0, relwidth=1, relheight=1)
        
        if args or kwargs:
            new_scene_function(*args, **kwargs)
        else:
            new_scene_function()
        
        steps = 20
        for i in range(steps + 1):
            t = i / steps
            self.main_container.place(relx=1.0 - t, rely=0, relwidth=1, relheight=1)
            old_container.place(relx=0 - t, rely=0, relwidth=1, relheight=1)
            self.update()
            self.after(1)
        
        old_container.destroy()
        self.main_container.pack(fill='both', expand=True)