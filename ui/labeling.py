"""Funkcje do oznaczania danych treningowych"""
import customtkinter as ctk
import pandas as pd
import os
from tkinter import messagebox
from config.appearance import COLORS, FONTS


def create_labeling_scene(app):
    """Tworzy scenę wyboru źródła do oznaczania"""
    app._clear_main_container()
    
    header_label = ctk.CTkLabel(
        app.main_container,
        text="Oznaczanie danych treningowych",
        font=FONTS['header'],
        text_color=COLORS['text']
    )
    header_label.pack(pady=(30, 20))
    
    instruction_label = ctk.CTkLabel(
        app.main_container,
        text="Wybierz źródło artykułów do oznaczenia preferencji:",
        font=FONTS['text'],
        text_color=COLORS['text']
    )
    instruction_label.pack(pady=(0, 20))
    
    try:
        df = pd.read_csv("articles.csv")
        if len(df) == 0:
            no_data_label = ctk.CTkLabel(
                app.main_container,
                text="Brak artykułów do oznaczenia. Najpierw pobierz artykuły.",
                font=FONTS['text'],
                text_color=COLORS['warning']
            )
            no_data_label.pack(pady=50)
            
            back_button = ctk.CTkButton(
                app.main_container,
                text="← Powrót",
                font=FONTS['button'],
                width=120,
                height=40,
                fg_color=COLORS['accent'],
                hover_color=COLORS['accent2'],
                corner_radius=8,
                command=app.create_main_menu
            )
            back_button.pack(pady=20)
            return
        
        sources = df['source'].unique()
        
        sources_frame = ctk.CTkScrollableFrame(
            app.main_container,
            fg_color=COLORS['bg_secondary'],
            width=700,
            height=400
        )
        sources_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        all_sources_button = ctk.CTkButton(
            sources_frame,
            text=f"Wszystkie źródła ({len(df)})",
            font=FONTS['text'],
            height=50,
            fg_color=COLORS['accent'],
            hover_color=COLORS['accent2'],
            corner_radius=8,
            command=lambda: app.start_labeling_session(df)
        )
        all_sources_button.pack(fill='x', pady=5, padx=10)
        
        for source in sources:
            df_source = df[df['source'] == source]
            source_button = ctk.CTkButton(
                sources_frame,
                text=f"{source} ({len(df_source)})",
                font=FONTS['text'],
                height=50,
                fg_color=COLORS['card'],
                hover_color=COLORS['accent'],
                corner_radius=8,
                command=lambda s=df_source: app.start_labeling_session(s)
            )
            source_button.pack(fill='x', pady=5, padx=10)
    
    except FileNotFoundError:
        no_file_label = ctk.CTkLabel(
            app.main_container,
            text="Nie znaleziono pliku articles.csv. Najpierw pobierz artykuły.",
            font=FONTS['text'],
            text_color=COLORS['warning']
        )
        no_file_label.pack(pady=50)
    
    except Exception as e:
        error_label = ctk.CTkLabel(
            app.main_container,
            text=f"Błąd: {str(e)}",
            font=FONTS['text'],
            text_color=COLORS['error']
        )
        error_label.pack(pady=50)
    
    back_button = ctk.CTkButton(
        app.main_container,
        text="← Powrót",
        font=FONTS['button'],
        width=120,
        height=40,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=8,
        command=app.create_main_menu
    )
    back_button.pack(pady=20)


def start_labeling_session(app, df):
    app.labeling_df = df.copy()
    app.labeling_df["label"] = None
    app.labeling_index = 0
    app.labeling_labeled = []
    
    show_labeling_record(app)


