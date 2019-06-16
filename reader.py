import pandas as pd
from edge import Edge
from typing import List


def map_reader():
    file = './src/data/edge.xlsx'
    df = pd.read_excel(file, sheet_name='edge')
    e_list = []
    # print(df.loc[0][['start', 'end']])
    for i in df.index:
        edge = Edge(
            eid=i,
            start=int(df.loc[i]['start']),
            end=int(df.loc[i]['end']),
            length=int(df.loc[i]['length']),
            capacity=int(df.loc[i]['capacity'])
        )
        # print(edge.eid, edge.start, edge.end, edge.length, edge.capacity)
        e_list.append(edge)
    return e_list


def route_reader():
    e_list = map_reader()  # type:List[Edge]
    file = './src/data/routing.txt'
    outsq = './src/output/sq.txt'
    outrt = './src/output/rt.txt'
    sq = [0 for i in range(79)]
    new_route = [0 for i in range(94)]
    with open(file, 'r') as f:
        route_data = f.readlines()
        for line in route_data:
            tmp = line.replace(',', '').strip('\r\n').split()
            for v in tmp:
                sq[int(v)] += 1
            for j in range(len(tmp) - 1):
                v1 = int(tmp[j])
                v2 = int(tmp[j + 1])
                for e in range(len(e_list)):
                    if e_list[e].start == v1 and e_list[e].end == v2 or e_list[e].end == v1 and e_list[e].start == v2:
                        new_route[e] += 1
                        break
    with open(outsq, 'w') as f:
        for i in range(79):
            tmp = str(i) + ' ' + str(sq[i]) + '\r\n'
            f.write(tmp)
    with open(outrt, 'w') as f:
        for i in range(94):
            tmp = str(i) + ' ' + str(new_route[i]) + ' ' + '(%s,%s)' % (str(e_list[i].start), str(e_list[i].end)) + '\r\n'
            f.write(tmp)
