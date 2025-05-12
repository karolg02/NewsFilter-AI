"""Widok listy artykułów z danego źródła"""
import customtkinter as ctk
import pandas as pd
from config.appearance import COLORS, FONTS


def create_articles_view(app, feed_name, df_filtered):
    """Tworzy widok listy artykułów z określonego źródła"""
    app._clear_main_container()
    app.current_feed_name = feed_name  # Zapisz dla kontekstu
    app.current_df = df_filtered       # Zapisz dla kontekstu
    
    top_panel = ctk.CTkFrame(
        app.main_container,
        fg_color=COLORS['bg_secondary'],
        height=70,
        corner_radius=0
    )
    top_panel.pack(fill='x')
    top_panel.pack_propagate(False)
    
    back_button = ctk.CTkButton(
        top_panel,
        text="← Powrót",
        font=FONTS['button'],
        width=100,
        height=40,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=8,
        command=app.create_main_menu
    )
    back_button.pack(side='left', padx=20, pady=15)
    
    header = ctk.CTkLabel(
        top_panel,
        text=feed_name,
        font=FONTS['header'],
        text_color=COLORS['text']
    )
    header.pack(side='left', padx=20)
    
    search_var = ctk.StringVar()
    search_frame = ctk.CTkFrame(app.main_container, fg_color="transparent")
    search_frame.pack(fill='x', pady=(10, 0), padx=20)
    
    search_entry = ctk.CTkEntry(
        search_frame,
        textvariable=search_var,
        font=FONTS['text'],
        width=600,
        placeholder_text="Szukaj w nagłówkach..."
    )
    search_entry.pack(side='left', pady=10, padx=(0, 10), fill='x', expand=True)
    
    articles_frame = ctk.CTkScrollableFrame(
        app.main_container,
        fg_color=COLORS['bg_primary'],
        width=1200,
        height=600
    )
    articles_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    def refresh_articles():
        for widget in articles_frame.winfo_children():
            widget.destroy()
        
        query = search_var.get().lower()
        
        if query:
            filtered = df_filtered[df_filtered['title'].str.lower().str.contains(query)]
        else:
            filtered = df_filtered
        
        if filtered.empty:
            no_results = ctk.CTkLabel(
                articles_frame,
                text="Brak artykułów spełniających kryteria wyszukiwania",
                font=FONTS['text'],
                text_color=COLORS['text_secondary']
            )
            no_results.pack(pady=50)
            return
        
        for i, row in filtered.iterrows():
            article_frame = ctk.CTkFrame(
                articles_frame,
                fg_color=COLORS['card'],
                corner_radius=10,
                height=80
            )
            article_frame.pack(fill='x', pady=5, padx=5)
            
            date_label = ctk.CTkLabel(
                article_frame,
                text=row.get('date', ''),
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            date_label.pack(anchor='w', padx=15, pady=(10, 0))
            
            article_btn = ctk.CTkButton(
                article_frame,
                text=row['title'],
                font=FONTS['text'],
                height=40,
                anchor='w',
                fg_color="transparent",
                hover_color=COLORS['accent'],
                text_color=COLORS['text'],
                command=lambda r=row: app.show_article_details(r)
            )
            article_btn.pack(fill='x', pady=(5, 10), padx=10)
            
            article_frame.bind("<Button-1>", lambda e, r=row: app.show_article_details(r))
    
    search_var.trace_add("write", lambda *args: refresh_articles())

    refresh_articles()


def fetch_and_display(app, feed_name, feed_url):
    import pandas as pd
    from tkinter import messagebox
    
    app._clear_main_container()

    loading_label = ctk.CTkLabel(
        app.main_container,
        text="Wczytuję artykuły...",
        font=FONTS['header']
    )
    loading_label.pack(pady=50)
    app.update()
    
    try:
        df = pd.read_csv("articles.csv")
        df_filtered = df[df['source'] == feed_name]
        
        if df_filtered.empty:
            messagebox.showinfo("Informacja", 
                               f"Brak artykułów dla źródła {feed_name}. Pobierz artykuły.")
            app.create_main_menu()
            return
        
        create_articles_view(app, feed_name, df_filtered)
        
    except FileNotFoundError:
        messagebox.showerror("Błąd", 
                            "Plik articles.csv nie istnieje. Pobierz artykuły.")
        app.create_main_menu()
    except Exception as e:
        messagebox.showerror("Błąd", 
                            f"Wystąpił problem podczas wczytywania artykułów: {str(e)}")
        app.create_main_menu()