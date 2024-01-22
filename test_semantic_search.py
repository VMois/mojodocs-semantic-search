import argparse
import logging

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Execute semantic search query on selected ChromaDB.')
parser.add_argument('--log-level', dest='log_level', default='INFO', help='Set the log level (debug, info, error)')
parser.add_argument('--db-input', required=True, dest='db_input', help='Path to database folder.')


def main():
    args = parser.parse_args()
    query = input('Enter your query: ')
    db = Chroma(persist_directory=args.db_input, embedding_function=OpenAIEmbeddings())
    docs = db.similarity_search(query)
    logger.info(f'Found {len(docs)} documents.')
    logger.info(f'Top result: {docs[0].page_content}')
    logger.info(f'Top result (source link): {docs[0].metadata["source_link"]}')


if __name__ == '__main__':
    main()
