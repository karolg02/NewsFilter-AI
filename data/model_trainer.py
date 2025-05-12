"""Moduł do trenowania modelu ML"""
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from tkinter import messagebox

from data.dataset import get_labeled_data
from config.appearance import COLORS, FONTS


def create_train_scene(app):
    app._clear_main_container()
    
    import customtkinter as ctk
    
    ctk.CTkLabel(
        app.main_container, 
        text="Trening modelu AI", 
        font=FONTS['header']
    ).pack(pady=(30, 20))
    
    info_text = "Trenuj model na oznaczonych danych, aby automatycznie\n"
    info_text += "klasyfikować nowe artykuły według twoich preferencji."
    
    ctk.CTkLabel(
        app.main_container,
        text=info_text,
        font=FONTS['text'],
    ).pack(pady=(0, 30))

    try:
        df = get_labeled_data()
        positive = len(df[df['label'] == 1])
        negative = len(df[df['label'] == 0])
        
        status_frame = ctk.CTkFrame(app.main_container, fg_color=COLORS['bg_secondary'])
        status_frame.pack(pady=20, padx=50, fill='x')
        
        ctk.CTkLabel(status_frame, text="Status oznaczeń:", font=FONTS['text']).pack(pady=(10,5))
        ctk.CTkLabel(status_frame, text=f"Artykuły interesujące: {positive}", font=FONTS['small']).pack(pady=2)
        ctk.CTkLabel(status_frame, text=f"Artykuły nieinteresujące: {negative}", font=FONTS['small']).pack(pady=2)
        ctk.CTkLabel(status_frame, text=f"Razem oznaczonych: {positive + negative}", font=FONTS['small']).pack(pady=(2,10))
        
        if positive < 2 or negative < 2:
            ctk.CTkLabel(
                status_frame,
                text="⚠️ Za mało oznaczeń! Oznacz przynajmniej po 2 artykuły jako interesujące i nieinteresujące.",
                font=FONTS['small'],
                text_color="#FFA726"
            ).pack(pady=(0,10))
    except Exception as e:
        print(f"Error getting labeled data stats: {e}")
    
    button_frame = ctk.CTkFrame(app.main_container, fg_color="transparent")
    button_frame.pack(pady=30)
    
    train_button = ctk.CTkButton(
        button_frame,
        text="Trenuj model",
        font=FONTS['button'],
        command=lambda: train_model(app)
    )
    train_button.pack(side="left", padx=10)
    
    back_button = ctk.CTkButton(
        button_frame,
        text="Powrót",
        font=FONTS['button'],
        command=app.create_main_menu
    )
    back_button.pack(side="left", padx=10)


def train_model(app):
    app._clear_main_container()
    
    import customtkinter as ctk

    info_label = ctk.CTkLabel(
        app.main_container, 
        text="Trenuję model...", 
        font=FONTS['header']
    )
    info_label.pack(pady=50)
    app.update()

    try:
        df = get_labeled_data()
        if len(df) < 4:
            messagebox.showerror("Błąd", "Za mało oznaczonych danych (minimum 4).")
            app.create_train_scene()
            return
        
        unique_labels = df["label"].unique()
        if len(unique_labels) < 2:
            messagebox.showerror("Błąd", "Potrzebujesz oznaczeń obu klas (0 i 1).")
            app.create_train_scene()
            return
            
        label_counts = df["label"].value_counts()
        min_count = min(label_counts)
        if min_count < 2:
            messagebox.showerror("Błąd", f"Potrzebujesz co najmniej 2 przykładów dla każdej klasy. Najmniejsza klasa ma {min_count}.")
            app.create_train_scene()
            return
        
        df["text"] = df["title"].fillna("") + " " + df["summary"].fillna("")
        
        df_majority = df[df.label == 1]
        df_minority = df[df.label == 0]
        
        if len(df_minority) < len(df_majority):
            df_minority_upsampled = resample(
                df_minority,
                replace=True,
                n_samples=len(df_majority),
                random_state=42
            )
            df_balanced = pd.concat([df_majority, df_minority_upsampled])
        elif len(df_majority) < len(df_minority):
            df_majority_upsampled = resample(
                df_majority,
                replace=True,
                n_samples=len(df_minority),
                random_state=42
            )
            df_balanced = pd.concat([df_majority_upsampled, df_minority])
        else:
            df_balanced = df
        
        X = df_balanced["text"]
        y = df_balanced["label"]
        
        min_class_count = min(df_balanced["label"].value_counts())
        test_size = 0.5 if min_class_count < 3 else 0.2
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, stratify=y, test_size=test_size, random_state=42
        )

        vectorizer = TfidfVectorizer(max_features=3000)
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)
        
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train_vec, y_train)
        
        joblib.dump(model, "model.pkl")
        joblib.dump(vectorizer, "vectorizer.pkl")
        
        y_pred = model.predict(X_test_vec)
        report = classification_report(y_test, y_pred)
        
        app._clear_main_container()
        
        ctk.CTkLabel(
            app.main_container, 
            text="Model wytrenowany pomyślnie!", 
            font=FONTS['header']
        ).pack(pady=(20, 10))

        results_frame = ctk.CTkFrame(app.main_container, fg_color=COLORS['bg_secondary'])
        results_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        ctk.CTkLabel(
            results_frame,
            text="Raport wyników:",
            font=FONTS['text'],
            anchor="w"
        ).pack(pady=(10, 0), padx=20, anchor="w")
        
        metrics_text = ctk.CTkTextbox(results_frame, width=600, height=300)
        metrics_text.pack(pady=10, padx=20, fill='both', expand=True)
        metrics_text.insert("1.0", f"{report}")
        metrics_text.configure(state="disabled")
        
        ctk.CTkLabel(
            app.main_container,
            text="✅ Model i wektor zapisane jako model.pkl i vectorizer.pkl",
            font=FONTS['text'],
            text_color=COLORS['success']
        ).pack(pady=(0, 10))
        
        ctk.CTkButton(
            app.main_container,
            text="Powrót do menu",
            command=app.create_main_menu
        ).pack(pady=20)
        
    except Exception as e:
        app._clear_main_container()
        ctk.CTkLabel(
            app.main_container, 
            text=f"Wystąpił błąd podczas trenowania:\n{str(e)}", 
            font=FONTS['text']
        ).pack(pady=50)
        
        ctk.CTkButton(
            app.main_container,
            text="Powrót",
            command=app.create_train_scene
        ).pack(pady=20)


