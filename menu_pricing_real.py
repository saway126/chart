"""
menu_pricing_real.py
~~~~~~~~~~~~~~~~~~~~

실제 상품별 판매 데이터를 기반으로 한 메뉴 가격 산정 프로그램
Excel 파일의 실제 데이터를 사용하여 원가 분석 및 가격 산정을 수행합니다.

주요 기능:
* 실제 상품 데이터(Excel)를 읽어 원가율을 분석합니다.
* 각 메뉴의 원가율을 바탕으로 이상적인 판매가를 계산합니다.
* 식재료비 비율과 총이익률을 고려한 가격 제안을 제공합니다.
* 가격 구간별 메뉴 분류 및 시각화를 제공합니다.

사용법:
    python menu_pricing_real.py --excel "상품별 판매 데이터.xlsx" [--tiers 3990 7990 9990] [--ideal_pct 0.3]
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

def read_excel_data(file_path: str) -> List[MenuItem]:
    """Excel 파일에서 상품 데이터 읽기"""
    try:
        # Excel 파일 읽기 (헤더 없이)
        df = pd.read_excel(file_path, header=None)
        print(f"Excel 파일 읽기 완료: {len(df)}행")
        
        menu_items = []
        
        # 데이터 행 찾기 (3행부터 시작)
        for i in range(3, len(df)):
            row = df.iloc[i]
            
            # 상품명과 원가율이 있는 행만 처리
            if pd.notna(row[0]) and pd.notna(row[-1]):
                try:
                    name = str(row[0]).strip()
                    daily_sales = float(row[1]) if pd.notna(row[1]) else 0.0
                    cost_ratio = float(row[-1]) if pd.notna(row[-1]) else 0.0
                    
                    # 유효한 데이터만 추가
                    if name and cost_ratio > 0:
                        menu_item = MenuItem(
                            name=name,
                            daily_sales=daily_sales,
                            cost_ratio=cost_ratio
                        )
                        menu_items.append(menu_item)
                        print(f"상품 추가: {name} (원가율: {cost_ratio})")
                except (ValueError, TypeError) as e:
                    print(f"데이터 처리 오류 (행 {i}): {e}")
                    continue
        
        print(f"총 {len(menu_items)}개 상품 데이터를 읽었습니다.")
        return menu_items
    
    except Exception as e:
        print(f"Excel 파일 읽기 오류: {e}")
        return []

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
    parser.add_argument('--excel', type=str, required=True, help='Excel 파일 경로')
    parser.add_argument('--tiers', type=float, nargs='+', default=[3990, 7990, 9990],
                        help='가격 구간 (원)')
    parser.add_argument('--ideal_pct', type=float, default=0.30,
                        help='이상적인 식재료비 비율')
    parser.add_argument('--base_cost', type=float, default=1000.0,
                        help='기준 원가 (원)')
    parser.add_argument('--board', type=str, default='real_menu_board.png',
                        help='생성할 메뉴판 이미지 파일명')
    
    args = parser.parse_args(argv)
    
    # Excel 데이터 읽기
    print("📁 Excel 파일을 읽는 중...")
    menu_items = read_excel_data(args.excel)
    
    if not menu_items:
        print("❌ 유효한 데이터를 찾을 수 없습니다.")
        return
    
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