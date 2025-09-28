"""
real_menu_pricing.py
~~~~~~~~~~~~~~~~~~~~

실제 상품별 판매 데이터를 기반으로 한 메뉴 가격 산정 프로그램
Excel 파일의 실제 데이터를 사용하여 원가 분석 및 가격 산정을 수행합니다.
"""

import argparse
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np

try:
    import matplotlib.pyplot as plt
    # 한글 폰트 설정
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False
except Exception:
    plt = None

@dataclass
class MenuItem:
    name: str
    daily_sales: float
    cost_ratio: float
    suggested_price: float = 0.0
    gross_margin: float = 0.0
    tier: str = ""

    def calculate_pricing(self, base_cost: float = 1000.0, ideal_pct: float = 0.30) -> None:
        """기준 원가를 바탕으로 가격 계산"""
        # 원가율을 이용해 실제 원가 계산
        actual_cost = base_cost * self.cost_ratio
        
        # 이상적인 판매가 계산 (식재료비 비율 기준)
        self.suggested_price = actual_cost / ideal_pct
        
        # 총이익률 계산
        if self.suggested_price > 0:
            self.gross_margin = (self.suggested_price - actual_cost) / self.suggested_price

    def categorize_tier(self, tiers: List[float]) -> None:
        """가격 구간별 분류"""
        for threshold in sorted(tiers):
            if self.suggested_price <= threshold:
                self.tier = f"≤{int(threshold):,}원"
                return
        self.tier = f">{int(tiers[-1]):,}원"

def load_real_data() -> List[MenuItem]:
    """실제 상품 데이터를 기반으로 한 데이터"""
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
    
    menu_items = []
    for name, (daily_sales, cost_ratio) in real_products.items():
        menu_item = MenuItem(
            name=name,
            daily_sales=daily_sales,
            cost_ratio=cost_ratio
        )
        menu_items.append(menu_item)
    
    return menu_items

def print_summary(menu_items: List[MenuItem], tiers: List[float], ideal_pct: float, base_cost: float) -> None:
    """분석 결과 요약 출력"""
    print("=" * 100)
    print("🍽️ 실제 상품 데이터 기반 메뉴 가격 분석")
    print("=" * 100)
    
    print(f"\n📊 분석 기준:")
    print(f"  • 기준 원가: {base_cost:,.0f}원")
    print(f"  • 식재료비 비율: {ideal_pct*100:.0f}%")
    print(f"  • 목표 총이익률: {(1-ideal_pct)*100:.0f}%")
    print(f"  • 분석 상품 수: {len(menu_items)}개")
    
    print(f"\n📈 상품별 원가율 분석:")
    print(f"{'상품명':<25} {'일평균판매량':<12} {'원가율':<10} {'실제원가':<12} {'제안가':<12} {'총이익률':<10} {'가격구간':<12}")
    print("-" * 100)
    
    for item in menu_items:
        actual_cost = base_cost * item.cost_ratio
        print(f"{item.name:<25} {item.daily_sales:<12.1f} {item.cost_ratio:<10.3f} {actual_cost:<12,.0f} {item.suggested_price:<12,.0f} {item.gross_margin:<10.1%} {item.tier:<12}")
    
    # 통계 요약
    print(f"\n📊 통계 요약:")
    suggested_prices = [item.suggested_price for item in menu_items]
    gross_margins = [item.gross_margin for item in menu_items]
    
    print(f"  • 평균 제안가: {np.mean(suggested_prices):,.0f}원")
    print(f"  • 최고가: {np.max(suggested_prices):,.0f}원")
    print(f"  • 최저가: {np.min(suggested_prices):,.0f}원")
    print(f"  • 평균 총이익률: {np.mean(gross_margins):.1%}")
    
    # 가격 구간별 분포
    print(f"\n💰 가격 구간별 분포:")
    tier_counts = {}
    for item in menu_items:
        tier_counts[item.tier] = tier_counts.get(item.tier, 0) + 1
    
    for tier, count in sorted(tier_counts.items()):
        percentage = (count / len(menu_items)) * 100
        print(f"  • {tier}: {count}개 ({percentage:.1f}%)")

