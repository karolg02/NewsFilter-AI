"""Zarządzanie źródłami RSS"""
import customtkinter as ctk
from tkinter import messagebox
from config.appearance import COLORS, FONTS
from utils.file_operations import load_links, add_link, save_links
from utils.feed import get_feed_count


def create_add_source_scene(app):
    app._clear_main_container()
    
    header_label = ctk.CTkLabel(
        app.main_container,
        text="Dodaj nowe źródło",
        font=FONTS['header'],
        text_color=COLORS['text']
    )
    header_label.pack(pady=(50, 30))
    
    form_frame = ctk.CTkFrame(app.main_container, fg_color=COLORS['bg_secondary'], corner_radius=10)
    form_frame.pack(padx=50, pady=20, fill='x')
    
    name_label = ctk.CTkLabel(
        form_frame,
        text="Nazwa źródła:",
        font=FONTS['text'],
        text_color=COLORS['text']
    )
    name_label.pack(anchor='w', padx=20, pady=(20, 5))
    
    name_entry = ctk.CTkEntry(
        form_frame,
        width=400,
        font=FONTS['text'],
        placeholder_text="np. Onet Sport"
    )
    name_entry.pack(fill='x', padx=20, pady=(0, 15))
    
    url_label = ctk.CTkLabel(
        form_frame,
        text="URL kanału RSS:",
        font=FONTS['text'],
        text_color=COLORS['text']
    )
    url_label.pack(anchor='w', padx=20, pady=(5, 5))
    
    url_entry = ctk.CTkEntry(
        form_frame,
        width=400,
        font=FONTS['text'],
        placeholder_text="np. https://sport.onet.pl/rss.xml"
    )
    url_entry.pack(fill='x', padx=20, pady=(0, 15))
    
    hint_label = ctk.CTkLabel(
        form_frame,
        text="Wskazówka: RSS to specjalny format używany przez strony internetowe do publikowania aktualizacji.",
        font=FONTS['small'],
        text_color=COLORS['text_secondary']
    )
    hint_label.pack(anchor='w', padx=20, pady=(0, 20))
    
    buttons_frame = ctk.CTkFrame(app.main_container, fg_color="transparent")
    buttons_frame.pack(pady=20)
    
    def validate_and_add():
        name = name_entry.get().strip()
        url = url_entry.get().strip()
        
        if not name:
            messagebox.showerror("Błąd", "Nazwa źródła nie może być pusta.")
            return
        
        if not url:
            messagebox.showerror("Błąd", "URL kanału RSS nie może być pusty.")
            return
        
        if not (url.startswith('http://') or url.startswith('https://')):
            messagebox.showerror("Błąd", "URL musi zaczynać się od http:// lub https://")
            return
        
        if not url.lower().endswith(('.xml', '.rss', 'rss.xml', 'feed', '/feed', '/rss')):
            if not messagebox.askyesno("Ostrzeżenie", 
                                     "URL nie wygląda na kanał RSS. Czy na pewno chcesz go dodać?"):
                return
        
        if add_link(app, name, url):
            messagebox.showinfo("Sukces", f"Dodano źródło: {name}")
            app.create_main_menu()
    
    add_button = ctk.CTkButton(
        buttons_frame,
        text="Dodaj źródło",
        font=FONTS['button'],
        width=150,
        height=40,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=8,
        command=validate_and_add
    )
    add_button.pack(side='left', padx=10)
    
    cancel_button = ctk.CTkButton(
        buttons_frame,
        text="Anuluj",
        font=FONTS['button'],
        width=150,
        height=40,
        fg_color=COLORS['card'],
        hover_color=COLORS['bg_secondary'],
        corner_radius=8,
        command=app.create_main_menu
    )
    cancel_button.pack(side='left', padx=10)


def remove_link(app, name, link):

    if not messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć źródło: {name}?"):
        return
    
    links = load_links()
    
    links = [l for l in links if l != (name, link)]
    
    if save_links(links):
        messagebox.showinfo("Sukces", f"Usunięto źródło: {name}")
        app.create_main_menu()
    else:
        messagebox.showerror("Błąd", f"Nie udało się usunąć źródła: {name}")