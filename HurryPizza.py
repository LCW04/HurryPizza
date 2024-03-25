import tkinter as tk
from tkinter import ttk
from plyer import notification
import time
import threading
import json

# 파일에 저장될 설정 파일 경로
config_file = "config.json"

# 남은 시간을 전역 변수로 선언합니다.
remaining_time = None

def send_notification(message):
    notification.notify(
        title='HurryPizza 1.0',
        message=message,
        app_name='H_P'
    )

def start_timer(hours, minutes, seconds, message):
    global remaining_time
    initial_seconds = hours * 3600 + minutes * 60 + seconds
    while True:  # 무한 루프를 추가하여 프로그램이 종료되기 전까지 계속 실행되게 함
        total_seconds = initial_seconds
        while total_seconds > 0:
            time.sleep(1)
            total_seconds -= 1
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            remaining_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        send_notification(message)

def save_config(hours, minutes, seconds, message):
    config_data = {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "message": message
    }
    with open(config_file, "w") as file:
        json.dump(config_data, file)

def load_config():
    global remaining_time
    try:
        with open(config_file, "r") as file:
            config_data = json.load(file)
            hour_combobox.set(config_data["hours"])
            minute_combobox.set(config_data["minutes"])
            second_combobox.set(config_data["seconds"])
            message_entry.delete(0, tk.END)
            message_entry.insert(0, config_data["message"])
            remaining_time = f"{config_data['hours']:02d}:{config_data['minutes']:02d}:{config_data['seconds']:02d}"
    except FileNotFoundError:
        pass

def on_start():
    global remaining_time
    hours = int(hour_combobox.get())
    minutes = int(minute_combobox.get())
    seconds = int(second_combobox.get())
    message = message_entry.get()
    remaining_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    save_config(hours, minutes, seconds, message)
    t = threading.Thread(target=start_timer, args=(hours, minutes, seconds, message))
    t.daemon = True
    t.start()
    update_timer()
    disable_inputs()

def on_save():
    hours = int(hour_combobox.get())
    minutes = int(minute_combobox.get())
    seconds = int(second_combobox.get())
    message = message_entry.get()
    save_config(hours, minutes, seconds, message)

def on_load():
    load_config()

def update_timer():
    if remaining_time:
        timer_label.config(text=f"남은 시간: {remaining_time}")
    root.after(1000, update_timer)  # 1초마다 update_timer 함수를 호출합니다.

def disable_inputs():
    hour_combobox.config(state="disabled")
    minute_combobox.config(state="disabled")
    second_combobox.config(state="disabled")
    message_entry.config(state="disabled")

def validate_input(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False

# GUI 생성
root = tk.Tk()
root.title("HurryPizza 1.0")
root.geometry("300x150")
root.resizable(False, False)
root.iconbitmap('icon.ico')

# 시간 입력 (마우스 스크롤)
time_frame = ttk.Frame(root)
time_frame.pack()

hour_label = ttk.Label(time_frame, text="시간:")
hour_label.pack(side=tk.LEFT, padx=5)
hour_combobox = ttk.Combobox(time_frame, values=[str(i) for i in range(0, 24)], width=5, validate="key", validatecommand=(root.register(validate_input), "%P"))
hour_combobox.pack(side=tk.LEFT, padx=5)

minute_label = ttk.Label(time_frame, text="분:")
minute_label.pack(side=tk.LEFT, padx=5)
minute_combobox = ttk.Combobox(time_frame, values=[str(i) for i in range(0, 60)], width=5, validate="key", validatecommand=(root.register(validate_input), "%P"))
minute_combobox.pack(side=tk.LEFT, padx=5)

second_label = ttk.Label(time_frame, text="초:")
second_label.pack(side=tk.LEFT, padx=5)
second_combobox = ttk.Combobox(time_frame, values=[str(i) for i in range(1, 60)], width=5, validate="key", validatecommand=(root.register(validate_input), "%P"))
second_combobox.pack(side=tk.LEFT, padx=5)

message_frame = ttk.Frame(root)
message_frame.pack()

# 메시지 입력
message_label = ttk.Label(message_frame, text="알림 메시지:")
message_label.pack(side=tk.LEFT, padx=5)
message_entry = ttk.Entry(message_frame, width=20)
message_entry.pack(side=tk.LEFT, padx=5)

# 버튼 프레임 생성
button_frame = ttk.Frame(root)
button_frame.pack()

# 저장 버튼
save_button = ttk.Button(button_frame, text="저장", command=on_save)
save_button.pack(side=tk.LEFT, padx=5)

# 불러오기 버튼
load_button = ttk.Button(button_frame, text="불러오기", command=on_load)
load_button.pack(side=tk.LEFT, padx=5)

# 시작 버튼
start_button = ttk.Button(button_frame, text="알림 설정 시작", command=on_start)    
start_button.pack(side=tk.LEFT, padx=5)

# 설정 불러오기

# 남은 시간을 표시하는 레이블 추가
timer_label = ttk.Label(root, text="남은 시간: 00:00:00")
timer_label.pack()

root.mainloop()
