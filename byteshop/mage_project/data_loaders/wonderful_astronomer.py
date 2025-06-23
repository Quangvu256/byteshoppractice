# Sửa lại Block 1 (Data Loader)
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_from_single_file(*args, **kwargs):
    """
    Đọc dữ liệu từ một file .jsonl duy nhất. Siêu nhanh!
    """
    filepath = 'generated_events_single/all_events.jsonl'

    # Pandas có thể đọc trực tiếp định dạng jsonl
    return pd.read_json(filepath, lines=True)