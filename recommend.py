# import numpy as np
# import csv

# food16_dict = {
#     # food_class : [carb, protein, vegge]
#     "basil": [0.45, 0.45, 0.1],
#     "curry": [0.5, 0.3, 0.2],
#     "fried_rice": [0.6, 0.3, 0.1],
#     "grilled_pork": [0.2, 0.8, 0],
#     "hy_fried_chicken": [0.2, 0.8, 0],
#     "mama": [0.9, 0.05, 0.05],
#     "noodles": [0.5, 0.35, 0.15],
#     "omelet": [0.5, 0.45, 0.05],
#     "papaya_salad": [0, 0.1, 0.9],
#     "pizza": [0.8, 0.15, 0.05],
#     "porridge": [0.7, 0.25, 0.05],
#     "red_crispy_pork": [0.5, 0.4, 0.1],
#     "sandwich": [0.8, 0.1, 0.1],
#     "sashimi": [0, 1, 0],
#     "steak": [0.2, 0.6, 0.2],
#     "stir_fried_veg": [0, 0.2, 0.8]
# }

# food_class_names = list(food16_dict.keys())

# ## Target ratio (normalized to 1:1:2)
# target_ratio = [1/3, 1/3, 1/3]

# # Function to recommend the next meal's ingredients based on the current average meal ratio
# def recommend_next_meal(current_avg_ratio):
#     recommend_ratio = [
#         np.float16(2 * target_ratio[0] - current_avg_ratio[0]),
#         np.float16(2 * target_ratio[1] - current_avg_ratio[1]),
#         np.float16(2 * target_ratio[2] - current_avg_ratio[2])
#     ]
#     return recommend_ratio

# # Function to calculate the average of previous meals
# def calculate_average(meal_history):
#     return [np.float16(x) for x in list(np.mean(meal_history, axis=0))]

# # Function to get a food class by index
# def get_food_class(index):
#     return food16_dict[food_class_names[index]]

# # Function to map recommended ratio to food items based on the highest value (focus on carb, protein, or vegge)
# def map_recommendation_to_foods(recommend_ratio, eaten_foods=None):
#     dominant_index = np.argmax(recommend_ratio)
#     component_name = ["carb", "protein", "vegge"][dominant_index]

#     sorted_foods = sorted(food16_dict.items(), key=lambda item: item[1][dominant_index], reverse=True)

#     if eaten_foods:
#         sorted_foods = [food for food in sorted_foods if food[0] not in eaten_foods]

#     if len(sorted_foods) < 3:
#         remaining_count = 3 - len(sorted_foods)
#         eaten_foods_subset = [food for food in food16_dict.items() if food[0] in eaten_foods]
#         sorted_foods.extend(eaten_foods_subset[:remaining_count])

#     top_3_foods = sorted_foods[:3]
#     return component_name, top_3_foods

# # Function to log meals, including food_class_index
# def log_meal_data(day, meal_history, food_classes, food_class_indices):
#     print("log")
#     with open('src/spark/assets/data/meal_log.csv', 'a', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         # Write the header only once at the start of the first day
#         if day == 1:
#             print("day 1")
#             writer.writerow(["Day", "Meal", "Food Class", "Food Class Number", "Carb", "Protein", "Vegge"])

#         # Write the meal data for each day
#         for meal_num, (meal, food_class, food_class_index) in enumerate(zip(meal_history, food_classes, food_class_indices), 1):
#             writer.writerow([day, meal_num, food_class, food_class_index, *meal])
#             print("day 2+")
# # Main loop for recommending meals
# def recommend_meals():
#     meal_history = []  # to store all meals for the day
#     food_classes_eaten = []  # to store the food classes eaten
#     food_class_indices = []  # to store the food class indices
    
#     # Loop for 3 meals in a day
#     for meal_num in range(1, 4):
#         if meal_num == 1:
#             # First meal
#             food_class_index = int(input("Enter 1st meal food class (0-15): "))
#             first_meal_ratio = get_food_class(food_class_index)
#             meal_history.append(first_meal_ratio)
#             food_classes_eaten.append(food_class_names[food_class_index])
#             food_class_indices.append(food_class_index)
#             print(f"Meal 1 is {food_class_names[food_class_index]}\nIngredients ratio: {first_meal_ratio}")
            
