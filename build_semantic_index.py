import argparse
import os
import logging

from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Build semantic index from Mojo manual using ChromaDB and OpenAI.')
parser.add_argument('--log-level', dest='log_level', default='INFO', help='Set the log level (debug, info, error)')
parser.add_argument('--input-directory', required=True, dest='input_directory', help='Set the input directory')
parser.add_argument('--db-output', required=True, dest='db_output', help='Set where to store final database file.')


def main():
    args = parser.parse_args()
    logging.getLogger().setLevel(args.log_level.upper())
    documents = []

    logger.info(f'Building ChromaDB from "{args.input_directory}" directory.')
    for root, _, files in os.walk(args.input_directory):
        for file in files:
            input_file_path = os.path.join(root, file)

            if file.endswith('.md'):
                raw_documents = TextLoader(input_file_path).load()
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                docs = text_splitter.split_documents(raw_documents)
                for d in docs:
                    d.metadata['source_link'] = f'https://docs.modular.com/{input_file_path.replace("/docs", "").replace(".md", "")}'
                documents.extend(docs)
                logger.info(f'Adding {input_file_path} file to documents')
            else:
                logger.info(f'Ignoring {input_file_path} (not a notebook or markdown file)')

    logger.info('Starting build vector index.')
    Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory=args.db_output)
    logger.info('Conversion and copying completed.')


if __name__ == '__main__':
    main()