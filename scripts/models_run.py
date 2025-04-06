import time
import requests
from multiprocessing import Process, Queue, set_start_method
import os

from func_classification import prepare_classificator, classify_question_llm
from func_llm import prepare_llm, ask_question

set_start_method('spawn', force=True)

def run_classification(queue):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Явно указываем первую видеокарту
    tokenizer, model, classes = prepare_classificator()
    while True:
        if not queue.empty():
            data = queue.get()
            classification_res = classify_question_llm(data, tokenizer, model, classes)
            queue.put({'class': classification_res})

def run_llm(queue):
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"  # Явно указываем вторую видеокарту
    vectorstore, llm = prepare_llm()
    while True:
        if not queue.empty():
            data = queue.get()
            llm_answer = ask_question(data, vectorstore, llm)
            queue.put({'answer': llm_answer})

def main():
    url = "https://design-by-oz.ru/api/models/query"
    queue = Queue()

    classification_process = Process(target=run_classification, args=(queue,))
    llm_process = Process(target=run_llm, args=(queue,))
    classification_process.start()
    llm_process.start()

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json():
                data = response.json()
                query = data['query']
                queue.put(query)

                results = {}
                for _ in range(2):
                    results.update(queue.get())

                post_response = requests.post(url, json=results)
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