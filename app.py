from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import regex
from collections import Counter
import emoji
import os

nltk.download('vader_lexicon')

app = Flask(__name__)

# Ensure the 'uploads' folder exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')


# Function to analyze sentiment and emojis in the uploaded chat file
def analyze_sentiment(file_path):
    with open(file_path, encoding="utf-8") as fp:
        lines = fp.readlines()

    data = []
    for line in lines:
        if line.strip():
            data.append(line.strip())

    df = pd.DataFrame(data, columns=["Message"])
    sentiments = SentimentIntensityAnalyzer()

    # Sentiment calculations
    df["Positive"] = df["Message"].apply(lambda x: sentiments.polarity_scores(x)["pos"])
    df["Negative"] = df["Message"].apply(lambda x: sentiments.polarity_scores(x)["neg"])
    df["Neutral"] = df["Message"].apply(lambda x: sentiments.polarity_scores(x)["neu"])

    positive_score = df["Positive"].sum()
    negative_score = df["Negative"].sum()
    neutral_score = df["Neutral"].sum()

    def extract_emojis(text):
        return [word for word in regex.findall(r'\X', text) if any(char in emoji.EMOJI_DATA for char in word)]

    df["Emojis"] = df["Message"].apply(extract_emojis)
    emoji_list = [item for sublist in df["Emojis"] for item in sublist]
    emoji_count = Counter(emoji_list)

    overall_sentiment = "Neutral"
    if positive_score > max(negative_score, neutral_score):
        overall_sentiment = "Positive"
    elif negative_score > max(positive_score, neutral_score):
        overall_sentiment = "Negative"

    return {
        "overall_sentiment": overall_sentiment,
        "positive_score": positive_score,
        "negative_score": negative_score,
        "neutral_score": neutral_score,
        "top_emojis": emoji_count.most_common(10)
    }


# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(url_for("index"))

        file = request.files["file"]
        if file.filename == "":
            return redirect(url_for("index"))

        # Save the uploaded file
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Analyze sentiment and emojis
        analysis = analyze_sentiment(file_path)
        return render_template("index.html", analysis=analysis)

    return render_template("index.html", analysis=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
