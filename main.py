"""Główny plik aplikacji NewsFilter AI"""
from ui.base_app import BaseApp
from ui.main_menu import create_main_menu
from ui.article_list import create_articles_view, fetch_and_display  # Dodaj import funkcji
from ui.article_detail import show_article_details
from ui.labeling import create_labeling_scene, start_labeling_session
from ui.sources_manager import create_add_source_scene, remove_link

from data.dataset import download_all_feeds, mark_as_not_interesting
from data.model_trainer import create_train_scene

from utils.file_operations import load_links, add_link


class NewsApp(BaseApp):
    
    def __init__(self):
        super().__init__()
        self.create_main_menu()
        
    def create_main_menu(self):
        create_main_menu(self)
        
    def create_articles_view(self, feed_name, df_filtered):
        create_articles_view(self, feed_name, df_filtered)
        
    def show_article_details(self, article_data):
        show_article_details(self, article_data)
        
    def create_labeling_scene(self):
        create_labeling_scene(self)
        
    def start_labeling_session(self, df):
        start_labeling_session(self, df)
        
    def download_all_feeds(self):
        download_all_feeds(self)
        
    def create_add_source_scene(self):
        create_add_source_scene(self)
        
    def mark_as_not_interesting(self, article_data):
        mark_as_not_interesting(self, article_data)
        
    def create_train_scene(self):
        create_train_scene(self)
        
    def remove_link(self, name, link):
        remove_link(self, name, link)
        
    def fetch_and_display(self, feed_name, feed_url):
        fetch_and_display(self, feed_name, feed_url)
        
    def show_filtered_articles(self):
        from data.model_trainer import predict_articles
        from tkinter import messagebox
        import pandas as pd
        
        df, error = predict_articles()
        
        if error:
            messagebox.showerror("Błąd", error)
            return
            
        if df is None or len(df) == 0:
            messagebox.showinfo("Informacja", "Brak artykułów do wyświetlenia.")
            return
        
        interesting_df = df[df['predicted_prob'] > 0.7].sort_values('predicted_prob', ascending=False)
        
        if len(interesting_df) == 0:
            messagebox.showinfo("Informacja", "Brak interesujących artykułów według modelu.")
            return
            
        self.create_articles_view("Interesujące artykuły", interesting_df)


if __name__ == "__main__":
    app = NewsApp()
    app.mainloop()