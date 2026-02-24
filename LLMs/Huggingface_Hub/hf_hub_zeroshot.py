from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
candidate_labels = ["sports", "politics", "technology"]
sentence = "The new iPhone has amazing features and a great camera."
result = classifier(sentence, candidate_labels)
print(result)
