import gradio as gr
import matplotlib.pyplot as plt
from theme_classifier.theme_classifier import ThemeClassifier


def get_themes(theme_list_str, subtitles_path, save_path):
    # Parse the theme list
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list=theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    # Remove 'dialogue' from the theme list and output DataFrame
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_df[theme_list]

    # Summarize the theme scores
    output_df = output_df.sum().reset_index()
    output_df.columns = ['Theme', 'Score']

    # Generate a bar plot
    plt.figure(figsize=(8, 4))
    plt.barh(output_df['Theme'], output_df['Score'], color='skyblue')
    plt.xlabel('Score')
    plt.title('Series Themes')
    plt.tight_layout()

    # Save the plot as an image
    plot_path = "output_plot.png"
    plt.savefig(plot_path)
    plt.close()

    return plot_path


def main():
    with gr.Blocks() as iface:
        with gr.Row():
            gr.HTML("<h1>Theme Classification (Zero Shot Classifiers)</h1>")

        with gr.Row():
            with gr.Column():
                theme_list = gr.Textbox(label="Themes (comma-separated)")
                subtitles_path = gr.Textbox(label="Subtitles or Script Path")
                save_path = gr.Textbox(label="Save Path")
                get_themes_button = gr.Button("Get Themes")
            with gr.Column():
                plot = gr.Image(label="Theme Classification Plot")

        # Link the button to the function
        get_themes_button.click(
            get_themes,
            inputs=[theme_list, subtitles_path, save_path],
            outputs=plot
        )

    iface.launch(share=True)


if __name__ == '__main__':
    main()