import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

# 配置参数
JSON_FILE = '/Users/huangwei/key_counter/daily_hourly_summary.json'
OUTPUT_IMAGE = '/Users/huangwei/key_counter/daily_key_counts.png'

def main():
    # 读取JSON文件
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取日期和总数
    dates = []
    counts = []
    
    # 按日期排序
    for date_str in sorted(data.keys()):
        # 转换日期字符串为datetime对象，便于绘图
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        dates.append(date_obj)
        counts.append(data[date_str]['total'])
    
    # 绘制图表
    plt.figure(figsize=(12, 6))
    plt.plot(dates, counts, marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=6)
    
    # 设置图表格式
    plt.title('keycounts for every day', fontsize=16)
    plt.xlabel('date', fontsize=12)
    plt.ylabel('keycounts', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 设置x轴日期格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.gcf().autofmt_xdate()  # 自动格式化日期标签
    
    # 添加数据标签
    for i, count in enumerate(counts):
        plt.annotate(f'{count}', 
                    (dates[i], counts[i]),
                    textcoords="offset points", 
                    xytext=(0, 10), 
                    ha='center',
                    fontsize=8)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    plt.savefig(OUTPUT_IMAGE, dpi=300)
    print(f"图表已保存至: {OUTPUT_IMAGE}")
    
    # 显示图表
    plt.show()

if __name__ == "__main__":
    main() 