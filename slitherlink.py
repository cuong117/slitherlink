import time
from threading import Event, Thread

import pycosat

n = 0
m = 0
puzzle = []
clause = []
result = dict()
stop_event = Event()


def get_line_from_box(i, j):
    return [i * n + j + 1, (m + 1) * n + (j + 1) * m + i + 1, (i + 1) * n + j + 1, (m + 1) * n + j * m + i + 1]


def get_line_from_node(k):
    i = int(k / (n + 1))
    j = int(k % (n + 1))
    if i == j == 0:
        return [i * n + j + 1, (m + 1) * n + j * m + i + 1]
    elif i == 0:
        if j == n:
            return [(m + 1) * n + j * m + i + 1, i * n + j]
        else:
            return [i * n + j + 1, (m + 1) * n + j * m + i + 1, i * n + j]
    elif j == 0:
        if i == m:
            return [(m + 1) * n + j * m + i, i * n + j + 1]
        else:
            return [(m + 1) * n + j * m + i, i * n + j + 1, (m + 1) * n + j * m + i + 1]
    elif i == m and j == n:
        return [(m + 1) * n + j * m + i, i * n + j]
    elif i == m:
        return [(m + 1) * n + j * m + i, i * n + j + 1, i * n + j]
    elif j == n:
        return [(m + 1) * n + j * m + i, (m + 1) * n + j * m + i + 1, i * n + j]
    else:
        return [(m + 1) * n + j * m + i, i * n + j + 1, (m + 1) * n + j * m + i + 1, i * n + j]


def rule1():
    clauses = []
    for i in range(m):
        for j in range(n):
            if puzzle[i][j] == 0:
                clauses += rule1_val_0(i, j)
            elif puzzle[i][j] == 1:
                clauses += rule1_val_1(i, j)
            elif puzzle[i][j] == 2:
                clauses += rule1_val_2(i, j)
            elif puzzle[i][j] == 3:
                clauses += rule1_val_3(i, j)
            elif puzzle[i][j] == 4:
                clauses += rule1_val_4(i, j)
    return clauses


def rule2():
    clauses = []
    size = (m + 1) * (n + 1)
    for k in range(size):
        lines = get_line_from_node(k)
        length = len(lines)
        for i in range(length):
            temp = [-lines[i]]
            for j in range(length):
                if j != i:
                    temp.append(lines[j])
            clauses.append(temp)
        if length > 2:
            for i in range(length):
                for j in range(i + 1, length):
                    for z in range(j + 1, length):
                        clauses.append([-lines[i], -lines[j], -lines[z]])
    return clauses


def rule3():
    global result
    global clause
    size = (n + 1) * (m + 1)
    count = 0
    cycle_element = 1
    sol = None
    clause = rule1() + rule2()
    count_loop = 0
    time_out = False
    while count != cycle_element:
        if stop_event.is_set():
            time_out = True
            break
        count_loop += 1
        count = 0
        if sol:
            temp = []
            for val in sol:
                temp.append(-val)
            clause.append(temp)
        sol = pycosat.solve(clause)
        if type(sol) is str:
            break

        for val in sol:
            if val > 0:
                count += 1

        check = False
        for k in range(size):
            lines = get_line_from_node(k)
            for line in lines:
                if sol[line - 1] > 0:
                    cycle_element = find_cycle_element(k, line, sol)
                    check = True
                    break
            if check:
                break
    if not time_out:
        result['result'] = sol
        result['reload'] = count_loop


def find_cycle_element(k, line, sol):
    count = 0
    pre_node = k
    current_node = None
    i = int(k / (n + 1))
    j = int(k % (n + 1))
    visited = [line]
    li = line
    while current_node != k:
        if (m + 1) * n + j * m + i == li:
            current_node = pre_node - n - 1
        elif i * n + j + 1 == li:
            current_node = pre_node + 1
        elif (m + 1) * n + j * m + i + 1 == li:
            current_node = pre_node + n + 1
        elif i * n + j == li:
            current_node = pre_node - 1
        lines = get_line_from_node(current_node)
        for val in lines:
            if sol[val - 1] > 0 and visited.count(val) == 0:
                li = val
                visited.append(val)
        pre_node = current_node
        i = int(current_node / (n + 1))
        j = int(current_node % (n + 1))
        count += 1
    return count


def rule1_val_0(i, j):
    clauses = []
    lines = get_line_from_box(i, j)
    for line in lines:
        clauses.append([-line])
    return clauses


def rule1_val_1(i, j):
    clauses = []
    lines = get_line_from_box(i, j)
    length = len(lines)
    for x in range(length):
        for y in range(x + 1, length):
            clauses.append([-lines[x], -lines[y]])
    clauses.append(lines)
    return clauses


def rule1_val_2(i, j):
    clauses = []
    lines = get_line_from_box(i, j)
    length = len(lines)
    for x in range(length):
        for y in range(x + 1, length):
            for z in range(y + 1, length):
                clauses.append([lines[x], lines[y], lines[z]])
                clauses.append([-lines[x], -lines[y], -lines[z]])
    return clauses


def rule1_val_3(i, j):
    clauses = []
    lines = get_line_from_box(i, j)
    length = len(lines)
    temp = []
    for val in lines:
        temp.append(-val)
    clauses.append(temp)
    for x in range(length):
        for y in range(x + 1, length):
            clauses.append([lines[x], lines[y]])
    return clauses


def rule1_val_4(i, j):
    return get_line_from_box(i, j)


def run():
    global stop_event
    action_thread = Thread(target=rule3)
    action_thread.start()
    action_thread.join(timeout=900)
    stop_event.set()
    stop_event = Event()
    if not result:
        result['result'] = "Time out"


def solve(matrix):
    global m
    global n
    global puzzle
    global result
    result = dict()
    m = len(matrix)
    n = len(matrix[0])
    puzzle = matrix
    start = time.time()
    run()
    end = time.time()
    if type(result['result'] is str):
        result["variables"] = (m+1)*n + n*m + m
    else:
        result['variables'] = len(result['result'])
    result["clauses"] = len(clause)
    result["time"] = (end - start) * 1000
    return result
