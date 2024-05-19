from pinecone import Pinecone
import torch
from sentence_transformers import SentenceTransformer
from transformers import BartTokenizer, BartForConditionalGeneration

def answer(query):
    context = query_pinecone(query, top_k=10)
    query = format_query(query, context["matches"])
    answer=generate_answer(query1)
    return answer
    

def query_pinecone(query, top_k):
    # generate embeddings for the query
    xq = retriever.encode([query]).tolist()
    # search pinecone index for context passage with the answer
    xc = index.query(vector=xq, top_k=top_k, include_metadata=True)
    return xc

def format_query(query, context):
    # extract Abstract from Pinecone search result and add the <P> tag
    context = [f"<P> {m['metadata']['Abstract']}" for m in context]

    context = " ".join(context)

    query = f"question: {query} context: {context}"
    return query

def generate_answer(query):
    # tokenize the query to get input_ids
    inputs = tokenizer([query], max_length=1024, return_tensors="pt").to(device)
    # use generator to predict output ids
    ids = generator.generate(inputs["input_ids"], num_beams=2, min_length=20, max_length=60)
    # use tokenizer to decode the output ids
    answer = tokenizer.batch_decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return answer

# Set the API key directly in the code
api_key = '87ccee14-0002-43e7-ad34-7fe0c3750adf'

# Initialize the Pinecone client using the API key
pc = Pinecone(api_key=api_key)
# set device to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'

index_name = "hydro-question-answering"
index = pc.Index(index_name)

# load the retriever model from huggingface model hub
retriever = SentenceTransformer("flax-sentence-embeddings/all_datasets_v3_mpnet-base", device=device)
retriever

# load bart tokenizer and model from huggingface
tokenizer = BartTokenizer.from_pretrained('vblagoje/bart_lfqa')
generator = BartForConditionalGeneration.from_pretrained('vblagoje/bart_lfqa').to(device)

query1 = "what are the different methods of hydrogen storage?"
context = query_pinecone(query1, top_k=10)
query1 = format_query(query1, context["matches"])
generate_answer(query1)