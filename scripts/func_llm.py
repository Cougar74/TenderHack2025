import os

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from langchain.document_loaders import TextLoader
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from pathlib import Path

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_pdf(file_path):
    reader = PdfReader(file_path)
    documents = []
    
    for i, page in enumerate(reader.pages):
        documents.append({
            "page_content": page.extract_text(),
            "metadata": {
                "source": os.path.basename(file_path),
                "page": i+1,
                "file_type": "pdf"
            }
        })
        
    return documents

def load_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    return [{
        "page_content": text,
        "metadata": {
            "source": os.path.basename(file_path),
            "file_type": "txt"
        }
    }]

def process_documents(documents, text_splitter, embeddings):
    texts = []
    metadatas = []
    
    for doc in documents:
        chunks = text_splitter.split_text(doc["page_content"])
        
        for chunk in chunks:
            texts.append(chunk)
            metadatas.append(doc["metadata"])
    
    return FAISS.from_texts(texts, embeddings, metadatas=metadatas)

def save_llm_model(model_name, save_path):
    Path(save_path).mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    tokenizer.save_pretrained(save_path)
    model.save_pretrained(save_path)
    
def load_local_llm_model(save_path):
    if Path(save_path).exists():
        tokenizer = AutoTokenizer.from_pretrained(save_path)
        model = AutoModelForCausalLM.from_pretrained(save_path)
        return tokenizer, model
    
    return None, None

def initialize_llm(model_name = "IlyaGusev/saiga_llama3_8b",
                  save_path = "./models/saiga_llama3_8b"):
    tokenizer, model = load_local_llm_model(save_path)
    
    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if device == "cuda" else torch.float32
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch_dtype,
            device_map="balanced_low_0" if device == "cuda" else None,
            low_cpu_mem_usage=True
        )
        
        save_llm_model(model_name, save_path)
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15
    )
    
    return HuggingFacePipeline(pipeline=pipe)

def ask_question(question, vectorstore, llm):
    if vectorstore is None:
        return {"answer": "Документы не загружены", "sources": []}
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    result = qa_chain({"query": question})
    
    torch.cuda.empty_cache()
    
    sources = []
    for doc in result["source_documents"]:
        source_info = {
            "document": doc.metadata["source"],
            "content": doc.page_content[:200] + "..."
        }
        if "page" in doc.metadata:
            source_info["page"] = doc.metadata["page"]
        sources.append(source_info)
    
    return {
        "short_answer": result['result'].split('Helpful Answer: ')[-1].split('Final Answer: ')[0].strip(),
        "answer": result["result"].split('Question:')[0].strip(),
        "short_sources": list({'source': t.metadata['source'], 'page': t.metadata['page']} for t in result["source_documents"]),
        "sources": sources,
    }
    
def prepare_llm():
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
    )
    
    llm = initialize_llm()
    
    documents_to_load = list(f'./datasets/{f}' for f in os.listdir('./datasets') if f.endswith('.pdf') | f.endswith('.txt') )
    all_documents = []
    for file_path in documents_to_load:
        if file_path.lower().endswith('.pdf'):
            all_documents.extend(load_pdf(file_path))
        elif file_path.lower().endswith('.txt'):
            all_documents.extend(load_txt(file_path))
    
    vectorstore = process_documents(all_documents, text_splitter, embeddings)
    
    return vectorstore, llm
    
if __name__ == '__main__':
    pass