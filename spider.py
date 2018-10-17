import re

import requests


def get_city_code():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9069'
    r = requests.get(url)
    pattern = re.compile(r'([\u4e00-\u9fa5]+)\|([A-Z]+)')
    city_code = pattern.findall(r.text)
    # print(dict(city_code))
    return dict(city_code)

def get_ticket_info(date,from_station,to_station):
    city_dict = get_city_code()
    from_station_code = city_dict[from_station]
    to_station_code = city_dict[to_station]
    city_dict_reverse = {v: k for k,v in city_dict.items()}
    # print(date,from_station_code,to_station_code)
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={}' \
          '&leftTicketDTO.from_station={}' \
          '&leftTicketDTO.to_station={}' \
          '&purpose_codes=ADULT'.format(date,from_station_code,to_station_code)
    r = requests.get(url)
    results = r.json()['data']['result']
    for result in results:
        data = result.split('|')
        train_num = data[3]
        start = city_dict_reverse[data[4]]
        end = city_dict_reverse[data[5]]
        start_time = data[8]
        arrive_time = data[9]
        total_time = data[10]
        top_seat = data[32] or '--'
        first_seat = data[31] or '--'
        second_seat = data[30] or '--'
        print('车次:{}\t出发站:{}\t到达站:{}\t出发时间:{}\t到达时间:{}\t历时:{}\n商务座:{}\t一等座:{}\t二等座:{}\n'.format(
            train_num,start,end,start_time,arrive_time,total_time,top_seat,first_seat,second_seat
        ))

if __name__ == '__main__':
    get_ticket_info('2018-10-11','北京','上海')
