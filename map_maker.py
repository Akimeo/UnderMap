import sys
import requests
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from god_squad import jesus_christ


def make_map_file(pos):
    global starting_point, zoom, map_type, points, image
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    central_point = jesus_christ(
        list(map(float, starting_point.split(','))),
        (512 * (pos[1] - 1), 384 * (pos[0] - 1)), int(zoom))
    map_params = {
        "ll": "{},{}".format(central_point[0], central_point[1]),
        "l": map_type,
        "z": zoom,
        "size": "512,384"
    }
    if points:
        map_params['pt'] = points
    try:
        response = requests.get(map_api_server, params=map_params)
    except Exception:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    try:
        img = Image.open(BytesIO(response.content))
        image.paste(img, (512 * pos[1], 384 * pos[0]))
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)


def main():
    global starting_point, zoom, map_type, points, image
    try:
        starting_point, zoom, map_type, points = sys.argv[1:]
    except Exception as e:
        print(e, sys.argv)
    if points == 'None':
        points = None
    image = Image.new('RGB', (1536, 1152), (192, 192, 192))
    pos_list = [[0, 0], [0, 1], [0, 2], [1, 0],
                [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    with ThreadPoolExecutor(9) as executor:
        for _ in executor.map(make_map_file, pos_list):
            pass
    image.save("full_map.png")


if __name__ == '__main__':
    main()
