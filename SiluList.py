import requests
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

# 데이터 총 개수 390437
# 시흥시 데이터 개수 14434

SiluList = []
url = "https://openapi.gg.go.kr/RegionMnyFacltStus"
key = "f324bd7732f64e7cba3c1a1ff7ff11ec"

def fetch_data(page_index):
    queryParams = {
        "Key": key,
        "Type": "xml",
        "pIndex": page_index,
        "pSize": 1000,
    }

    response = requests.get(url, params=queryParams)
    root = ET.fromstring(response.text)
    
    local_list = []
    for item in root.iter("row"):
        cityName = item.findtext("SIGUN_NM")  # 시군명
        if cityName != "시흥시" :
            continue
        
        Name = item.findtext("CMPNM_NM")  # 상호명
        roadAddr = item.findtext("REFINE_ROADNM_ADDR")  # 정제도로명주소
        Addr = item.findtext("REFINE_LOTNO_ADDR")  # 정제지번주소
        lat = item.findtext("REFINE_WGS84_LAT")  # 정제 위도
        long = item.findtext("REFINE_WGS84_LOGT")  # 정제 경도
        industry = item.findtext("INDUTYPE_CD")  # 업종 코드

        local_list.append([Name, roadAddr, Addr, lat, long, industry])
    
    return local_list

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_data, i) for i in range(100 , 200)]
    
    for future in as_completed(futures):
        SiluList.extend(future.result())

def getList() :
    return SiluList