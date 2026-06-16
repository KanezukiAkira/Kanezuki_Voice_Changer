import os
import re
with open('infer-web.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r' +html_path = os\.path\.join\(script_dir, "frontend_extracted\.html"\)\r?\n +try:\r?\n +with open\(html_path, "r", encoding="utf-8"\) as fh:\r?\n +return HTMLResponse\(content=fh\.read\(\)\)\r?\n +except Exception as read_err:\r?\n +print\(f"\[WRAPPER\] Error reading frontend_extracted\.html: \{read_err\}", file=sys\.stderr\)\r?\n +pass'

new_content = re.sub(pattern, '', content, flags=re.DOTALL)

with open('infer-web.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
