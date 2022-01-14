import json
from ..models import Ingredient
import csv
from pathlib import Path


def run():
#    Ingredient.objects.create(name='Ингредиент1', measurement_unit='ед.изм.').save()
    with open(Path('data/ingredients.csv'), newline='',encoding="cp1251") as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            Ingredient.objects.create(name=row[0], measurement_unit=row[1]).save()
        print('Данные успешно импортированы')
