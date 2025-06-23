# generate_events_single_file.py
# PHIÊN BẢN TỐI ƯU: Ghi tất cả vào một file duy nhất
import json
import random
import uuid
import os
import time
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
EVENT_TYPES = ['view_product', 'add_to_cart', 'remove_from_cart', 'purchase']
EVENT_WEIGHTS = [0.6, 0.2, 0.1, 0.1]
PRODUCTS = [{'product_id': i, 'product_name': fake.word().capitalize() + " " + random.choice(['Gadget', 'Tool', 'Device', 'Kit']), 'price': round(random.uniform(10, 500), 2)} for i in range(50)]

def generate_event(user_id, session_id):
    product = random.choice(PRODUCTS)
    event_type = random.choices(EVENT_TYPES, weights=EVENT_WEIGHTS, k=1)[0]
    event = {'event_id': str(uuid.uuid4()),'user_id': user_id,'session_id': session_id,'event_timestamp_utc': (datetime.utcnow() - timedelta(seconds=random.randint(0, 30))).isoformat() + "Z",'event_type': event_type,'product_id': product['product_id'],'product_name': product['product_name'],'price': product['price']}
    if event_type == 'purchase':
        event['quantity'] = random.randint(1, 3)
    return event

def main():
    output_dir = 'generated_events_single' # Thư mục mới
    os.makedirs(output_dir, exist_ok=True)

    # Tên file duy nhất sẽ chứa tất cả dữ liệu
    output_file_path = os.path.join(output_dir, 'all_events.jsonl') # .jsonl là định dạng tốt hơn

    all_events = [] # Tạo một cái "thùng" rỗng

    print("Bắt đầu sản xuất 'gạch' và cho vào một thùng lớn...")
    for user_id in range(1001, 1011):
      for _ in range(random.randint(1, 3)):
        session_id = str(uuid.uuid4())
        num_events_in_session = random.randint(5, 30)
        for i in range(num_events_in_session):
            event_data = generate_event(user_id, session_id)
            all_events.append(event_data) # Cho từng viên gạch vào thùng

    # Sau khi gom đủ, ghi toàn bộ cái "thùng" xuống file một lần duy nhất
    with open(output_file_path, 'w') as f:
        for event in all_events:
            f.write(json.dumps(event) + '\n') # Ghi từng dòng JSON

    print(f"\n✅ HOÀN THÀNH! Toàn bộ {len(all_events)} 'viên gạch' đã được ghi vào file duy nhất: '{output_file_path}'.")

if __name__ == "__main__":
    main()