from PIL import Image

def count_colored_dots_v1(image_path):
   
    try:
        img = Image.open(image_path).convert("RGB") 
    except FileNotFoundError:
        return {"error": f"Файл изображения не найден по пути: {image_path}"}
    except Exception as e:
        return {"error": f"Ошибка при открытии или обработке изображения: {e}"}

    width, height = img.size
    pixel_data = img.load()

    # Определяем примерные RGB-диапазоны для каждого цвета.
    color_ranges = {
        "green": ((0, 100, 0), (100, 255, 100)),  # Примерный диапазон зеленого
        "red": ((100, 0, 0), (255, 100, 100)),    # Примерный диапазон красного
        "pink": ((200, 50, 50), (255, 150, 150)), # Примерный диапазон розового
        "blue": ((0, 0, 100), (100, 100, 255)),   # Примерный диапазон синего
    }

    # Белый фон
    white_threshold = 230

    counts = {color: 0 for color in color_ranges}
    dots_counted = 0 # Общее количество найденных точек

    for x in range(width):
        for y in range(height):
            r, g, b = pixel_data[x, y]

            # Игнорируем пиксели, которые слишком близки к белому фону
            if r > white_threshold and g > white_threshold and b > white_threshold:
                continue

            is_counted = False
            for color_name, (lower, upper) in color_ranges.items():
                r_min, g_min, b_min = lower
                r_max, g_max, b_max = upper

                if (r_min <= r <= r_max and
                    g_min <= g <= g_max and
                    b_min <= b <= b_max):
                    counts[color_name] += 1
                    dots_counted += 1
                    is_counted = True
                    break 
       

    print(f"--- Результаты Варианта 2 (Подсчет пикселей каждого цвета) ---")
    print(f"Общее количество пикселей, отнесенных к цветным точкам: {dots_counted}")
    for color, count in counts.items():
        print(f"{color.capitalize()}: {count}")
    return counts

image_file_path = 'circles.png'
result_v1 = count_colored_dots_v1(image_file_path)
print(result_v1)