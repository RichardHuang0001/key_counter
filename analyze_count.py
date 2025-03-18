import json
from datetime import datetime, timedelta
from collections import defaultdict

# 配置参数
INPUT_LOG = '/Users/huangwei/key_counter/key_log.txt'
OUTPUT_JSON = '/Users/huangwei/key_counter/daily_hourly_summary.json'
MAX_INTERVAL_MS = 300  # 最大间隔时间为300毫秒

# 加载原始数据
def load_data(file_path):
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[2:]  # 跳过日志标题
        for line in lines:
            if ' - ' in line:
                dt_str, key_name = line.strip().split(' - ')
                timestamp = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
                records.append({'timestamp': timestamp, 'key': key_name})
    return records

# 数据清洗（去除连续300ms内相同按键超过2次的情况）
def clean_data(records):
    if not records:
        return []

    cleaned = []
    current_sequence = [records[0]]

    for record in records[1:]:
        last_record = current_sequence[-1]
        interval = (record['timestamp'] - last_record['timestamp']).total_seconds() * 1000

        if record['key'] == last_record['key'] and interval <= MAX_INTERVAL_MS:
            current_sequence.append(record)
        else:
            # 检查序列长度并只保留第一次和最后一次（最多2个）
            if len(current_sequence) > 2:
                cleaned.append(current_sequence[0])
                cleaned.append(current_sequence[-1])
            else:
                cleaned.extend(current_sequence)
            current_sequence = [record]

    # 最后的序列特殊处理
    if len(current_sequence) > 2:
        cleaned.append(current_sequence[0])
        cleaned.append(current_sequence[-1])
    else:
        cleaned.extend(current_sequence)

    return cleaned

# 按天和小时统计
def analyze_data(records):
    summary = defaultdict(lambda: {'total': 0, 'hourly': defaultdict(int)})

    for record in records:
        date_str = record['timestamp'].strftime('%Y-%m-%d')
        hour_str = record['timestamp'].strftime('%H')
        summary[date_str]['total'] += 1
        summary[date_str]['hourly'][hour_str] += 1

    # 转换hourly defaultdict 为普通dict，便于json保存
    for date in summary:
        summary[date]['hourly'] = dict(summary[date]['hourly'])

    return dict(summary)

# 保存为json
def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 主函数
def main():
    records = load_data(INPUT_LOG)
    cleaned_records = clean_data(records)
    summary = analyze_data(cleaned_records)
    save_json(summary, OUTPUT_JSON)
    print(f"分析完成，结果已保存到：{OUTPUT_JSON}")

if __name__ == "__main__":
    main()
