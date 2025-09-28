"""
menu_pricing.py
~~~~~~~~~~~~~~~~

이 스크립트는 재료 비용을 분석하고 레시피를 기반으로 메뉴 가격을 계산하는 예제입니다. 
주요 기능은 다음과 같습니다.

* 재료 데이터(CSV/딕셔너리)를 읽어 kg당 단가를 계산합니다.
* 각 메뉴에 사용되는 재료와 양을 읽어 총 원가를 계산합니다.
* 식재료비 비율(일반적으로 28–35% 사이)로 이상적 판매가를 계산합니다:contentReference[oaicite:0]{index=0}.
* 총이익률(70% 목표)도 보고합니다:contentReference[oaicite:1]{index=1}.
* 3,990원/7,990원/9,990원 구간으로 메뉴를 분류합니다.
* matplotlib이 설치되어 있으면 메뉴판 이미지를 생성합니다.

사용법:
    python menu_pricing.py --ingredients ingredients.csv --recipes recipes.csv \
        [--tiers 3990 7990 9990] [--ideal_pct 0.3]

CSV 파일이 없으면 내부 샘플 데이터를 사용합니다.
"""

import argparse
import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

try:
    import matplotlib.pyplot as plt  # 메뉴판 이미지를 그리기 위해 사용
except Exception:
    plt = None

@dataclass
class Ingredient:
    name: str
    weight_kg: float
    cost_won: float

    @property
    def price_per_kg(self) -> float:
        if self.weight_kg <= 0:
            raise ValueError(f"Weight must be positive for ingredient {self.name}")
        return self.cost_won / self.weight_kg

@dataclass
class Recipe:
    name: str
    ingredients: Dict[str, float]  # ingredient name -> quantity in kg

    def cost(self, price_lookup: Dict[str, float]) -> float:
        total = 0.0
        for item, qty in self.ingredients.items():
            if item not in price_lookup:
                raise KeyError(f"Ingredient '{item}' missing from price list.")
            total += price_lookup[item] * qty
        return total

def read_ingredients(path: str) -> Dict[str, Ingredient]:
    ingredients: Dict[str, Ingredient] = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['ingredient'].strip()
            weight = float(row['weight'])
            unit = row.get('weight_unit', 'kg').strip().lower()
            cost = float(row['cost'])
            if unit in ('g', 'gram', 'grams'):
                weight_kg = weight / 1000.0
            elif unit in ('kg', 'kilogram', 'kilograms'):
                weight_kg = weight
            elif unit in ('l', 'liter', 'litre', 'liters', 'litres'):
                weight_kg = weight  # 1리터≈1kg 가정
            else:
                raise ValueError(f"Unknown weight unit '{unit}' for ingredient {name}")
            ingredients[name] = Ingredient(name, weight_kg, cost)
    return ingredients

def read_recipes(path: str) -> List[Recipe]:
    recipes: List[Recipe] = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            menu_name = row['menu'].strip()
            ing_quantities: Dict[str, float] = {}
            for key, value in row.items():
                if key == 'menu' or value in (None, ''):
                    continue
                qty = float(value)
                if qty > 0:
                    ing_quantities[key.strip()] = qty
            recipes.append(Recipe(menu_name, ing_quantities))
    return recipes

def suggest_price(cost: float, ideal_pct: float) -> float:
    if ideal_pct <= 0 or ideal_pct >= 1:
        raise ValueError("ideal_pct must be between 0 and 1 (exclusive)")
    return cost / ideal_pct

def gross_margin(price: float, cost: float) -> float:
    if price <= 0:
        raise ValueError("price must be positive")
    return (price - cost) / price

def categorise_price(price: float, tiers: List[float]) -> str:
    for threshold in sorted(tiers):
        if price <= threshold:
            return f"≤{int(threshold):,}원"
    return f">{int(tiers[-1]):,}원"

def load_sample_data() -> Tuple[Dict[str, Ingredient], List[Recipe]]:
    # 실제 상품 데이터를 기반으로 한 샘플 데이터
    ingredients = {
        'rice': Ingredient('rice', weight_kg=20.0, cost_won=40000),
        'chicken': Ingredient('chicken', weight_kg=10.0, cost_won=70000),
        'onion': Ingredient('onion', weight_kg=5.0, cost_won=10000),
        'soy_sauce': Ingredient('soy_sauce', weight_kg=1.0, cost_won=5000),
        'spice_mix': Ingredient('spice_mix', weight_kg=0.5, cost_won=8000),
    }
    recipes = [
        Recipe('Teriyaki Chicken Rice',
               {'rice': 0.20, 'chicken': 0.15, 'onion': 0.02, 'soy_sauce': 0.05}),
        Recipe('Chicken Salad',
               {'chicken': 0.20, 'onion': 0.10, 'spice_mix': 0.05}),
        Recipe('Onion Fried Rice',
               {'rice': 0.30, 'onion': 0.10, 'soy_sauce': 0.02}),
    ]
    return ingredients, recipes

