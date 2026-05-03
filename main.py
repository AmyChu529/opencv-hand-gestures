import cv2
import mediapipe as mp
import random
import tkinter as tk

# 取得螢幕解析度 (用於計算隨機位置的安全範圍)
try:
    root = tk.Tk()
    SCREEN_W = root.winfo_screenwidth()
    SCREEN_H = root.winfo_screenheight()
    root.withdraw()
except:
    SCREEN_W = 1920
    SCREEN_H = 1080

# 設定主視窗的安全避讓範圍
MAIN_WIN_W = 700
MAIN_WIN_H = 550

# 初始化 MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("❌ Camera 打不開")
    exit()

# 提前建立主視窗並固定在左上角
cv2.namedWindow("CV Project")
cv2.moveWindow("CV Project", 0, 0)
# 👉 新增這行：讓主視窗永遠置頂
cv2.setWindowProperty("CV Project", cv2.WND_PROP_TOPMOST, 1)


# ===== 圖片讀取區 =====
try:
    yeah_img = cv2.imread("assets/yeahMouse.jpg")
    mouth_img = cv2.imread("assets/memePopCat.jpg")
    like_img = cv2.imread("assets/thumbUp.jpg")
    heart_img = cv2.imread("assets/heart.jpg")
    five_img = cv2.imread("assets/five.jpg")

    # 確認圖片都有讀到，避免後續 resize 報錯
    if any(img is None for img in [yeah_img, mouth_img, like_img, heart_img, five_img]):
        raise ValueError("有一張或多張圖片讀取失敗，請檢查檔名與路徑。")

    # 縮小圖片
    yeah_img = cv2.resize(yeah_img, (500, 500))
    mouth_img = cv2.resize(mouth_img, (500, 500))
    like_img = cv2.resize(like_img, (500, 500))
    heart_img = cv2.resize(heart_img, (500, 500))
    five_img = cv2.resize(five_img, (500, 500))

except Exception as e:
    print(f"⚠️ {e}")
    exit()

# 管理視窗狀態的字典
windows_state = {
    "LIKE": {"img": like_img, "w": 500, "h": 500, "buffer_count": 0, "showing": False},
    "HEART": {"img": heart_img, "w": 500, "h": 500, "buffer_count": 0, "showing": False},
    "YEAH!!!": {"img": yeah_img, "w": 500, "h": 500, "buffer_count": 0, "showing": False},
    "MOUTH OPEN!!!": {"img": mouth_img, "w": 600, "h": 600, "buffer_count": 0, "showing": False},
    "FIVE!!!": {"img": five_img, "w": 500, "h": 500, "buffer_count": 0, "showing": False}
}

BUFFER_THRESHOLD = 3

# 產生安全隨機座標的函式


def get_safe_random_pos(img_w, img_h):
    for _ in range(50):
        max_x = max(0, SCREEN_W - img_w)
        max_y = max(0, SCREEN_H - img_h - 80)

        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        if x > MAIN_WIN_W or y > MAIN_WIN_H:
            return x, y

    return (SCREEN_W - img_w, SCREEN_H - img_h - 80)

# ===== 判斷邏輯區 =====


def is_like(hand_landmarks):
    return (
        hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y and
        hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y and
        hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y
    )


def is_heart(hand_landmarks):
    thumb = hand_landmarks.landmark[4]
    index = hand_landmarks.landmark[8]
    return (abs(thumb.x - index.x) + abs(thumb.y - index.y)) < 0.08


def is_yeah(hand_landmarks):
    tips = [8, 12, 16, 20]
    fingers = []
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers == [1, 1, 0, 0]

# 判斷是否比五


def is_five(hand_landmarks):
    fingers_up = all(
        hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y
        for tip in [8, 12, 16, 20]
    )
    dist_tip = abs(hand_landmarks.landmark[4].x - hand_landmarks.landmark[17].x) + abs(
        hand_landmarks.landmark[4].y - hand_landmarks.landmark[17].y)
    dist_joint = abs(hand_landmarks.landmark[2].x - hand_landmarks.landmark[17].x) + abs(
        hand_landmarks.landmark[2].y - hand_landmarks.landmark[17].y)
    thumb_open = dist_tip > dist_joint

    return fingers_up and thumb_open


def mouth_open(face_landmarks):
    top = face_landmarks.landmark[13].y
    bottom = face_landmarks.landmark[14].y
    return abs(bottom - top) > 0.02


# ===== 主迴圈 =====
while True:
    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hand_result = hands.process(rgb)
    face_result = face_mesh.process(rgb)

    current_detections = {key: False for key in windows_state.keys()}

    # 手勢偵測
    if hand_result.multi_hand_landmarks:
        for hand in hand_result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            # 使用 elif 避免多重觸發
            if is_like(hand):
                current_detections["LIKE"] = True
            elif is_heart(hand):
                current_detections["HEART"] = True
            elif is_five(hand):
                current_detections["FIVE!!!"] = True
            elif is_yeah(hand):
                current_detections["YEAH!!!"] = True

    # 嘴巴偵測
    if face_result.multi_face_landmarks:
        for face in face_result.multi_face_landmarks:
            if mouth_open(face):
                current_detections["MOUTH OPEN!!!"] = True

    # 視窗控制邏輯
    for win_name, state in windows_state.items():
        if current_detections[win_name]:
            state["buffer_count"] = min(
                state["buffer_count"] + 1, BUFFER_THRESHOLD)
        else:
            state["buffer_count"] = max(state["buffer_count"] - 1, 0)

        # 顯示視窗並設定安全隨機位置
        if state["buffer_count"] == BUFFER_THRESHOLD and not state["showing"]:
            cv2.imshow(win_name, state["img"])

            safe_x, safe_y = get_safe_random_pos(state["w"], state["h"])
            cv2.moveWindow(win_name, safe_x, safe_y)

            # 👉 新增這行：讓彈出來的圖片視窗也永遠置頂
            cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)

            state["showing"] = True

        elif state["buffer_count"] == 0 and state["showing"]:
            try:
                cv2.destroyWindow(win_name)
            except cv2.error:
                pass
            state["showing"] = False

    # 顯示主視窗
    cv2.imshow("CV Project", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
