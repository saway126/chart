import pandas as pd
import sys

def test_excel():
    try:
        file_path = "C:/Users/kks/Documents/카카오톡 받은 파일/상품별 판매 데이터.xlsx"
        print(f"Excel 파일 읽기 시도: {file_path}")
        
        df = pd.read_excel(file_path, header=None)
        print(f"Excel 파일 읽기 완료: {len(df)}행")
        
        # 데이터 확인
        for i in range(3, min(10, len(df))):
            row = df.iloc[i]
            print(f"행 {i}: {row[0]} - {row[1]} - {row[-1]}")
            
    except Exception as e:
        print(f"오류: {e}")

if __name__ == "__main__":
    test_excel()
