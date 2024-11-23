---
license: llama2
datasets:
- uonlp/CulturaX
language:
- ru
- en
metrics:
- chrf
- accuracy
- bleu
---



# SambaLingo-Russian-Base

<img src="SambaLingo_Logo.png" width="340" style="margin-left:'auto' margin-right:'auto' display:'block'"/>

<!-- Provide a quick summary of what the model is/does. -->
SambaLingo-Russian-Base is a pretrained Bi-lingual Russian and English model that adapts [Llama-2-7b](https://huggingface.co/meta-llama/Llama-2-7b-hf) to Russian by training on 63 billion tokens from the Russian split of the [Cultura-X](https://huggingface.co/datasets/uonlp/CulturaX) dataset. This model reports state of the art evaluation results in perplexity and FLORES-200 translation. For the chat version of this model, please see [sambanovasystems/SambaLingo-Russian-Chat](https://huggingface.co/sambanovasystems/SambaLingo-Russian-Chat), or try it out at [SambaLingo-chat-space](https://huggingface.co/spaces/sambanovasystems/SambaLingo-chat-space).

## Model Description
<!-- Provide a longer summary of what this model is. -->

- **Developed by:** [SambaNova Systems](https://sambanova.ai/)
- **Model type:** Language Model
- **Language(s):** Russian, English
- **Finetuned from model:** [Llama 2](https://huggingface.co/meta-llama/Llama-2-7b-hf)
- **Try the chat version of this model**: [SambaLingo-chat-space](https://huggingface.co/spaces/sambanovasystems/SambaLingo-chat-space).
- **Paper:** [SambaLingo: Teaching Large Language Models New Languages](https://arxiv.org/abs/2404.05829)
- **Blog Post**: [sambalingo-open-source-language-experts](https://sambanova.ai/blog/sambalingo-open-source-language-experts)

## Getting Started

### Loading Model With Hugging Face
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("sambanovasystems/SambaLingo-Russian-Base")
model = AutoModelForCausalLM.from_pretrained("sambanovasystems/SambaLingo-Russian-Base", device_map="auto", torch_dtype="auto")
```

### Suggested Inference Parameters
We suggest setting do_sample=False as this is a pretrained checkpoint.

### Prompting Guidelines
This model is a pretrained checkpoint, so to use it effectively please use few shot prompting with exemplars. The only other prompt templating required is the standard \<s\> (BOS) token from the Llama tokenizer. If you want to interact with this model with direct questions or queries, please use the chat version of the model that has been aligned with human preferences [sambanovasystems/SambaLingo-Russian-Chat](https://huggingface.co/sambanovasystems/SambaLingo-Russian-Chat).

## Training Details
All pre-training is done on the [Cultura-X](https://huggingface.co/datasets/uonlp/CulturaX) dataset. We mix the data to be 75% data from the language we are adapting to, and 25% English as suggested by [Csaki et al.](https://arxiv.org/abs/2311.05741) We pack the data into sequences of length 4096, and ensure that when learning a token we only attend to previous tokens in the context of the corresponding text document. We train with a global batch size of 1024, sequence length of 4096, maximum learning rate of 1e-4 with cosine decay, warmup ratio of 0.01 and a weight decay of 0.1. 

## Tokenizer Details
We extended the vocabulary of the base llama model from 32,000 tokens to 57,000 tokens by adding up to 25,000 non-overlapping tokens from the new language.

## Evaluation Results 
For evaluation results see our paper: [SambaLingo: Teaching Large Language Models New Languages](https://arxiv.org/abs/2404.05829)

## Uses
<!-- Address questions around how the model is intended to be used, including the foreseeable users of the model and those affected by the model. -->

### Direct Use

<!-- This section is for the model use without fine-tuning or plugging into a larger ecosystem/app. -->
Use of this model is governed by the Meta’s [Llama 2 Community License Agreement](https://ai.meta.com/llama/license/). Please review and accept the license before downloading the model weights.

### Out-of-Scope Use

<!-- This section addresses misuse, malicious use, and uses that the model will not work well for. -->
SambaLingo should NOT be used for:

- Mission-critical applications
- Applications that involve the safety of others
- Making highly important decisions

## Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->
Like all LLMs, SambaLingo has certain limitations:
- Hallucination: Model may sometimes generate responses that contain plausible-sounding but factually incorrect or irrelevant information.
- Code Switching: The model might unintentionally switch between languages or dialects within a single response, affecting the coherence and understandability of the output.
- Repetition: The Model may produce repetitive phrases or sentences, leading to less engaging and informative responses.
- Coding and Math: The model's performance in generating accurate code or solving complex mathematical problems may be limited.
- Toxicity: The model could inadvertently generate responses containing inappropriate or harmful content.

## Acknowledgments
We extend our heartfelt gratitude to the open-source AI community; this endeavor would not have been possible without open source. SambaNova embraces the open-source community and aspires to actively contribute to this initiative.

We would like to give a special thanks to the following groups:
- Meta for open sourcing LLama 2 and open sourcing FLORES-200 dataset
- Nguyen et al for open sourcing CulturaX dataset
- CohereAI for releasing AYA-101 and open sourcing a multilingual instruction tuning dataset
- EleutherAI for their open source evaluation framework
- Hugging Face-H4 team for open source the zephyr training recipe and alignment handbook repo


## Cite SambaLingo
```
@misc{csaki2024sambalingo,
      title={SambaLingo: Teaching Large Language Models New Languages}, 
      author={Zoltan Csaki and Bo Li and Jonathan Li and Qiantong Xu and Pian Pawakapan and Leon Zhang and Yun Du and Hengyu Zhao and Changran Hu and Urmish Thakker},
      year={2024},
      eprint={2404.05829},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
