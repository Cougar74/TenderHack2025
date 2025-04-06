import time
import requests
from func_llm import prepare_llm, ask_question

# Подготовка LLM
vectorstore, llm = prepare_llm()

def main_loop():
    url = "https://design-by-oz.ru/api/models/query"
    
    while True:
        response = requests.get(url)
        if response.status_code == 200 and response.json():
            data = response.json()
            query = data['query']
        
            llm_answer = ask_question(query, vectorstore, llm)

            response = requests.post("http://localhost:5001/classify", json={'query': query, 'answer': llm_answer})
            if response.status_code == 200:
                print("Успешно отправлено во второй скрипт")
            else:
                print("Ошибка: не удалось отправить данные во второй скрипт")

        time.sleep(0.5)

if __name__ == '__main__':
    main_loop()
