import requests
from flask import Flask, request, jsonify
from func_classification import prepare_classificator, classify_question_llm

app = Flask(__name__)

# Подготовка классификатора
tokenizer, model, classes = prepare_classificator()

@app.route('/classify', methods=['POST'])
def classify_request():
    data = request.json
    if not data or 'query' not in data or 'answer' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    query = data['query']
    llm_answer = data['answer']
    classification_res = classify_question_llm(query, tokenizer, model, classes)

    # Отправляем результат через POST
    result = {
        'class': classification_res,
        'answer': llm_answer
    }
    response = requests.post("https://design-by-oz.ru/api/models/query", json=result)
    if response.status_code == 200:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': 'Failed to send data to server'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
