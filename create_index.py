import os
import pinecone
from langchain.vectorstores import Pinecone
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from pathlib import Path

os.environ["OPENAI_API_KEY"] = "api_key"
#os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
#Note: If running protobuf > 3.20.x, you may want to attempt to set this environment variable after importing the os library,
#as the Pinecone clients may not import otherwise. If this doesn't work, downgrade protobuf to 3.20.x or lower and run rest of script.

pdf_folder_path = Path('.../imdb_reviews/')

loaders = DirectoryLoader(pdf_folder_path)
docs = loaders.load()

embeddings = OpenAIEmbeddings()

pinecone.init(api_key="api_key", environment="environment")
pinecone.create_index("imdb-reviews", dimensions=1536)
#Load index with Pinecone.from_existing_index("imdb-reviews", embeddings)

imdb_store = Pinecone.from_texts([d.page_content for d in docs], embeddings, index_name="imdb-reviews")

#If you have issues with the text files not loading and/or you forgot to specify the utf-8 encoding
#when creating the text files, use the following loop to show you what the file encodings might be.
#Non-ascii and utf-8 files represent documents that need to be re-saved with utf-8 encodings.
#filepath should = folder path/*.txt.

#import chardet
#import glob

#def error_txt(filepath):
#    for filename in glob.glob(filepath):
#        with open(filename, 'rb') as rawdata:
#            result = chardet.detect(rawdata.read())
#        print(filename, result['encoding'])
