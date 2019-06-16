import reader
import math
import random
from typing import List
from edge import Edge
from vertex import Vertex
from sys import maxsize

INF = maxsize / 10
a1 = 0
a2 = 0
a3 = 0
a4 = 1


def fitness(path, ev_map, vc_map):
    di = ev_map[path[0]][path[1]]
    li = 0
    jam = 0
    for i in range(len(path) - 1):
        li += ev_map[path[i]][path[i + 1]]
        jam += vc_map[path[i]][path[i + 1]]
    psi = 1 / li * math.exp(-jam)
    si = vc_map[path[-1]][path[-2]]
    fit = a1 * math.exp(-di) + a2 * math.exp(-psi) + a3 * math.exp(-si) + a4 * math.exp(-li)
    return fit


def dijkstra(maps, start, end):
    mins = 0
    min_num = 0
    path = [-1 for i in range(79)]
    v = [False for i in range(79)]
    d = [INF for i in range(79)]
    for i in range(1, 79):
        d[i] = maps[start][i]
        if d[i] != INF and i != start:
            path[i] = start
        else:
            path[i] = -1
    v[start] = True
    unvisited = list(set([i for i in range(1, 79)]) - {start})
    while len(unvisited) != 0:
        mins = INF
        for child in unvisited:
            if d[child] < mins:
                mins = d[child]
                min_num = child
        unvisited.pop(unvisited.index(min_num))
        for j in range(1, 79):
            if d[j] > mins + maps[min_num][j]:
                path[j] = min_num
                d[j] = mins + maps[min_num][j]
    current = end
    norm_path = []
    while current != start:
        norm_path.append(current)
        current = path[current]
    norm_path.append(start)
    norm_path = norm_path[::-1]
    return norm_path


def main():
    result = open('./route.txt', 'w')
    e_list = reader.map_reader()  # type: List[Edge]
    v_list = []
    q_list = [64, 78]
    ev_map = [[INF for i in range(79)] for i in range(79)]
    for i in range(79):
        ev_map[i][i] = 0
        v_list.append(Vertex(vid=i))
    guest = 0
    for i in range(len(e_list)):
        v_list[e_list[i].start].edge.append(i)
        v_list[e_list[i].end].edge.append(i)
        ev_map[e_list[i].start][e_list[i].end] = e_list[i].length
        ev_map[e_list[i].end][e_list[i].start] = e_list[i].length
        for j in range(e_list[i].capacity):
            e_list[i].load.append(guest)
            guest += 1
    exit_flow = [[] for nn in range(5)]
    print('Total Guest:', guest)
    time = 0
    while guest > 2:
        exit_flow[0].append(len(e_list[67].load))
        exit_flow[1].append(len(e_list[87].load))
        exit_flow[2].append(len(e_list[91].load))
        exit_flow[3].append(len(e_list[92].load))
        exit_flow[4].append(len(e_list[93].load))
        for i in range(len(e_list)):
            e_list[i].done = False
        bfs_queue = [64, 78]
        for i in bfs_queue:
            for child in v_list[i].edge:
                if not e_list[child].done:
                    e_list[child].done = True
                    v1 = e_list[child].start
                    v2 = e_list[child].end
                    if i == v1:
                        target = v2
                    else:
                        target = v1
                    if target not in bfs_queue:
                        bfs_queue.append(target)
                    if len(e_list[child].load) == 0:
                        continue
                    if i in q_list:
                        if len(e_list[child].load) > 0:
                            e_list[child].load.pop(0)
                            guest -= 1
                    else:
                        po_map = [[INF for mm in range(79)] for nm in range(79)]
                        vc_map = [[INF for mm in range(79)] for nm in range(79)]
                        for edge in e_list:
                            po_map[edge.start][edge.end] = len(edge.load)
                            po_map[edge.end][edge.start] = len(edge.load)
                            vc_map[edge.start][edge.end] = len(edge.load) / edge.max_c
                            vc_map[edge.end][edge.start] = len(edge.load) / edge.max_c
                        path_six = [
                            dijkstra(ev_map, i, 64),
                            dijkstra(ev_map, i, 78),
                            dijkstra(po_map, i, 64),
                            dijkstra(po_map, i, 78),
                            dijkstra(vc_map, i, 64),
                            dijkstra(vc_map, i, 78)
                        ]
                        collect = {}
                        for j in range(6):
                            collect[j] = fitness(path_six[j], ev_map, vc_map)
                        new_collect = sorted(collect.items(), key=lambda x: x[1], reverse=True)  # type:List[tuple]
                        pop = 0
                        for each in new_collect:
                            index = each[0]
                            if vc_map[path_six[index][0]][path_six[index][1]] < 1 and len(e_list[child].load) > 0:
                                out = e_list[child].load[0]
                                for j in range(len(e_list)):
                                    if e_list[j].start == path_six[index][0] and e_list[j].end == path_six[index][1] or e_list[j].end == path_six[index][0] and e_list[j].start == path_six[index][1]:
                                        if vc_map[path_six[index][0]][path_six[index][1]] > 0.2:
                                            rand = random.random()
                                            rate = vc_map[path_six[index][0]][path_six[index][1]]
                                            if rand > math.sqrt(rate):
                                                e_list[j].load.append(out)
                                                e_list[child].load.pop(0)
                                                pop += 1
                                                break
                                        else:
                                            e_list[j].load.append(out)
                                            e_list[child].load.pop(0)
                                            pop += 1
                                            break
                            # if pop == 6:
                            #     break
        time += 1
        print(time, guest)
    for i in range(len(exit_flow[0])):
        stt = ''
        for j in range(5):
            stt += str(exit_flow[j][i])
            stt += ','
        stt += '\n'
        result.write(stt)


if __name__ == '__main__':
    main()
