# N-gram Language Model Demo

A single-file HTML application that lets economics students build, train, and experiment with n-gram language models. Demystifies how modern LLMs work by making next-token prediction visible and interactive.

Created by [Chris Berg](https://chrisberg.org/), 2026. It is really wonderful.

## Usage

Open `index.html` in any browser. No server, build step, dependencies, or API keys required.

1. Go to the **Train** tab and select one or more texts
2. Click **Train model** (builds n-gram tables for n=2 through n=6)
3. Switch to the **Generate** tab, type a seed phrase, and generate text

## Features

- **7 embedded texts** from Project Gutenberg (~970k words total) spanning economics classics and fiction
- **N-gram slider** (2–6) switches instantly between pre-built tables — no retraining needed
- **Temperature slider** (0.1–3.0) controls randomness of word selection
- **Probability display** shows a bar chart of top candidate words after each step
- **Step mode** generates one word at a time for close inspection
- **Backoff strategy** falls back to shorter contexts when an n-gram isn't found
- **Guided experiments** with suggested activities for students

## Included Texts

| Text | Author | Words |
|------|--------|------:|
| The Wealth of Nations | Adam Smith | 381,076 |
| The Economic Consequences of the Peace | J.M. Keynes | 69,966 |
| On the Principles of Political Economy and Taxation | David Ricardo | 117,799 |
| Principles of Political Economy | John Stuart Mill | 238,736 |
| A Christmas Carol | Charles Dickens | 28,541 |
| Pride and Prejudice | Jane Austen | 126,629 |
| The Communist Manifesto | Marx & Engels | 11,467 |

All texts are public domain, sourced from [Project Gutenberg](https://www.gutenberg.org/).

## Pedagogical Goals

- Language models predict the next word based on previous words
- More context (higher n) produces more coherent text but demands exponentially more data
- The curse of dimensionality: high n with small data leads to pure memorisation
- Temperature controls the randomness/creativity tradeoff
- This simple mechanism connects to how ChatGPT and other LLMs work at massive scale

## Build (for developers)

The repo includes build scripts used to fetch and embed the Gutenberg texts. These are not needed to run the app — `index.html` is self-contained.

```bash
# Download raw texts from Project Gutenberg
# (already done — results in texts/ directory)

# Clean texts and generate texts_data.js
python process_texts.py

# Embed texts_data.js into index.html
python build.py
```
