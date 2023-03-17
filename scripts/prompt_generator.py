"""
Copyright 2023 Imrayya

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


import gradio as gr
import modules
from modules import script_callbacks
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import re
import json

result_prompt = ""
models = {}


class Model:
    def __init__(self, name, model, tokenizer) -> None:
        self.name = name
        self.model = model
        self.tokenizer = tokenizer
        pass


def populate_models():
    path = "./extensions/stable-diffusion-webui-Prompt_Generator/models.json"
    with open(path, 'r') as f:
        data = json.load(f)
    for item in data:
        name = item["Title"]
        model = item["Model"]
        tokenizer = item["Tokenizer"]
        models[name] = Model(name, model, tokenizer)



def add_to_prompt(num):  # A function that determines which prompt to pass
    hand_over_prompt_list = result_prompt.splitlines()
    try:
        return (hand_over_prompt_list[int(num)-1][3:])
    except Exception as e:
        print(
            f"That line does not exist. Check number of prompts: {e}")
        return gr.update(), f"Error: {e}"


def get_list_blacklist():
    # Set the directory you want to start from
    file_path = './extensions/stable-diffusion-webui-Prompt_Generator/blacklist.txt'
    things_to_black_list = []
    with open(file_path, 'r') as f:
        # Read each line in the file and append it to the list
        for line in f:
            things_to_black_list.append(line.rstrip())

    return things_to_black_list


def on_ui_tabs():
    # Method to create the extended prompt

    def generate_longer_generic(prompt, temperature, top_k,
                                max_length, repetition_penalty, num_return_sequences, name, use_punctuation=False, use_blacklist=False):
        try:
            tokenizer = GPT2Tokenizer.from_pretrained(models[name].tokenizer)
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            # Full credits for the model to FredZhang7 (https://huggingface.co/FredZhang7). Under creativeml-openrail-m license.
            model = GPT2LMHeadModel.from_pretrained(models[name].model)
        except Exception as e:
            print(f"Exception encountered while attempting to install tokenizer")
            return gr.update(), f"Error: {e}"
        try:
            print(f"Generate new prompt from: \"{prompt}\" with {name}")
            input_ids = tokenizer(prompt, return_tensors='pt').input_ids
            if(use_punctuation):
                output = model.generate(input_ids, do_sample=True, temperature=temperature,
                                    top_k=round(top_k), max_length=max_length,
                                    num_return_sequences=num_return_sequences,
                                    repetition_penalty=float(
                                        repetition_penalty),
                                    early_stopping=True)
            else:
                output = model.generate(input_ids, do_sample=True, temperature=temperature,
                                    top_k=round(top_k), max_length=max_length,
                                    num_return_sequences=num_return_sequences,
                                    repetition_penalty=float(
                                        repetition_penalty),
                                    penalty_alpha=0.6, no_repeat_ngram_size=1,
                                    early_stopping=True)
            print("Generation complete!")
            tempString = ""
            if (use_blacklist):
                blacklist = get_list_blacklist()
            for i in range(len(output)):

                tempString += str(i+1)+": "+tokenizer.decode(
                    output[i], skip_special_tokens=True) + "\n"

                if (use_blacklist):
                    for to_check in blacklist:
                        tempString = re.sub(
                            to_check, "", tempString, flags=re.IGNORECASE)
                if (i == 0):
                    global result_prompt

            result_prompt = tempString
            # print(result_prompt)

            return {results: tempString,
                    send_to_img2img: gr.update(visible=True),
                    send_to_txt2img: gr.update(visible=True),
                    send_to_text: gr.update(visible=True),
                    results_col: gr.update(visible=True),
                    warning: gr.update(visible=True),
                    promptNum_col: gr.update(visible=True)
                    }
        except Exception as e:
            print(
                f"Exception encountered while attempting to generate prompt: {e}")
            return gr.update(), f"Error: {e}"

    # UI structure
    txt2img_prompt = modules.ui.txt2img_paste_fields[0][0]
    img2img_prompt = modules.ui.img2img_paste_fields[0][0]

    with gr.Blocks(analytics_enabled=False) as prompt_generator:
        with gr.Column():
            with gr.Row():
                promptTxt = gr.Textbox(
                    lines=2, elem_id="promptTxt", label="Start of the prompt")
        with gr.Column():
            gr.HTML(
                "Mouse over the labels to access tooltips that provide explanations for the parameters.")
            with gr.Row():
                temp_slider = gr.Slider(
                    elem_id="temp_slider", label="Temperature", interactive=True, minimum=0, maximum=1, value=0.9)
                max_length_slider = gr.Slider(
                    elem_id="max_length_slider", label="Max Length", interactive=True, minimum=1, maximum=200, step=1, value=90)
                top_k_slider = gr.Slider(
                    elem_id="top_k_slider", label="Top K", value=8, minimum=1, maximum=20, step=1, interactive=True)
        with gr.Column():
            with gr.Row():
                repetition_penalty_slider = gr.Slider(
                    elem_id="repetition_penalty_slider", label="Repetition Penalty", value=1.2, minimum=0.1, maximum=10, interactive=True)
                num_return_sequences_slider = gr.Slider(
                    elem_id="num_return_sequences_slider", label="How Many To Generate", value=5, minimum=1, maximum=20, interactive=True, step=1)
        with gr.Column():
            with gr.Row():
                use_blacklist_checkbox = gr.Checkbox(label="Use blacklist?")
                gr.HTML(value="<center>Using <code>\".\extensions\stable-diffusion-webui-Prompt_Generator\\blacklist.txt</code>\".<br>It will delete any matches to the generated result (case insensitive).</center>")
        with gr.Column():
            with gr.Row():
                populate_models()
                generate_dropdown = gr.Dropdown(choices=list(models.keys()), value="FredZhang7", label = "Which model to use?",show_label=True)
                use_punctuation_check = gr.Checkbox(label="Use punctuation?")
                generateButton_fred = gr.Button(
                    value="Generate", elem_id="generate_button")
        with gr.Column(visible=False) as results_col:
            results = gr.Text(
                label="Results", elem_id="Results_textBox", interactive=False)
        with gr.Column(visible=False) as promptNum_col:
            with gr.Row():
                promptNum = gr.Textbox(
                    lines=1, elem_id="promptNum", label="Send which prompt")
        with gr.Column():
            warning = gr.HTML(
                value="Select one number and send that prompt to txt2img or img2img", visible=False)
            with gr.Row():
                send_to_txt2img = gr.Button('Send to txt2img', visible=False)
                send_to_img2img = gr.Button('Send to img2img', visible=False)
                send_to_text = gr.Button(
                    'Send to back to prompter', visible=False)

        # events
        generateButton_fred.click(fn=generate_longer_generic, inputs=[
            promptTxt, temp_slider, top_k_slider, max_length_slider,
            repetition_penalty_slider, num_return_sequences_slider,
            generate_dropdown,use_punctuation_check, use_blacklist_checkbox],
            outputs=[results, send_to_img2img, send_to_txt2img, send_to_text,
                     results_col, warning, promptNum_col])
        send_to_img2img.click(add_to_prompt, inputs=[
                              promptNum], outputs=[img2img_prompt])
        send_to_txt2img.click(add_to_prompt, inputs=[
                              promptNum], outputs=[txt2img_prompt])
        send_to_text.click(add_to_prompt, inputs=[
                           promptNum], outputs=[promptTxt])
        send_to_txt2img.click(None, _js='switch_to_txt2img',
                              inputs=None, outputs=None)
        send_to_img2img.click(None, _js="switch_to_img2img",
                              inputs=None, outputs=None)
    return (prompt_generator, "Prompt Generator", "Prompt Generator"),


script_callbacks.on_ui_tabs(on_ui_tabs)
