from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scrape")
def scrape_biz_info(biz_num: str):
    clean_biz_num = biz_num.replace("-", "")
    
    # 1. 타겟 사이트 URL (예: 잡코리아, 사람인, 나이스비즈인포, 비즈노 등)
    url = f"https://example-biz-site.com/search?q={clean_biz_num}" 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # response = requests.get(url, headers=headers, timeout=10)
        # soup = BeautifulSoup(response.text, 'html.parser')
        
        # -----------------------------------------------------------
        # [데이터 추출 로직 구현부]
        # 실제 타겟 사이트의 HTML 구조에 맞춰 아래 변수들을 추출하게 됩니다.
        # -----------------------------------------------------------
        
        # 지금은 HTML 프론트엔드로 잘 넘어가는지 확인하기 위한 '테스트 데이터'입니다.
        return {
            "success": True,
            "companyName": "소상공인경영전략연구소",  # 상호명
            "establishedDate": "2020-03-15 (업력 6년)", # 설립일 및 업력
            "industry": "정보통신 및 컨설팅업",         # 업종/업태
            "region": "경기도 의정부시",                # 지역
            "revenue": "15억 3천만원",                  # 매출
            "credit": "B+ (850점)"                     # 기업신용
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}
