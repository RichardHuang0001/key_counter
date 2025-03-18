import numpy as np
import matplotlib.pyplot as plt
import json

# 加载数据
with open('key_position_summary.json', 'r') as f:
    position_summary = json.load(f)

# 自定义键盘布局（示例）
keyboard_layout = [
    ['Key.esc', '', '', '', '', '', '', '', '', '', '', '', 'Key.backspace'],
    ['Key.tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '', 'Key.enter'],
    ['Key.caps_lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '', '', ''],
    ['Key.shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '', '', '', 'Key.shift', ''],
    ['Key.ctrl', 'cmd', 'Key.alt', 'Key.space', 'Key.alt', 'cmd', '', '', '', '', '', '']
]

# 构建热力图矩阵
heatmap_matrix = np.zeros((len(keyboard_layout), len(keyboard_layout[0])))
for i, row in enumerate(keyboard_layout):
    for j, key in enumerate(row):
        if key:
            heatmap_matrix[i, j] = position_summary.get(key, 0)

# 绘制热力图
plt.figure(figsize=(12, 6))
plt.imshow(heatmap_matrix, cmap='hot', interpolation='nearest')
plt.colorbar(label='按键次数')

# 添加键名
for i, row in enumerate(keyboard_layout):
    for j, key in enumerate(row):
        if key:
            plt.text(j, i, key.replace('Key.', ''), ha='center', va='center', color='white')

plt.title('键盘按键热力图')
plt.xticks([])
plt.yticks([])
plt.tight_layout()
plt.show()
