from pinecone import Pinecone
import torch
from sentence_transformers import SentenceTransformer
from transformers import BartTokenizer, BartForConditionalGeneration

def answer(query):
    context = query_pinecone(query, top_k=10)
    query = format_query(query, context["matches"])
    answer=generate_answer(query)
    return answer
    

def query_pinecone(query, top_k):

    xq = retriever.encode([query]).tolist()

    xc = index.query(vector=xq, top_k=top_k, include_metadata=True)
    return xc

def format_query(query, context):

    context = [f"<P> {m['metadata']['Abstract']}" for m in context]

    context = " ".join(context)

    query = f"question: {query} context: {context}"
    return query

def generate_answer(query):

    inputs = tokenizer([query], max_length=1024, return_tensors="pt").to(device)

    ids = generator.generate(inputs["input_ids"], num_beams=2, min_length=20, max_length=60)

    answer = tokenizer.batch_decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return answer


api_key = '<Paste Pinecone API key here>'


pc = Pinecone(api_key=api_key)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

index_name = "hydro-question-answering"
index = pc.Index(index_name)


retriever = SentenceTransformer("flax-sentence-embeddings/all_datasets_v3_mpnet-base", device=device)


tokenizer = BartTokenizer.from_pretrained('vblagoje/bart_lfqa')
generator = BartForConditionalGeneration.from_pretrained('vblagoje/bart_lfqa').to(device)