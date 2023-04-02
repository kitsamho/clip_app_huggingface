import streamlit as st
from backend.app_pages import image_clustering, image_classification, text_classification, text_clustering, semantic_search
from backend.clip_functions import download_clip_model
from backend.load import load_yaml, load_cached_embeddings


st.set_page_config(layout="wide")
config = load_yaml("config.yaml")
clip_model = config['CLIP_MODEL'][0]
model, processor, tokeniser = download_clip_model(clip_model) # load the model, processor and tokeniser - this is cached

cached_embedding_path_rock_archive = 'data/embeddings/image_clustering_embeds_rockarchive.pickle'
df_cached_embeddings_rock = load_cached_embeddings(cached_embedding_path_rock_archive)

cached_embedding_path_conceptual_captions = 'data/embeddings/text_clustering_embeds_ccaptioning.pickle'
df_cached_embeddings_captions = load_cached_embeddings(cached_embedding_path_conceptual_captions).sample(1500)
# st.write(df_cached_embeddings_captions)


# Define menu items for each sub-app
navigation_buttons = {"Zero Shot Image Classification": image_classification,
                      "Zero Shot Text Classification": text_classification,
                      "Image Clustering": image_clustering,
                      "Text Clustering": text_clustering,
                      "Semantic Search": semantic_search}

st.sidebar.image('assets/OpenAI_Logo_old.png',width=300)

st.sidebar.title('CLIP Demo')
selection = st.sidebar.radio("Go to", list(navigation_buttons.keys()))
page = navigation_buttons[selection]
if selection == 'Zero Shot Image Classification':
    page.write(processor, model, tokeniser)

elif selection == 'Zero Shot Text Classification':
    page.write(tokeniser, model)

elif selection == 'Image Clustering':
    page.write(df_cached_embeddings_rock, processor, model)

elif selection == 'Text Clustering':
    page.write(df_cached_embeddings_captions, tokeniser, model)

elif selection == 'Semantic Search':
    page.write(df_cached_embeddings_rock, model, tokeniser)