"""
현장조사 고객별 정리 통계 분석
MECE(Mutually Exclusive, Collectively Exhaustive) 프레임워크 기반 통계학적 분석
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

class CustomerSurveyAnalyzer:
    def __init__(self):
        """MECE 프레임워크 기반 분석 클래스 초기화"""
        self.raw_data = self._load_raw_data()
        self.processed_data = self._process_data()
        
    def _load_raw_data(self):
        """원시 데이터 로드"""
        # 김기성 데이터 (6명)
        kim_data = [
            {"id": "K1", "age_group": "40대", "gender": "여성", "occupation": "주부", 
             "preferred_menu": "폭립", "visit_reason": "집과 가까움", "complaints": "없음", 
             "notes": "폭립 메뉴 자주 구매", "visit_frequency": "자주"},
            
            {"id": "K2", "age_group": "60대", "gender": "부부", "occupation": "부부", 
             "preferred_menu": "새우튀김, 샐러드", "visit_reason": "없음", "complaints": "없음", 
             "notes": "의사결정권자가 주로 아내", "visit_frequency": "미기재"},
            
            {"id": "K3", "age_group": "30대", "gender": "남성", "occupation": "직장인", 
             "preferred_menu": "튀김류, 안주거리", "visit_reason": "회사가 근처", 
             "complaints": "음식이 눅눅함, 차별점 못 느낌", "notes": "다른 이마트/트레이더스와 차별점 못 느낌", "visit_frequency": "2주/1"},
            
            {"id": "K4", "age_group": "50대", "gender": "여성", "occupation": "직장인", 
             "preferred_menu": "없음", "visit_reason": "사무실 근처(주2회 방문)", 
             "complaints": "출입구 표시 미흡", "notes": "홍보 및 안내 표시 개선 요청", "visit_frequency": "주2회"},
            
            {"id": "K5", "age_group": "50대", "gender": "부부", "occupation": "부부", 
             "preferred_menu": "오징어 튀김", "visit_reason": "없음", 
             "complaints": "오징어 링 형태 제품 없어짐, 튀김이 조각남", "notes": "비주얼 불만족", "visit_frequency": "미기재"},
            
            {"id": "K6", "age_group": "50대", "gender": "여성", "occupation": "미기재", 
             "preferred_menu": "튀김류, 허니버터 감자", "visit_reason": "없음", 
             "complaints": "제품 찾기 어려움", "notes": "허니버터 감자 위치 파악 어려워 구매 못한 경험", "visit_frequency": "미기재"}
        ]
        
        # 김민진&박가람 데이터 (6명)
        kim_park_data = [
            {"id": "KP1", "age_group": "50대", "gender": "여성", "occupation": "미기재", 
             "preferred_menu": "유부롤, 후토마끼, 샐러드", "visit_reason": "혼자 간단히", 
             "complaints": "없음", "notes": "신선함, 메뉴 다양", "visit_frequency": "미기재", "satisfaction": "신선함, 메뉴 다양"},
            
            {"id": "KP2", "age_group": "50대", "gender": "여성", "occupation": "미기재", 
             "preferred_menu": "초밥", "visit_reason": "미기재", "complaints": "없음", 
             "notes": "가격 저렴, 메뉴 다양", "visit_frequency": "미기재", "satisfaction": "가격 저렴, 메뉴 다양"},
            
            {"id": "KP3", "age_group": "30대", "gender": "남성", "occupation": "미기재", 
             "preferred_menu": "샐러드", "visit_reason": "가족 식사", 
             "complaints": "그 가격에 그 맛, 튀김이 눅눅함", "notes": "가격 저렴, 메뉴 다양", "visit_frequency": "2주/1", "satisfaction": "가격 저렴, 메뉴 다양"},
            
            {"id": "KP4", "age_group": "50대", "gender": "여성", "occupation": "미기재", 
             "preferred_menu": "파스타, 꼬막비빔밥", "visit_reason": "딸에게 주려고", 
             "complaints": "없음", "notes": "딸이 좋아해서", "visit_frequency": "자주 아님", "satisfaction": "딸이 좋아해서"},
            
            {"id": "KP5", "age_group": "60대", "gender": "여성", "occupation": "미기재", 
             "preferred_menu": "샐러드", "visit_reason": "친구들과 한끼 대체", 
             "complaints": "피자가 부실하다, 동선이 너무 자주 바뀜", "notes": "매장이 가깝음, 가격 대비 good", "visit_frequency": "주1회", "satisfaction": "매장이 가깝음, 가격 대비 good, 메뉴 다양"},
            
            {"id": "KP6", "age_group": "40대", "gender": "남성", "occupation": "직장인", 
             "preferred_menu": "초밥", "visit_reason": "회사, 가족과 간단하게 식사할 때", 
             "complaints": "가격이 놀라는 것 같음", "notes": "간단히 먹기 good", "visit_frequency": "주2회", "satisfaction": "간단히 먹기 good"}
        ]
        
        return kim_data + kim_park_data
    
    def _process_data(self):
        """데이터 전처리 및 MECE 구조화"""
        df = pd.DataFrame(self.raw_data)
        
        # MECE 1: 고객 특성 (Demographics)
        df['age_group_clean'] = df['age_group'].str.extract(r'(\d+)대').astype(int)
        df['gender_clean'] = df['gender'].apply(lambda x: '여성' if '여성' in x else '남성' if '남성' in x else '부부')
        
        # MECE 2: 행동 패턴 (Behavioral)
        df['visit_frequency_clean'] = df['visit_frequency'].map({
            '주2회': 2, '주1회': 1, '2주/1': 0.5, '자주 아님': 0.25, '미기재': np.nan
        })
        
        # MECE 3: 만족 요인 (Satisfaction Factors)
        satisfaction_keywords = ['가격', '메뉴 다양', '신선함', '매장이 가깝', '간단히']
        for keyword in satisfaction_keywords:
            df[f'satisfaction_{keyword}'] = df['satisfaction'].str.contains(keyword, na=False)
        
        # MECE 4: 불만 요인 (Dissatisfaction Factors)
        complaint_keywords = ['눅눅', '조각', '찾기 어려', '표시 미흡', '동선', '차별점', '가격이 놀라']
        for keyword in complaint_keywords:
            df[f'complaint_{keyword}'] = df['complaints'].str.contains(keyword, na=False)
        
        # MECE 5: 메뉴 선호도 (Menu Preferences)
        menu_categories = ['초밥', '샐러드', '튀김', '한식', '일식', '양식']
        for menu in menu_categories:
            df[f'menu_{menu}'] = df['preferred_menu'].str.contains(menu, na=False)
        
        return df
    
    def analyze_demographics(self):
        """MECE 1: 고객 특성 분석"""
        print("=" * 60)
        print("MECE 1: 고객 특성 분석 (Demographics)")
        print("=" * 60)
        
        # 연령대별 분포
        age_dist = self.processed_data['age_group'].value_counts().sort_index()
        age_pct = self.processed_data['age_group'].value_counts(normalize=True).sort_index() * 100
        
        print("\n📊 연령대별 분포:")
        for age, count in age_dist.items():
            print(f"  {age}: {count}명 ({age_pct[age]:.1f}%)")
        
        # 성별 분포
        gender_dist = self.processed_data['gender_clean'].value_counts()
        gender_pct = self.processed_data['gender_clean'].value_counts(normalize=True) * 100
        
        print("\n👥 성별 분포:")
        for gender, count in gender_dist.items():
            print(f"  {gender}: {count}명 ({gender_pct[gender]:.1f}%)")
        
        return age_dist, gender_dist
    
    def analyze_behavioral_patterns(self):
        """MECE 2: 행동 패턴 분석"""
        print("\n" + "=" * 60)
        print("MECE 2: 행동 패턴 분석 (Behavioral)")
        print("=" * 60)
        
        # 방문 빈도 분석
        visit_freq = self.processed_data['visit_frequency'].value_counts()
        visit_pct = self.processed_data['visit_frequency'].value_counts(normalize=True) * 100
        
        print("\n🔄 방문 빈도 분포:")
        for freq, count in visit_freq.items():
            print(f"  {freq}: {count}명 ({visit_pct[freq]:.1f}%)")
        
        # 방문 이유 분석
        visit_reasons = []
        for reason in self.processed_data['visit_reason'].dropna():
            if reason not in ['없음', '미기재']:
                visit_reasons.append(reason)
        
        reason_counter = Counter(visit_reasons)
        print(f"\n🎯 방문 이유 TOP 3:")
        for reason, count in reason_counter.most_common(3):
            print(f"  {reason}: {count}명")
        
        return visit_freq, reason_counter
    
    def analyze_satisfaction_factors(self):
        """MECE 3: 만족 요인 분석"""
        print("\n" + "=" * 60)
        print("MECE 3: 만족 요인 분석 (Satisfaction Factors)")
        print("=" * 60)
        
        satisfaction_cols = [col for col in self.processed_data.columns if col.startswith('satisfaction_')]
        satisfaction_summary = {}
        
        for col in satisfaction_cols:
            factor_name = col.replace('satisfaction_', '')
            count = self.processed_data[col].sum()
            percentage = (count / len(self.processed_data)) * 100
            satisfaction_summary[factor_name] = {'count': count, 'percentage': percentage}
        
        print("\n✅ 만족 요인 순위:")
        sorted_satisfaction = sorted(satisfaction_summary.items(), key=lambda x: x[1]['count'], reverse=True)
        for factor, data in sorted_satisfaction:
            print(f"  {factor}: {data['count']}명 ({data['percentage']:.1f}%)")
        
        return satisfaction_summary
    
    def analyze_dissatisfaction_factors(self):
        """MECE 4: 불만 요인 분석"""
        print("\n" + "=" * 60)
        print("MECE 4: 불만 요인 분석 (Dissatisfaction Factors)")
        print("=" * 60)
        
        complaint_cols = [col for col in self.processed_data.columns if col.startswith('complaint_')]
        complaint_summary = {}
        
        for col in complaint_cols:
            factor_name = col.replace('complaint_', '')
            count = self.processed_data[col].sum()
            percentage = (count / len(self.processed_data)) * 100
            complaint_summary[factor_name] = {'count': count, 'percentage': percentage}
        
        print("\n❌ 불만 요인 순위:")
        sorted_complaints = sorted(complaint_summary.items(), key=lambda x: x[1]['count'], reverse=True)
        for factor, data in sorted_complaints:
            print(f"  {factor}: {data['count']}명 ({data['percentage']:.1f}%)")
        
        return complaint_summary
    
    def analyze_menu_preferences(self):
        """MECE 5: 메뉴 선호도 분석"""
        print("\n" + "=" * 60)
        print("MECE 5: 메뉴 선호도 분석 (Menu Preferences)")
        print("=" * 60)
        
        menu_cols = [col for col in self.processed_data.columns if col.startswith('menu_')]
        menu_summary = {}
        
        for col in menu_cols:
            menu_name = col.replace('menu_', '')
            count = self.processed_data[col].sum()
            percentage = (count / len(self.processed_data)) * 100
            menu_summary[menu_name] = {'count': count, 'percentage': percentage}
        
        print("\n🍽️ 메뉴 선호도 순위:")
        sorted_menu = sorted(menu_summary.items(), key=lambda x: x[1]['count'], reverse=True)
        for menu, data in sorted_menu:
            print(f"  {menu}: {data['count']}명 ({data['percentage']:.1f}%)")
        
        return menu_summary
    
    def cross_analysis_age_satisfaction(self):
        """연령대별 만족도 교차 분석"""
        print("\n" + "=" * 60)
        print("교차 분석: 연령대별 만족 요인")
        print("=" * 60)
        
        satisfaction_cols = [col for col in self.processed_data.columns if col.startswith('satisfaction_')]
        
        for col in satisfaction_cols:
            factor_name = col.replace('satisfaction_', '')
            print(f"\n📈 {factor_name} 만족도 (연령대별):")
            
            cross_table = pd.crosstab(self.processed_data['age_group'], self.processed_data[col])
            cross_pct = pd.crosstab(self.processed_data['age_group'], self.processed_data[col], normalize='index') * 100
            
            for age_group in cross_table.index:
                satisfied_count = cross_table.loc[age_group, True] if True in cross_table.columns else 0
                total_count = cross_table.loc[age_group].sum()
                percentage = (satisfied_count / total_count * 100) if total_count > 0 else 0
                print(f"  {age_group}: {satisfied_count}/{total_count}명 ({percentage:.1f}%)")
    
    def statistical_summary(self):
        """통계학적 요약"""
        print("\n" + "=" * 60)
        print("통계학적 요약")
        print("=" * 60)
        
        # 표본 크기
        n = len(self.processed_data)
        print(f"\n📊 표본 크기: {n}명")
        
        # 신뢰구간 계산 (95% 신뢰도)
        confidence_level = 0.95
        z_score = 1.96  # 95% 신뢰도
        
        # 주요 만족 요인 신뢰구간
        satisfaction_cols = [col for col in self.processed_data.columns if col.startswith('satisfaction_')]
        
        print(f"\n📈 주요 만족 요인 신뢰구간 (95% 신뢰도):")
        for col in satisfaction_cols:
            factor_name = col.replace('satisfaction_', '')
            p = self.processed_data[col].mean()
            if p > 0:
                margin_error = z_score * np.sqrt((p * (1 - p)) / n)
                lower_bound = p - margin_error
                upper_bound = p + margin_error
                print(f"  {factor_name}: {p:.3f} ± {margin_error:.3f} [{lower_bound:.3f}, {upper_bound:.3f}]")
        
        # 주요 불만 요인 신뢰구간
        complaint_cols = [col for col in self.processed_data.columns if col.startswith('complaint_')]
        
        print(f"\n📉 주요 불만 요인 신뢰구간 (95% 신뢰도):")
        for col in complaint_cols:
            factor_name = col.replace('complaint_', '')
            p = self.processed_data[col].mean()
            if p > 0:
                margin_error = z_score * np.sqrt((p * (1 - p)) / n)
                lower_bound = p - margin_error
                upper_bound = p + margin_error
                print(f"  {factor_name}: {p:.3f} ± {margin_error:.3f} [{lower_bound:.3f}, {upper_bound:.3f}]")
    
    def create_visualizations(self):
        """시각화 생성"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('현장조사 고객별 통계 분석 (MECE 프레임워크)', fontsize=16, fontweight='bold')
        
        # 1. 연령대별 분포
        age_dist = self.processed_data['age_group'].value_counts().sort_index()
        axes[0, 0].pie(age_dist.values, labels=age_dist.index, autopct='%1.1f%%', startangle=90)
        axes[0, 0].set_title('연령대별 분포')
        
        # 2. 성별 분포
        gender_dist = self.processed_data['gender_clean'].value_counts()
        axes[0, 1].pie(gender_dist.values, labels=gender_dist.index, autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title('성별 분포')
        
        # 3. 방문 빈도
        visit_freq = self.processed_data['visit_frequency'].value_counts()
        axes[0, 2].bar(range(len(visit_freq)), visit_freq.values)
        axes[0, 2].set_xticks(range(len(visit_freq)))
        axes[0, 2].set_xticklabels(visit_freq.index, rotation=45)
        axes[0, 2].set_title('방문 빈도 분포')
        axes[0, 2].set_ylabel('고객 수')
        
        # 4. 만족 요인
        satisfaction_cols = [col for col in self.processed_data.columns if col.startswith('satisfaction_')]
        satisfaction_counts = [self.processed_data[col].sum() for col in satisfaction_cols]
        satisfaction_labels = [col.replace('satisfaction_', '') for col in satisfaction_cols]
        
        axes[1, 0].barh(satisfaction_labels, satisfaction_counts)
        axes[1, 0].set_title('만족 요인 순위')
        axes[1, 0].set_xlabel('고객 수')
        
        # 5. 불만 요인
        complaint_cols = [col for col in self.processed_data.columns if col.startswith('complaint_')]
        complaint_counts = [self.processed_data[col].sum() for col in complaint_cols]
        complaint_labels = [col.replace('complaint_', '') for col in complaint_cols]
        
        axes[1, 1].barh(complaint_labels, complaint_counts)
        axes[1, 1].set_title('불만 요인 순위')
        axes[1, 1].set_xlabel('고객 수')
        
        # 6. 메뉴 선호도
        menu_cols = [col for col in self.processed_data.columns if col.startswith('menu_')]
        menu_counts = [self.processed_data[col].sum() for col in menu_cols]
        menu_labels = [col.replace('menu_', '') for col in menu_cols]
        
        axes[1, 2].barh(menu_labels, menu_counts)
        axes[1, 2].set_title('메뉴 선호도 순위')
        axes[1, 2].set_xlabel('고객 수')
        
        plt.tight_layout()
        plt.savefig('customer_survey_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def run_complete_analysis(self):
        """완전한 MECE 분석 실행"""
        print("🔍 현장조사 고객별 통계 분석 (MECE 프레임워크)")
        print("=" * 80)
        
        # MECE 1-5 분석 실행
        demographics = self.analyze_demographics()
        behavioral = self.analyze_behavioral_patterns()
        satisfaction = self.analyze_satisfaction_factors()
        dissatisfaction = self.analyze_dissatisfaction_factors()
        menu_prefs = self.analyze_menu_preferences()
        
        # 교차 분석
        self.cross_analysis_age_satisfaction()
        
        # 통계학적 요약
        self.statistical_summary()
        
        # 시각화
        self.create_visualizations()
        
        return {
            'demographics': demographics,
            'behavioral': behavioral,
            'satisfaction': satisfaction,
            'dissatisfaction': dissatisfaction,
            'menu_preferences': menu_prefs
        }

# 분석 실행
if __name__ == "__main__":
    analyzer = CustomerSurveyAnalyzer()
    results = analyzer.run_complete_analysis()
    
    print("\n" + "=" * 80)
    print("✅ MECE 프레임워크 기반 통계 분석 완료!")
    print("📊 시각화 파일: customer_survey_analysis.png")
    print("=" * 80)
