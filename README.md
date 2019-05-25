# using_korea_weather
동네예보정보조회 서비스를 사용해 날씨를 추출한 후, 머신러닝 알고리즘에 Feature로 사용할 예정


### 사용한 공공 데이터
- [(신)동네예보정보조회서비스](https://www.data.go.kr/dataset/15000099/openapi.do)
- 초단기예보조회

### 준비 사항
- data.go.kr 가입 후, 활용 신청
- 활용 신청 후 토큰 발급
- 동네예보조회서비스_격자_위경도 저장(저는 weather_xy.csv로 했어요)
- {date_now}_{time_now}.csv로 저장


### 소스엔 없지만 진행한 상황
- Airflow를 사용해 1시간마다 1번씩 request 날리고, 그 데이터를 BigQuery에 저장함
