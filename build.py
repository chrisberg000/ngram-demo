"""Build script: embeds texts_data.js into index.html, replacing TEXTS_PLACEHOLDER."""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('texts_data.js', 'r', encoding='utf-8') as f:
    texts_js = f.read()

html = html.replace('TEXTS_PLACEHOLDER', texts_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

import os
size = os.path.getsize('index.html')
print(f"index.html: {size:,} bytes ({size / 1024 / 1024:.1f} MB)")
print("Build complete.")
