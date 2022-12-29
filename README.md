# Prompt Generator

Adds a tab to the webui that allows the user to generate a prompt from a small base prompt. Based on [FredZhang7/distilgpt2-stable-diffusion-v2](https://huggingface.co/FredZhang7/distilgpt2-stable-diffusion-v2). I did nothing apart from porting it to [AUTOMATIC1111 WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

![image](https://user-images.githubusercontent.com/8998556/209890919-203463fe-4b25-4ba0-9b29-57b1744dfd0f.png)


## Installation:

1. Install [AUTOMATIC1111's Stable Diffusion Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
2. Clone this repository into the `extensions` folder inside the webui

## Usage:

1. Write in the prompt in the *Start of the prompt* text box
2. Click Generate and wait

## Prompt Explanation 
- **Start of the prompt**: As the name, the start of the prompt that the generator should start with
- **Temperature**: A higher temperature will produce more diverse results, but with a higher risk of less coherent text
- **Top K**: The number of tokens to sample from at each step
- **Max Length**: the maximum number of tokens for the output of the model
- **Repetition Penalty**: The penalty value for each repetition of a token
- **How Many To Generate**: The number of results to generate
