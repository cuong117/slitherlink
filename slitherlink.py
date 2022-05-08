import pycosat

n = 5
m = 5
puzzle1 = [[-1, -1, 0, 2, -1],
           [2, 2, 2, -1, -1],
           [-1, -1, -1, 2, -1],
           [2, 1, -1, 0, 3],
           [-1, 2, 3, 3, -1]]

puzzle = [[-1, -1, -1, 3, -1],
          [2, 2, 0, -1, 2],
          [2, -1, 2, -1, 2],
          [-1, -1, 0, -1, -1],
          [-1, 3, 3, 3, -1]]


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
    clause = []
    size = (m + 1) * (n + 1)
    for k in range(size):
        lines = get_line_from_node(k)
        length = len(lines)
        for i in range(length):
            temp = [-lines[i]]
            for j in range(length):
                if j != i:
                    temp.append(lines[j])
            clause.append(temp)
        if length > 2:
            for i in range(length):
                for j in range(i + 1, length):
                    for z in range(j + 1, length):
                        clause.append([-lines[i], -lines[j], -lines[z]])
    return clause


def run_rule3():
    size = (n + 1) * (m + 1)
    count = 0
    cycle_element = 1
    sol = None
    clauses = rule1() + rule2()
    while count != cycle_element:
        count = 0
        if sol:
            temp = []
            for val in sol:
                temp.append(-val)
            clauses.append(temp)
        sol = pycosat.solve(clauses)
        # print(sol)
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

    if type(sol) is str:
        return False
    else:
        return sol


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


def rule2_test(k):
    clause = []
    lines = get_line_from_node(k)
    length = len(lines)
    for i in range(length):
        temp = [-lines[i]]
        for j in range(length):
            if j != i:
                temp.append(lines[j])
        clause.append(temp)
    if length > 2:
        for i in range(length):
            for j in range(i + 1, length):
                for z in range(j + 1, length):
                    clause.append([-lines[i], -lines[j], -lines[z]])
    return clause


def read_result(sol):
    if not sol:
        print("Không có lời giải")
        return
    for i in range(m + 1):
        for j in range(n + 1):
            if j == m:
                print("*", end='')
            else:
                line = i * n + j + 1
                if sol[line - 1] > 0:
                    print("*---", end="")
                else:
                    print("*   ", end="")
        print()
        if i < m:
            for j in range(m + 1):
                line = (m + 1) * n + j * m + i + 1
                if sol[line - 1] > 0:
                    print("|", end="")
                else:
                    print(" ", end="")
                if j <= n - 1 and i <= m - 1:
                    if puzzle[i][j] > -1:
                        print(" ", puzzle[i][j], " ", sep="", end="")
                    else:
                        print('   ', end="")
            print()


read_result(run_rule3())
# print(run_rule3())
# s = pycosat.itersolve(rule1() + rule2())
# for si in s:
#     read_result(si)
#     print('\n')
