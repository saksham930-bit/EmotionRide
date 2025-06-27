from transformers import pipeline

print("⏳ Loading emotion model...")

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)

print("✅ Model loaded successfully!")

def detect_emotion(text):
    result = emotion_classifier(text)
    print("DEBUG:", result)

    if isinstance(result[0], list):
        result = result[0][0]
    else:
        result = result[0]

    label = result['label']
    score = result['score']
    return label, round(score, 2)
