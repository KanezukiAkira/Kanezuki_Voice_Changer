import os
import re
with open('infer-web.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r' +if hasattr\(res, "body"\):\r?\n +try:\r?\n +html = res\.body\.decode\("utf-8"\).*?return res'

new_code = '''                                html_str = None
                                from fastapi.responses import HTMLResponse
                                if isinstance(res, str):
                                    html_str = res
                                elif isinstance(res, HTMLResponse) or hasattr(res, "body"):
                                    body = getattr(res, "body", res)
                                    if isinstance(body, bytes):
                                        html_str = body.decode("utf-8", errors="ignore")
                                    else:
                                        html_str = res
                                
                                if html_str is not None and isinstance(html_str, str):
                                    injection = """
                                    <script>
                                    document.addEventListener("DOMContentLoaded", function() {
                                        setInterval(() => {
                                            var btns = document.querySelectorAll('button, div.tabitem, div[role="tab"], .tab-nav > button');
                                            for (var i = 0; i < btns.length; i++) {
                                                var txt = btns[i].textContent || "";
                                                if (txt.includes('FAQ') || txt.includes('Câu hỏi thường gặp') || txt.includes('Câu hỏi') || txt.includes('Hỏi đáp') || txt.includes('hỏi đáp')) {
                                                    btns[i].style.display = 'none';
                                                    var tabId = btns[i].getAttribute('aria-controls');
                                                    if (tabId) {
                                                        var panel = document.getElementById(tabId);
                                                        if (panel) panel.style.display = 'none';
                                                    }
                                                }
                                            }
                                            var btn1 = document.getElementById('train-extract-btn');
                                            if (btn1 && btn1.textContent.includes('2.')) btn1.textContent = '2. Tách nhạc';
                                        }, 500);
                                    });
                                    </script>
                                    """
                                    if "</body>" in html_str:
                                        html_str = html_str.replace("</body>", injection + "</body>")
                                    else:
                                        html_str += injection
                                    if isinstance(res, str):
                                        return html_str
                                    return HTMLResponse(content=html_str)
                                return res'''

new_content = re.sub(pattern, new_code, content, flags=re.DOTALL)

with open('infer-web.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
