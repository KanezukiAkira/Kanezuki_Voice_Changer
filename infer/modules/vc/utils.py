import os

from fairseq import checkpoint_utils


def get_index_path_from_model(sid):
    if not sid:
        return ""
    
    index_files = []
    index_root = os.getenv("index_root")
    if index_root and os.path.exists(index_root):
        for root, _, files in os.walk(index_root, topdown=False):
            for name in files:
                if name.endswith(".index") and "trained" not in name:
                    index_files.append(os.path.join(root, name))
                    
    name_no_ext = os.path.splitext(sid)[0]
    
    # 1. Try exact match
    for f in index_files:
        if name_no_ext in os.path.basename(f):
            return f
            
    # 2. Try match by removing suffix parts split by '_'
    parts = name_no_ext.split("_")
    while len(parts) > 1:
        parts.pop()
        sub_name = "_".join(parts)
        if sub_name:
            for f in index_files:
                if sub_name in os.path.basename(f):
                    return f
                    
    # 3. Fallback to matching by first part if it's long enough
    if parts and len(parts[0]) >= 3:
        for f in index_files:
            if parts[0] in os.path.basename(f):
                return f
                
    return ""


def load_hubert(config):
    models, _, _ = checkpoint_utils.load_model_ensemble_and_task(
        ["assets/hubert/hubert_base.pt"],
        suffix="",
    )
    hubert_model = models[0]
    hubert_model = hubert_model.to(config.device)
    if config.is_half:
        hubert_model = hubert_model.half()
    else:
        hubert_model = hubert_model.float()
    return hubert_model.eval()
