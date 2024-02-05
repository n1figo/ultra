from selenium import webdriver
import os, time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# import pyperclip, pyautogui


# 패키지설치
# pip install selenium --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
# pip install webdriver-manager --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
# pip install pandas --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
# pip install lxml --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
# pip install html5lib --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
# pip install beautifulsoup4 --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
# pip install pyinstaller --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org


options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--no-sandbox")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())
        
# chrome driver
driver = webdriver.Chrome(service=service, options=options) # <- options로 변경

# 웹사이트를 불러옵니다.
url = 'https://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN='
driver.get(url)

#####################################
# 최근 손익정보 합치기 (최신 1년)
#####################################
html = driver.page_source
driver.quit()
print("driver has been quit!")
soup = BeautifulSoup(html, 'html5lib')
print(soup)
# table_손익 = soup.find_all(id='divSonikQ')
table_손익 = soup.find_all(id='div15')

# div15 highlight_D_Y um_table
# /html/body/div[2]/div/div[2]/div[3]/div[13]/div[3]
print(table_손익)

# 2. 매출총이익 스크래핑
# 재무정보 테이블화 (beautifuklsoup resultset은 문자열로 전환해줘야 한다!)
table_손익 = pd.read_html(str(table_손익))

# 테이블에서 0번 항목만 내리기
df_손익 = table_손익[0]
df_손익 = df_손익.set_index(df_손익.columns[0])

# 전년동기 정보 삭제
selected_cols = [x for x in df_손익.columns if '전년동기' not in x]
df_손익_selected = df_손익[selected_cols]

# # 주어진 XPath를 사용하여 웹 요소를 선택합니다.

# element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[3]/div[13]')

# # data = element.text.split('\n')
# text = element.text

# # data = pd.read_html(html.get_attribute('outerHTML'))
# data = pd.read_html(text)


# 데이터프레임으로 변환
# df = pd.DataFrame(data, columns=['열 이름'])
# df = pd.DataFrame(data)
df_손익_selected.to_csv('sample.csv', encoding='cp949')

# 데이터프레임 출력
# print(df)

# WebDriver를 종료합니다.
# driver.quit()
