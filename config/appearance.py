"""Konfiguracja wyglądu aplikacji"""

# === Kolory ===
COLORS = {
    'bg_primary': '#1E1E2E',
    'bg_secondary': '#2D2D44',
    'accent': '#5C7EBF',
    'accent2': '#4A66A0',
    'text': '#E0E0E0',
    'text_secondary': '#A0A0C0',
    'border': '#3A3A5A',
    'error': '#E57373',
    'success': '#81C784',
    'card': '#252538',
    'warning': '#FFA726'
}

# === Czcionki ===
FONTS = {
    'title': ("Roboto", 36, "bold"),
    'header': ("Roboto", 24),
    'text': ("Roboto", 14),
    'button': ("Roboto Medium", 14),
    'small': ("Roboto Light", 12)
}

def configure_theme():
    """Konfiguracja globalnego motywu CustomTkinter"""
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")