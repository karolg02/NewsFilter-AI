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
    
    sort_btn = ctk.CTkButton(
        search_frame,
        text="Sortuj wg AI",
        command=lambda: refresh_articles(df_filtered.sort_values('predicted_prob', ascending=False) 
                      if 'predicted_prob' in df_filtered.columns else df_filtered)
    )
    sort_btn.pack(side='right', pady=10, padx=10)
    
    articles_frame = ctk.CTkScrollableFrame(
        app.main_container,
        fg_color=COLORS['bg_primary'],
        width=1200,
        height=600
    )
    articles_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    def refresh_articles(filtered_df=None):
        for widget in articles_frame.winfo_children():
            widget.destroy()
        
        query = search_var.get().lower()
        
        if query:
            filtered = df_filtered[df_filtered['title'].str.lower().str.contains(query)]
        else:
            filtered = df_filtered
        
        if filtered_df is not None:
            filtered = filtered_df
        
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
            
            title_frame = ctk.CTkFrame(
                article_frame,
                fg_color="transparent"
            )
            title_frame.pack(fill='x', pady=(5, 0), padx=10)
            
            if 'predicted_prob' in row and row['predicted_prob'] > 0.7:
                ai_label = ctk.CTkLabel(
                    title_frame,
                    text="proponowane poprzez AI",
                    font=("Helvetica", 9),
                    text_color="#4CAF50",  # zielony kolor
                    padx=5
                )
                ai_label.pack(side="right", pady=(0, 0))
            
            article_btn = ctk.CTkButton(
                title_frame,
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
            
            if 'predicted_prob' in row:
                prob = row['predicted_prob'] * 100
                confidence = f" [AI: {prob:.0f}%]" if prob > 50 else ""
                article_btn.configure(text=row['title'] + confidence)
            
            article_frame.bind("<Button-1>", lambda e, r=row: app.show_article_details(r))
    
    search_var.trace_add("write", lambda *args: refresh_articles())

    refresh_articles()


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