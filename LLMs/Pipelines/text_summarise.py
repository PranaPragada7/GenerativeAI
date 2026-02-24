from transformers import pipeline
#: Summarization Pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#  Summarize the text
output = summarizer(
    "Apple Released a new iPhone - iPhone 17 Pro",
    max_length=25,
    min_length=5,
    do_sample=False
)
print(output[0]['summary_text'])

