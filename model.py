import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.utils import resample
import joblib

df = pd.read_csv("dane.csv")
if "label" not in df or len(set(df["label"])) < 2 or min(df["label"].value_counts()) < 2:
    print("Za mało przykładów w jednej z klas! Oznacz przynajmniej po dwa artykuły jako 0 i 1.")
    exit(1)

df["text"] = df["title"].fillna("") + " " + df["summary"].fillna("")

df_majority = df[df.label == 1]
df_minority = df[df.label == 0]

df_minority_upsampled = resample(
    df_minority,
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)

df_balanced = pd.concat([df_majority, df_minority_upsampled])

if len(df_balanced) < 4 or min(df_balanced["label"].value_counts()) < 2:
    print("Za mało danych po zbalansowaniu! Oznacz więcej artykułów jako 0 i 1.")
    exit(1)

# Dane i etykiety
X = df_balanced["text"]
y = df_balanced["label"]

min_class_count = min(df_balanced["label"].value_counts())
if min_class_count < 3:
    test_size = 0.5
else:
    test_size = 0.2

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=test_size, random_state=42
)

vectorizer = TfidfVectorizer(max_features=3000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)
print(classification_report(y_test, y_pred))

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("✅ Model i wektor zapisane jako model.pkl i vectorizer.pkl")
