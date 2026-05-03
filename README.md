# 🎮 手勢互動彈出專案

這是一個使用 **MediaPipe + OpenCV** 製作的電腦視覺小型實驗專案，透過即時攝影機辨識手勢與臉部動作，並觸發對應的圖片彈出效果。

---

## 📌 專案簡介

本專案主要是練習電腦視覺與手勢辨識技術。

當攝影機偵測到特定手勢或動作時，會在螢幕上隨機位置跳出對應圖片，用來模擬簡單的互動效果。

---

## ✋ 支援的手勢

| 手勢        | 觸發效果      |
| ----------- | ------------- |
| 👍 比讚     | LIKE          |
| 🤟 比心     | HEART         |
| ✌️ 比 YA    | YEAH!!!       |
| 🖐️ 張開五指 | FIVE!!!       |
| 😮 張嘴     | MOUTH OPEN!!! |

---

## 🧠 功能特色

- 即時手部關鍵點追蹤（MediaPipe）
- 臉部偵測（嘴巴張開判斷）
- 多種手勢辨識
- 彈出圖片隨機位置顯示
- 防抖機制（避免誤判連續觸發）
- 多視窗控制（OpenCV）

---

## 🛠️ 使用技術

- Python
- OpenCV
- MediaPipe
- Tkinter（取得螢幕解析度）
- Random（隨機視窗位置）

---

## 📷 運作方式

1. 使用攝影機擷取即時影像
2. MediaPipe 偵測手部與臉部關鍵點
3. 判斷手勢是否符合條件
4. 觸發對應圖片彈出
5. 圖片會在螢幕安全範圍內隨機出現

---

## 🚀 如何執行

### 1️⃣ 建立虛擬環境（建議）

`python -m venv cv-env`

### 2️⃣ 啟動虛擬環境

Mac / Linux：

`source cv-env/bin/activate`

Windows：

`cv-env\Scripts\activate`

### 3️⃣ 安裝套件

`pip install opencv-python mediapipe`

### 4️⃣ 執行專案

`python3 main.py`
