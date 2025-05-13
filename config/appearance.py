"""Konfiguracja wyglądu aplikacji"""

# === Kolory ===
COLORS = {
    'bg_primary': '#121212',      # Ciemniejsze tło
    'bg_secondary': '#1E1E1E',    # Lżejsze tło
    'accent': '#4F6BFF',          # Nowoczesny niebieski akcent
    'accent2': '#3D56E0',         # Ciemniejszy akcent do hover
    'text': '#F5F5F5',            # Jaśniejszy biały tekst
    'text_secondary': '#A0A0A0',  # Jaśniejszy szary
    'border': '#2A2A2A',          # Subtelniejsze obramowanie
    'error': '#FF5252',           # Jaśniejszy czerwony
    'success': '#4CAF50',         # Zieleń
    'card': '#1A1A1A',            # Tło kart
    'warning': '#FFC107'          # Żółty
}

# === Czcionki ===
FONTS = {
    'title': ("Inter", 36, "bold"),
    'header': ("Inter", 22),
    'text': ("Inter", 13),
    'button': ("Inter Medium", 13),
    'small': ("Inter Light", 11)
}

def configure_theme():
    """Konfiguracja globalnego motywu CustomTkinter"""
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")