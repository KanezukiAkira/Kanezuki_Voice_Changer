import os
with open('infer-web.py', 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'isawaitable' in line:
        for j in range(max(0, i-2), min(len(lines), i+20)):
            print(repr(lines[j]))
        break
