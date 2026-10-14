n = int(input())

INF = float('inf')
matr = [[INF] * n for _ in range(n)]

for i in range(n):
    row = input().split()
    for pair in row:
        v, w = pair.split(':')
        matr[i][int(v) - 1] = int(w)

start = int(input()) - 1
finish = int(input()) - 1

dis = [INF] * n
vis = [False] * n
prev = [-1] * n
dis[start] = 0

for _ in range(n):
    now = -1
    for i in range(n):
        if not vis[i] and (now == -1 or dis[i] < dis[now]):
            now = i

    if now == -1 or dis[now] == INF:
        break

    vis[now] = True


    for i in range(n):
        if matr[now][i] != INF and dis[now] + matr[now][i] < dis[i]:
            dis[i] = dis[now] + matr[now][i]
            prev[i] = now


if dis[finish] == INF:
    print(-1)
else:
    path = []
    v = finish
    while v != -1:
        path.append(v)
        v = prev[v]
    path.reverse()

    weights = []
    for i in range(len(path) - 1):
        weights.append(matr[path[i]][path[i + 1]])
    print(dis[finish])
    print(' '.join(str(v + 1) for v in path))