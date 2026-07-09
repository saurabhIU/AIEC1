from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyMuPDFLoader
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from app.rag import tiktoken_len

load_dotenv()

@lru_cache(maxsize=1)
def _build_generator_clients():
    from ragas.llms import llm_factory
    from ragas.embeddings import embedding_factory
    
    client = OpenAI(api_key=os.environ["GENERATOR_API_KEY"])
    llm = llm_factory(os.environ.get("GENERATOR_MODEL_NAME"), provider="openai", client=client)
    embeddings = embedding_factory(
                        provider="openai",
                        model=os.environ.get("GENERATOR_EMBEDDING_MODEL"),
                        client=client)
    return llm, embeddings

def run_ragas_sync(func, *args, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(func, *args, **kwargs).result()

def generate_testset(data_dir: str, test_size: int = 5) -> pd.DataFrame:
    
    from ragas.testset import TestsetGenerator
    from ragas.testset.transforms import default_transforms_for_prechunked, CustomNodeFilter

    generator_llm, generator_embeddings = _build_generator_clients()
    try:
        directory_loader = DirectoryLoader(
            data_dir, glob="**/*.pdf", loader_cls=PyMuPDFLoader
        )
        documents = directory_loader.load()
    except Exception as ex:
        raise RuntimeError(f"Failed to load PDFs from '{data_dir}'") from ex
    
    if not documents:
        raise ValueError(f"No PDF documents found in {data_dir}")

    
    generation_splitter = RecursiveCharacterTextSplitter(
    chunk_size=int(os.environ.get("RAG_CHUNK_SIZE", 900))    ,
    chunk_overlap=int(os.environ.get("RAG_CHUNK_OVERLAP", 70)),
    length_function=tiktoken_len,
    )
    generation_chunks = generation_splitter.split_documents(documents)

    generation_transforms = [
    transform
    for transform in default_transforms_for_prechunked(
        llm=generator_llm,
        embedding_model=generator_embeddings,
    )
    if not isinstance(transform, CustomNodeFilter)
    ]

    generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)
    testset = run_ragas_sync(generator.generate_with_chunks,
        chunks=generation_chunks,
        testset_size=test_size,   
        transforms=generation_transforms,
    )
    synthetic_testset_df = testset.to_pandas()      # to_pandas() is on the Testset result
    return synthetic_testset_df[["user_input",
                        "reference",
                        "reference_contexts"]].copy()