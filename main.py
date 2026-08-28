from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# 프론트엔드 통신 허용 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scrape")
def scrape_biz_info(biz_num: str):
    # 1. 하이픈(-) 제거하여 비즈노 URL 규격에 맞춤
    clean_biz_num = biz_num.replace("-", "")
    url = f"https://bizno.net/article/{clean_biz_num}" 
    
    # 2. 크롤링 차단 방지를 위한 브라우저 헤더 정보
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return {"success": False, "error": f"페이지 접근 실패 (상태 코드: {response.status_code})"}
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. 데이터 추출을 위한 초기값 설정
        company_name = "-"
        established_date = "-"
        industry = "-"
        business_type = "-"
        region = "-"

        # [상호명 추출]: 웹페이지 타이틀에서 가져오기
        title_tag = soup.find('title')
        if title_tag:
            company_name = title_tag.text.split('-')[0].strip()

        # 데이터가 없는 유령 사업자번호인 경우 방어
        if "비즈노" in company_name and len(company_name) < 5:
            return {"success": False, "error": "해당 사업자번호의 정보를 찾을 수 없습니다."}

        # [세부 정보 추출]: 테이블(tr, th, td) 구조를 순회하며 텍스트 매칭
        for tr in soup.find_all('tr'):
            th = tr.find('th')
            td = tr.find('td')
            
            if th and td:
                # 라벨(th)의 띄어쓰기를 모두 제거하여 검색의 정확도를 높임
                key = th.text.strip().replace(" ", "") 
                val = td.text.strip()
                
                if "설립일" in key:
                    established_date = val
                elif "업종" in key:
                    industry = val
                elif "업태" in key:
                    business_type = val
                elif "회사주소" in key or "사업장소재지" in key or "주소" in key:
                    region = val
        
        # 파편화된 업종과 업태를 보기 좋게 합치기
        combined_industry = "-"
        if industry != "-" and business_type != "-":
            combined_industry = f"[{business_type}] {industry}"
        elif industry != "-":
            combined_industry = industry
        elif business_type != "-":
            combined_industry = business_type

        # 비즈노는 매출과 신용점수를 제공하지 않으므로 무조건 빈칸(-) 처리
        revenue = "-"
        credit = "-"

        # 4. 프론트엔드(HTML)로 수집한 데이터 전송
        return {
            "success": True,
            "companyName": company_name,
            "establishedDate": established_date,
            "industry": combined_industry,
            "region": region,
            "revenue": revenue,
            "credit": credit
        }
        
    except Exception as e:
        return {"success": False, "error": f"크롤링 에러 발생: {str(e)}"}
