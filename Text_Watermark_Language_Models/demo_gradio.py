import gradio as gr
from models.watermark_faster import watermark_model
import pdb
from options import get_parser_main_model

opts = get_parser_main_model().parse_args()
model = watermark_model(language=opts.language, mode=opts.mode, tau_word=opts.tau_word, lamda=opts.lamda)
def watermark_embed_demo(raw):

    watermarked_text = model.embed(raw)
    return watermarked_text

def watermark_extract(raw):
    is_watermark, p_value, n, ones, z_value = model.watermark_detector_fast(raw)
    confidence = (1 - p_value) * 100

    return f"{confidence:.2f}%"

def precise_watermark_detect(raw):
    is_watermark, p_value, n, ones, z_value = model.watermark_detector_precise(raw)
    confidence = (1 - p_value) * 100

    return f"{confidence:.2f}%"


demo = gr.Blocks()
with demo:
    with gr.Column():
        gr.Markdown("# Watermarking Text Generated by Black-Box Language Models")

        inputs = gr.TextArea(label="Input text", placeholder="Copy your text here...")
        output = gr.Textbox(label="Watermarked Text")
        analysis_button = gr.Button("Inject Watermark")
        inputs_embed = [inputs]
        analysis_button.click(fn=watermark_embed_demo, inputs=inputs_embed, outputs=output)

        inputs_w = gr.TextArea(label="Text to Analyze", placeholder="Copy your watermarked text here...")

        mode = gr.Dropdown(
            label="Detection Mode", choices=["Fast", "Precise"], default="Fast"
        )
        output_detect = gr.Textbox(label="Confidence (the likelihood of the text containing a watermark)")
        detect_button = gr.Button("Detect")

        def detect_watermark(inputs_w, mode):
            if mode == "Fast":
                return watermark_extract(inputs_w)
            else:
                return precise_watermark_detect(inputs_w)

        detect_button.click(fn=detect_watermark, inputs=[inputs_w, mode], outputs=output_detect)


if __name__ == "__main__":
    gr.close_all()
    demo.title = "Watermarking Text Generated by Black-Box Language Models"
    demo.launch(share = True, server_port=8899)