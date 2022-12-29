import subprocess
import platform
import math
import json
import sys
import os
import re
from pathlib import Path

import gradio as gr
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageFilter
import cv2

from modules.ui import create_refresh_button, folder_symbol
from modules.shared import opts, OptionInfo
from modules import shared, paths, script_callbacks
from transformers import GPT2Tokenizer, GPT2LMHeadModel


def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as prompt_generator:

        # structure
        with gr.Column():
            with gr.Row():
                promptTxt = gr.Textbox(
                    lines=2, elem_id="promptTxt", label="Start of the prompt")
        with gr.Column():
            with gr.Row():
                temp_slider = gr.Slider(
                    elem_id="temp_slider", label="Temperature", interactive=True, minimum=0, maximum=1, value=0.9)
                max_length_slider = gr.Slider(
                    elem_id="max_length_slider", label="Max Length", interactive=True, minimum=1, maximum=200, step=1, value=80)
                top_k_slider = gr.Slider(
                    elem_id="top_k_slider", label="Top K", value=8, minimum=1, maximum=20, interactive=True)
        with gr.Column():
            with gr.Row():
                repetition_penalty_slider = gr.Slider(
                    elem_id="repetition_penalty_slider", label="Repetition Penalty", value=1.2, minimum=0, maximum=10, interactive=True)
                num_return_sequences_slider = gr.Slider(
                    elem_id="num_return_sequences_slider", label="How Many To Generate", value=5, minimum=1, maximum=20, interactive=True)
        with gr.Column():
            with gr.Row():
                generateButton = gr.Button(
                    value="Generate", elem_id="generate_button")
        with gr.Column():
            Results = gr.Text(elem_id="Results_textBox", interactive=False)

        # events
        def generate_longer_prompt(prompt, temperature, top_k,
                                   max_length, repetition_penalty, num_return_sequences):
            try:
                tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
                tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                model = GPT2LMHeadModel.from_pretrained(
                    'FredZhang7/distilgpt2-stable-diffusion-v2')
            except Exception as e:
                print(f"Exception encountered while attempting to install tokenizer")
            try:
                print(f"Generate new prompt from: \"{prompt}\"")
                input_ids = tokenizer(prompt, return_tensors='pt').input_ids
                output = model.generate(input_ids, do_sample=True, temperature=temperature,
                                        top_k=top_k, max_length=max_length,
                                        num_return_sequences=num_return_sequences,
                                        repetition_penalty=repetition_penalty,
                                        penalty_alpha=0.6, no_repeat_ngram_size=1, early_stopping=True)
                print("Generation complete!")
                tempString = ""
                for i in range(len(output)):
                    tempString += tokenizer.decode(output[i], skip_special_tokens=True) + "\n"
                return tempString
            except Exception as e:
                print(f"Exception encountered while attempting to generate prompt: {e}")
                return gr.update(), f"Error: {e}"
        generateButton.click(fn=generate_longer_prompt, inputs=[
                             promptTxt,temp_slider , top_k_slider, max_length_slider, 
                             repetition_penalty_slider, num_return_sequences_slider], 
                             outputs=[Results])
    return (prompt_generator, "Prompt Generator", "Prompt Generator"),

# def on_ui_settings():
#     picker_path = Path(paths.script_path) / "training-picker"
#     section = ('training-picker', "Training Picker")
#     opts.add_option("training_picker_fixed_size", OptionInfo(512, "Fixed size to resize images to", section=section))
#     opts.add_option("training_picker_videos_path", OptionInfo(str(picker_path / "videos"), "Path to read videos from", section=section))
#     opts.add_option("training_picker_framesets_path", OptionInfo(str(picker_path / "extracted-frames"), "Path to store extracted frame sets in", section=section))
#     opts.add_option("training_picker_default_output_path", OptionInfo(str(picker_path / "cropped-frames"), "Default cropped image output directory", section=section))


# script_callbacks.on_ui_settings(on_ui_settings)
script_callbacks.on_ui_tabs(on_ui_tabs)
