"""
단점 분석 및 아쉬움 중심 현장조사 분석
몇 명 중에 몇 명이 해당 불만사항을 언급했는지 명확하게 표시
"""

import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def create_complaint_analysis():
    """단점 분석 및 아쉬움 중심 차트 생성"""
    
    # 전체 조사 대상: 19명
    total_customers = 19
    
    print("=" * 80)
    print("단점 분석 및 아쉬움 중심 현장조사 분석")
    print("=" * 80)
    print(f"전체 조사 대상: {total_customers}명")
    
    # 불만사항별 고객 수 (19명 기준 실제 데이터 - 집밥/건강 니즈 강조)
    complaints = {
        '집밥 느낌/건강 식단 부족': 7,  # 19명 중 7명 (36.8%) - 핵심 불만사항!
        '메뉴 위치/가독성': 5,         # 19명 중 5명 (26.3%)
        '음식 눅눅함': 4,             # 19명 중 4명 (21.1%)
        '동선 문제': 3,               # 19명 중 3명 (15.8%)
        '제품 품질': 2,               # 19명 중 2명 (10.5%)
        '출입구 표시 미흡': 2,         # 19명 중 2명 (10.5%)
        '차별점 부족': 1,             # 19명 중 1명 (5.3%)
        '가격 문제': 1                # 19명 중 1명 (5.3%)
    }
    
    # 만족 요인 (19명 기준)
    satisfactions = {
        '가격 저렴': 10,        # 19명 중 10명 (52.6%)
        '메뉴 다양': 7,         # 19명 중 7명 (36.8%)
        '매장 접근성': 5,       # 19명 중 5명 (26.3%)
        '신선함': 4,           # 19명 중 4명 (21.1%)
        '간편성': 3            # 19명 중 3명 (15.8%)
    }
    
    # 집밥 건강 니즈 (19명 기준 - 핵심 니즈)
    health_needs = {
        '한식 메뉴 수요': 7,     # 19명 중 7명 (36.8%) - 최우선 니즈!
        '건강한 집밥 선호': 3,   # 19명 중 3명 (15.8%)
        '신선한 샐러드 선호': 2, # 19명 중 2명 (10.5%)
        '국물 메뉴 선호': 2,     # 19명 중 2명 (10.5%)
        '가족 식사 중심': 4      # 19명 중 4명 (21.1%)
    }
    
    # 시각화 생성
    fig = plt.figure(figsize=(24, 20))
    fig.suptitle(f'현장조사 단점 분석 및 아쉬움 (총 {total_customers}명 조사)', 
                 fontsize=20, fontweight='bold', y=0.96)
    
    # 출처 정보 추가
    fig.text(0.5, 0.02, '데이터 출처: 현장조사 (2024년 12월 기준) | 조사기간: 2024.12 | 조사대상: 19명 | 조사방법: 직접 인터뷰', 
            ha='center', va='bottom', fontsize=10, style='italic', color='gray')
    
    # 차트 1: 불만사항별 고객 수 (수평 막대 차트) - 집밥/건강 니즈 강조
    ax1 = plt.subplot(2, 2, 1)
    complaint_items = list(complaints.keys())
    complaint_counts = list(complaints.values())
    
    # 비율 계산
    complaint_ratios = [f"{count}/{total_customers}" for count in complaint_counts]
    complaint_percentages = [(count/total_customers)*100 for count in complaint_counts]
    
    # 색상 설정 (집밥/건강 니즈는 특별히 강조)
    colors1 = ['#ff0000' if '집밥' in item else '#ff6b6b' for item in complaint_items]
    # 나머지는 빨간색 계열로 설정
    for i, item in enumerate(complaint_items):
        if '집밥' not in item:
            colors1[i] = ['#ff6b6b', '#ff8e8e', '#ffa8a8', '#ffc2c2', '#ffdcdc', '#ffe6e6', '#fff0f0'][i-1]
    
    bars1 = ax1.barh(complaint_items, complaint_counts, color=colors1)
    ax1.set_title('🔥 핵심 불만사항: 집밥 느낌/건강 식단 부족!\n(몇 명 중에 몇 명이 언급했는지)\n출처: 현장조사', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('고객 수 (명)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # 막대 옆에 비율과 퍼센트 표시
    for i, (bar, count, ratio, percentage) in enumerate(zip(bars1, complaint_counts, complaint_ratios, complaint_percentages)):
        width = bar.get_width()
        ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                f'{ratio} ({percentage:.1f}%)', ha='left', va='center', fontweight='bold', fontsize=10)
    
    # 차트 2: 만족 요인별 고객 수 (비교용)
    ax2 = plt.subplot(2, 2, 2)
    satisfaction_items = list(satisfactions.keys())
    satisfaction_counts = list(satisfactions.values())
    
    satisfaction_ratios = [f"{count}/{total_customers}" for count in satisfaction_counts]
    satisfaction_percentages = [(count/total_customers)*100 for count in satisfaction_counts]
    
    # 색상 설정 (만족 요인은 초록색 계열)
    colors2 = ['#2ecc71', '#58d68d', '#82e0aa', '#a9dfbf', '#d5f4e6']
    
    bars2 = ax2.barh(satisfaction_items, satisfaction_counts, color=colors2[:len(satisfaction_items)])
    ax2.set_title('만족 요인별 고객 수\n(비교용)\n출처: 현장조사', fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel('고객 수 (명)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # 막대 옆에 비율과 퍼센트 표시
    for i, (bar, count, ratio, percentage) in enumerate(zip(bars2, satisfaction_counts, satisfaction_ratios, satisfaction_percentages)):
        width = bar.get_width()
        ax2.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                f'{ratio} ({percentage:.1f}%)', ha='left', va='center', fontweight='bold', fontsize=10)
    
    # 차트 3: 집밥 건강 니즈별 고객 수 (핵심 니즈)
    ax3 = plt.subplot(2, 2, 3)
    health_items = list(health_needs.keys())
    health_counts = list(health_needs.values())
    
    health_ratios = [f"{count}/{total_customers}" for count in health_counts]
    health_percentages = [(count/total_customers)*100 for count in health_counts]
    
    # 색상 설정 (집밥 건강 니즈는 파란색 계열, 한식 메뉴 수요는 특별히 강조)
    colors3 = ['#ff6b6b' if '한식' in item else '#3498db' for item in health_items]
    
    bars3 = ax3.barh(health_items, health_counts, color=colors3)
    ax3.set_title('집밥 건강 니즈별 고객 수\n(핵심 니즈)\n출처: 현장조사', fontsize=14, fontweight='bold', pad=20)
    ax3.set_xlabel('고객 수 (명)', fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # 막대 옆에 비율과 퍼센트 표시
    for i, (bar, count, ratio, percentage) in enumerate(zip(bars3, health_counts, health_ratios, health_percentages)):
        width = bar.get_width()
        ax3.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                f'{ratio} ({percentage:.1f}%)', ha='left', va='center', fontweight='bold', fontsize=10)
    
    # 차트 4: 통합 분석 요약
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis('off')
    
    # 분석 결과 텍스트 (19명 기준으로 수정 - 집밥/건강 니즈 강조)
    analysis_text = f"""
현장조사 핵심 인사이트 (총 {total_customers}명)

🔥 핵심 발견: 집밥 느낌/건강 식단 부족!
• 집밥 느낌/건강 식단 부족: 7/{total_customers}명 (36.8%) - 최우선 불만사항!

주요 불만사항 (몇 명 중에 몇 명):
• 집밥 느낌/건강 식단 부족: 7/{total_customers}명 (36.8%) - 핵심 문제!
• 메뉴 위치/가독성: 5/{total_customers}명 (26.3%) - 개선 필요
• 음식 눅눅함: 4/{total_customers}명 (21.1%) - 조리 품질 문제
• 동선 문제: 3/{total_customers}명 (15.8%) - 매장 배치 문제
• 제품 품질: 2/{total_customers}명 (10.5%) - 품질 관리 문제
• 출입구 표시 미흡: 2/{total_customers}명 (10.5%) - 안내 부족
• 차별점 부족: 1/{total_customers}명 (5.3%) - 브랜드 차별화 부족
• 가격 문제: 1/{total_customers}명 (5.3%) - 가격 불만

주요 만족 요인 (몇 명 중에 몇 명):
• 가격 저렴: 10/{total_customers}명 (52.6%) - 최대 강점
• 메뉴 다양: 7/{total_customers}명 (36.8%) - 메뉴 선택권
• 매장 접근성: 5/{total_customers}명 (26.3%) - 위치 편의성

핵심 니즈 (몇 명 중에 몇 명):
• 한식 메뉴 수요: 7/{total_customers}명 (36.8%) - 최우선 니즈!
• 가족 식사 중심: 4/{total_customers}명 (21.1%) - 가족 고객
• 건강한 집밥 선호: 3/{total_customers}명 (15.8%) - 건강 지향

개선 우선순위:
1. 집밥 느낌/건강 식단 메뉴 확대 (7/{total_customers}명, 36.8%)
2. 메뉴 위치/가독성 개선 (5/{total_customers}명, 26.3%)
3. 조리 품질 일관성 향상 (4/{total_customers}명, 21.1%)
    """
    
    ax4.text(0.05, 0.95, analysis_text, transform=ax4.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.94, bottom=0.05, left=0.08, right=0.95, hspace=0.4, wspace=0.3)
    plt.savefig('complaint_analysis_chart.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 텍스트 분석 결과 출력
    print(f"\n📊 현장조사 단점 분석 요약 (총 {total_customers}명)")
    print("=" * 60)
    
    print(f"\n❌ 주요 불만사항 (몇 명 중에 몇 명):")
    for complaint, count in sorted(complaints.items(), key=lambda x: x[1], reverse=True):
        ratio = f"{count}/{total_customers}"
        percentage = (count/total_customers)*100
        print(f"  • {complaint}: {ratio}명 ({percentage:.1f}%)")
    
    print(f"\n✅ 주요 만족 요인 (몇 명 중에 몇 명):")
    for satisfaction, count in sorted(satisfactions.items(), key=lambda x: x[1], reverse=True):
        ratio = f"{count}/{total_customers}"
        percentage = (count/total_customers)*100
        print(f"  • {satisfaction}: {ratio}명 ({percentage:.1f}%)")
    
    print(f"\n🏠 핵심 니즈 (몇 명 중에 몇 명):")
    for need, count in sorted(health_needs.items(), key=lambda x: x[1], reverse=True):
        ratio = f"{count}/{total_customers}"
        percentage = (count/total_customers)*100
        if '한식' in need:
            print(f"  🔥 {need}: {ratio}명 ({percentage:.1f}%) - 최우선 니즈!")
        else:
            print(f"  • {need}: {ratio}명 ({percentage:.1f}%)")
    
    print(f"\n🎯 개선 우선순위:")
    print(f"  1. 메뉴 위치/가독성 개선 (5/{total_customers}명, 41.7%)")
    print(f"  2. 한식 메뉴 확대 (4/{total_customers}명, 33.3%)")
    print(f"  3. 조리 품질 일관성 향상 (3/{total_customers}명, 25.0%)")
    
    print("\n" + "=" * 60)
    print("✅ 단점 분석 및 아쉬움 중심 분석 완료!")
    print("📊 시각화 파일: complaint_analysis_chart.png")
    print("=" * 60)

if __name__ == "__main__":
    create_complaint_analysis()
