from flask import Flask, request, jsonify, render_template
from theme_classifier.theme_classifier import ThemeClassifier
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Route for rendering the input form
@app.route('/')
def index():
    return render_template('index.html')  # Frontend form to accept input

# Route to process the form data, generate the plot, and return the result
@app.route('/get_themes', methods=['POST'])
def get_themes():
    try:
        # Extract form data
        theme_list_str = request.form.get('themes')  # Themes list (comma separated)
        subtitles_path = request.form.get('subtitles_path')  # Path to subtitles
        save_path = request.form.get('save_path')  # Path to save the output (if necessary)

        # Check if the subtitles path exists
        if not os.path.exists(subtitles_path):
            return jsonify({"error": f"Subtitles path '{subtitles_path}' does not exist."}), 400

        # Initialize the theme classifier and process the data
        theme_list = theme_list_str.split(',')  # Convert theme list to a Python list
        theme_classifier = ThemeClassifier(theme_list)  # Initialize the theme classifier
        output_df = theme_classifier.get_themes(subtitles_path, save_path)  # Get the themes DataFrame

        # Clean the data by removing 'dialogue' from the theme list
        theme_list = [theme for theme in theme_list if theme != 'dialogue']
        output_df = output_df[theme_list]

        # Summing the scores for each theme and formatting the DataFrame
        output_df = output_df[theme_list].sum().reset_index()
        output_df.columns = ['Theme', 'Score']

        # Create the Plotly bar chart
        fig = px.bar(
            output_df,
            x='Theme',
            y='Score',
            title='Series Themes',
            labels={'Theme': 'Theme', 'Score': 'Score'},
            text='Score'
        )
        fig.update_traces(textposition='outside')  # Display the score outside the bars
        fig.update_layout(height=400, width=800)

        # Convert the figure to HTML
        plot_html = pio.to_html(fig, full_html=False)

        # Render the results page with the plot
        return render_template('results.html', plot_html=plot_html)

    except Exception as e:
        # Return error message if something goes wrong
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)