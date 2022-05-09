from slitherlink import solve
from ReadFile import maps5, maps7, maps10, maps15, maps20, maps30

outputFile = 'output/output.txt'


def read_result(result, file):
    sol = result["result"]
    time = result['time']
    variables = result['variables']
    clauses = result['clauses']
    from slitherlink import m, n, puzzle
    file.write(f'{m} x {n}\n')
    if type(sol) is str:
        file.write(f'Result: {sol}\nTime: %.3f ms\nVariables: {variables}\n' % time)
        file.write(f'Clauses: {clauses}\n\n')
        return
    reload = result['reload']
    file.write("Result:\n")
    for i in range(m + 1):
        for j in range(n + 1):
            if j == m:
                file.write("*")
            else:
                line = i * n + j + 1
                if sol[line - 1] > 0:
                    file.write("*---")
                else:
                    file.write("*   ")
        file.write("\n")
        if i < m:
            for j in range(m + 1):
                line = (m + 1) * n + j * m + i + 1
                if sol[line - 1] > 0:
                    file.write("|")
                else:
                    file.write(" ")
                if j <= n - 1 and i <= m - 1:
                    if puzzle[i][j] > -1:
                        file.write(f' {puzzle[i][j]} ')
                    else:
                        file.write('   ')
            file.write("\n")
    file.write(f'Time: %.3f ms\nVariables: {variables}\n' % time)
    file.write(f'Clauses: {clauses}\nReload: {reload}\n\n')


def run_all_test():
    # maps = [maps5, maps7, maps10, maps15, maps20, maps30]
    maps = [maps5, maps7, maps10]
    file = open(outputFile, 'w')
    for mapi in maps:
        for m in mapi:
            read_result(solve(m), file)
    file.close()


run_all_test()
