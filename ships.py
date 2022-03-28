from random import choice

field_plr1 = [["*" for _ in range(10)] for _ in range(10)]
field_plr2 = [["*" for _ in range(10)] for _ in range(10)]
buffer_field = [["*" for _ in range(10)] for _ in range(10)]
lett = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
ori = {"право": 0, "низ": 1, "0": 0, "1": 1}
plr2_ships = []  # может быть пк
plr1_ships = []  # точно игрок
plr1_can_shoot = []
plr2_can_shoot = []
plr1_name = ""
plr2_name = ""
all_players = 1
x = [i for i in range(10)]
y = [i for i in range(10)]
for x1 in x:
    for y1 in y:
        plr1_can_shoot.append([x1, y1])
        plr2_can_shoot.append([x1, y1])


def clear_buffer():
    global buffer_field
    buffer_field = [["*" for _ in range(10)] for _ in range(10)]


def new_game():
    global field_plr1,\
        field_plr2,\
        plr2_ships,\
        plr1_ships,\
        plr1_can_shoot,\
        plr2_can_shoot,\
        all_players
    field_plr1 = [["*" for _ in range(10)] for _ in range(10)]
    field_plr2 = [["*" for _ in range(10)] for _ in range(10)]
    clear_buffer()
    plr2_ships = []  # может быть пк
    plr1_ships = []  # точно игрок
    plr1_can_shoot = []
    plr2_can_shoot = []
    plr1_name = ""
    plr2_name = ""
    all_players = 1
    for x2 in x:
        for y2 in y:
            plr1_can_shoot.append([x2, y2])
            plr2_can_shoot.append([x2, y2])


def print_field(field):
    print("  ", end="")
    for i in letters:
        print(i, end=" ")
    print()
    print("  - - - - - - - - - -")
    for j in range(10):
        print(j, end="")
        print("|", end="")
        for i in range(10):
            print(field[i][j], end="")
            print(" ", end="")
        print()


def check_ship(ship, ship_list):
    for ship_l in ship_list:
        for part_cords in ship_l:
            for cords_2 in ship:
                if cords_2[0] in [part_cords[0] + 1, part_cords[0], part_cords[0] - 1] and \
                        cords_2[1] in [part_cords[1] + 1, part_cords[1], part_cords[1] - 1]:
                    return False
    return True

# право: 0 вниз: 1 влево: 2 вверх: 3
def create_ships():
    global plr2_ships
    ships = plr2_ships
    lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for length in lengths:
        ship_genned = False
        generator_counter = 0
        while not ship_genned:
            x_ship = choice(x)
            y_ship = choice(y)
            point = choice([0, 1])
            if ((x_ship + length - 1) < 10 and point == 0) or ((y_ship + length - 1) < 10 and point == 1):
                ship = list([x_ship + (point == 0) * i, y_ship + (point == 1) * i] for i in range(length))
                if check_ship(ship, ships):
                    ships.append(ship)
                    ship_genned = True
                else:
                    ship_genned = False
                    generator_counter += 1
            else:
                ship_genned = False
                generator_counter += 1
            if generator_counter == 70:
                generator_counter = 0
                ships = []


def check_pointers(nums, cords, can_shoot):
    if nums:
        pointer = choice(nums)
    else:
        return None
    if pointer == 0:
        cords_point = [cords[0] + 1, cords[1]]
    elif pointer == 1:
        cords_point = [cords[0], cords[1] + 1]
    elif pointer == 2:
        cords_point = [cords[0] - 1, cords[1]]
    else:
        cords_point = [cords[0], cords[1] - 1]
    if cords_point not in can_shoot:
        nums.remove(pointer)
        return check_pointers(nums, cords, can_shoot)
    else:
        return cords_point


def is_ship(cords, ship_list):
    for ship_l in ship_list:
        s_ship = ship_l
        for part_cords in ship_l:
            if cords[0] == part_cords[0] and cords[1] == part_cords[1]:
                return s_ship
    return False


def write_to_field(cords, field, letter, can_shoot=None):
    field[cords[0]][cords[1]] = letter
    if can_shoot is not None and cords in can_shoot:
        can_shoot.remove(cords)
    else:
        pass


