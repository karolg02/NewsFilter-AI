import pandas as pd
import joblib

# Wczytaj model i wektorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Wczytaj nowe artykuły
df = pd.read_csv("articles.csv")
df["text"] = df["title"].fillna("") + " " + df["summary"].fillna("")

# Zamień tekst na wektory
X = vectorizer.transform(df["text"])

# Przewidywanie
predictions = model.predict(X)
df["predicted_label"] = predictions

# Zapisz do nowego pliku
df.to_csv("articles_predicted.csv", index=False)
print(f"✅ Przewidziano etykiety dla {len(df)} artykułów i zapisano do articles_predicted.csv")