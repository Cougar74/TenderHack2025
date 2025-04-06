import time
import requests

from func_classification import prepare_classificator, classify_question_llm
from func_llm import prepare_llm, ask_question

tokenizer, model, classes = prepare_classificator()
vectorstore, llm = prepare_llm()

def process_data(data):
    classification_res = classify_question_llm(data, tokenizer, model, classes)
    llm_answer = ask_question(data, vectorstore, llm)
    
    return {
        'class': classification_res,
        'answer': llm_answer,
    }

def main():
    url = "https://design-by-oz.ru:12349/api/models/query"

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json():
                data = response.json()
                
                send_data = process_data(data['query'])
                post_response = requests.post(url, json=send_data)
                if post_response.status_code == 200:
                    print("Data successfully sent to the server.")
                else:
                    print(f"Failed to send data: {post_response.status_code}")
            else:
                print("No data received or GET request failed.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()