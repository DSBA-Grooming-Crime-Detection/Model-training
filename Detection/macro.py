import pyautogui
import time

# 화면 크기 가져오기
width, height = pyautogui.size()
center_x = width // 2
center_y = height // 2

# 시작 메시지 및 대기
print("5초 후 마우스 자동 반복 이동 시작...")
time.sleep(5)

# 무한 반복
while True:
    # 십자 형태로 움직이기
    pyautogui.moveTo(center_x + 50, center_y, duration=0.3)
    pyautogui.moveTo(center_x, center_y + 50, duration=0.3)
    pyautogui.moveTo(center_x - 50, center_y, duration=0.3)
    pyautogui.moveTo(center_x, center_y - 50, duration=0.3)
    pyautogui.moveTo(center_x, center_y, duration=0.3)  # 다시 중앙으로
    pyautogui.click()
    
    # 반복 간 딜레이 (선택)
    time.sleep(2)
