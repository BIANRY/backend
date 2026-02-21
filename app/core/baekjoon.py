import re
import json
import urllib.request
from datetime import datetime
from typing import List, Dict, Any

try:
    import cloudscraper
except ImportError:
    cloudscraper = None

def fetch_solvedac_tier(baekjoon_id: str) -> int:
    """
    solved.ac 공식 API를 통해 유저의 티어 정보(Integer)를 가져옵니다.
    0: Unrated, 1~5: Bronze 5~1, 6~10: Silver 5~1 등
    """
    url = f"https://solved.ac/api/v3/user/show?handle={baekjoon_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        import ssl
        context = ssl._create_unverified_context()
        res = urllib.request.urlopen(req, context=context)
        data = json.loads(res.read().decode('utf-8'))
        return data.get('tier', 0)
    except Exception as e:
        print(f"[{baekjoon_id}] solved.ac 티어 정보를 가져오는데 실패했습니다: {e}")
        return 0

def fetch_baekjoon_grass(baekjoon_id: str) -> List[Dict[str, Any]]:
    """
    백준 유저 페이지에서 잔디(solved) 데이터를 크롤링합니다.
    bot 차단을 피하기 위해 cloudscraper를 사용합니다.
    """
    if not cloudscraper:
        print("cloudscraper 라이브러리가 설치되어 있지 않습니다.")
        return []

    url = f"https://www.acmicpc.net/user/{baekjoon_id}"
    
    scraper = cloudscraper.create_scraper()
    
    try:
        response = scraper.get(url, timeout=10)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"[{baekjoon_id}] 백준 프로필 데이터를 가져오는데 실패했습니다: {e}")
        return []

    # 백준 페이지의 잔디 데이터는 22~25번째 script 태그 내에 
    # const user_day_problems = [[20250102,1],[20250103,1],...]; 형태로 변수로 삽입됩니다.
    match = re.search(r"const\s+user_day_problems\s*=\s*(\[.*?\]);", html)
    
    if not match:
        print(f"[{baekjoon_id}] 잔디 데이터 배열을 찾을 수 없습니다.")
        return []
    
    data_str = match.group(1)
    
    try:
        points = json.loads(data_str)
    except:
        # JSON 파싱 실패 시 정규식 사용
        points = [(int(d), int(c)) for d, c in re.findall(r"\[(\d+),\s*(\d+)\]", data_str)]
    
    grass_data = []
    
    for point in points:
        date_int = point[0]  # 예: 20250102
        count = point[1]
        
        # 20250102 -> 2025, 01, 02 추출 후 datetime 객체 생성
        year = date_int // 10000
        month = (date_int % 10000) // 100
        day = date_int % 100
        
        try:
            dt = datetime(year, month, day)
            grass_data.append({
                "date": dt.date(),
                "solved_count": count
            })
        except ValueError:
            continue
            
    # 최신 날짜순으로 정렬
    grass_data.sort(key=lambda x: x["date"], reverse=True)
    return grass_data
