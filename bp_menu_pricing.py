# -*- coding: utf-8 -*-
"""
BP 정리 자료 기반 메뉴 가격 산정 프로그램
HWP 파일의 BP 정리 자료를 분석하여 메뉴별 원가 및 가격을 계산합니다.
"""

def analyze_bp_menu_data():
    """BP 정리 자료 기반 메뉴 분석"""
    
    print('=' * 100)
    print('🍽️ BP 정리 자료 기반 메뉴 가격 분석')
    print('=' * 100)
    
    # BP 정리 자료에서 추출한 메뉴 데이터
    bp_menus = {
        # 저속라인렌틸콩 메뉴
        '렌틸콩 카레 볶음': {
            'category': '저속라인렌틸콩',
            'cost_per_kg': 5000,
            'weight_g': 200,  # 추정 중량
            'reason': '풍부한 식이섬유, 혈당 조절, 항산화 효과',
            'trend': '건강 관심 증가에 적합'
        },
        '렌틸콩 스프': {
            'category': '저속라인렌틸콩',
            'cost_per_kg': 5000,
            'weight_g': 300,  # 추정 중량
            'reason': '풍부한 식이섬유, 혈당 조절, 항산화 효과',
            'trend': '건강 관심 증가에 적합'
        },
        
        # 프리미엄 메뉴
        '채소 프듬뿍 리 직화불고기 비비고 영양밥': {
            'category': '프리미엄',
            'ingredients': {
                '불고기': {'weight_g': 70, 'cost_per_g': 24.465, 'total_cost': 1713},
                '밥': {'weight_g': 150, 'cost_per_g': 1.4, 'total_cost': 210},
                '기본 야채·양념': {'weight_g': 0, 'cost_per_g': 0, 'total_cost': 220},
                '추가 볶은 채소': {'weight_g': 100, 'cost_per_g': 2.0, 'total_cost': 200},
                '포장': {'weight_g': 0, 'cost_per_g': 0, 'total_cost': 150}
            },
            'total_weight_g': 340,
            'total_cost': 2493,
            'reason': '국민 반찬의 집밥 취향, 40-50대 선호, 비비고 브랜드 신뢰도 4.7점'
        },
        
        '연어 유자간장 양밥': {
            'category': '프리미엄',
            'selling_price': 9990,
            'ingredients': {
                '연어(훈제/그라브락스)': {'weight_g': 80, 'estimated_cost_per_g': 15, 'total_cost': 1200},
                '현미·퀴노아 밥': {'weight_g': 150, 'estimated_cost_per_g': 2, 'total_cost': 300},
                '채소 믹스': {'weight_g': 30, 'estimated_cost_per_g': 3, 'total_cost': 90},
                '유자간장(저당)': {'weight_g': 20, 'estimated_cost_per_g': 2, 'total_cost': 40},
                '포장/부자재': {'weight_g': 0, 'estimated_cost_per_g': 0, 'total_cost': 100}
            },
            'total_weight_g': 280,
            'total_cost': 1730
        },
        
        '양배추 닭가슴살 야채말이': {
            'category': '프리미엄',
            'selling_price': 9990,
            'weight_g': 370,
            'cost_per_kg': 9222,
            'margin_rate': 0.658,
            'reason': '건강하게 한끼, 아삭한 식감, 소스 없이도 맛있음'
        },
        
        '닭가슴살 테이크 보울': {
            'category': '프리미엄',
            'selling_price': 7990,
            'weight_g': 300,
            'cost_per_kg': 7433,
            'margin_rate': 0.721,
            'reason': '고단백, 가성비 우수, 편리한 식사'
        }
    }
    
    # 분석 기준 설정
    ideal_food_cost_ratio = 0.30  # 30% 식재료비 비율
    target_margin = 0.70  # 70% 목표 마진
    
    print(f'\n📊 분석 기준:')
    print(f'  • 식재료비 비율: {ideal_food_cost_ratio*100:.0f}%')
    print(f'  • 목표 마진율: {target_margin*100:.0f}%')
    print(f'  • 분석 메뉴 수: {len(bp_menus)}개')
    
    print(f'\n📈 메뉴별 상세 분석:')
    print(f'{"메뉴명":<35} {"카테고리":<15} {"중량(g)":<8} {"원가(원)":<10} {"제안가(원)":<12} {"마진율":<8} {"특징":<20}')
    print('-' * 120)
    
    total_costs = []
    suggested_prices = []
    margin_rates = []
    
    for menu_name, data in bp_menus.items():
        category = data['category']
        
        # 원가 계산
        if 'total_cost' in data:
            cost = data['total_cost']
        elif 'cost_per_kg' in data and 'weight_g' in data:
            cost = (data['cost_per_kg'] * data['weight_g']) / 1000
        else:
            cost = 0
        
        # 제안가 계산
        if 'selling_price' in data:
            suggested_price = data['selling_price']
        else:
            suggested_price = cost / ideal_food_cost_ratio
        
        # 마진율 계산
        if 'margin_rate' in data:
            margin_rate = data['margin_rate']
        else:
            margin_rate = (suggested_price - cost) / suggested_price if suggested_price > 0 else 0
        
        # 특징
        if 'reason' in data:
            feature = data['reason'][:20] + '...' if len(data['reason']) > 20 else data['reason']
        else:
            feature = 'BP 정리 자료'
        
        print(f'{menu_name:<35} {category:<15} {data.get("weight_g", 0):<8} {cost:<10,.0f} {suggested_price:<12,.0f} {margin_rate:<8.1%} {feature:<20}')
        
        total_costs.append(cost)
        suggested_prices.append(suggested_price)
        margin_rates.append(margin_rate)
    
    # 통계 요약
    print(f'\n📊 통계 요약:')
    print(f'  • 평균 원가: {sum(total_costs)/len(total_costs):,.0f}원')
    print(f'  • 평균 제안가: {sum(suggested_prices)/len(suggested_prices):,.0f}원')
    print(f'  • 평균 마진율: {sum(margin_rates)/len(margin_rates):.1%}')
    print(f'  • 최고가: {max(suggested_prices):,.0f}원')
    print(f'  • 최저가: {min(suggested_prices):,.0f}원')
    
    # 카테고리별 분석
    print(f'\n🏷️ 카테고리별 분석:')
    categories = {}
    for menu_name, data in bp_menus.items():
        category = data['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(menu_name)
    
    for category, menus in categories.items():
        print(f'  • {category}: {len(menus)}개 메뉴')
        for menu in menus:
            print(f'    - {menu}')
    
    # 비즈니스 인사이트
    print(f'\n🎯 비즈니스 인사이트:')
    print(f'  • 렌틸콩 메뉴: 건강 트렌드에 맞는 저비용 고효율 메뉴')
    print(f'  • 프리미엄 메뉴: 높은 마진율로 수익성 우수')
    print(f'  • 불고기 메뉴: 40-50대 타겟층 선호도 높음')
    print(f'  • 연어 메뉴: 고가격 프리미엄 포지셔닝')
    
    # 가격 전략 제안
    print(f'\n💡 가격 전략 제안:')
    print(f'  • 저속라인렌틸콩: 3,000-5,000원 (건강 메시지 강조)')
    print(f'  • 프리미엄 메뉴: 7,000-10,000원 (품질과 브랜드 가치)')
    print(f'  • 불고기 메뉴: 8,000-12,000원 (가족 단위 타겟)')
    print(f'  • 연어 메뉴: 9,000-15,000원 (프리미엄 포지셔닝)')

if __name__ == '__main__':
    analyze_bp_menu_data()
