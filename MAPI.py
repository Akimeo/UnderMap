import requests
import pygame
import sys
import os
from text_input import PygameTextBox, Button

pygame.init()
screen = pygame.display.set_mode((512, 412))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


def make_map_file(ll, z, l, spn=None):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": ll,
        "l": l,
        "z": z,
        "size": "512,384"
    }
    if spn:
        map_params['spn'] = spn
    try:
        response = requests.get(map_api_server, params=map_params)
    except Exception:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        pygame.quit()
        os.remove("map.png")
        sys.exit(1)
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        pygame.quit()
        os.remove("map.png")
        sys.exit(1)
    try:
        with open("map.png", "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        pygame.quit()
        os.remove("map.png")
        sys.exit(2)


def make_spn(toponym):
    delta_x = str(float(toponym['boundedBy']['Envelope']['upperCorner'].split()[
        0]) - float(toponym['boundedBy']['Envelope']['lowerCorner'].split()[0]))
    delta_y = str(float(toponym['boundedBy']['Envelope']['upperCorner'].split()[
        1]) - float(toponym['boundedBy']['Envelope']['lowerCorner'].split()[1]))
    return [delta_x, delta_y]


def search_place(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {"geocode": toponym_to_find, "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    address_ll = list(map(float, toponym["Point"]["pos"].split(" ")))
    spn = make_spn(toponym)
    return (address_ll, spn)


input_box = PygameTextBox(0, 0, 434, 28)
btn = Button(434, 0, 78, 28)

starting_point = [0, 0]
zoom = 1
map_type = ["map"]

clock = pygame.time.Clock()
FPS = 30
running = True
event_check = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        input_box.update(events)
        if input_box.is_not_active():
            if event.type == pygame.KEYDOWN:
                event_check = True
                if event.key == pygame.K_m:
                    if map_type[0] == "map":
                        map_type[0] = "sat"
                    else:
                        map_type[0] = "map"
                elif event.key == pygame.K_s:
                    if "skl" in map_type:
                        map_type.remove("skl")
                    else:
                        map_type.append("skl")
                elif event.key == pygame.K_t:
                    if "trf" in map_type:
                        map_type.remove("trf")
                    else:
                        map_type.append("trf")
                elif event.key == pygame.K_KP9:
                    if zoom < 17:
                        zoom += 1
                elif event.key == pygame.K_KP3:
                    if zoom > 1:
                        zoom -= 1
                elif event.key == pygame.K_UP:
                    starting_point[1] += 255 / 2 ** zoom
                    if starting_point[1] > 85:
                        starting_point[1] = 85
                elif event.key == pygame.K_DOWN:
                    starting_point[1] -= 255 / 2 ** zoom
                    if starting_point[1] < -85:
                        starting_point[1] = -85
                elif event.key == pygame.K_LEFT:
                    starting_point[0] -= 720 / 2 ** zoom
                    if starting_point[0] < -180:
                        starting_point[0] += 360
                elif event.key == pygame.K_RIGHT:
                    starting_point[0] += 720 / 2 ** zoom
                    if starting_point[0] > 180:
                        starting_point[0] -= 360
    name = input_box.get_name()
    if name:
        place = search_place(name)
        make_map_file(
            "{},{}".format(place[0][0], place[0][1]),
            str(zoom),
            ','.join(map_type),
            ','.join(place[1])
        )
    if event_check:
        make_map_file(
            "{},{}".format(starting_point[0], starting_point[1]),
            str(zoom),
            ','.join(map_type)
        )
    input_box.draw(screen)
    btn.update(events)
    btn.draw(screen)
    screen.blit(pygame.image.load("map.png"), (0, 28))
    pygame.display.flip()
    clock.tick(FPS)
    event_check = False
pygame.quit()
os.remove("map.png")
