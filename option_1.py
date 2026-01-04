import cv2
import numpy as np

def count_colored_dots(image_path):

    # 1. Загрузка изображения
    img = cv2.imread(image_path)
    if img is None:
        print(f"Ошибка: Не удалось загрузить изображение по пути: {image_path}")
        return None

    # 2. Преобразование изображения в цветовое пространство HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 3. Определение диапазонов цветов в HSV 
    # Нижние границы (lower) и верхние границы (upper) для каждого цвета
    # Формат: [H, S, V]
    color_ranges = {
        'green': ([35, 50, 50], [85, 255, 255]),
        'red': ([0, 50, 50], [10, 255, 255]),  # Первая часть красного
        'red_2': ([160, 50, 50], [179, 255, 255]), # Вторая часть красного
        'pink': ([140, 50, 50], [160, 255, 255]),
        'blue': ([100, 50, 50], [130, 255, 255]),
    }

    dot_counts = {
        'green': 0,
        'red': 0,
        'pink': 0,
        'blue': 0,
    }

    # 4. Сегментация каждого цвета и подсчет точек
    for color_name, (lower_bound, upper_bound) in color_ranges.items():
        lower_bound = np.array(lower_bound)
        upper_bound = np.array(upper_bound)

        # Создание маски для текущего цвета
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Для красного цвета объединяем две маски
        if color_name == 'red_2':
            continue # Обработаем красный в следующем шаге

        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        
        for cnt in contours:
            # Если площадь контура достаточно велика (например, больше 5 пикселей), считаем его точкой
            area = cv2.contourArea(cnt)
            if area > 5: # Порог площади, можно настроить
                if color_name == 'red':
                    dot_counts['red'] += 1
                else:
                    dot_counts[color_name] += 1

    # Обработка второго диапазона красного
    lower_bound_red_2 = np.array(color_ranges['red_2'][0])
    upper_bound_red_2 = np.array(color_ranges['red_2'][1])
    mask_red_2 = cv2.inRange(hsv, lower_bound_red_2, upper_bound_red_2)
    contours_red_2, _ = cv2.findContours(mask_red_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_red_2:
        area = cv2.contourArea(cnt)
        if area > 10: # Порог площади
            dot_counts['red'] += 1


    return dot_counts

if __name__ == "__main__":
    
    image_file_path = 'circles.png'

    counts = count_colored_dots(image_file_path)

    if counts:
        print("Количество точек по цветам:")
        for color, count in counts.items():
            print(f"{color.capitalize()}: {count}")