def load_real_data() -> Tuple[Dict[str, Ingredient], List[Recipe]]:
    """실제 상품 데이터를 기반으로 한 데이터"""
    # 실제 상품별 원가율 데이터
    real_products = {
        '시그니처양념치킨': 0.536,
        '시그니처통살치킨': 0.596,
        '마늘간장치킨': 0.539,
        '윙봉콤보': 0.520,
        '단호박오리구이': 0.477,
        '칠리깐쇼새우': 0.618,
        '매콤칠리나시고랭': 0.334,
        '오징어튀김': 0.467,
        '잡채': 0.364,
        '크림새우': 0.611,
        '스파이시깐풍치킨': 0.555,
        '게살볶음밥': 0.223,
        '새우볶음밥': 0.429,
        '치즈소떡소떡': 0.500,
        '해산물빠에야': 0.482,
        '마늘간장미트볼': 0.412,
    }
    
    # 기준 원가 1000원으로 설정
    base_cost = 1000.0
    
    # 재료 데이터 생성 (실제 원가율을 반영)
    ingredients = {}
    for product, cost_ratio in real_products.items():
        actual_cost = base_cost * cost_ratio
        ingredients[product] = Ingredient(product, weight_kg=1.0, cost_won=actual_cost)
    
    # 레시피 데이터 생성 (각 상품이 자신의 재료를 사용)
    recipes = []
    for product, cost_ratio in real_products.items():
        recipes.append(Recipe(product, {product: 1.0}))
    
    return ingredients, recipes

def print_summary(ingredients: Dict[str, Ingredient], recipes: List[Recipe],
                  tiers: List[float], ideal_pct: float) -> None:
    price_lookup: Dict[str, float] = {name: ing.price_per_kg for name, ing in ingredients.items()}
    print("Ingredient price per kg:")
    print(f"{'Ingredient':<15}{'Weight (kg)':>12}{'Cost (₩)':>12}{'Price/kg (₩)':>15}")
    for name, ing in ingredients.items():
        print(f"{name:<15}{ing.weight_kg:>12.3f}{ing.cost_won:>12,.0f}{ing.price_per_kg:>15,.2f}")
    print()
    print(f"Menu summary (ideal food-cost pct = {ideal_pct*100:.0f}%):")
    print(f"{'Menu':<25}{'Cost (₩)':>12}{'Suggested Price (₩)':>20}{'Gross Margin':>15}{'Tier':>10}")
    for recipe in recipes:
        c = recipe.cost(price_lookup)
        suggested = suggest_price(c, ideal_pct)
        margin = gross_margin(suggested, c)
        tier = categorise_price(suggested, tiers)
        print(f"{recipe.name:<25}{c:>12,.0f}{suggested:>20,.0f}{margin:>15.0%}{tier:>10}")

def generate_menu_board(recipes: List[Recipe], price_lookup: Dict[str, float],
                        tiers: List[float], ideal_pct: float, outfile: str):
    if plt is None:
        return None
    names: List[str] = []
    costs: List[float] = []
    suggested_prices: List[float] = []
    categories: List[str] = []
    for recipe in recipes:
        c = recipe.cost(price_lookup)
        s = suggest_price(c, ideal_pct)
        names.append(recipe.name)
        costs.append(c)
        suggested_prices.append(s)
        categories.append(categorise_price(s, tiers))
    # 색상 정의
    def _cat_key(cat: str) -> float:
        digits = ''.join(ch for ch in cat if ch.isdigit())
        return float(digits) if digits else float('inf')
    unique_cats = sorted(set(categories), key=_cat_key)
    colours = plt.cm.get_cmap('Set2', len(unique_cats))
    cat_to_colour = {cat: colours(i) for i, cat in enumerate(unique_cats)}
    fig, ax = plt.subplots(figsize=(8, 4 + 0.4 * len(recipes)))
    for i, (name, price, cat) in enumerate(zip(names, suggested_prices, categories)):
        ax.barh(i, price, color=cat_to_colour[cat], edgecolor='black')
        ax.text(price * 1.01, i, f"₩{price:,.0f}", va='center', fontsize=10)
    ax.set_yticks(range(len(recipes)))
    ax.set_yticklabels(names)
    ax.set_xlabel('Price (₩)')
    ax.invert_yaxis()
    ax.set_title('Recommended Menu Prices by Tier')
    for cat in unique_cats:
        ax.barh([], [], color=cat_to_colour[cat], label=cat)
    ax.legend(title='Tier', bbox_to_anchor=(1.05, 1), loc='upper left')
    fig.tight_layout()
    fig.savefig(outfile)
    plt.close(fig)
    return outfile

def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Analyse ingredient costs and compute menu pricing.")
    parser.add_argument('--ingredients', type=str, help='CSV file containing ingredient data.')
    parser.add_argument('--recipes', type=str, help='CSV file containing recipe data.')
    parser.add_argument('--tiers', type=float, nargs='+', default=[3990, 7990, 9990],
                        help='Price tiers (원) for categorisation.')
    parser.add_argument('--ideal_pct', type=float, default=0.30,
                        help='Ideal food-cost percentage used to calculate suggested prices.')
    parser.add_argument('--board', type=str, default='menu_board.png',
                        help='Filename for the generated menu board image.')
    args = parser.parse_args(argv)
    if args.ingredients and args.recipes:
        ingredients = read_ingredients(args.ingredients)
        recipes = read_recipes(args.recipes)
    else:
        # 실제 상품 데이터 사용
        print("실제 상품 데이터를 로드합니다...")
        ingredients, recipes = load_real_data()
        print(f"로드된 상품 수: {len(ingredients)}개")
    print_summary(ingredients, recipes, tiers=args.tiers, ideal_pct=args.ideal_pct)
    price_lookup: Dict[str, float] = {name: ing.price_per_kg for name, ing in ingredients.items()}
    image_path = generate_menu_board(recipes, price_lookup, tiers=args.tiers,
                                     ideal_pct=args.ideal_pct, outfile=args.board)
    if image_path:
        print(f"\n메뉴판 이미지 생성 완료: {image_path}")
    else:
        print("\nmatplotlib이 설치되어 있지 않아 메뉴판 이미지를 생성하지 않았습니다.")

if __name__ == '__main__':
    main()