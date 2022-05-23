from slitherlink import solve
from slitherlink_optimize import solve as solve_op
from ReadFile import maps5, maps7, maps10, maps15, maps20, maps30

outputFile = 'output/output.txt'
outputFile_new = 'output/output_new'


def read_result(result, outFile):
    sol = result["result"]
    time = result['time']
    variables = result['variables']
    clauses = result['clauses']
    if outFile == outputFile:
        from slitherlink import m, n, puzzle
    else:
        from slitherlink_optimize import m, n, puzzle
    file = open(outFile, 'a')
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
    file.close()


def run_all_test():
    maps = [maps5, maps7, maps10, maps15, maps20, maps30]
    count = 1

    for mapi in maps:
        for m in mapi:
            print(f'test {count} running...', end=" ")
            read_result(solve_op(m), outputFile_new)
            print("ended")
            count += 1


run_all_test()
