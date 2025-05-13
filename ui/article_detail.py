"""Widok szczegółów artykułu"""
import customtkinter as ctk
import webbrowser
import requests
from config.appearance import COLORS, FONTS
from content.extraction import extract_article_content
from content.summarizer import generate_summary


def show_article_details(app, article_data):
    app._clear_main_container()
    
    top_frame = ctk.CTkFrame(
        app.main_container,
        fg_color=COLORS['bg_secondary'],
        height=60,
        corner_radius=0
    )
    top_frame.pack(fill='x')
    top_frame.pack_propagate(False)
    
    back_command = app.create_main_menu
    if app.current_feed_name and app.current_df is not None:
        back_command = lambda: app.create_articles_view(app.current_feed_name, app.current_df)
    
    back_button = ctk.CTkButton(
        top_frame,
        text="← Powrót",
        font=FONTS['button'],
        width=100,
        height=36,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        command=back_command
    )
    back_button.pack(side='left', padx=20, pady=12)
    
    # Artykuł
    content_frame = ctk.CTkScrollableFrame(
        app.main_container,
        fg_color=COLORS['bg_primary']
    )
    content_frame.pack(fill='both', expand=True, padx=0, pady=0)
    
    article_card = ctk.CTkFrame(
        content_frame,
        fg_color=COLORS['card'],
        corner_radius=15,
        border_width=1,
        border_color=COLORS['border']
    )
    article_card.pack(fill='x', expand=True, padx=40, pady=20)
    
    # Nagłówek artykułu
    header_frame = ctk.CTkFrame(
        article_card,
        fg_color="transparent"
    )
    header_frame.pack(fill='x', padx=25, pady=(25, 10))
    
    title_label = ctk.CTkLabel(
        header_frame,
        text=article_data['title'],
        font=FONTS['header'],
        text_color=COLORS['text'],
        wraplength=800,
        justify="center"
    )
    title_label.pack(pady=(0, 12))
    
    meta_frame = ctk.CTkFrame(
        header_frame,
        fg_color="transparent",
        height=30
    )
    meta_frame.pack(fill='x')
    
    if 'date' in article_data and article_data['date']:
        date_label = ctk.CTkLabel(
            meta_frame,
            text=article_data['date'],
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        date_label.pack(side='left')
    
    if 'source' in article_data and article_data['source']:
        source_label = ctk.CTkLabel(
            meta_frame,
            text=f"Źródło: {article_data['source']}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        source_label.pack(side='right')
    
    # Separator
    separator = ctk.CTkFrame(article_card, height=1, fg_color=COLORS['border'])
    separator.pack(fill='x', pady=(10, 0), padx=20)
    
    # Treść artykułu
    content_box_frame = ctk.CTkFrame(article_card, fg_color="transparent")
    content_box_frame.pack(fill='both', expand=True, pady=15, padx=25)
    
    # Zakładki treści (podsumowanie oryginalne/AI)
    view_mode_var = ctk.StringVar(value="summary")
    
    tab_frame = ctk.CTkFrame(content_box_frame, fg_color="transparent", height=40)
    tab_frame.pack(fill='x')
    
    def switch_to_summary():
        view_mode_var.set("summary")
        summary_tab.configure(fg_color=COLORS['accent'])
        ai_tab.configure(fg_color="transparent")
        toggle_view()
        
    def switch_to_ai():
        view_mode_var.set("ai_summary")
        ai_tab.configure(fg_color=COLORS['accent'])
        summary_tab.configure(fg_color="transparent")
        toggle_view()
    
    summary_tab = ctk.CTkButton(
        tab_frame,
        text="Podsumowanie oryginalne",
        font=FONTS['button'],
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        command=switch_to_summary
    )
    summary_tab.pack(side='left', padx=(0, 5))
    
    ai_tab = ctk.CTkButton(
        tab_frame,
        text="Streszczenie AI",
        font=FONTS['button'],
        fg_color="transparent",
        hover_color=COLORS['accent2'],
        corner_radius=6,
        command=switch_to_ai
    )
    ai_tab.pack(side='left')
    
    summary_box = ctk.CTkTextbox(
        content_box_frame,
        font=FONTS['text'],
        fg_color=COLORS['bg_secondary'],
        text_color=COLORS['text'],
        wrap="word",
        height=400,
        corner_radius=6,
        border_width=1,
        border_color=COLORS['border']
    )
    summary_box.pack(fill='both', expand=True, pady=(15, 20))
    summary_box.insert("1.0", article_data.get('summary', 'Brak podsumowania.'))
    summary_box.configure(state="disabled")
    
    ai_summary_box = None
    
    def toggle_view():
        nonlocal ai_summary_box
        
        if view_mode_var.get() == "summary":
            if ai_summary_box:
                ai_summary_box.pack_forget()
            summary_box.pack(fill='both', expand=True, pady=(15, 20))
        else:
            summary_box.pack_forget()
            
            if ai_summary_box is None:
                loading_label = ctk.CTkLabel(
                    content_box_frame,
                    text="Generuję streszczenie artykułu...",
                    font=FONTS['text']
                )
                loading_label.pack(pady=40)
                app.update()
                
                try:
                    response = requests.get(article_data['link'], timeout=10)
                    response.raise_for_status()
                    raw_html = response.text
                    
                    article_text = extract_article_content(raw_html)
                    
                    summary = generate_summary(article_text, article_data['title'])

                    loading_label.destroy()
                    
                    ai_summary_box = ctk.CTkTextbox(
                        content_box_frame,
                        font=FONTS['text'],
                        fg_color=COLORS['bg_secondary'],
                        text_color=COLORS['text'],
                        wrap="word",
                        height=400,
                        corner_radius=6,
                        border_width=1,
                        border_color=COLORS['border']
                    )
                    ai_summary_box.insert("1.0", summary)
                    ai_summary_box.configure(state="disabled")
                    ai_summary_box.pack(fill='both', expand=True, pady=(15, 20))
                    
                except Exception as e:
                    loading_label.destroy()
                    error_label = ctk.CTkLabel(
                        content_box_frame,
                        text=f"Nie udało się wygenerować streszczenia: {str(e)}",
                        font=FONTS['text'],
                        text_color=COLORS['error'],
                        wraplength=700
                    )
                    error_label.pack(pady=40)
                    ai_summary_box = error_label
            else:
                ai_summary_box.pack(fill='both', expand=True, pady=(15, 20))
    
    # Przyciski akcji
    button_frame = ctk.CTkFrame(article_card, fg_color="transparent", height=50)
    button_frame.pack(fill='x', pady=(5, 25), padx=25)
    
    browser_button = ctk.CTkButton(
        button_frame,
        text="🌐 Otwórz w przeglądarce",
        font=FONTS['button'],
        width=200,
        height=40,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=6,
        command=lambda: webbrowser.open(article_data['link'])
    )
    browser_button.pack(side='left', padx=5)
    
    not_interesting_button = ctk.CTkButton(
        button_frame,
        text="👎 Nie interesuje mnie",
        font=FONTS['button'],
        width=200,
        height=40,
        fg_color=COLORS['error'],
        hover_color="#C62828",
        corner_radius=6,
        command=lambda: app.mark_as_not_interesting(article_data)
    )
    not_interesting_button.pack(side='right', padx=5)