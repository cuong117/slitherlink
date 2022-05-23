import time
from threading import Event, Thread

import pycosat

n = 0
m = 0
count_box = 0
line_box = dict()
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
    global count_box
    clauses = []
    for i in range(m):
        for j in range(n):
            if puzzle[i][j] > 0:
                count_box += 1
                line = get_line_from_box(i, j)
                for var in line:
                    if var in line_box:
                        line_box[var].append((i, j))
                    else:
                        line_box[var] = [(i, j)]
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
    sol = None
    clause = rule1() + rule2()
    count_loop = 0
    time_out = False
    while True:
        if stop_event.is_set():
            time_out = True
            break
        count_loop += 1
        sol = pycosat.solve(clause)
        if type(sol) is str:
            break
        res = check_cycle(sol)
        if type(res) is bool and res:
            break
        else:
            clause += res

    if not time_out:
        result['result'] = sol
        result['reload'] = count_loop


def check_cycle(solves):
    size = (m + 1) * (n + 1)
    true_element = 0
    visited_line = []
    clauses = []
    visited_node = []
    for val in solves:
        if val > 0:
            true_element += 1
    while True:
        node, line = find_node_start_cycle(solves, visited_node, size)
        if line:
            line_element, box_element, line_list, node_list = find_cycle_element(node, line, solves)
            if true_element == line_element:
                return True
            if count_box > box_element:
                clauses.append([-var for var in line_list])
            visited_line += line_list
            visited_node += node_list
        else:
            return clauses


def find_cycle_element(node, line, solves):
    visited_line = [line]
    visited_node = [node]
    visited_box = set()
    pre_node = node
    current_node = None
    li = line
    i = int(node / (n + 1))
    j = int(node % (n + 1))
    count = 0
    while current_node != node:
        if current_node:
            lines = get_line_from_node(current_node)
            for val in lines:
                if solves[val - 1] > 0 and val not in visited_line:
                    li = val
                    visited_line.append(val)
                    visited_node.append(current_node)
            pre_node = current_node
            i = int(current_node / (n + 1))
            j = int(current_node % (n + 1))

        if (m + 1) * n + j * m + i == li:
            current_node = pre_node - n - 1
        elif i * n + j + 1 == li:
            current_node = pre_node + 1
        elif (m + 1) * n + j * m + i + 1 == li:
            current_node = pre_node + n + 1
        elif i * n + j == li:
            current_node = pre_node - 1
        if li in line_box:
            for var in line_box[li]:
                visited_box.add(var)
        count += 1
    return [count, len(visited_box), visited_line, visited_node]


def find_node_start_cycle(solves, visited_node, size):
    for val in range(size):
        if val not in visited_node:
            lines = get_line_from_node(val)
            for line in lines:
                if solves[line - 1] > 0:
                    return [val, line]
    return [False, False]


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
    while action_thread.is_alive():
        pass
    if not result:
        result['result'] = "Time out"


def solve(matrix):
    global m
    global n
    global puzzle
    global result
    global stop_event
    stop_event = Event()
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
