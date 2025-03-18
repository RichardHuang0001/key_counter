import json
from datetime import datetime
from collections import defaultdict

INPUT_LOG = "/Users/huangwei/key_counter/key_log.txt"
OUTPUT_JSON = "/Users/huangwei/key_counter/key_position_summary.json"
MAX_INTERVAL_MS = 300  # 300毫秒

# 加载日志数据
def load_data(file_path):
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[2:]  # 跳过标题行
        for line in lines:
            if ' - ' in line:
                dt_str, key_name = line.strip().split(' - ')
                timestamp = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
                records.append({'timestamp': timestamp, 'key': key_name})
    return records

# 数据清洗（300毫秒内相同按键只保留第一个和最后一个）
def clean_data(records):
    if not records:
        return []

    cleaned = []
    current_sequence = [records[0]]

    for record in records[1:]:
        interval = (record['timestamp'] - current_sequence[-1]['timestamp']).total_seconds() * 1000

        if record['key'] == current_sequence[-1]['key'] and interval <= MAX_INTERVAL_MS:
            current_sequence.append(record)
        else:
            # 保留第一个和最后一个
            if len(current_sequence) > 2:
                cleaned.extend([current_sequence[0], current_sequence[-1]])
            else:
                cleaned.extend(current_sequence)
            current_sequence = [record]

    # 处理最后一组
    if len(current_sequence) > 2:
        cleaned.extend([current_sequence[0], current_sequence[-1]])
    else:
        cleaned.extend(current_sequence)

    return cleaned

# 统计每个按键的位置（键名）累计按键次数
def analyze_positions(records):
    position_counter = defaultdict(int)
    for record in records:
        position_counter[record['key']] += 1
    return position_counter

# 存储为JSON文件
def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    records = load_data(INPUT_LOG)
    cleaned_records = clean_data(records)
    print(len(cleaned_records))
    positions_summary = analyze_positions(cleaned_records)

    save_to_json(positions_summary, OUTPUT_JSON)
    print(f"按键位置统计结果已保存至 {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
