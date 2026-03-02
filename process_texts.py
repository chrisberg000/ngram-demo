import re
import os
import json

TEXTS = {
    "wealth_of_nations": {
        "file": "texts/wealth_of_nations.txt",
        "title": "The Wealth of Nations",
        "author": "Adam Smith",
        "desc": "The foundational text of classical economics. Covers the division of labour, the invisible hand, free markets, and the nature of wealth.",
    },
    "economic_consequences": {
        "file": "texts/economic_consequences.txt",
        "title": "The Economic Consequences of the Peace",
        "author": "John Maynard Keynes",
        "desc": "Keynes' influential critique of the Treaty of Versailles. Analyses the economic impact of war reparations and post-war policy.",
    },
    "ricardo": {
        "file": "texts/ricardo.txt",
        "title": "On the Principles of Political Economy and Taxation",
        "author": "David Ricardo",
        "desc": "Classical economics and trade theory. Introduces comparative advantage, labour theory of value, and rent theory.",
    },
    "mill": {
        "file": "texts/mill.txt",
        "title": "Principles of Political Economy",
        "author": "John Stuart Mill",
        "desc": "A comprehensive treatise on economics and political philosophy. Covers production, distribution, exchange, and the role of government.",
    },
    "christmas_carol": {
        "file": "texts/christmas_carol.txt",
        "title": "A Christmas Carol",
        "author": "Charles Dickens",
        "desc": "Classic Victorian fiction \u2014 completely different domain from economics. Useful for comparing how training data affects output style.",
    },
    "pride_prejudice": {
        "file": "texts/pride_prejudice.txt",
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "desc": "A large, coherent novel with a very distinctive writing style. Good for testing how a big corpus affects generation quality.",
    },
    "communist_manifesto": {
        "file": "texts/communist_manifesto.txt",
        "title": "The Communist Manifesto",
        "author": "Karl Marx & Friedrich Engels",
        "desc": "A very short political text. Useful for demonstrating what happens when training data is scarce \u2014 the model tends to just memorise.",
    }
}


def clean_gutenberg(text):
    """Strip Gutenberg boilerplate and clean text."""
    start_pat = r'\*\*\* ?START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*'
    m = re.search(start_pat, text, re.IGNORECASE)
    if m:
        text = text[m.end():]

    end_pat = r'\*\*\* ?END OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*'
    m = re.search(end_pat, text, re.IGNORECASE)
    if m:
        text = text[:m.start()]

    # Remove [Illustration: ...] tags
    text = re.sub(r'\[Illustration[^\]]*\]', '', text)
    # Normalize line endings
    text = text.replace('\r\n', '\n')
    # Collapse 3+ newlines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Collapse multiple spaces/tabs to single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Strip each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    text = text.strip()
    return text


def count_words(text):
    return len(text.split())


def escape_for_js_template(text):
    """Escape text for JS template literal (backtick string)."""
    text = text.replace('\\', '\\\\')
    text = text.replace('`', '\\`')
    text = text.replace('$' + '{', '\\$' + '{')
    return text


results = {}
for key, info in TEXTS.items():
    with open(info["file"], 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()

    cleaned = clean_gutenberg(raw)
    wc = count_words(cleaned)
    js_text = escape_for_js_template(cleaned)

    results[key] = {
        **info,
        "word_count": wc,
        "js_text": js_text
    }
    print(f"{info['title']}: {wc:,} words, {len(cleaned):,} chars")

with open("texts_data.js", 'w', encoding='utf-8') as f:
    f.write("// Auto-generated from Project Gutenberg texts\n")
    f.write("const LIBRARY = [\n")
    for key, r in results.items():
        f.write("  {\n")
        f.write('    id: "' + key + '",\n')
        f.write('    title: ' + json.dumps(r["title"]) + ',\n')
        f.write('    author: ' + json.dumps(r["author"]) + ',\n')
        f.write('    description: ' + json.dumps(r["desc"]) + ',\n')
        f.write('    wordCount: ' + str(r["word_count"]) + ',\n')
        f.write('    text: `' + r["js_text"] + '`\n')
        f.write("  },\n")
    f.write("];\n")

total_size = os.path.getsize("texts_data.js")
print(f"\nTotal texts_data.js: {total_size:,} bytes ({total_size / 1024 / 1024:.1f} MB)")
