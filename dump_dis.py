import marshal
import dis
with open('infer-web-real.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)
with open('infer-web-real.dis', 'w', encoding='utf-8') as f:
    dis.dis(code, file=f)
