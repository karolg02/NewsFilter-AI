import re
from collections import Counter


def generate_summary(text, title):
    if not text or len(text) < 100:
        return "Nie udało się wygenerować streszczenia (za mało tekstu)."
    
    sentence_delimiters = r'[.!?][\s]{1,2}(?=[A-ZŚĄĘĆŃÓŁŹŻ])'
    sentences = re.split(sentence_delimiters, text)
    sentences = [s.strip() + "." for s in sentences if s and len(s.strip()) > 30]
    
    if len(sentences) < 3:
        return "Nie udało się wygenerować streszczenia (za mało zdań)."
    
    stop_words = {'i', 'w', 'na', 'z', 'do', 'że', 'to', 'o', 'jak', 'a', 'po',
                  'lub', 'ale', 'przez', 'dla', 'więc', 'się', 'of', 'the', 'in',
                  'nie', 'być', 'jest', 'są', 'and', 'to', 'from', 'czy', 'co'}
    
    words = re.findall(r'\w+', text.lower())
    words = [word for word in words if len(word) > 3 and word not in stop_words]
    
    word_freq = Counter(words)
    
    title_words = set(re.findall(r'\w+', title.lower()))
    title_words = {w for w in title_words if len(w) > 3 and w not in stop_words}
    
    def score_sentence(sentence, index):
        sentence_lower = sentence.lower()
        sentence_words = set(re.findall(r'\w+', sentence_lower))
        
        score = 0.0
        
        if index < 3:
            score += 2.0  # Zdania na początku
        elif index > len(sentences) - 5:
            score += 1.0  # Zdania na końcu
            
        length = len(sentence_words)
        if 8 <= length <= 20:
            score += 1.0  # Optymalna długość
        elif length > 30:
            score -= 1.0  # Za długie
            
        # Słowa z tytułu
        title_overlap = sum(1 for word in title_words if word in sentence_words)
        score += title_overlap * 2.0
        
        # Ważne słowa z tekstu (częste słowa)
        important_words = sum(word_freq[word] for word in sentence_words if word in word_freq)
        score += important_words / 10.0
        
        # Frazy wskazujące na podsumowanie lub ważne informacje
        indicator_phrases = ['podsumowując', 'najważniejsze', 'kluczowe', 'w rezultacie',
                            'oznacza to', 'dlatego', 'w konsekwencji', 'ostatecznie']
        for phrase in indicator_phrases:
            if phrase in sentence_lower:
                score += 2.0
                
        return score
    
    scored_sentences = [(score_sentence(s, i), i, s) for i, s in enumerate(sentences)]
    
    num_sentences = min(5, max(3, len(sentences) // 10))
    
    scored_sentences.sort(reverse=True)
    top_sentences = scored_sentences[:num_sentences]

    summary_sentences = sorted([(i, s) for _, i, s in top_sentences])

    summary = f"📝 STRESZCZENIE ARTYKUŁU\n\n"
    summary += '\n\n'.join([s for _, s in summary_sentences])
    
    return summary