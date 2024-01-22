import argparse
import os
import logging
import shutil

import nbformat
from nbconvert import MarkdownExporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Convert Mojo docs to Markdown.')
parser.add_argument('--log-level', dest='log_level', default='INFO', help='Set the log level (debug, info, error)')
parser.add_argument('--input-directory', dest='input_directory', help='Set the input directory')
parser.add_argument('--output-directory', dest='output_directory', help='Set the output directory')


if __name__ == '__main__':
    args = parser.parse_args()
    logging.getLogger().setLevel(args.log_level.upper())

    logger.info(f'Converting notebooks to Markdown in "{args.input_directory}" directory.')
    for root, dirs, files in os.walk(args.input_directory):
        for file in files:
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(args.output_directory, root, file)

            if file.endswith('.ipynb'):
                logger.info(f'Converting {input_file_path} to Markdown.')
                notebook = nbformat.read(input_file_path, as_version=4)
                exporter = MarkdownExporter()
                body, resources = exporter.from_notebook_node(notebook)
                output_file_path = output_file_path.replace('.ipynb', '.md')

                logger.info(f'Writing file to {output_file_path}.')
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                with open(output_file_path, 'w') as f:
                    f.write(body)
            elif file.endswith('.md'):
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                shutil.copy(input_file_path, output_file_path)
                logger.info(f'Copying {input_file_path} to {output_file_path}')
            else:
                logger.info(f'Ignoring {file} (not a notebook or markdown file)')

    logger.info('Conversion and copying complete.')