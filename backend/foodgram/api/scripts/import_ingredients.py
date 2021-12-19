import json
from ..models import Ingredient
import csv
from pathlib import Path


def run():
    # currentDirectory = Path('../../data/ingredients.csv')
    #
    # for currentFile in currentDirectory.iterdir():
    #     print(currentFile)
    with open(Path('../../data/ingredients.csv'), newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            Ingredient.objects.create(name=row[0], measurement_unit=row[1]).save()
        print('Данные успешно импортированы')