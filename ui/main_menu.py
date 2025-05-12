"""Ekran głównego menu aplikacji"""
import customtkinter as ctk

from config.appearance import COLORS, FONTS
from utils.file_operations import load_links
from utils.feed import get_feed_count


def create_main_menu(app):
    app._clear_main_container()
    
    title_label = ctk.CTkLabel(
        app.main_container,
        text="NewsFilter AI",
        font=FONTS['title'],
        text_color=COLORS['text']
    )
    title_label.pack(pady=(50, 30))
    
    main_buttons_frame = ctk.CTkFrame(app.main_container, fg_color="transparent")
    main_buttons_frame.pack(pady=10)
    
    download_btn = ctk.CTkButton(
        main_buttons_frame,
        text="📥 Pobierz newsy",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        command=app.download_all_feeds
    )
    download_btn.pack(side="left", padx=10, pady=10)
    
    add_source_btn = ctk.CTkButton(
        main_buttons_frame,
        text="➕ Dodaj źródło",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        command=app.create_add_source_scene
    )
    add_source_btn.pack(side="left", padx=10, pady=10)
    
    label_btn = ctk.CTkButton(
        main_buttons_frame,
        text="✓ Oznacz dane",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        command=app.create_labeling_scene
    )
    label_btn.pack(side="left", padx=10, pady=10)
    
    train_btn = ctk.CTkButton(
        main_buttons_frame,
        text="🤖 Wytrenuj AI",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        command=app.create_train_scene
    )
    train_btn.pack(side="left", padx=10, pady=10)
    
    sources_header = ctk.CTkLabel(
        app.main_container,
        text="Twoje źródła:",
        font=FONTS['header'],
        text_color=COLORS['text']
    )
    sources_header.pack(pady=(30, 10))
    
    links = load_links()
    if links:
        sources_frame = ctk.CTkScrollableFrame(
            app.main_container,
            fg_color=COLORS['bg_secondary'],
            width=800,
            height=350
        )
        sources_frame.pack(padx=50, pady=10, fill="both", expand=True)
        
        for name, link in links:
            try:
                count = get_feed_count(link)
            except:
                count = 0
                
            source_row = ctk.CTkFrame(sources_frame, fg_color="transparent")
            source_row.pack(fill="x", padx=5, pady=5)
            
            source_btn = ctk.CTkButton(
                source_row,
                text=f"{name} ({count})" if count > 0 else name,
                font=FONTS['text'],
                fg_color=COLORS['card'],
                hover_color=COLORS['accent'],
                height=40,
                anchor="w",
                command=lambda n=name, l=link: app.fetch_and_display(n, l)
            )
            source_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            delete_btn = ctk.CTkButton(
                source_row,
                text="🗑️",
                font=FONTS['text'],
                fg_color=COLORS['error'],
                hover_color="#C62828",
                width=40,
                command=lambda n=name, l=link: app.remove_link(n, l)
            )
            delete_btn.pack(side="right", padx=0)
    else:
        no_sources_label = ctk.CTkLabel(
            app.main_container,
            text="Brak dodanych źródeł. Dodaj pierwsze źródło, aby rozpocząć.",
            font=FONTS['text'],
            text_color=COLORS['text_secondary']
        )
        no_sources_label.pack(pady=50)