import tkinter as tk
from tkinter import scrolledtext

class Dessert:
    def __init__(self, name, calories):
        self.name = name
        self.calories = calories

class Girl:
    def __init__(self, name):
        self.name = name

class DessertCombination:
    def __init__(self, desserts, girls):
        self.desserts = desserts
        self.girls = girls
        self.combinations = []
        self.filtered_combinations = []
        self.min_calories = []
        self.max_calories = []

    def generate_combinations(self):
        for i in range(len(self.desserts)):
            for j in range(len(self.desserts)):
                for k in range(len(self.desserts)):
                    combination = [self.desserts[i], self.desserts[j], self.desserts[k]]
                    if combination not in self.combinations:
                        self.combinations.append(combination)

    def filter_combinations(self, max_calories):
        self.filtered_combinations = [combination for combination in self.combinations
                                      if sum(dessert.calories for dessert in combination) <= max_calories]

    def find_extreme(self, func, mode):
        if mode == "min":
            extreme = min(self.filtered_combinations, key=func)
        elif mode == "max":
            extreme = max(self.filtered_combinations, key=func)
        return extreme

    def calorie_count(self, combination):
        count = 0
        for dessert in combination:
            count += dessert.calories
        return count

    def calculate_combinations(self, max_calories):
        self.generate_combinations()
        self.filter_combinations(max_calories)
        self.filtered_combinations = sorted(self.filtered_combinations, key=self.calorie_count)
        self.min_calories = self.find_extreme(self.calorie_count, "min")
        self.max_calories = self.find_extreme(self.calorie_count, "max")

    def print_combinations(self):
        count = len(self.filtered_combinations)
        for i, combination in enumerate(self.filtered_combinations):
            print("Вариант №", i + 1, "- калорийность:", self.calorie_count(combination))
            for girl, dessert in zip(self.girls, combination):
                print(girl.name, 'будет есть', dessert.name, '({} ккал)'.format(dessert.calories))
            print('-' * 20)
        print("Итоговое количество вариантов:", count)
        print('-' * 20)

    def print_extreme_calories(self):
        print("Самый низкий уровень калорийности:")
        print("Калорийность:", self.calorie_count(self.min_calories))
        for girl, dessert in zip(self.girls, self.min_calories):
            print(girl.name, 'будет есть', dessert.name, '({} ккал)'.format(dessert.calories))
        print('-' * 20)

        print("Самый высокий уровень калорийности:")
        print("Калорийность:", self.calorie_count(self.max_calories))
        for girl, dessert in zip(self.girls, self.max_calories):
            print(girl.name, 'будет есть', dessert.name, '({} ккал)'.format(dessert.calories))
        print('-' * 20)



class DessertGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Комбинация десертов")

        self.desserts = [
            Dessert('десерт №1', 200),
            Dessert('десерт №2', 300),
            Dessert('десерт №3', 150),
            Dessert('десерт №4', 250),
            Dessert('десерт №5', 350),
            Dessert('десерт №6', 180),
            Dessert('десерт №7', 280),
            Dessert('десерт №8', 220),
            Dessert('десерт №9', 320),
            Dessert('десерт №10', 120)
        ]

        self.girls = [
            Girl('1-ая девушка'),
            Girl('2-ая девушка'),
            Girl('3-ая девушка')
        ]

        self.max_calories_label = tk.Label(root, text='Максимальная калорийность:')
        self.max_calories_label.pack(pady=10)

        self.max_calories_scale = tk.Scale(root, from_=360, to=1050, orient=tk.HORIZONTAL, length=300)
        self.max_calories_scale.pack()

        self.calculate_button = tk.Button(root, text='Рассчитать', command=self.calculate_combinations)
        self.calculate_button.pack(pady=5)

        self.result_text = tk.scrolledtext.ScrolledText(root, width=60, height=100)
        self.result_text.pack(pady=10)



    def calculate_combinations(self):
        max_calories = self.max_calories_scale.get()

        dessert_combination = DessertCombination(self.desserts, self.girls)
        dessert_combination.calculate_combinations(max_calories)

        result = "Комбинации десертов:\n\n"
        for i, combination in enumerate(dessert_combination.filtered_combinations):
            result += f"Вариант № {i + 1} - калорийность: {dessert_combination.calorie_count(combination)}\n"
            for girl, dessert in zip(self.girls, combination):
                result += f"{girl.name} будет есть {dessert.name} ({dessert.calories} ккал)\n"
            result += '-' * 20 + '\n'
        result += f"Итоговое количество вариантов: {len(dessert_combination.filtered_combinations)}\n\n"

        result += "Самый низкий уровень калорийности:\n"
        result += f"Калорийность: {dessert_combination.calorie_count(dessert_combination.min_calories)}\n"
        for girl, dessert in zip(self.girls, dessert_combination.min_calories):
            result += f"{girl.name} будет есть {dessert.name} ({dessert.calories} ккал)\n"
        result += '-' * 20 + '\n'

        result += "Самый высокий уровень калорийности:\n"
        result += f"Калорийность: {dessert_combination.calorie_count(dessert_combination.max_calories)}\n"
        for girl, dessert in zip(self.girls, dessert_combination.max_calories):
            result += f"{girl.name} будет есть {dessert.name} ({dessert.calories} ккал)\n"
        result += '-' * 20 + '\n'

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)



root = tk.Tk()
root.geometry("400x800")

dessert_gui = DessertGUI(root)
root.mainloop()