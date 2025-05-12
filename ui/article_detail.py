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
        height=70,
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
        width=120,
        height=40,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=8,
        command=back_command
    )
    back_button.pack(side='left', padx=20, pady=15)
    
    content_frame = ctk.CTkScrollableFrame(
        app.main_container,
        fg_color=COLORS['bg_primary']
    )
    content_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    title_label = ctk.CTkLabel(
        content_frame,
        text=article_data['title'],
        font=FONTS['header'],
        text_color=COLORS['text'],
        wraplength=800
    )
    title_label.pack(pady=(10, 5))
    
    if 'date' in article_data and article_data['date']:
        date_label = ctk.CTkLabel(
            content_frame,
            text=article_data['date'],
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        date_label.pack(pady=(0, 15))
    
    if 'source' in article_data and article_data['source']:
        source_label = ctk.CTkLabel(
            content_frame,
            text=f"Źródło: {article_data['source']}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        source_label.pack(pady=(0, 15))
    
    content_box_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['card'], corner_radius=10)
    content_box_frame.pack(fill='both', expand=True, pady=10, padx=5)
    
    view_mode_var = ctk.StringVar(value="summary")
    
    summary_box = ctk.CTkTextbox(
        content_box_frame,
        font=FONTS['text'],
        fg_color="transparent",
        text_color=COLORS['text'],
        wrap="word",
        height=400
    )
    summary_box.pack(fill='both', expand=True, pady=10, padx=10)
    summary_box.insert("1.0", article_data.get('summary', 'Brak podsumowania.'))
    summary_box.configure(state="disabled")
    
    ai_summary_box = None
    
    def toggle_view():
        nonlocal ai_summary_box
        
        if view_mode_var.get() == "summary":
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
                        fg_color="transparent",
                        text_color=COLORS['text'],
                        wrap="word",
                        height=400
                    )
                    ai_summary_box.insert("1.0", summary)
                    ai_summary_box.configure(state="disabled")
                    ai_summary_box.pack(fill='both', expand=True, pady=10, padx=10)
                    
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
                ai_summary_box.pack(fill='both', expand=True, pady=10, padx=10)
            
            view_mode_var.set("ai_summary")
            toggle_button.configure(text="Pokaż oryginalny opis")
        else:
            if ai_summary_box:
                ai_summary_box.pack_forget()
            summary_box.pack(fill='both', expand=True, pady=10, padx=10)
            view_mode_var.set("summary")
            toggle_button.configure(text="Pokaż streszczenie AI")
    
    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame.pack(fill='x', pady=15)
    
    toggle_button = ctk.CTkButton(
        button_frame,
        text="Pokaż streszczenie AI",
        font=FONTS['button'],
        width=200,
        height=40,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=8,
        command=toggle_view
    )
    toggle_button.pack(side='left', padx=10)
    
    browser_button = ctk.CTkButton(
        button_frame,
        text="🌐 Otwórz w przeglądarce",
        font=FONTS['button'],
        width=200,
        height=40,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=8,
        command=lambda: webbrowser.open(article_data['link'])
    )
    browser_button.pack(side='left', padx=10)
    
    not_interesting_button = ctk.CTkButton(
        button_frame,
        text="👎 Nie interesuje mnie",
        font=FONTS['button'],
        width=200,
        height=40,
        fg_color=COLORS['error'],
        hover_color="#C62828",
        corner_radius=8,
        command=lambda: app.mark_as_not_interesting(article_data)
    )
    not_interesting_button.pack(side='right', padx=10)