#             # Recommend second meal based on the first meal
#             recommended_second_meal = recommend_next_meal(first_meal_ratio)
#             component, top_foods = map_recommendation_to_foods(recommended_second_meal, food_classes_eaten)
#             print(f"Recommended ratio for 2nd meal: {recommended_second_meal}")
#             print(f"Focusing on {component}, top 3 recommended foods: {top_foods}\n")
        
#         elif meal_num == 2:
#             # Second meal
#             food_class_index = int(input("Enter 2nd meal food class (0-15): "))
#             second_meal_ratio = get_food_class(food_class_index)
#             meal_history.append(second_meal_ratio)
#             food_classes_eaten.append(food_class_names[food_class_index])
#             food_class_indices.append(food_class_index)
#             avg_meal_1_2 = calculate_average(meal_history)
#             print(f"Meal 2 is {food_class_names[food_class_index]}\nIngredients ratio: {second_meal_ratio}")
#             print(f"Average ratio of 2 meals: {avg_meal_1_2}")
            
#             # Recommend third meal based on the average of the first two meals
#             recommended_third_meal = recommend_next_meal(avg_meal_1_2)
#             component, top_foods = map_recommendation_to_foods(recommended_third_meal, food_classes_eaten)
#             print(f"Recommended ratio for 3rd meal: {recommended_third_meal}")
#             print(f"Focusing on {component}, top 3 recommended foods: {top_foods}\n")
        
#         elif meal_num == 3:
#             # Third meal
#             # food_class_index = int(input("Enter 3rd meal food class (0-15): "))
#             food_class_index = ...
#             third_meal_ratio = get_food_class(food_class_index)
#             meal_history.append(third_meal_ratio)
#             food_classes_eaten.append(food_class_names[food_class_index])
#             food_class_indices.append(food_class_index)
#             avg_meal_1_2_3 = calculate_average(meal_history)
#             print(f"Meal 3 is {food_class_names[food_class_index]}\nIngredients ratio: {third_meal_ratio}")
#             print(f"Average ratio of 3 meals: {avg_meal_1_2_3}\n")
    
#     # End of the day: summarize the average ratio and food classes
#     day_average = calculate_average(meal_history)
#     print(f"Final average ratio of all 3 meals: {day_average}")
#     print(f"Meals eaten today: {food_classes_eaten}")
    
#     return meal_history, food_classes_eaten, food_class_indices

# # Function to simulate for 30 days and log the data
# def simulate_monthly_meals():
#     for day in range(1, 31):
#         print(f"\nDay {day}:\n")
#         meal_history, food_classes, food_class_indices = recommend_meals()
#         log_meal_data(day, meal_history, food_classes, food_class_indices)

# # Run the meal recommendation system for 30 days and log meals
# if __name__ == "__main__":
#     simulate_monthly_meals()

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

## Target ratio (normalized to 1:1:2)
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
    return [np.float16(x) for x in list(np.mean(meal_history, axis=0))]

# Function to get a food class by index
def get_food_class(index):
    return food16_dict[food_class_names[index]]

# Function to map recommended ratio to food items based on the highest value (focus on carb, protein, or vegge)
def map_recommendation_to_foods(recommend_ratio, eaten_foods=None):
    dominant_index = np.argmax(recommend_ratio)
    component_name = ["carb", "protein", "vegge"][dominant_index]

    sorted_foods = sorted(food16_dict.items(), key=lambda item: item[1][dominant_index], reverse=True)

    if eaten_foods:
        sorted_foods = [food for food in sorted_foods if food[0] not in eaten_foods]

    if len(sorted_foods) < 3:
        remaining_count = 3 - len(sorted_foods)
        eaten_foods_subset = [food for food in food16_dict.items() if food[0] in eaten_foods]
        sorted_foods.extend(eaten_foods_subset[:remaining_count])

    top_3_foods = sorted_foods[:3]
    return component_name, top_3_foods

