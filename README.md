# Prompt Generator

Adds a tab to the webui that allows the user to generate a prompt from a small base prompt. Based on [FredZhang7/distilgpt2-stable-diffusion-v2](https://huggingface.co/FredZhang7/distilgpt2-stable-diffusion-v2) and [Gustavosta/MagicPrompt-Stable-Diffusion](https://huggingface.co/Gustavosta/MagicPrompt-Stable-Diffusion). I did nothing apart from porting it to [AUTOMATIC1111 WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

![screenshot](https://user-images.githubusercontent.com/8998556/212550120-df38601b-6811-4470-9e37-6980fbd94369.png)


## Installation

1. Install [AUTOMATIC1111's Stable Diffusion Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
2. Clone this repository into the `extensions` folder inside the webui

## Usage

1. Write in the prompt in the *Start of the prompt* text box
2. Click Generate and wait

The initial use of the model may take longer as it needs to be downloaded to your machine for offline use. The model will be used on your device and will be stored in the default location of `*username*/.cache/huggingface/hub/models`. The entire process of generating results will be done on your local machine and not require internet access.

## Parameters Explanation

- **Start of the prompt**: As the name suggests, the start of the prompt that the generator should start with
- **Temperature**: A higher temperature will produce more diverse results, but with a higher risk of less coherent text
- **Top K**: Strategy is to sample from a shortlist of the top K tokens. This approach allows the other high-scoring tokens a chance of being picked.
- **Max Length**: the maximum number of tokens for the output of the model
- **Repetition Penalty**: The parameter for repetition penalty. 1.0 means no penalty. See [this paper](https://arxiv.org/pdf/1909.05858.pdf) for more details. Default setting is 1.2
- **How Many To Generate**: The number of results to generate
- **Use blacklist?** Using `.\extensions\stable-diffusion-webui-Prompt_Generator\blacklist.txt`. It will delete any matches to the generated result (case insensitive). Each item to be filtered out should be on a new line. *Be aware that it simply deletes it and doesn't generate more to make up for the lost words*

## Models

There are two models provided:

### FredZhang7

Made by [FredZhang7](https://huggingface.co/FredZhang7) under creativeml-openrail-m license. 

Useful to get styles for a prompt. Eg: "A cat sitting" -> "A cat sitting on a chair, digital art. The room is made of clay and metal with the sun shining through in front trending at Artstation 4k uhd..."

### MagicPrompt

Made by [Gustavosta](https://huggingface.co/Gustavosta) under the MIT license. 

Useful to get more natural language prompts. Eg: "A cat sitting" -> "A cat sitting in a chair, wearing pair of sunglasses"

*Be aware that sometimes the model fails to produce anything or less than the wanted amount, either try again or use a new prompt in that case*

## Credits

Credits to both [FredZhang7](https://huggingface.co/FredZhang7) and [Gustavosta](https://huggingface.co/Gustavosta)
