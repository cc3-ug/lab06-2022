from subprocess import run
from subprocess import PIPE
from xml.dom import minidom
from tabulate import tabulate


# executes a shell command
def execute(cmd=[], shell=False, timeout=10):
    return run(cmd, shell=shell, stdout=PIPE, stderr=PIPE, timeout=timeout)


# reads a file
def read(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    return text.strip()


# creates a pretty result report
def create_report(table):
    return tabulate(table, headers=['Exercise', 'Grade', 'Message'])


# checks splitters.circ
def check_ex1():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/ex1.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip()
    expected = read('tests/expected/ex1')
    if output == expected:
        return (100 / 3, 'passed', '')
    else:
        return (0, 'failed', '')


# checks rotr.circ
def check_ex2():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/ex2.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())

    # check used components
    tree = minidom.parse('rotr.circ')
    invalid_components = ['shifter']
    for circuit in tree.getElementsByTagName('circuit'):
        for component in circuit.getElementsByTagName('comp'):
            name = component.getAttribute('name').lower()
            lib = component.getAttribute('lib')
            if name in invalid_components and lib != '':
                return (0, 'do not use logisim shifters', '')

    output = task.stdout.decode().strip()
    expected = read('tests/expected/ex2')
    if output == expected:
        return (100 / 3, 'passed', '')
    else:
        return (0, 'failed', '')


# checks ALU.circ
def check_ex3():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/ex3.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip()
    expected = read('tests/expected/ex3')
    if output == expected:
        return (100 / 3, 'passed', '')
    else:
        return (0, 'failed', '')


# checks lab 5
def lab6_logisim():
    ex1_result = check_ex1()
    ex2_result = check_ex2()
    ex3_result = check_ex3()
    table = []
    table.append(('1. Splitters', *ex1_result[0: 2]))
    table.append(('2. Rotate Right', *ex2_result[0: 2]))
    table.append(('3. ALU', *ex3_result[0: 2]))
    errors = ex1_result[2]
    errors += '\n' + ex2_result[2]
    errors += '\n' + ex3_result[2]
    errors = errors.strip()
    grade = 0
    grade += ex1_result[0]
    grade += ex2_result[0]
    grade += ex3_result[0]
    grade = min(round(grade), 100)
    report = create_report(table)
    if errors != '':
        report += '\n\nMore Info:\n\n' + errors
    print(report)
    print('\n=> Score: %d/100' % grade)


if __name__ == '__main__':
    lab6_logisim()
