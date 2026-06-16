with open('wrapper.html', 'r', encoding='utf-8') as f:
    content = f.read()
if 'http://127.0.0.1:7897/' in content:
    content = content.replace('http://127.0.0.1:7897/', 'http://127.0.0.1:7897/?v=2')
    with open('wrapper.html', 'w', encoding='utf-8') as f:
        f.write(content)