# Function to log meals, including food_class_index
def log_meal_data(day, meal_history, food_classes, food_class_indices):
    with open('meal_log.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header only once at the start of the first day
        if day == 1:
            writer.writerow(["Day", "Meal", "Food Class", "Food Class Number", "Carb", "Protein", "Vegge"])

        # Write the meal data for each day
        for meal_num, (meal, food_class, food_class_index) in enumerate(zip(meal_history, food_classes, food_class_indices), 1):
            writer.writerow([day, meal_num, food_class, food_class_index, *meal])

# Main loop for recommending meals
def recommend_meals():
    meal_history = []  # to store all meals for the day
    food_classes_eaten = []  # to store the food classes eaten
    food_class_indices = []  # to store the food class indices

    # Loop for 3 meals in a day
    for meal_num in range(1, 4):
        if meal_num == 1:
            # First meal
            food_class_index = int(input("Enter 1st meal food class (0-15): "))
            first_meal_ratio = get_food_class(food_class_index)
            meal_history.append(first_meal_ratio)
            food_classes_eaten.append(food_class_names[food_class_index])
            food_class_indices.append(food_class_index)
            print(f"Meal 1 is {food_class_names[food_class_index]}\nIngredients ratio: {first_meal_ratio}")

            # Recommend second meal based on the first meal
            recommended_second_meal = recommend_next_meal(first_meal_ratio)
            component, top_foods = map_recommendation_to_foods(recommended_second_meal, food_classes_eaten)
            print(f"Recommended ratio for 2nd meal: {recommended_second_meal}")
            print(f"Focusing on {component}, top 3 recommended foods: {top_foods}\n")

        elif meal_num == 2:
            # Second meal
            food_class_index = int(input("Enter 2nd meal food class (0-15): "))
            second_meal_ratio = get_food_class(food_class_index)
            meal_history.append(second_meal_ratio)
            food_classes_eaten.append(food_class_names[food_class_index])
            food_class_indices.append(food_class_index)
            avg_meal_1_2 = calculate_average(meal_history)
            print(f"Meal 2 is {food_class_names[food_class_index]}\nIngredients ratio: {second_meal_ratio}")
            print(f"Average ratio of 2 meals: {avg_meal_1_2}")

            # Recommend third meal based on the average of the first two meals
            recommended_third_meal = recommend_next_meal(avg_meal_1_2)
            component, top_foods = map_recommendation_to_foods(recommended_third_meal, food_classes_eaten)
            print(f"Recommended ratio for 3rd meal: {recommended_third_meal}")
            print(f"Focusing on {component}, top 3 recommended foods: {top_foods}\n")

        elif meal_num == 3:
            # Third meal
            food_class_index = int(input("Enter 3rd meal food class (0-15): "))
            # food_class_index = int(input("Enter 3rd meal food class (0-15): "))
            food_class_index = ...
            third_meal_ratio = get_food_class(food_class_index)
            meal_history.append(third_meal_ratio)
            food_classes_eaten.append(food_class_names[food_class_index])
            food_class_indices.append(food_class_index)
            avg_meal_1_2_3 = calculate_average(meal_history)
            print(f"Meal 3 is {food_class_names[food_class_index]}\nIngredients ratio: {third_meal_ratio}")
            print(f"Average ratio of 3 meals: {avg_meal_1_2_3}\n")

    # End of the day: summarize the average ratio and food classes
    day_average = calculate_average(meal_history)
    print(f"Final average ratio of all 3 meals: {day_average}")
    print(f"Meals eaten today: {food_classes_eaten}")

    return meal_history, food_classes_eaten, food_class_indices

# Function to simulate for 30 days and log the data
def simulate_monthly_meals():
    for day in range(1, 31):
        print(f"\nDay {day}:\n")
        meal_history, food_classes, food_class_indices = recommend_meals()
        log_meal_data(day, meal_history, food_classes, food_class_indices)

# Run the meal recommendation system for 30 days and log meals
if __name__ == "__main__":
    simulate_monthly_meals()