def show_labeling_record(app):
    app._clear_main_container()
    
    if app.labeling_index >= len(app.labeling_df):
        show_labeling_summary(app)
        return
    
    record = app.labeling_df.iloc[app.labeling_index]
    
    progress_frame = ctk.CTkFrame(
        app.main_container,
        fg_color=COLORS['bg_secondary'],
        height=50,
        corner_radius=0
    )
    progress_frame.pack(fill='x')
    progress_frame.pack_propagate(False)
    
    progress_text = f"Artykuł {app.labeling_index + 1} z {len(app.labeling_df)}"
    progress_label = ctk.CTkLabel(
        progress_frame,
        text=progress_text,
        font=FONTS['text'],
        text_color=COLORS['text']
    )
    progress_label.pack(side='left', padx=20, pady=10)
    
    exit_button = ctk.CTkButton(
        progress_frame,
        text="Zakończ oznaczanie",
        font=FONTS['button'],
        width=150,
        fg_color=COLORS['error'],
        hover_color="#C62828",
        corner_radius=8,
        command=lambda: show_labeling_summary(app)
    )
    exit_button.pack(side='right', padx=20, pady=5)
    
    content_frame = ctk.CTkScrollableFrame(
        app.main_container,
        fg_color=COLORS['bg_primary']
    )
    content_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    source_date_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    source_date_frame.pack(fill='x')
    
    source_label = ctk.CTkLabel(
        source_date_frame,
        text=f"Źródło: {record['source']}",
        font=FONTS['small'],
        text_color=COLORS['text_secondary']
    )
    source_label.pack(side='left')
    
    if 'date' in record and record['date']:
        date_label = ctk.CTkLabel(
            source_date_frame,
            text=f"Data: {record['date']}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        date_label.pack(side='right')
    
    title_label = ctk.CTkLabel(
        content_frame,
        text=record['title'],
        font=FONTS['header'],
        text_color=COLORS['text'],
        wraplength=800
    )
    title_label.pack(pady=(5, 15))
    
    summary_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['card'], corner_radius=10)
    summary_frame.pack(fill='both', expand=True, pady=5, padx=5)
    
    summary_text = ctk.CTkTextbox(
        summary_frame,
        font=FONTS['text'],
        fg_color="transparent",
        text_color=COLORS['text'],
        wrap="word",
        height=300
    )
    summary_text.pack(fill='both', expand=True, pady=10, padx=10)
    summary_text.insert("1.0", record.get('summary', 'Brak podsumowania.'))
    summary_text.configure(state="disabled")  # Tylko do odczytu
    
    link_label = ctk.CTkLabel(
        content_frame,
        text=f"Link: {record['link']}",
        font=FONTS['small'],
        text_color=COLORS['text_secondary']
    )
    link_label.pack(pady=(10, 20))
    
    buttons_frame = ctk.CTkFrame(app.main_container, fg_color="transparent", height=100)
    buttons_frame.pack(fill='x', padx=20, pady=20)
    buttons_frame.pack_propagate(False)
    
    def mark_and_next(label_value):
        app.labeling_df.at[app.labeling_df.index[app.labeling_index], 'label'] = label_value
        labeled_record = app.labeling_df.iloc[app.labeling_index].to_dict()
        app.labeling_labeled.append(labeled_record)
        app.labeling_index += 1
        show_labeling_record(app)
    
    interesting_button = ctk.CTkButton(
        buttons_frame,
        text="👍 Interesujący",
        font=FONTS['button'],
        width=200,
        height=60,
        fg_color=COLORS['success'],
        hover_color="#2E7D32",
        corner_radius=8,
        command=lambda: mark_and_next(1.0)
    )
    interesting_button.pack(side='left', padx=20, expand=True)
    
    not_interesting_button = ctk.CTkButton(
        buttons_frame,
        text="👎 Nie interesujący",
        font=FONTS['button'],
        width=200,
        height=60,
        fg_color=COLORS['error'],
        hover_color="#C62828",
        corner_radius=8,
        command=lambda: mark_and_next(0.0)
    )
    not_interesting_button.pack(side='right', padx=20, expand=True)


def show_labeling_summary(app):
    app._clear_main_container()
    
    # Nagłówek
    header_label = ctk.CTkLabel(
        app.main_container,
        text="Zakończono oznaczanie",
        font=FONTS['header'],
        text_color=COLORS['text']
    )
    header_label.pack(pady=(50, 30))
    
    if not hasattr(app, 'labeling_labeled') or len(app.labeling_labeled) == 0:
        no_labels_label = ctk.CTkLabel(
            app.main_container,
            text="Nie oznaczono żadnych artykułów.",
            font=FONTS['text'],
            text_color=COLORS['warning']
        )
        no_labels_label.pack(pady=20)
    else:
        labels_df = pd.DataFrame(app.labeling_labeled)
        positive = sum(labels_df['label'] == 1.0)
        negative = sum(labels_df['label'] == 0.0)
        total = len(labels_df)
        
        # Panel z informacjami
        stats_frame = ctk.CTkFrame(app.main_container, fg_color=COLORS['bg_secondary'], corner_radius=10)
        stats_frame.pack(pady=20, padx=50)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"Oznaczono łącznie: {total} artykułów",
            font=FONTS['text'],
            text_color=COLORS['text']
        ).pack(pady=(20, 10), padx=20)
        
        ctk.CTkLabel(
            stats_frame,
            text=f"• Artykuły interesujące: {positive}",
            font=FONTS['text'],
            text_color=COLORS['text']
        ).pack(pady=5, padx=20, anchor='w')
        
        ctk.CTkLabel(
            stats_frame,
            text=f"• Artykuły nieinteresujące: {negative}",
            font=FONTS['text'],
            text_color=COLORS['text']
        ).pack(pady=(5, 20), padx=20, anchor='w')
        
        try:
            if os.path.exists("dane.csv"):
                existing_df = pd.read_csv("dane.csv")
                
                new_df = labels_df[['title', 'summary', 'link', 'date', 'source', 'label']]
                
                for index, row in new_df.iterrows():
                    mask = existing_df['link'] == row['link']
                    if any(mask):
                        existing_df.loc[mask, 'label'] = row['label']
                    else:
                        existing_df = pd.concat([existing_df, pd.DataFrame([row])], ignore_index=True)
                
                existing_df.to_csv("dane.csv", index=False)
            else:
                labels_df[['title', 'summary', 'link', 'date', 'source', 'label']].to_csv("dane.csv", index=False)
            
            success_label = ctk.CTkLabel(
                app.main_container,
                text="Dane zostały zapisane do pliku dane.csv",
                font=FONTS['text'],
                text_color=COLORS['success']
            )
            success_label.pack(pady=20)
            
        except Exception as e:
            # Błąd zapisu
            error_label = ctk.CTkLabel(
                app.main_container,
                text=f"Błąd zapisu danych: {str(e)}",
                font=FONTS['text'],
                text_color=COLORS['error']
            )
            error_label.pack(pady=20)
    
    back_button = ctk.CTkButton(
        app.main_container,
        text="Powrót do menu",
        font=FONTS['button'],
        width=200,
        height=40,
        fg_color=COLORS['accent'],
        hover_color=COLORS['accent2'],
        corner_radius=8,
        command=app.create_main_menu
    )
    back_button.pack(pady=30)