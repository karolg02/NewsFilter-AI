import os
import json
from tkinter import messagebox


def load_links(filename="links.txt"):
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                links = []
                for line in f:
                    try:
                        name, url = line.strip().split(";;;")
                        links.append((name, url))
                    except ValueError:
                        pass
                return links
        return []
    except Exception as e:
        print(f"Error loading links: {e}")
        return []


def save_links(links, filename="links.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for name, url in links:
                f.write(f"{name};;;{url}\n")
        return True
    except Exception as e:
        print(f"Error saving links: {e}")
        return False


def add_link(app, name, url):
    links = load_links()
    
    for existing_name, existing_url in links:
        if existing_name.lower() == name.lower():
            messagebox.showerror("Błąd", f"Źródło o nazwie '{name}' już istnieje.")
            return False
        if existing_url.lower() == url.lower():
            messagebox.showerror("Błąd", f"URL '{url}' jest już dodany jako '{existing_name}'.")
            return False
    
    links.append((name, url))
    if save_links(links):
        app.create_main_menu() 
        return True
    else:
        messagebox.showerror("Błąd", "Nie udało się zapisać źródła.")
        return False


def remove_source(name, url):
    links = load_links()
    links = [link for link in links if link != (name, url)]
    return save_links(links)