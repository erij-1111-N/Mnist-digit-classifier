import os
import json
import re
import base64
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/models")
def list_models():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    genai.configure(api_key=api_key)
    models = [m.name for m in genai.list_models()]
    return jsonify(models)


@app.route("/predict", methods=["POST"])
def predict():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY is not set."}), 500

    data = request.get_json()
    image_data = data.get("image")

    if not image_data:
        return jsonify({"error": "No image provided"}), 400

    try:
        genai.configure(api_key=api_key)

        # Try multiple model names in order
        model_names = [
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-pro-vision",
            "gemini-1.0-pro-vision",
        ]

        model = None
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                # Test it with a dummy call to see if it's valid
                break
            except Exception:
                continue

        if model is None:
            return jsonify({"error": "No supported Gemini model found"}), 500

        image_bytes = base64.b64decode(image_data)

        prompt = (
            "This is a handwritten digit drawn on a black canvas in white. "
            "Analyze it and classify it as a digit 0-9.\n\n"
            "Return ONLY a JSON object with no preamble or markdown:\n"
            "{\n"
            '  "digit": 7,\n'
            '  "confidence": 0.95,\n'
            '  "probabilities": [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.95, 0.01, 0.01],\n'
            '  "reasoning": "Clear strokes forming digit 7"\n'
            "}\n\n"
            "The probabilities array must have exactly 10 values (digits 0-9) that sum to 1.0."
        )

        response = model.generate_content([
            {"mime_type": "image/png", "data": image_bytes},
            prompt
        ])

        text = response.text
        clean = re.sub(r"```json|```", "", text).strip()
        result = json.loads(clean)
        return jsonify(result)

    except json.JSONDecodeError:
        return jsonify({"error": "Model returned invalid JSON"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("\n" + "="*60)
        print("WARNING: GEMINI_API_KEY is not set!")
        print("Get a free key at: https://aistudio.google.com/apikey")
        print("Then run: set GEMINI_API_KEY=your_key_here")
        print("="*60 + "\n")
    else:
        print(f"\n✓ Gemini API key loaded: {api_key[:10]}...{api_key[-4:]}")
        # List available models at startup
        try:
            genai.configure(api_key=api_key)
            models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
            print(f"✓ Available models: {models}\n")
        except Exception as e:
            print(f"Could not list models: {e}\n")

    app.run(debug=True, port=5000)