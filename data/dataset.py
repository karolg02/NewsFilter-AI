"""Funkcje do zarządzania danymi"""
import os
import pandas as pd
from tkinter import messagebox

from utils.file_operations import load_links
from utils.feed import download_feeds_to_dataframe


def download_all_feeds(app):
    links = load_links()
    if not links:
        messagebox.showerror("Błąd", "Brak źródeł. Najpierw dodaj źródła.")
        return False
    
    try:
        app._clear_main_container()
        import customtkinter as ctk
        from config.appearance import FONTS
        
        info_label = ctk.CTkLabel(
            app.main_container, 
            text="Pobieram artykuły...", 
            font=FONTS['header']
        )
        info_label.pack(pady=50)
        app.update()
        
        df = download_feeds_to_dataframe(links)
        
        df.to_csv("articles.csv", index=False)

        app.create_main_menu()
        messagebox.showinfo("Sukces", f"Pobrano {len(df)} artykułów.")
        return True
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem podczas pobierania: {str(e)}")
        app.create_main_menu()
        return False


def mark_as_not_interesting(app, article_data):
    """Zapisuje artykuł do dane.csv z oznaczeniem 0 (nieinteresujący)"""
    article = article_data.copy()
    article['label'] = 0.0  # Oznaczamy jako nieinteresujący
    
    df_article = pd.DataFrame([article])
    
    try:
        if os.path.exists("dane.csv"):
            df_existing = pd.read_csv("dane.csv")
            if not df_existing[df_existing['link'] == article['link']].empty:
                df_existing.loc[df_existing['link'] == article['link'], 'label'] = 0.0
                df_existing.to_csv("dane.csv", index=False)
                messagebox.showinfo("Zapisano", "Zaktualizowano oznaczenie artykułu jako nieinteresujący.")
            else:
                df_combined = pd.concat([df_existing, df_article])
                df_combined.to_csv("dane.csv", index=False)
                messagebox.showinfo("Zapisano", "Dodano artykuł jako nieinteresujący do bazy treningowej.")
        else:
            df_article.to_csv("dane.csv", index=False)
            messagebox.showinfo("Zapisano", "Dodano artykuł jako nieinteresujący do nowej bazy treningowej.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać oznaczenia: {str(e)}")


def get_labeled_data():
    if os.path.exists("dane.csv"):
        try:
            df = pd.read_csv("dane.csv")
            return df[df['label'].notna()]
        except Exception as e:
            print(f"Error loading labeled data: {e}")
    
    return pd.DataFrame()


def save_predictions(df_with_predictions):
    try:
        df_with_predictions.to_csv("articles_predicted.csv", index=False)
        return True
    except Exception as e:
        print(f"Error saving predictions: {e}")
        return False
    
def get_predicted_articles(threshold=0.5):
    """Zwraca artykuły przewidziane jako interesujące"""
    try:
        if os.path.exists("articles_predicted.csv"):
            df = pd.read_csv("articles_predicted.csv")
            return df[df['predicted_prob'] > threshold]
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading predicted articles: {e}")
        return pd.DataFrame()