def generate_menu_board(menu_items: List[MenuItem], tiers: List[float], outfile: str = "real_menu_board.png"):
    """실제 메뉴 데이터 기반 메뉴판 시각화"""
    if plt is None:
        return None
    
    # 데이터 준비
    names = [item.name for item in menu_items]
    suggested_prices = [item.suggested_price for item in menu_items]
    categories = [item.tier for item in menu_items]
    
    # 색상 정의
    def _cat_key(cat: str) -> float:
        digits = ''.join(ch for ch in cat if ch.isdigit())
        return float(digits) if digits else float('inf')
    
    unique_cats = sorted(set(categories), key=_cat_key)
    colors = plt.cm.get_cmap('Set3', len(unique_cats))
    cat_to_colour = {cat: colors(i) for i, cat in enumerate(unique_cats)}
    
    # 그래프 생성
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
    
    # 상단: 가격별 막대 그래프
    y_pos = np.arange(len(names))
    bars = ax1.barh(y_pos, suggested_prices, color=[cat_to_colour[cat] for cat in categories], alpha=0.8)
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names, fontsize=10)
    ax1.set_xlabel('제안가 (원)', fontsize=12)
    ax1.set_title('실제 상품 데이터 기반 메뉴 가격 분석', fontsize=16, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 막대 위에 가격 표시
    for i, (bar, price) in enumerate(zip(bars, suggested_prices)):
        width = bar.get_width()
        ax1.text(width + 50, bar.get_y() + bar.get_height()/2,
                f'₩{price:,.0f}', ha='left', va='center', fontsize=9)
    
    # 하단: 총이익률 분석
    gross_margins = [item.gross_margin * 100 for item in menu_items]
    bars2 = ax2.barh(y_pos, gross_margins, color=[cat_to_colour[cat] for cat in categories], alpha=0.8)
    
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(names, fontsize=10)
    ax2.set_xlabel('총이익률 (%)', fontsize=12)
    ax2.set_title('메뉴별 총이익률 분석', fontsize=16, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axvline(x=70, color='red', linestyle='--', alpha=0.7, label='목표 이익률 (70%)')
    ax2.legend()
    
    # 막대 위에 이익률 표시
    for i, (bar, margin) in enumerate(zip(bars2, gross_margins)):
        width = bar.get_width()
        ax2.text(width + 1, bar.get_y() + bar.get_height()/2,
                f'{margin:.1f}%', ha='left', va='center', fontsize=9)
    
    # 범례 추가
    for cat in unique_cats:
        ax1.barh([], [], color=cat_to_colour[cat], label=cat)
    ax1.legend(title='가격 구간', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(outfile, dpi=300, bbox_inches='tight')
    plt.show()
    
    return outfile

def main(argv: Optional[List[str]] = None) -> None:
    """메인 함수"""
    parser = argparse.ArgumentParser(description="실제 상품 데이터 기반 메뉴 가격 분석")
    parser.add_argument('--tiers', type=float, nargs='+', default=[3990, 7990, 9990],
                        help='가격 구간 (원)')
    parser.add_argument('--ideal_pct', type=float, default=0.30,
                        help='이상적인 식재료비 비율')
    parser.add_argument('--base_cost', type=float, default=1000.0,
                        help='기준 원가 (원)')
    parser.add_argument('--board', type=str, default='real_menu_board.png',
                        help='생성할 메뉴판 이미지 파일명')
    
    args = parser.parse_args(argv)
    
    # 실제 상품 데이터 로드
    print("📁 실제 상품 데이터를 로드합니다...")
    menu_items = load_real_data()
    print(f"✅ {len(menu_items)}개 상품 데이터를 읽었습니다.")
    
    # 각 메뉴의 가격 계산
    for item in menu_items:
        item.calculate_pricing(args.base_cost, args.ideal_pct)
        item.categorize_tier(args.tiers)
    
    # 결과 출력
    print_summary(menu_items, args.tiers, args.ideal_pct, args.base_cost)
    
    # 메뉴판 생성
    print(f"\n📊 메뉴판 이미지 생성 중...")
    image_path = generate_menu_board(menu_items, args.tiers, args.board)
    
    if image_path:
        print(f"✅ 메뉴판 이미지 생성 완료: {image_path}")
    else:
        print("❌ matplotlib이 설치되어 있지 않아 이미지를 생성하지 않았습니다.")

if __name__ == '__main__':
    main()
