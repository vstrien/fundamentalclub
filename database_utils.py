import time
import dotenv
import os
from openai import OpenAI, RateLimitError
from config_fundamentalclub import GENERAL_INDEX_NAME
from pinecone import Pinecone
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Top number of results to return
SEARCH_TOP_K = 3
dotenv.load_dotenv()

def tokenize(input_text: str, filename: str):
    """
    Tokenize a text
    """
    tokenizer = tiktoken.encoding_for_model('gpt-4')
    # tokenizer = tiktoken.get_encoding(tokenizer_name)

    def tiktoken_len(text):
        tokens = tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=["\n\n", "\n", " ", ""]
    )

    texts = text_splitter.split_text(input_text)
    chunks = [{
        'id': filename + f'-{i}',
        'text': texts[i],
        'chunk': i
    } for i in range(len(texts))]
    return chunks

def upsert_tokenized_text(chunks, batch_size = 100, embed_model = "text-embedding-ada-002"):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(GENERAL_INDEX_NAME)
    # Open OpenAI client
    oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    from tqdm.auto import tqdm
    for i in tqdm(range(0, len(chunks), batch_size)):
        # find end of batch
        i_end = min(len(chunks), i+batch_size)
        meta_batch = chunks[i:i_end]
        # get ids
        ids_batch = [x['id'] for x in meta_batch]
        # get texts to encode
        texts = [x['text'] for x in meta_batch]

        # create embeddings (try-except added to avoid RateLimitError)
        try:
            res = oai.embeddings.create(input=texts, model=embed_model)
        except RateLimitError:
            done = False
            while not done:
                time.sleep(5)
                try:
                    res = oai.embeddings.create(input=texts, model=embed_model)
                    done = True
                except:
                    pass
        embeds = [record.embedding for record in res.data]
        meta_batch = [{
            'text': x['text'],
            'chunk': x['chunk']
        } for x in meta_batch]
        to_upsert = list(zip(ids_batch, embeds, meta_batch))

        # upsert to Pinecone
        index.upsert(vectors=to_upsert)
    

def upsert_files_in_directory(directory: str):
    """
    Upload all files under a directory to the vector database.
    """
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r") as f:
            content = f.read()
            chunks = tokenize(content, filename)

            print(f"Tokenization complete. {len(chunks)} chunks found.")
            upsert_tokenized_text(chunks)
            print(f"Upserted {filename} to database.")