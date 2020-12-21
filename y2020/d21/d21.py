import re
from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str

RE_INGREDIENTS = re.compile(r"(.+?) \(contains (.+?)\)")


def count_non_allergens(file: List[str]) -> List[str]:
    all_ingredients = set()
    ingredients: dict = {}
    allergens: dict = {}
    ingredients_count: dict = {}
    for line in file:
        raw_ingredients, raw_allergens = RE_INGREDIENTS.match(line).groups()
        ingredients_line = raw_ingredients.split(" ")
        allergens_line = raw_allergens.split(", ")
        # List allergen possibilities for the current ingredient
        for ingredient in ingredients_line:
            all_ingredients.add(ingredient)
            ingredients[ingredient] = ingredients.get(ingredient) or set()
            ingredients_count[ingredient] = ingredients_count.get(ingredient, 0) + 1
            for allergen in allergens_line:
                ingredients[ingredient].add(allergen)
        # List possible ingredients for a given allergen
        for allergen in allergens_line:
            s = set()
            for ingredient in ingredients_line:
                s.add(ingredient)
            allergens[allergen] = (allergens.get(allergen, s)).intersection(s)
    # Once file is processed, check which ingredient isn't in allergens
    probably_allergens = set()
    for (_, ingredients_set) in allergens.items():
        for ingredient in ingredients_set:
            probably_allergens.add(ingredient)
    non_allergens = all_ingredients.copy()
    for ingredient in probably_allergens:
        non_allergens.remove(ingredient)
    # Now count how many times they appear in the recipes
    print(allergens)
    return sum(count for (ingredient, count) in ingredients_count.items() if ingredient in non_allergens)


def test():
    test_data = read_file_list_str("test.txt")
    assert count_non_allergens(test_data) == 5
    print("✅ Valid test")


def real():
    real_data = read_file_list_str("data.txt")
    part1 = count_non_allergens(real_data)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


test()
real()
