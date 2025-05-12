from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import traceback  # ← 追加！

app = Flask(__name__)

# Gemini APIキー設定
genai.configure(api_key="AIzaSyBdUuk7kdfb7wijwFRue9wRIjluEcFms6o")

# モデルの準備
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# フロントエンドのHTMLを返す
@app.route("/")
def index():
    return render_template("index.html")

# 解析リクエスト処理
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    sentence = data.get("sentence")

    prompt = f"""
以下の英文について、以下の3点を日本語で丁寧に説明してください：

1. 各単語の品詞（名詞・動詞・形容詞など）をリスト形式で  
2. 文の構文構造（主語・述語・目的語など）を簡潔に説明  
3. 各単語の意味を日本語で示す（単語と訳を対応させて）  
4. 最後にその文を覚えやすくするためのコメントを1文付けてください

英文: "{sentence}"

出力形式:

---
📘 入力文:
[英文を表示]

🧠 品詞一覧:
1. ...
2. ...

🔧 構文構造:
- 主語: ...
- 動詞: ...
- 目的語: ...

📚 単語の意味:
- 単語: 意味
- ...

💡 コメント:
[文を覚えるヒントやポイント]
---
"""

    try:
        response = model.generate_content(prompt)
        output = getattr(response, "text", None)

        if not output:
            return jsonify({"error": "Geminiからの応答が空でした。"}), 500

        return jsonify({"result": output})
    
    except Exception as e:
        # ターミナルにエラー内容を出力
        print("=== Geminiエラー発生 ===")
        print(traceback.format_exc())
        return jsonify({"error": "サーバーでエラーが発生しました。"}), 500

if __name__ == "__main__":
    app.run(debug=True)
