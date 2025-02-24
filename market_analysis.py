from flask import Flask, request, jsonify, Response
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze_news():
    """ วิเคราะห์ข่าวและส่งคืนค่า sentiment (Positive, Neutral, Negative) """
    data = request.json
    news_list = data.get("news", [])

    if not news_list:
        return jsonify({"error": "No news provided"}), 400

    analyzed_news = []
    for news in news_list:
        sentiment_score = analyzer.polarity_scores(news["title"])["compound"]
        sentiment = "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"
        analyzed_news.append({**news, "sentiment": sentiment})

    return jsonify(analyzed_news)

@app.route('/market-trend', methods=['GET'])
def market_trend():
    """ คำนวณแนวโน้มตลาดจากค่าของข่าว """
    response = analyze_news()

    if isinstance(response, Response):
        news_data = json.loads(response.get_data(as_text=True))
    else:
        return Response(json.dumps({"error": "No news analyzed"}, ensure_ascii=False),
                        content_type="application/json; charset=utf-8", status=400)

    # นับจำนวนข่าวที่เป็น Positive และ Negative
    positive_count = sum(1 for item in news_data if item["sentiment"] == "Positive")
    negative_count = sum(1 for item in news_data if item["sentiment"] == "Negative")

    # สร้างแนวโน้มตลาด
    trend = "Bullish 📈" if positive_count > negative_count else "Bearish 📉"

    return jsonify({"trend": trend})

if __name__ == '__main__':
    print("✅ Flask Server กำลังเริ่มทำงาน...")
    app.run(port=5001, debug=True)