def predict_articles():
    """Przewiduje kategorie dla nowych artykułów"""
    try:
        if not os.path.exists("model.pkl") or not os.path.exists("vectorizer.pkl"):
            return None, "Brak wytrenowanego modelu. Najpierw wytrenuj model."
        
        if not os.path.exists("articles.csv"):
            return None, "Brak artykułów. Najpierw pobierz artykuły."
        
        model = joblib.load("model.pkl")
        vectorizer = joblib.load("vectorizer.pkl")
        
        df = pd.read_csv("articles.csv")

        df["text"] = df["title"].fillna("") + " " + df["summary"].fillna("")
        
        X = vectorizer.transform(df["text"])
        
        df["predicted_label"] = model.predict(X)
        df["predicted_prob"] = model.predict_proba(X)[:, 1]
        
        df.to_csv("articles_predicted.csv", index=False)
        
        return df, None
        
    except Exception as e:
        return None, str(e)


def predict_on_dataframe(df):
    """Wykonuje predykcję na dataframe i zwraca df z dodatkową kolumną predicted_prob"""
    import pandas as pd
    import os
    
    # Próbuj najpierw odczytać istniejące predykcje
    try:
        if os.path.exists("articles_predicted.csv"):
            df_predicted = pd.read_csv("articles_predicted.csv")
            
            # Znajdź pasujące artykuły po linku lub tytule
            merged = pd.merge(
                df, 
                df_predicted[['link', 'predicted_prob']], 
                on='link', 
                how='left'
            )
            
            # Jeśli udało się znaleźć predykcje, użyj ich
            if 'predicted_prob' in merged.columns and not merged['predicted_prob'].isna().all():
                return merged
    except Exception as e:
        print(f"Błąd podczas wczytywania predictions: {e}")
    
    # Jeśli nie udało się odczytać predykcji, spróbuj użyć modelu
    try:
        import pickle
        import joblib
        
        if os.path.exists('model.pkl') and os.path.exists('vectorizer.pkl'):
            try:
                # Najpierw próbujemy z joblib (bardziej niezawodny)
                model = joblib.load('model.pkl')
                vectorizer = joblib.load('vectorizer.pkl')
            except:
                # Jeśli nie zadziałało, próbujemy standardowym pickle
                with open('model.pkl', 'rb') as f:
                    model = pickle.load(f)
                with open('vectorizer.pkl', 'rb') as f:
                    vectorizer = pickle.load(f)
            
            # Przygotuj dane
            texts = df['title'].fillna('') + ' ' + df['summary'].fillna('')
            
            # Wektoryzuj teksty
            X = vectorizer.transform(texts)
            
            # Wykonaj predykcję
            predictions = model.predict_proba(X)[:, 1]
            
            # Dodaj predykcje do dataframe
            df['predicted_prob'] = predictions
            
            return df
    except Exception as e:
        print(f"Error podczas predykcji: {e}")
    
    # Jeśli wszystko zawiedzie, zwróć oryginalny dataframe
    return df