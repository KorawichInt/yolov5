import numpy as np
import csv

food16_dict = {
    # food_class : [carb, protein, vegge]
    "basil": [0.45, 0.45, 0.1],
    "curry": [0.5, 0.3, 0.2],
    "fried_rice": [0.6, 0.3, 0.1],
    "grilled_pork": [0.2, 0.8, 0],
    "hy_fried_chicken": [0.2, 0.8, 0],
    "mama": [0.9, 0.05, 0.05],
    "noodles": [0.5, 0.35, 0.15],
    "omelet": [0.5, 0.45, 0.05],
    "papaya_salad": [0, 0.1, 0.9],
    "pizza": [0.8, 0.15, 0.05],
    "porridge": [0.7, 0.25, 0.05],
    "red_crispy_pork": [0.5, 0.4, 0.1],
    "sandwich": [0.8, 0.1, 0.1],
    "sashimi": [0, 1, 0],
    "steak": [0.2, 0.6, 0.2],
    "stir_fried_veg": [0, 0.2, 0.8]
}

food_class_names = list(food16_dict.keys())

# Target ratio (normalized to 1:1:1)
target_ratio = [1/3, 1/3, 1/3]

# Function to recommend the next meal's ingredients based on the current average meal ratio
def recommend_next_meal(current_avg_ratio):
    recommend_ratio = [
        np.float16(2 * target_ratio[0] - current_avg_ratio[0]),
        np.float16(2 * target_ratio[1] - current_avg_ratio[1]),
        np.float16(2 * target_ratio[2] - current_avg_ratio[2])
    ]
    return recommend_ratio

# Function to calculate the average of previous meals
def calculate_average(meal_history):
    if not meal_history:
        return [0.0, 0.0, 0.0]
    avg = np.mean(meal_history, axis=0)
    return [np.float16(x) for x in avg]

# Function to map recommended ratio to food items based on the highest value (focus on carb, protein, or vegge)
def map_recommendation_to_foods(recommend_ratio, eaten_foods=None):
    # Determine the dominant component (0 = carb, 1 = protein, 2 = vegge)
    dominant_index = np.argmax(recommend_ratio)
    component_name = ["carb", "protein", "vegge"][dominant_index]

    # Sort food items based on the dominant component
    sorted_foods = sorted(food16_dict.items(), key=lambda item: item[1][dominant_index], reverse=True)

    # Exclude foods that have already been eaten
    if eaten_foods:
        sorted_foods = [food for food in sorted_foods if food[0] not in eaten_foods]

    # If less than 3 foods remain after exclusion, include the eaten foods as well
    if len(sorted_foods) < 3:
        remaining_count = 3 - len(sorted_foods)
        eaten_foods_subset = [food for food in food16_dict.items() if food[0] in eaten_foods]
        sorted_foods.extend(eaten_foods_subset[:remaining_count])

    # Get the top 3 foods for that component
    top_3_foods = sorted_foods[:3]
    return component_name, top_3_foods

# Function to log meals
def log_meal_data(day, meal_history, food_classes):
    with open('meal_log.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([f"Day {day}", "Meal", "Food Class", "Carb", "Protein", "Vegge"])
        for meal_num, (meal, food_class) in enumerate(zip(meal_history, food_classes), 1):
            writer.writerow([f"Day {day}", f"Meal {meal_num}", food_class, *meal])

# Function to recommend meals based on classes_eaten
def recommend_meals(classes_eaten):
    # Map classes_eaten to meal_history (list of [carb, protein, vegge])
    meal_history = [food16_dict[class_name] for class_name in classes_eaten if class_name in food16_dict]

    # Calculate average ratio
    avg_ratio = calculate_average(meal_history)

    # Recommend next meal based on avg_ratio
    recommend_ratio = recommend_next_meal(avg_ratio)

    # Map to food items
    component, top_foods = map_recommendation_to_foods(recommend_ratio, eaten_foods=classes_eaten)

    return avg_ratio, component, top_foods
