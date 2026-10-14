def solve_party():
    # Надежное считывание n и m
    line = input().split()
    while len(line) < 2:
        line += input().split()
    n, m = map(int, line)

    total_cells = n * m
    field = []

    # Считываем строки, убираем пробелы внутри строки
    for _ in range(n):
        row = input().replace(" ", "").strip()
        # Если строка пустая (например, из-за лишнего переноса), пропускаем
        while len(row) == 0:
            row = input().replace(" ", "").strip()
        field.extend(list(row))

    # Проверка на соответствие размера
    if len(field) != total_cells:
        # Если размер не совпадает, значит, данные некорректны
        # Но по условию задачи такого быть не должно
        pass

    visit_time = [-1] * total_cells
    queue = []
    read_ptr = 0
    students_left = 0

    for i in range(total_cells):
        char = field[i]
        if char == 'D':
            visit_time[i] = 0
            queue.append(i)
        elif char == 'S':
            students_left += 1

    if students_left == 0:
        print(0)
        return

    if not queue:
        print(-1)
        return

    answer_time = 0
    offsets = [-m, m, -1, 1]

    while read_ptr < len(queue):
        curr = queue[read_ptr]
        read_ptr += 1
        curr_time = visit_time[curr]

        if field[curr] == 'S':
            students_left -= 1
            if curr_time > answer_time:
                answer_time = curr_time

        for step in offsets:
            nxt = curr + step

            # Проверка на выход за границы строки
            if step == -1 and curr % m == 0:
                continue
            if step == 1 and curr % m == m - 1:
                continue

            if 0 <= nxt < total_cells:
                if field[nxt] != '*' and visit_time[nxt] == -1:
                    visit_time[nxt] = curr_time + 1
                    queue.append(nxt)

    if students_left == 0:
        print(answer_time)
    else:
        print(-1)


if __name__ == "__main__":
    solve_party()