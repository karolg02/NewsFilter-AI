"""Ekran głównego menu aplikacji"""
import customtkinter as ctk

from config.appearance import COLORS, FONTS
from utils.file_operations import load_links
from utils.feed import get_feed_count


def create_main_menu(app):
    app._clear_main_container()
    
    # Logo i nagłówek
    title_frame = ctk.CTkFrame(app.main_container, fg_color="transparent")
    title_frame.pack(pady=(50, 10))
    
    logo_label = ctk.CTkLabel(
        title_frame,
        text="📰",
        font=("Inter", 48)
    )
    logo_label.pack(pady=(0, 5))
    
    title_label = ctk.CTkLabel(
        title_frame,
        text="NewsFilter AI",
        font=FONTS['title'],
        text_color=COLORS['text']
    )
    title_label.pack()
    
    subtitle = ctk.CTkLabel(
        app.main_container,
        text="Spersonalizowane wiadomości z AI",
        font=FONTS['small'],
        text_color=COLORS['text_secondary']
    )
    subtitle.pack(pady=(0, 30))
    
    # Rama przycisków z nowoczesnym wyglądem
    main_buttons_frame = ctk.CTkFrame(app.main_container, fg_color="transparent")
    main_buttons_frame.pack(pady=10)
    
    download_btn = ctk.CTkButton(
        main_buttons_frame,
        text="📥 Pobierz newsy",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        height=38,
        command=app.download_all_feeds
    )
    download_btn.pack(side="left", padx=6, pady=10)
    
    add_source_btn = ctk.CTkButton(
        main_buttons_frame,
        text="➕ Dodaj źródło",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        height=38,
        command=app.create_add_source_scene
    )
    add_source_btn.pack(side="left", padx=6, pady=10)
    
    label_btn = ctk.CTkButton(
        main_buttons_frame,
        text="✓ Oznacz dane",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        height=38,
        command=app.create_labeling_scene
    )
    label_btn.pack(side="left", padx=6, pady=10)
    
    train_btn = ctk.CTkButton(
        main_buttons_frame,
        text="🤖 Wytrenuj AI",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        height=38,
        command=app.create_train_scene
    )
    train_btn.pack(side="left", padx=6, pady=10)
    
    filter_btn = ctk.CTkButton(
        main_buttons_frame,
        text="🔍 Filtruj interesujące",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        height=38,
        command=app.show_filtered_articles
    )
    filter_btn.pack(side="left", padx=6, pady=10)
    
    # Nagłówek źródeł
    sources_header = ctk.CTkLabel(
        app.main_container,
        text="Twoje źródła",
        font=FONTS['header'],
        text_color=COLORS['text']
    )
    sources_header.pack(pady=(40, 15))
    
    # Lista źródeł
    links = load_links()
    if links:
        sources_frame = ctk.CTkScrollableFrame(
            app.main_container,
            fg_color="transparent",
            width=800,
            height=350
        )
        sources_frame.pack(padx=50, pady=10, fill="both", expand=True)
        
        for name, link in links:
            try:
                count = get_feed_count(link)
            except:
                count = 0
                
            source_card = ctk.CTkFrame(
                sources_frame, 
                fg_color=COLORS['card'],
                corner_radius=8,
                border_width=1,
                border_color=COLORS['border']
            )
            source_card.pack(fill="x", padx=5, pady=8, ipady=2)
            
            source_btn = ctk.CTkButton(
                source_card,
                text=f"{name} ({count})" if count > 0 else name,
                font=FONTS['text'],
                fg_color="transparent",
                hover_color=COLORS['bg_secondary'],
                height=40,
                anchor="w",
                text_color=COLORS['text'],
                command=lambda n=name, l=link: app.fetch_and_display(n, l)
            )
            source_btn.pack(side="left", fill="x", expand=True, padx=(10, 10))
            
            delete_btn = ctk.CTkButton(
                source_card,
                text="🗑️",
                font=FONTS['text'],
                fg_color="transparent",
                hover_color=COLORS['error'],
                text_color=COLORS['text_secondary'],
                width=40,
                corner_radius=6,
                command=lambda n=name, l=link: app.remove_link(n, l)
            )
            delete_btn.pack(side="right", padx=10)
    else:
        no_sources_frame = ctk.CTkFrame(
            app.main_container,
            fg_color=COLORS['bg_secondary'],
            corner_radius=10,
            height=100
        )
        no_sources_frame.pack(pady=30, padx=50, fill="x")
        
        no_sources_label = ctk.CTkLabel(
            no_sources_frame,
            text="Brak dodanych źródeł. Dodaj pierwsze źródło, aby rozpocząć.",
            font=FONTS['text'],
            text_color=COLORS['text_secondary']
        )
        no_sources_label.pack(pady=40)