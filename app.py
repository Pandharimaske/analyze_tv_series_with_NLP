import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from theme_classification.theme_classifier import ThemeClassifier
from character_network import NamedEntityRecognizer, CharacterNetworkGenerator

# Initialize session state for persistence
if "theme_output_df" not in st.session_state:
    st.session_state["theme_output_df"] = None
if "character_network_html" not in st.session_state:
    st.session_state["character_network_html"] = None

st.title("Interactive ML Tool")

# Theme Classification Section
st.header("Theme Classification")
theme_list_str = st.text_input(
    "Enter themes (comma-separated):",
    value="friendship, hope, sacrifice, battle, self-development, betrayal, love",
)
subtitles_path = st.text_input(
    "Enter subtitles/script path:",
    value="/Users/pandhari/Desktop/NLP + GEN AI/PROJECTS/proj/Data/Subtitles",
)
save_path = st.text_input(
    "Enter save path:",
    value="/Users/pandhari/Desktop/NLP + GEN AI/PROJECTS/proj/stubs/theme_classifier_output.csv",
)

if st.button("Get Themes"):
    if subtitles_path and save_path:
        try:
            # Clean and filter the theme list
            theme_list = theme_list_str.split(',')
            theme_list = [theme.strip() for theme in theme_list if theme.strip().lower() not in ['dialogue', 'episode']]
            
            st.write(f"Filtered Themes: {theme_list}")  # Debugging output
            
            # Initialize Theme Classifier and generate output
            theme_classifier_instance = ThemeClassifier(theme_list)
            output_df = theme_classifier_instance.get_themes(subtitles_path, save_path)
            output_df = output_df.drop(columns=['dialogue', 'episode'], errors='ignore')

            # Ensure numeric conversion
            output_df = output_df.apply(pd.to_numeric, errors='coerce')
            output_df.dropna(how='all', axis=1, inplace=True)  # Drop columns with all NaN
            
            # Store output in session state for persistence
            st.session_state["theme_output_df"] = output_df

            # Display DataFrame
            st.dataframe(output_df)

            # Calculate mean scores and create a bar plot
            st.subheader("Theme Scores Barplot")
            theme_scores = output_df.mean().reset_index()
            theme_scores.columns = ['Theme', 'Score']
            
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(theme_scores['Theme'], theme_scores['Score'], color='skyblue')
            ax.set_xlabel("Score")
            ax.set_ylabel("Theme")
            ax.set_title("Theme Scores (Mean)")
            st.pyplot(fig)
        
        except Exception as e:
            st.error(f"An error occurred while processing themes: {e}")
    else:
        st.error("Please provide valid paths for subtitles and save location.")

# Display the theme classification output persistently
if st.session_state["theme_output_df"] is not None:
    st.write("Persistent Themes Identified:")
    st.dataframe(st.session_state["theme_output_df"])

# Character Network Section
st.header("Character Network")
subtitles_path_ner = st.text_input("Enter subtitles/script path for Character Network:" , value = "/Users/pandhari/Desktop/NLP + GEN AI/PROJECTS/proj/Data/Subtitles")
ner_path = st.text_input("Enter NERs save path:" ,value =  "/Users/pandhari/Desktop/NLP + GEN AI/PROJECTS/proj/stubs/ners_output.csv")

if st.button("Generate Character Network"):
    if subtitles_path_ner and ner_path:
        try:
            # Named Entity Recognition
            ner = NamedEntityRecognizer()
            ner_df = ner.get_ners(subtitles_path_ner, ner_path)
            
            # Character Network Generation
            character_network_generator = CharacterNetworkGenerator()
            relationship_df = character_network_generator.generate_character_network(ner_df)
            
            # Generate HTML for the character network graph
            html = character_network_generator.draw_network_graph(relationship_df)

            # Store HTML graph in session state for persistence
            st.session_state["character_network_html"] = html

            # Display Relationship DataFrame
            st.write("Character Network Relationships:")
            st.dataframe(relationship_df)

            # Display the Graph
            st.subheader("Character Network Graph")
            st.components.v1.html(html, height=800, width=800, scrolling=True)

        except Exception as e:
            st.error(f"An error occurred while generating the character network: {e}")
    else:
        st.error("Please provide valid paths for subtitles and NER save location.")

# Display the character network graph persistently
if st.session_state["character_network_html"] is not None:
    st.subheader("Persistent Character Network Graph")
    st.components.v1.html(st.session_state["character_network_html"], height=800, width=800, scrolling=True)