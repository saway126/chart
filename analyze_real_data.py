# -*- coding: utf-8 -*-
"""
실제 상품 데이터 기반 메뉴 가격 분석 프로그램
Excel에서 추출한 실제 상품 데이터를 사용하여 가격 분석을 수행합니다.
"""

# 실제 상품별 원가율 데이터 (Excel에서 추출)
real_products = {
    '시그니처양념치킨': (82.075, 0.536),
    '시그니처통살치킨': (77.775, 0.596),
    '마늘간장치킨': (74.75, 0.539),
    '윙봉콤보': (77.175, 0.520),
    '단호박오리구이': (46.05, 0.477),
    '칠리깐쇼새우': (36.45, 0.618),
    '매콤칠리나시고랭': (32.475, 0.334),
    '오징어튀김': (34.975, 0.467),
    '잡채': (25.3, 0.364),
    '크림새우': (34.15, 0.611),
    '스파이시깐풍치킨': (36.475, 0.555),
    '게살볶음밥': (21.925, 0.223),
    '새우볶음밥': (19.0, 0.429),
    '치즈소떡소떡': (24.15, 0.500),
    '해산물빠에야': (20.125, 0.482),
    '마늘간장미트볼': (27.225, 0.412),
}

def analyze_real_data():
    base_cost = 1000.0
    ideal_pct = 0.30
    
    print('=' * 100)
    print('🍽️ 실제 상품 데이터 기반 메뉴 가격 분석')
    print('=' * 100)
    print(f'\n📊 분석 기준:')
    print(f'  • 기준 원가: {base_cost:,.0f}원')
    print(f'  • 식재료비 비율: {ideal_pct*100:.0f}%')
    print(f'  • 목표 총이익률: {(1-ideal_pct)*100:.0f}%')
    print(f'  • 분석 상품 수: {len(real_products)}개')
    
    print(f'\n📈 상품별 원가율 분석:')
    print(f'{"상품명":<25} {"일평균판매량":<12} {"원가율":<10} {"실제원가":<12} {"제안가":<12} {"총이익률":<10} {"가격구간":<12}')
    print('-' * 100)
    
    suggested_prices = []
    gross_margins = []
    
    for name, (daily_sales, cost_ratio) in real_products.items():
        actual_cost = base_cost * cost_ratio
        suggested_price = actual_cost / ideal_pct
        gross_margin = (suggested_price - actual_cost) / suggested_price
        
        # 가격 구간 분류
        if suggested_price <= 3990:
            tier = '≤3,990원'
        elif suggested_price <= 7990:
            tier = '≤7,990원'
        elif suggested_price <= 9990:
            tier = '≤9,990원'
        else:
            tier = '>9,990원'
        
        print(f'{name:<25} {daily_sales:<12.1f} {cost_ratio:<10.3f} {actual_cost:<12,.0f} {suggested_price:<12,.0f} {gross_margin:<10.1%} {tier:<12}')
        
        suggested_prices.append(suggested_price)
        gross_margins.append(gross_margin)
    
    # 통계 요약
    print(f'\n📊 통계 요약:')
    print(f'  • 평균 제안가: {sum(suggested_prices)/len(suggested_prices):,.0f}원')
    print(f'  • 최고가: {max(suggested_prices):,.0f}원')
    print(f'  • 최저가: {min(suggested_prices):,.0f}원')
    print(f'  • 평균 총이익률: {sum(gross_margins)/len(gross_margins):.1%}')
    
    # 가격 구간별 분포
    print(f'\n💰 가격 구간별 분포:')
    tier_counts = {}
    for name, (daily_sales, cost_ratio) in real_products.items():
        actual_cost = base_cost * cost_ratio
        suggested_price = actual_cost / ideal_pct
        
        if suggested_price <= 3990:
            tier = '≤3,990원'
        elif suggested_price <= 7990:
            tier = '≤7,990원'
        elif suggested_price <= 9990:
            tier = '≤9,990원'
        else:
            tier = '>9,990원'
        
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
    
    for tier, count in sorted(tier_counts.items()):
        percentage = (count / len(real_products)) * 100
        print(f'  • {tier}: {count}개 ({percentage:.1f}%)')
    
    print(f'\n🎯 비즈니스 인사이트:')
    print(f'  • 모든 상품이 3,990원 이하로 매우 경쟁력 있는 가격')
    print(f'  • 70% 총이익률로 높은 수익성 확보')
    print(f'  • 게살볶음밥(22.3%)과 매콤칠리나시고랭(33.4%)이 가장 효율적')
    print(f'  • 시그니처양념치킨(82.1개)이 가장 인기 상품')

if __name__ == '__main__':
    analyze_real_data()
