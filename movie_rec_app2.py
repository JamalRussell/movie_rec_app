import os
import pinecone
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st

os.environ["OPENAI_API_KEY"] = "api_key"
#os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
#Note: If running protobuf > 3.20.x, you may want to attempt to set this environment variable after importing the os library,
#as the Pinecone clients may not import otherwise. If this doesn't work, downgrade protobuf to 3.20.x or lower and run rest of script.

embeddings = OpenAIEmbeddings()

pinecone.init(api_key="api_key", environment="environment")
imdb_store = Pinecone.from_existing_index("imdb-reviews", embeddings)

description = """This is an app that will recommend a number of movies from the IMDb Top 1000 list based on their
preferred genre of film, as well as the emotions, affects, and sentiments they would like the film to make them
feel, or see in the film itself. Please enter the genre (preferrably one, no more than three, comma-separated)
and sentiments (no more than five, comma-separated) of choice into their respective fields to get your
recommendations.

To clear your results, simply clear out one or both of the text fields."""

st.title("Movie Recommendation App")
st.markdown(description)
genre = st.text_input("Genre:", key="genre")
sentiments = st.text_input("Sentiments:", key="sentiments")

query = f'I am interested in {genre} movies that make me feel {sentiments}.'

query_ans = imdb_store.similarity_search(query)

content1 = query_ans[0].page_content
content2 = query_ans[1].page_content
content3 = query_ans[2].page_content

template = """You are a lifelong movie reviewer with a vast knowledge of films in different genres. You love to
recommend films to others based on their tastes and preferences.

Respond to the query below by recommending the movies reviewed in each of the context position in the voice of
said review. Each recommendation should specify the title of the movie and its genre, followed by a two sentence
description of the film.

Format your responses in the following manner:

'Title:

Genre:

Description:'

Context: '{content1}'

Context: '{content2}'

Context: '{content3}'

Query: 'I am interested in {genre}' movies that make me feel {sentiments}.'

AI:"""

prompt = PromptTemplate(input_variables=['content1', 'content2', 'content3', 'genre', 'sentiments'],
                        template=template)

llm = ChatOpenAI(temperature=0.9, model_name='gpt-3.5-turbo-16k')
chain = LLMChain(prompt=prompt, llm=llm)

if st.session_state.genre and st.session_state.sentiments:
    result = chain.run({'content1': content1, 'content2': content2, 'content3': content3, 'genre': genre,
                    'sentiments': sentiments})
    st.write(result)
