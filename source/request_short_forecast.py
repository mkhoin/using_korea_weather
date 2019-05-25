import datetime
import pytz
import pandas as pd
import requests

weather_xy = pd.read_csv("/Users/byeon/Downloads/weather_xy.csv")


private_key = 'your_key'

time_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H')
date_now = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')

def request_short_term_weather(x, y):
    base_url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData?'
    key = "ServiceKey=" + private_key
    date = "&base_date=" + date_now
    time = "&base_time=" + time_now + "00"
    nx = "&nx=" + str(x)
    ny = "&ny=" + str(y)
    num_of_rows = "&numOfRows=100"
    response_type = "&_type=json"

    api_url = base_url + key + date + time + nx + ny + num_of_rows + response_type
    response = requests.get(api_url)
    response_data = response.json()
    return response_data


weather_xy['response'] = weather_xy.apply(lambda x: request_short_term_weather(x['x'], x['y']), axis=1)
base_df = pd.DataFrame(columns=['baseDate','baseTime','category','fcstDate','fcstTime','fcstValue','nx','ny'])
for i in range(len(weather_xy)):
    temp_df = pd.DataFrame(weather_xy['response'][i]['response']['body']['items']['item'])
    base_df = pd.concat([base_df, temp_df], axis=0).reset_index(drop=True)

base_df['nx'] = base_df['nx'].astype(int)
base_df['ny'] = base_df['ny'].astype(int)

merge_df = base_df.merge(weather_xy[['si','gu','x','y']], how='right', left_on=['nx', 'ny'], right_on=['x', 'y'])
merge_df = merge_df[['si','gu','nx','ny','baseDate', 'baseTime', 'category', 'fcstDate', 'fcstTime', 'fcstValue']]

merge_df = merge_df.drop_duplicates(['si', 'gu', 'nx', 'ny', 'baseDate', 'baseTime', 'category', 'fcstDate', 'fcstTime', 'fcstValue']).reset_index(drop=True)
merge_df.to_csv(f"{date_now}_{time_now}.csv")
