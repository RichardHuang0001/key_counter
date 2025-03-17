from pynput import keyboard
from datetime import datetime
import threading
import os
import atexit

LOG_FILE = "/Users/huangwei/key_counter/key_log.txt"

BUFFER_SIZE = 100  # 缓存的按键数量
FLUSH_INTERVAL = 10  # 定时刷新的间隔（秒）

buffer = []
lock = threading.Lock()
key_count = 0
running = True  # 控制主程序运行状态

# 确保日志文件存在
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("按键记录日志 - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + "\n\n")

# 将缓存内容写入文件
def write_to_file():
    global buffer
    with lock:
        if buffer:
            try:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.writelines(buffer)
                buffer.clear()
            except Exception as e:
                print(f"写入文件时出错: {e}")

# 按键监听函数
def on_press(key):
    global key_count, buffer
    key_count += 1

    try:
        key_name = key.char
    except AttributeError:
        key_name = str(key)

    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} - {key_name}\n"

    with lock:
        buffer.append(log_entry)

        if len(buffer) >= BUFFER_SIZE:
            # 达到BUFFER_SIZE时触发写入
            threading.Thread(target=write_to_file, daemon=True).start()

    if key_count % 500 == 0:
        print(f"键盘已敲击 {key_count} 次")

# 定时刷新缓存区到文件的函数（持续执行，不新建线程）
def periodic_flush():
    if running:
        write_to_file()
        threading.Timer(FLUSH_INTERVAL, periodic_flush).start()

# 程序退出时确保数据写入
def exit_handler():
    global running
    running = False
    write_to_file()
    print("程序退出，数据已安全写入。")

# 注册退出事件处理函数
atexit.register(exit_handler)

# 开始定时缓存刷新任务
periodic_flush()

# 启动键盘监听
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