def write_ship_to_field(ship, field, can_shoot):
    field_to_write = []
    for cords in ship:
        spec_cord = [[cords[0] - 1, cords[1]],
                     [cords[0] - 1, cords[1] - 1],
                     [cords[0], cords[1] - 1],
                     [cords[0] + 1, cords[1] - 1],
                     [cords[0] + 1, cords[1]],
                     [cords[0] + 1, cords[1] + 1],
                     [cords[0], cords[1] + 1],
                     [cords[0] - 1, cords[1] + 1],
                     [cords[0], cords[1]]]
        for cord in spec_cord:
            if cord not in field_to_write:
                field_to_write.append(cord)
    for cords in field_to_write:
        if cords in ship and cords in can_shoot:
            field[cords[0]][cords[1]] = "@"
        elif cords in can_shoot:
            field[cords[0]][cords[1]] = "#"
        else:
            continue
        if cords in can_shoot:
            can_shoot.remove(cords)


def fire(shooting_at, shooted_into, shoot_cords, ships_list):
    global field_plr1
    field = field_plr1
    print("Стреляю по:", letters[shoot_cords[0]] + str(shoot_cords[1]))
    fire_state = is_ship(shoot_cords, ships_list)
    if fire_state:
        print("Нашёл часть корабля")
        write_to_field(shoot_cords, field, "@", plr2_can_shoot)
        if shooting_at:
            pass
        else:
            shooting_at = fire_state
        shooted_into.append(shoot_cords)
        shooted_into.sort()
        if shooting_at == shooted_into:
            ships_list.remove(shooting_at)
            write_ship_to_field(shooting_at, field, plr2_can_shoot)
            print("Твой корабль был успешно уничтожен")
            shooting_at = []
            shooted_into = []
            return False, shooting_at, shooted_into
        else:
            return False, shooting_at, shooted_into
    else:
        print("Оу, я промазал")
        write_to_field(shoot_cords, field, "#", plr2_can_shoot)
        return True, shooting_at, shooted_into


def pc_turn(shooting_at=None, shooted_into=None):
    if not shooted_into:
        shooted_into = []
    if not shooting_at:
        shooting_at = []
    global plr1_ships
    ships = plr1_ships
    missed = False
    while not missed:
        if shooting_at:
            if len(shooted_into) == 1:
                choice_array = [0, 1, 2, 3]
                shoot_cords = check_pointers(choice_array, shooted_into[0], plr2_can_shoot)
                missed, shooting_at, shooted_into = fire(shooting_at, shooted_into, shoot_cords, ships)
            else:
                if shooted_into[0][0] == shooted_into[1][0] - 1:
                    choice_array = [check_pointers([2], shooted_into[0], plr2_can_shoot),
                                    check_pointers([0], shooted_into[-1], plr2_can_shoot)]
                else:
                    choice_array = [check_pointers([3], shooted_into[0], plr2_can_shoot),
                                    check_pointers([1], shooted_into[-1], plr2_can_shoot)]
                if None in choice_array:
                    choice_array.remove(None)
                shoot_cords = choice(choice_array)
                missed, shooting_at, shooted_into = fire(shooting_at, shooted_into, shoot_cords, ships)
        else:
            shoot_cords = choice(plr2_can_shoot)
            missed, shooting_at, shooted_into = fire(shooting_at, shooted_into, shoot_cords, ships)
        if not ships:
            break
    return shooting_at, shooted_into


def get_form_pl(player_num):
    global plr1_ships,\
        plr2_ships,\
        field_plr1,\
        field_plr2
    if player_num == 1:
        return plr1_ships, field_plr1
    else:
        return plr2_ships, field_plr2


def plr_set_ship(length, orientation, cords, player_num):
    if ((lett[cords[0]] + length - 1) < 10 and ori[orientation] == 0) or (
            (int(cords[1]) + length - 1) < 10 and ori[orientation] == 1):
        ship = list([lett[cords[0]] + (ori[orientation] == 0) * i, int(cords[1]) + (ori[orientation] == 1) * i] for i in range(length))
        ships, field = get_form_pl(player_num)
        if check_ship(ship, ships):
            ships.append(ship)
        else:
            return False, None
        if all_players == 1:
            for cords in ship:
                write_to_field(cords, field, "X")
            return True, field
        else:
            for cords in ship:
                write_to_field(cords, buffer_field, "X")
            return True, buffer_field
    else:
        return False, None


