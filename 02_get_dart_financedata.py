# pip install selenium==4.1.3
# pip install webdriver-manager
# pip install webdriver-manager --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org

import os
import time
import re
import zipfile

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager



# ChromeDriver의 경로를 지정합니다. 여기에는 실제 파일 경로를 입력해야 합니다.
path_to_chromedriver =  'D:/github/ultra/chromedriver'

# ChromeDriver 서비스를 설정합니다.
service = Service(executable_path=path_to_chromedriver)

# # Chrome WebDriver 인스턴스를 생성합니다.
driver = webdriver.Chrome(service=service)
# driver = webdriver.Chrome(service=service, options=options)

# # # 웹 페이지를 엽니다. 예를 들어, Google 홈페이지를 열어봅니다.
# driver.get('https://www.google.com')

# # # 코드 실행이 끝나면, 브라우저를 닫습니다.
# driver.quit()





# Replace 'YOUR_CHROME_VERSION' with the major version number of your Chrome browser (e.g., '94', '95', etc.)
# chrome_version = '115.0.5790.171'

# options = webdriver.ChromeOptions()
# service = Service(ChromeDriverManager(version=chrome_version).install())
# service = Service(ChromeDriverManager(version=chrome_version).install())





# # service = Service(executable_path=r'/usr/bin/chromedriver')

# # 크롬 드라이버 최신 버전 설정
# service = Service(executable_path=ChromeDriverManager(version="114.0.5735.90").install())
# # driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install(), options= options)
# options = webdriver.ChromeOptions()
# options.add_argument('window-size=1920,1080')
        
# # chrome driver
# driver = webdriver.Chrome(service=service, options=options) # <- options로 변경




# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=service, options=options)





###########




# service = Service()

# options = webdriver.ChromeOptions()
# options.add_argument('window-size=1920,1080')
# options.add_argument("--headless")

# driver = webdriver.Chrome('chromedriver.exe', options=options)
#driver = webdriver.Chrome('chromedriver.exe', options=options)


# driver = webdriver.Chrome(ChromeDriverManager().install(), options= options)

# options = webdriver.ChromeOptions()
# # driver = webdriver.Chrome(service=service, options=options)
# driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install(), options= options)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# ...


###########


# BASE_DIR = 'C:\\Users\\USER\\dev\\quantylab\\data\\dart'  # 원하는 경로로 수정하세요


import os

# ... (other imports)

# Set BASE_DIR to the directory where the current code is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
STOCK_CODE_DIR = os.path.join(BASE_DIR, 'stock_code')

# Create the stock_code directory if it doesn't exist
if not os.path.exists(STOCK_CODE_DIR):
    os.makedirs(STOCK_CODE_DIR)

# ... (rest of the code)

# def download():
#     # ...
#     options.add_experimental_option("prefs", {
#         "download.default_directory": STOCK_CODE_DIR,  # Change the download directory to STOCK_CODE_DIR
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True
#     })


def exists(filename=None):
    for _filename in os.listdir(BASE_DIR):
        if filename is not None:
            if filename == _filename:
                return _filename
        else:
            if _filename.endswith('.part') or _filename.endswith('.crdownload'):
                continue
            return _filename
    return ''


def wait_download(filename=None, seconds=60):
    trycnt = 0
    while trycnt < seconds:
        if exists(filename=filename):
            print('Done')
            return True
        trycnt += 1
        print('Wait "{}" {}'.format(filename if filename is not None else 'unknown', trycnt))
        time.sleep(1)
    return False


def download():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": STOCK_CODE_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    service = Service(executable_path=path_to_chromedriver)
    # # Chrome WebDriver 인스턴스를 생성합니다.
    browser = webdriver.Chrome(service=service)
    browser.implicitly_wait(3)
    browser.get('https://opendart.fss.or.kr/disclosureinfo/fnltt/dwld/main.do')

    elem_nav = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.date_choice_ext"))
    )
    for elem_tab in elem_nav.find_elements(By.TAG_NAME, 'li'):
        elem_tab.click()  # 탭 클릭
        time.sleep(0.2)
        elem_tb = browser.find_element(By.CSS_SELECTOR, 'table.tb01')
        for elem_a in elem_tb.find_elements(By.LINK_TEXT, '다운로드'):
            filename = re.findall(r'.*\(.*\'(.+)\'\).*', elem_a.get_attribute('onclick'))[0]
            elem_a.click()  # 다운로드 버튼 클릭
            wait_download(filename)
            # 압축파일 로드
            # filepath = os.path.join(BASE_DIR, filename)

            # 압축 해제할 ZIP 파일의 경로
            zip_path = 'C:/Users/kbins/Downloads/2023_1Q_BS_20230801040420.zip'

            # 압축 해제될 폴더의 경로 (옵션)
            extract_path = './finance_data'


            import zipfile
            import os
            

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for info in zip_ref.infolist():
                    # 파일명을 cp437에서 euc-kr로 디코딩
                    _filename = info.filename.encode('cp437').decode('euc-kr')
                    _filepath = os.path.join(extract_path, _filename)

                    # 해당 경로의 폴더가 없으면 생성
                    os.makedirs(os.path.dirname(_filepath), exist_ok=True)

                    # 파일 압축 해제
                    with zip_ref.open(info.filename) as source, open(_filepath, 'wb') as target:
                        target.write(source.read())

            print(f'{zip_path} has been extracted to {extract_path}')



            # if not os.path.exists(extract_path):
            #     os.makedirs(extract_path)
            # # extract_path = 'D:/github/ultra'

            # # ZIP 파일 열기
            # with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            #     # 모든 파일과 폴더를 지정된 경로로 압축 해제
            #     zip_ref.extractall(extract_path)

            # print(f'{zip_path} has been extracted to {extract_path}')
            


            # # z = zipfile.ZipFile(filepath)
            # for info in z.infolist():
            #     # 한글 파일명 인코딩 수정
            #     _filename = info.filename.encode('cp437').decode('euc-kr')
            #     _filepath = os.path.join(BASE_DIR, _filename)
            #     if os.path.exists(_filepath):
            #         continue
            #     info.filename = _filename
            #     # # 압축해제
            #     # z.extract(info, BASE_DIR)  
            # z.close()
            break  # 전체 다운로드 버튼 클릭하려면 제거하세요
        break  # 전체 탭 다운로드하려면 제거하세요
    browser.quit()


download()


import pandas as pd

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
finace_data_path = os.path.join(BASE_DIR, 'finance_data')


file  = os.listdir(finace_data_path)[0]
file_연결 = os.listdir(finace_data_path)[1]

finance_file_path = os.path.join(finace_data_path, file)
finance_file_path_연결 = os.path.join(finace_data_path, file_연결)

df = pd.read_csv(finance_file_path, sep='\t', encoding='cp949')
df_연결 = pd.read_csv(finance_file_path_연결, sep='\t', encoding='cp949')


print(df.head())
print(df_연결.head())
# driver.quit()

