import time
import requests
from multiprocessing import Process, Queue, set_start_method
import os
import traceback

from func_classification import prepare_classificator, classify_question_llm
from func_llm import prepare_llm, ask_question

set_start_method('spawn', force=True)

def run_classification(queue, queue_r):
    # os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Явно указываем первую видеокарту
    # os.environ['TORCH_USE_CUDA_DSA'] = "0"
    tokenizer, model, classes = prepare_classificator()
    print('----- CLASSIFICATOR READY -----')
    
    while True:
        if not queue.empty():
            data = queue.get()
            classification_res = classify_question_llm(data, tokenizer, model, classes)
            queue_r.put({'class': classification_res})

def run_llm(queue, queue_r):
    # os.environ["CUDA_VISIBLE_DEVICES"] = "1"  # Явно указываем вторую видеокарту
    # os.environ['TORCH_USE_CUDA_DSA'] = "1"
    vectorstore, llm = prepare_llm()
    print('----- LLM READY -----')
    
    while True:
        if not queue.empty():
            data = queue.get()
            llm_answer = ask_question(data, vectorstore, llm)
            queue_r.put({'answer': llm_answer})

def main():
    url = "https://design-by-oz.ru/api/models/query"
    queue_class = Queue()
    queue_llm = Queue()
    queue_r = Queue()

    classification_process = Process(target=run_classification, args=(queue_class, queue_r, ))
    llm_process = Process(target=run_llm, args=(queue_llm, queue_r,))
    classification_process.start()
    llm_process.start()

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json():
                data = response.json()
                query = data['query']
                queue_class.put(query)
                queue_llm.put(query)

                results = {}
                for i in range(2):
                    temp = queue_r.get()
                    print(f'{i}: {temp}')
                    results.update(temp)

                post_response = requests.post(url, json=results)
                if post_response.status_code == 200:
                    print("Data successfully sent to the server.")
                else:
                    print(f"Failed to send data: {post_response.status_code}")
            else:
                # print("No data received or GET request failed.")
                pass
        except Exception as e:
            print('\n\n')
            traceback.print_exc()
            # print(f"An error occurred: {e}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()