def plr_delete_ship(cords, pl_num):
    ships, field = get_form_pl(pl_num)
    if all_players == 1:
        pass
    else:
        field = buffer_field
    ship_to_delete = is_ship(cords, ships)
    if ship_to_delete:
        ships.remove(ship_to_delete)
        for cords in ship_to_delete:
            write_to_field(cords, field, "*")
        return True, len(ship_to_delete), field
    else:
        return False, None, field


def plr_set_ships(pl_num):
    ships_to_place = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    while ships_to_place:
        print("Доступные длины кораблей:", ships_to_place)
        command = input("\"добавить\" или \"удалить\" корабль?(1/0): ")
        if command == "добавить" or command == "1":
            try:
                counter = 0
                for leng in ships_to_place:
                    if ships_to_place[0] == leng:
                        counter += 1
                if counter == len(ships_to_place):
                    length = ships_to_place[0]
                else:
                    length = int(input("Введите длину корабля, который хотите поставить: "))
                    if length not in ships_to_place:
                        print("Нет корабля с заданной длинной!")
                        continue
                if length != 1:
                    orientation = input("Введите ориентацию корабля(право, низ)/(0, 1): ")
                else:
                    orientation = "право"
                if orientation not in ori:
                    print("Введена неправильная ориентация!")
                    continue
                cords = input("Введите координаты корабля: ")
                if cords == "" or cords[0] not in lett or cords[1] not in list(map(str, y)):
                    print("Введены неправильные координаты")
                    continue
                cords = [cords[0], int(cords[1])]

                place_state, field = plr_set_ship(length, orientation, cords, pl_num)
                if place_state:
                    ships_to_place.remove(length)
                    print("Вы успешно поставили корабль")
                    print_field(field)
                else:
                    print("Постановка корабля не удалась, попробуйте ещё раз")
                    continue
            except:
                print("Ошибка ввода, попробуйте ещё раз")
                continue
        elif command == "удалить" or command == "0":
            if len(get_form_pl(pl_num)[0]) == 0:
                print("Нечего удалять")
                continue
            cords = input("Введите координаты корабля: ")
            if cords == "" or cords[0] not in lett or cords[1] not in list(map(str, y)):
                print("Введены неправильные координаты")
                continue
            cords = [lett[cords[0]], int(cords[1])]
            delete_state, deleted_len, field = plr_delete_ship(cords, pl_num)
            if delete_state:
                ships_to_place.append(deleted_len)
                ships_to_place.sort(reverse=True)
                print("Корабль успешно удалён")
                print_field(field)
            else:
                print("Корабль не найден")
        else:
            print("Неизвестная команда")
    clear_buffer()


def plr_fire(player, shooted_at=None):
    if shooted_at is None:
        shooted_at = []
    missed = False
    if all_players == 1:
        is_pc = True
    else:
        is_pc = False
    if player == 1:
        ships_list = plr2_ships
        can_shoot = plr1_can_shoot
        field = field_plr2
    else:
        ships_list = plr1_ships
        can_shoot = plr2_can_shoot
        field = field_plr1
    while not missed:
        cords = input("Введите координаты для стрельбы: ")
        if cords == "" or cords[0] not in lett or cords[1] not in list(map(str, y)):
            print("Введены неправильные координаты")
            continue
        cords = [lett[cords[0]], int(cords[1])]
        if cords not in can_shoot:
            print("Координата уже занята")
            continue
        else:
            fire_state = is_ship(cords, ships_list)
            if fire_state:
                shooted_at_ship = None
                for ship in shooted_at:
                    fl = 0
                    for cords1 in ship:
                        if cords1 in fire_state:
                            ship.append(cords)
                            ship.sort()
                            shooted_at_ship = ship
                            fl = 1
                            break
                    if fl == 1:
                        break
                if not shooted_at_ship:
                    shooted_at.append([cords])
                    shooted_at_ship = [cords]
                print("Попадание")
                if shooted_at_ship == fire_state:
                    ships_list.remove(shooted_at_ship)
                    write_ship_to_field(shooted_at_ship, field, can_shoot)
                    print("Корабль уничтожен")
                    shooted_at.remove(shooted_at_ship)
                else:
                    write_to_field(cords, field, "@")
                if not ships_list:
                    break
                print_fields(is_pc)
            else:
                print("Промах")
                write_to_field(cords, field, "#", can_shoot)
                return shooted_at


