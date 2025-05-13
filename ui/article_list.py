"""Widok listy artykułów z danego źródła"""
import customtkinter as ctk
import pandas as pd
from config.appearance import COLORS, FONTS


def create_articles_view(app, feed_name, df_filtered):
    """Tworzy widok listy artykułów z określonego źródła"""
    app._clear_main_container()
    app.current_feed_name = feed_name
    app.current_df = df_filtered
    
    # Pasek górny
    top_frame = ctk.CTkFrame(
        app.main_container,
        fg_color=COLORS['bg_secondary'],
        height=60,
        corner_radius=0
    )
    top_frame.pack(fill='x')
    top_frame.pack_propagate(False)
    
    back_button = ctk.CTkButton(
        top_frame,
        text="← Menu",
        font=FONTS['button'],
        width=100,
        height=36,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        command=app.create_main_menu
    )
    back_button.pack(side='left', padx=20, pady=12)
    
    title_label = ctk.CTkLabel(
        top_frame,
        text=feed_name,
        font=FONTS['header'],
        text_color=COLORS['text']
    )
    title_label.pack(side='left', padx=15, pady=15)
    
    # Pasek wyszukiwania
    search_frame = ctk.CTkFrame(
        app.main_container,
        fg_color=COLORS['bg_secondary'],
        height=60
    )
    search_frame.pack(fill='x', pady=2)
    search_frame.pack_propagate(False)
    
    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Wyszukaj w artykułach...",
        width=300,
        height=36,
        font=FONTS['text'],
        corner_radius=6
    )
    search_entry.pack(side='left', padx=20, pady=10)
    
    search_button = ctk.CTkButton(
        search_frame,
        text="🔍 Szukaj",
        font=FONTS['button'],
        width=100,
        height=36,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        command=lambda: search_articles(search_entry.get())
    )
    search_button.pack(side='left', padx=5, pady=10)
    
    if 'predicted_prob' in df_filtered.columns:
        sort_btn = ctk.CTkButton(
            search_frame,
            text="Sortuj wg AI",
            font=FONTS['button'],
            width=110,
            height=36,
            fg_color=COLORS['success'],  
            hover_color="#3D8B40",
            corner_radius=6,
            command=lambda: refresh_articles(df_filtered.sort_values('predicted_prob', ascending=False))
        )
        sort_btn.pack(side='right', pady=10, padx=20)
    
    # Rama artykułów
    articles_container = ctk.CTkFrame(
        app.main_container,
        fg_color=COLORS['bg_primary']
    )
    articles_container.pack(fill='both', expand=True)
    
    articles_frame = ctk.CTkScrollableFrame(
        articles_container,
        fg_color=COLORS['bg_primary'],
        corner_radius=0
    )
    articles_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    def search_articles(query):
        if not query:
            refresh_articles(df_filtered)
            return
            
        query = query.lower()
        filtered = df_filtered[
            df_filtered['title'].str.lower().str.contains(query, na=False) | 
            df_filtered['summary'].str.lower().str.contains(query, na=False)
        ]
        
        refresh_articles(filtered)
    
    def refresh_articles(filtered_df):
        for widget in articles_frame.winfo_children():
            widget.destroy()
            
        if filtered_df is None or len(filtered_df) == 0:
            no_results = ctk.CTkLabel(
                articles_frame,
                text="Brak artykułów do wyświetlenia",
                font=FONTS['text'],
                text_color=COLORS['text_secondary']
            )
            no_results.pack(pady=50)
            return
        
        for i, row in filtered_df.iterrows():
            article_card = ctk.CTkFrame(
                articles_frame,
                fg_color=COLORS['card'],
                corner_radius=10,
                border_width=1,
                border_color=COLORS['border']
            )
            article_card.pack(fill='x', pady=8, padx=5)
            
            # Dodaj oznaczenie dla proponowanych artykułów
            title_frame = ctk.CTkFrame(
                article_card,
                fg_color="transparent"
            )
            title_frame.pack(fill='x', pady=(8, 0), padx=12)
            
            article_btn = ctk.CTkButton(
                title_frame,
                text=row['title'],
                font=FONTS['text'],
                anchor="w",
                fg_color="transparent", 
                hover_color=COLORS['bg_secondary'],
                text_color=COLORS['text'],
                height=40,
                corner_radius=0,
                command=lambda r=row: app.show_article_details(r)
            )
            article_btn.pack(side="left", fill="x", expand=True)
            
            # Zmiana z 0.7 na 0.6 - artykuły powyżej 60% otrzymają etykietę
            if 'predicted_prob' in row and row['predicted_prob'] > 0.6:
                ai_badge = ctk.CTkLabel(
                    title_frame,
                    text="Proponowane",
                    font=("Inter", 10),
                    text_color=COLORS['success'],
                    fg_color=COLORS['bg_secondary'],
                    corner_radius=4,
                    padx=8,
                    pady=2
                )
                ai_badge.pack(side="right", pady=(0, 0))
            
            # Dodaj podsumowanie i datę
            details_frame = ctk.CTkFrame(
                article_card,
                fg_color="transparent"
            )
            details_frame.pack(fill='x', pady=(0, 8), padx=14)
            
            summary = row.get('summary', '')
            if len(summary) > 100:
                summary = summary[:100] + "..."
                
            summary_label = ctk.CTkLabel(
                details_frame,
                text=summary,
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                anchor="w",
                wraplength=700,
                justify="left"
            )
            summary_label.pack(anchor="w", pady=(0, 5))
            
            meta_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            meta_frame.pack(fill='x')
            
            if 'date' in row and row['date']:
                date_label = ctk.CTkLabel(
                    meta_frame,
                    text=row['date'],
                    font=FONTS['small'],
                    text_color=COLORS['text_secondary']
                )
                date_label.pack(side='left')
            
            if 'source' in row and row['source']:
                source_label = ctk.CTkLabel(
                    meta_frame,
                    text=f"Źródło: {row['source']}",
                    font=FONTS['small'],
                    text_color=COLORS['text_secondary']
                )
                source_label.pack(side='right')

    refresh_articles(df_filtered)


def fetch_and_display(app, feed_name, feed_url):
    """Pobiera i wyświetla artykuły z określonego źródła, filtrując przez model ML"""
    import pandas as pd
    from utils.feed import fetch_feed
    
    df = fetch_feed(feed_url)
    
    if df is not None and not df.empty:
        # Tutaj dodajemy predykcję i filtrowanie
        try:
            from data.model_trainer import predict_on_dataframe
            # Próba zastosowania modelu na danych
            df_predicted = predict_on_dataframe(df)
            if 'predicted_prob' in df_predicted.columns:
                # Sortuj według przewidywań (najciekawsze na górze)
                df = df_predicted.sort_values('predicted_prob', ascending=False)
                # Możesz dodać również filtrowaie np.:
                # df = df_predicted[df_predicted['predicted_prob'] > 0.5]
        except:
            # Jeśli model nie zadziała, pokazujemy dane bez filtrowania
            pass
            
        app.create_articles_view(f"{feed_name} (filtrowane)", df)
    else:
        from tkinter import messagebox
        messagebox.showerror("Błąd", f"Nie udało się pobrać danych z {feed_name}")