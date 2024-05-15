#pip install pillow
#pip install googlemaps
#pip install requests
import tkinter as tk
import tkinter.ttk as ttk
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
import io
import sys
import json
import datetime 

# 공공데이터 API 키
api_key = "f324bd7732f64e7cba3c1a1ff7ff11ec"
url = "https://openapi.gg.go.kr/RegionMnyFacltStus"

params = {
    "KEY": api_key,
    "Type": 'xml',
    "pIndex": 5,
    "pSize" : 1000
}

response = requests.get(url, params=params)
root = ET.fromstring(response.content)
items = root.findall(".//row")

franchisees = []
for item in items:
    franchisee = {
        "city": item.findtext("SIGUN_NM"), # 시군명
        "business": item.findtext("CMPNM_NM"),  # 상호명
        "address" : item.findtext("REFINE_ROADNM_ADDR"), # 도로명주소
        "latitude" : item.findtext("REFINE_WGS84_LAT") , # 위도
        "longitude" : item.findtext("REFINE_WGS84_LOGT") # 경도

    }
    franchisees.append(franchisee)

def load_map():
    api_key = "8dc8b71bb0126e11ff1deaf83c388b9a"
    latitude = 37.5665  # 예시 위도
    longitude = 126.9780  # 예시 경도
    zoom_level = 3  # 지도 확대/축소 레벨
    
    url = f"https://dapi.kakao.com/v2/maps/staticmap?center={latitude},{longitude}&level={zoom_level}&apiKey={api_key}"
    response = requests.get(url)
    
    with open("map.png", "wb") as f:
        f.write(response.content)
    
    map_image = tk.PhotoImage(file="map.png")
    map_label.config(image=map_image)
    map_label.image = map_image

# Tkinter 창 생성
root = tk.Tk()
root.title("Kakao Map")

# 지도를 표시할 라벨
map_label = tk.Label(root)
map_label.pack()

# 지도 불러오기 버튼
load_button = tk.Button(root, text="지도 불러오기", command=load_map)
load_button.pack()

root.mainloop()