def print_fields(is_bot):
    if is_bot:
        str1 = "Ваше поле:"
        str2 = "Поле компьютера:"
    else:
        str1 = f"Поле игрока {plr1_name}:"
        str2 = f"Поле игрока {plr2_name}:"
    print("-----------------------------")
    print(str1)
    print_field(field_plr1)
    print("-----------------------------")
    print(str2)
    print_field(field_plr2)
    print("-----------------------------")


def main_loop():
    global all_players,\
        plr1_name,\
        plr2_name
    flag = True
    while flag:
        try:
            all_players = int(input("Введите количество игроков(1-2): "))
            if 1 > all_players > 2:
                print("Некорректный ввод!")
                continue
        except ValueError:
            print("Некорректный ввод!")
            continue
        if all_players == 1:
            print("Новая игра с компьютером")
            print("Фаза создания кораблей")
            print_field(field_plr1)
            plr_set_ships(1)
            print("Игрок успешно поставил все корабли")
            print("Компьютер расставляет свои корабли")
            create_ships()
            print("Компьютер расставил корабли")
            print("Фаза игры")
            print_fields(True)
            print("Ваш ход")
            mem_pl = plr_fire(1)
            print_fields(True)
            print("Ход компьютера")
            mem_pc = pc_turn()
            while True:
                print_fields(True)
                print("Ваш ход")
                mem_pl = plr_fire(1, mem_pl)
                if not plr2_ships:
                    print_fields(True)
                    print("Вы победили!")
                    break
                print_fields(True)
                print("Ход компьютера")
                mem_pc = pc_turn(mem_pc[0], mem_pc[1])
                if not plr1_ships:
                    print_fields(True)
                    print("Компьютер победил!")
                    break
        else:
            print("Новая игра с другим игроком")
            plr1_name = input("Введите имя первого игрока: ")
            if plr1_name == "":
                plr1_name == "1"
            plr2_name = input("Введите имя второго игрока: ")
            if plr1_name == "":
                plr1_name == "2"
            print("Фаза создания кораблей")
            print(f"Очередь игрока {plr1_name}")
            input("Нажмите Enter если готовы")
            print_field(field_plr1)
            plr_set_ships(1)
            print(f"Игрок {plr1_name} успешно поставил все корабли")
            print("\n" * 50)
            print(f"Очередь игрока {plr2_name}")
            input("Нажмите Enter если готовы")
            print_field(field_plr2)
            plr_set_ships(2)
            print(f"Игрок {plr2_name} успешно поставил все корабли")
            print("\n" * 50)
            print("Фаза игры")
            print_fields(False)
            print(f"Ход игрока {plr1_name}")
            mem_pl1 = plr_fire(1)
            print_fields(False)
            print(f"Ход игрока {plr2_name}")
            mem_pl2 = plr_fire(2)
            while True:
                print_fields(False)
                print(f"Ход игрока {plr1_name}")
                mem_pl1 = plr_fire(1, mem_pl1)
                if not plr2_ships:
                    print_fields(False)
                    print(f"Игрок {plr1_name} победили!")
                    break
                print_fields(False)
                print(f"Ход игрока {plr2_name}")
                mem_pl2 = plr_fire(2, mem_pl2)
                if not plr1_ships:
                    print_fields(False)
                    print(f"Игрок {plr2_name} победил!")
                    break
        wp = input("Сыграть ещё раз?[Y/N]")
        if wp == "Y":
            new_game()
        else:
            flag = False


main_loop()