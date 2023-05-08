"""
Copyright 2023 Imrayya

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


import json
import re

import gradio as gr
import modules
from pathlib import Path
from modules import script_callbacks
import modules.scripts as scripts
from transformers import GPT2LMHeadModel, GPT2Tokenizer

result_prompt = ""
models = {}
max_no_results = 20  # TODO move to setting panel
base_dir = scripts.basedir()
model_file = Path(base_dir, "models.json")


class Model:
    '''
    Small strut to hold data for the text generator
    '''

    def __init__(self, name, model, tokenizer) -> None:
        self.name = name
        self.model = model
        self.tokenizer = tokenizer
        pass


def populate_models():
    """Get the models that this extension can use via models.json
    """
    # TODO add button to refresh and update model list
    path = model_file
    with open(path, 'r') as f:
        data = json.load(f)
    for item in data:
        name = item["Title"]
        model = item["Model"]
        tokenizer = item["Tokenizer"]
        models[name] = Model(name, model, tokenizer)


def add_to_prompt(prompt):  # A holder TODO figure out how to get rid of it
    return prompt


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
                                max_length, repetition_penalty,
                                num_return_sequences, name, use_punctuation=False,
                                use_blacklist=False):  # TODO make the progress bar work
        """Generates a longer string from the input

        Args:
            prompt (str): As the name suggests, the start of the prompt that the generator should start with.

            temperature (float): A higher temperature will produce more diverse results, but with a higher risk of less coherent text

            top_k (float): Strategy is to sample from a shortlist of the top K tokens. This approach allows the other high-scoring tokens a chance of being picked.

            max_length (int): the maximum number of tokens for the output of the model

            repetition_penalty (float): The parameter for repetition penalty. 1.0 means no penalty. Default setting is 1.2

            num_return_sequences (int): The number of results to generate

            name (str): Which Model to use

            use_punctuation (bool): Allows the use of commas in the output. Defaults to False.

            use_blacklist (bool): It will delete any matches to the generated result (case insensitive). Each item to be filtered out should be on a new line. Defaults to False.

        Returns:
            Returns only an error otherwise saves it in result_prompt
        """
        try:
            print("[Prompt_Generator]:","Loading Tokenizer")
            tokenizer = GPT2Tokenizer.from_pretrained(models[name].tokenizer)
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            print("[Prompt_Generator]:","Loading Model")
            model = GPT2LMHeadModel.from_pretrained(models[name].model)
        except Exception as e:
            print("[Prompt_Generator]:",f"Exception encountered while attempting to install tokenizer")
            return gr.update(), f"Error: {e}"
        try:
            print("[Prompt_Generator]:",f"Generate new prompt from: \"{prompt}\" with {name}")
            input_ids = tokenizer(prompt, return_tensors='pt').input_ids
            if (use_punctuation):
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
            print("[Prompt_Generator]:","Generation complete!")
            tempString = ""
            if (use_blacklist):
                blacklist = get_list_blacklist()
            for i in range(len(output)):

                tempString += tokenizer.decode(
                    output[i], skip_special_tokens=True) + "\n"

                if (use_blacklist):
                    for to_check in blacklist:
                        tempString = re.sub(
                            to_check, "", tempString, flags=re.IGNORECASE)
                if (i == 0):
                    global result_prompt

            result_prompt = tempString
            # print(result_prompt)
        except Exception as e:
            print("[Prompt_Generator]:",
                f"Exception encountered while attempting to generate prompt: {e}")
            return gr.update(), f"Error: {e}"

    def ui_dynamic_result_visible(num):
        """Makes the results visible"""
        k = int(num)
        return [gr.Row.update(visible=True)]*k + [gr.Row.update(visible=False)]*(max_no_results-k)

    def ui_dynamic_result_prompts():
        """Populates the results with the prompts"""

        lines = result_prompt.splitlines()
        num = len(lines)
        result_list = []
        for i in range(int(max_no_results)):
            if (i < num):
                result_list.append(lines[i])
            else:
                result_list.append("")
        return result_list

    def ui_dynamic_result_batch():
        return result_prompt

    def save_prompt_to_file(path, append: bool):
        if len(result_prompt) == 0:
            print("[Prompt_Generator]:","Prompt is empty")
            return
        with open(path, encoding="utf-8", mode="a" if append else "w") as f:
            f.write(result_prompt)
        print("[Prompt_Generator]:","Prompt written to: ", path)

    # ----------------------------------------------------------------------------
    # UI structure
    txt2img_prompt = modules.ui.txt2img_paste_fields[0][0]
    img2img_prompt = modules.ui.img2img_paste_fields[0][0]

    with gr.Blocks(analytics_enabled=False) as prompt_generator:
        # Handles UI for prompt creation
        with gr.Column():
            with gr.Row():
                prompt_textbox = gr.Textbox(
                    lines=2, elem_id="promptTxt", label="Start of the prompt")
        with gr.Column():
            gr.HTML(
                "Mouse over the labels to access tooltips that provide explanations for the parameters.")
            with gr.Row():
                temp_slider = gr.Slider(
                    elem_id="temp_slider", label="Temperature", interactive=True, minimum=0, maximum=1, value=0.9)
                maxLength_slider = gr.Slider(
                    elem_id="max_length_slider", label="Max Length", interactive=True, minimum=1, maximum=200, step=1, value=90)
                topK_slider = gr.Slider(
                    elem_id="top_k_slider", label="Top K", value=8, minimum=1, maximum=20, step=1, interactive=True)
        with gr.Column():
            with gr.Row():
                repetitionPenalty_slider = gr.Slider(
                    elem_id="repetition_penalty_slider", label="Repetition Penalty", value=1.2, minimum=0.1, maximum=10, interactive=True)
                numReturnSequences_slider = gr.Slider(
                    elem_id="num_return_sequences_slider", label="How Many To Generate", value=5, minimum=1, maximum=max_no_results, interactive=True, step=1)
        with gr.Column():
            with gr.Row():
                useBlacklist_checkbox = gr.Checkbox(label="Use blacklist?")
                gr.HTML(value="<center>Using <code>\".\extensions\stable-diffusion-webui-Prompt_Generator\\blacklist.txt</code>\".<br>It will delete any matches to the generated result (case insensitive).</center>")
        with gr.Column():
            with gr.Row():
                populate_models()
                generate_dropdown = gr.Dropdown(choices=list(models.keys()), value=list(models.keys())[
                                                1 if len(models) > 0 else 0], label="Which model to use?", show_label=True)  # TODO Add default to setting page
                use_punctuation_check = gr.Checkbox(label="Use punctuation?")
                generate_button = gr.Button(
                    value="Generate", elem_id="generate_button")  # TODO Add element to show that it is working in the background so users don't think nothing is happening

        # Handles UI for results
        results_vis = []
        results_txt_list = []
        with gr.Tab("Results"):
            with gr.Column():
                for i in range(max_no_results):
                    with gr.Row(visible=False) as row:
                        # Doesn't seem to do anything
                        row.style(equal_height=True)
                        with gr.Column(scale=3):  # Guessing at the scale
                            textBox = gr.Textbox(label="", lines=3)
                        with gr.Column(scale=1):
                            txt2img = gr.Button("send to txt2img")
                            img2img = gr.Button("send to img2img")
                        # Handles ___2img buttons
                        txt2img.click(add_to_prompt, inputs=[
                            textBox], outputs=[txt2img_prompt]).then(None, _js='switch_to_txt2img',
                                                                     inputs=None, outputs=None)
                        img2img.click(add_to_prompt, inputs=[
                            textBox], outputs=[img2img_prompt]).then(None, _js='switch_to_img2img',
                                                                     inputs=None, outputs=None)
                        results_txt_list.append(textBox)
                    results_vis.append(row)
        with gr.Tab("Batch"):
            with gr.Column():
                batch_texbox = gr.Textbox("", label="Results")
                with gr.Row():
                    with gr.Column(scale=4):
                        savePathText = gr.Textbox(
                            Path(base_dir, "batch_prompt.txt"), label="Path", interactive=True)
                    with gr.Column(scale=1):
                        append_checkBox = gr.Checkbox(label="Append")
                        save_button = gr.Button("Save To file")

        # ----------------------------------------------------------------------------------
        # Handle buttons
        save_button.click(fn=save_prompt_to_file, inputs=[
            savePathText, append_checkBox])
        # Please note that we use `.then()` to run other ui elements after the generation is done
        generate_button.click(fn=generate_longer_generic, inputs=[
            prompt_textbox, temp_slider, topK_slider, maxLength_slider,
            repetitionPenalty_slider, numReturnSequences_slider,
            generate_dropdown, use_punctuation_check, useBlacklist_checkbox]).then(
            fn=ui_dynamic_result_visible, inputs=numReturnSequences_slider,
            outputs=results_vis).then(
            fn=ui_dynamic_result_prompts, outputs=results_txt_list).then(fn=ui_dynamic_result_batch, outputs=batch_texbox)
    return (prompt_generator, "Prompt Generator", "Prompt Generator"),


script_callbacks.on_ui_tabs(on_ui_tabs)
