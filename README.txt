cve 정보를 두가지 방식으로 저장.

1. 사용자의 PC에 디렉토리 형태로 저장 - 각 디렉토리 내부에는 엑셀 파일로 해당 CVE에 대한 정보 저장 
					저장하는 정보 : CVE number / cve description / cve url / exploit-db url /  Exploit code  / 취약한 버전의 프로그램 저장

2. Database에 저장 - MONGODB 사용하여 디비에 정보 저장


------------------파일 별 설명------------------------
read_csv.py : CVE에서 제공하는 csv 파일을 이용하여 2011년 이후의 "CVE-NUMBER"를 추출하여 디렉토리 생성 / mongodb에 저장 - 최초 1회만 실행
# 오로지 CVE NUMBER만을 추출하여 저장

twit_crwal.py : CVEnew 라는 이름의 CVE 공식 twitter에 새로운 cve가 등장 할 때마다 발생하는 알림을 파싱하여 디렉토리 생성 및 csv 파일 생성/ mongodb에 저장 - 상주하는 프로세스
# 트위터 파싱 및 csv 파일 추가

cve_operationl.py : CVE 홈페이지에서 cve 디렉토리 이름을 기준으로 하여 / db 정보를 기준으로 하여 정보를 파싱하여 저장 - 1회 실행
# 실제 CVE 홈페이지에서 정보 파싱하여 저장


실행 순서 : read_csv.py -> cve_operational.py -> twit_crawl.py

cve_list : cve 에 대한 디렉토리들이 생성되고 정보가 저장되는 디렉토리
cve_allitems.csv : 10월 20일 기준 CVE 홈페이지에서 공식적으로 제공하는 csv 파일