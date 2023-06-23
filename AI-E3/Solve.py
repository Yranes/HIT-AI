from Bayes import BN
from Bayes import cpt

def read_network(path):
    with open(path, 'r', encoding = 'utf-8') as f:
        variable_num = int(f.readline())
        f.readline()
        variables = f.readline().strip('\n').split(' ')
        f.readline()
        graph = []
        for i in range(variable_num):
            line = f.readline().strip('\n').split(' ')
            graph.append(list(map(int, line)))
        f.readline()
        
        cpts = []
        for i in range(variable_num):
            probabilities = []
            while True:
                line = f.readline().strip('\n ').split(' ')
                if line == ['']:
                    break
                probabilities.append(list(map(float, line)))
            C = cpt(variables[i], [], probabilities)
            cpts.append(C) # 建立cpt表

    for i in range(variable_num):
        for j in range(variable_num):
            if graph[i][j] == 1:
                cpts[j].parents.append(i) # add_parents
    return BN(variable_num, variables, graph, cpts)

def read_events(path, variables): # 0-变量false, 1-变量true, 2变量为所求（0/1）, 3变量需消去(0/1)
    with open(path, 'r', encoding = 'utf-8') as f:
        events = []
        for line in f:
            if line == '\n':
                continue
            event = []
            for v in variables:
                index = line.find(v)
                if index != -1:
                    if line[index + len(v)] == ' ':
                        event.append(2)
                    else:
                        if line[index + len(v) + 1] == 't':
                            event.append(1)
                        else:
                            event.append(0)
                else:
                    event.append(3)
            events.append(event)
    return events

if __name__ == '__main__':
    bayesnet = read_network("Network.txt")
    events = read_events("Query.txt", bayesnet.variables)
    for event in events:
        print(bayesnet.CalculateProbability(event))