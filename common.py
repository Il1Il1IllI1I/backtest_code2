import csv
from datetime import datetime

# CSV 파일에서 모든 정보를 딕셔너리 리스트로 반환하는 함수
def get_data_from_csv(filename):
    data_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_list.append(row)
    return data_list

def get_common_data_from_files(filenames):
    common_data_list = None
    
    for filename in filenames:
        data_list = get_data_from_csv(filename)
        
        if common_data_list is None:
            common_data_list = data_list
        else:
            # 공통 데이터 찾기 (Name 기준)
            common_names = set(item['Name'] for item in common_data_list)
            data_names = set(item['Name'] for item in data_list)
            common_names &= data_names
            
            common_data_list = [item for item in data_list if item['Name'] in common_names]
    
    return common_data_list

# common_data_result를 CSV 파일로 저장하는 함수
def save_data_to_csv(data_list, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data_list[0].keys())
        writer.writeheader()  # 헤더 쓰기
        for data in data_list:
            writer.writerow(data)

def compare_common_data_from_files(*csv_files):
    # 함수 호출하여 공통 데이터 찾기
    common_data_result = get_common_data_from_files(list(csv_files))

    # 현재 날짜를 가져와서 문자열로 변환
    current_date_str = datetime.now().strftime('%m-%d')
    filename = f"common_{current_date_str}.csv"

    # common_data_result를 'common_월-일.csv' 형식의 파일로 저장
    save_data_to_csv(common_data_result, filename)

# 사용 예:
compare_common_data_from_files('turtle_buy_08-18.csv', 'minervini_08-18.csv')
