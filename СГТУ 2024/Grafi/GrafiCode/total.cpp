#include "total.h"
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

void ex_1()
{
    int n;
    cin >> n;

    vector<vector<int>> adj(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> adj[i][j];
        }
    }

    vector<int> inDegree(n, 0);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (adj[i][j] == 1) {
                inDegree[j]++;
            }
        }
    }

    queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) {
            q.push(i);
        }
    }

    vector<int> topologicalOrder;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        topologicalOrder.push_back(u);

        for (int v = 0; v < n; ++v) {
            if (adj[u][v] == 1) {
                inDegree[v]--;
                if (inDegree[v] == 0) {
                    q.push(v);
                }
            }
        }
    }

    for (int i = 0; i < n; ++i) {
        cout << topologicalOrder[i] + 1 << " ";
    }
}


void ex_22();

void ex_3();

void dfs(int u, vector<vector<int>>& graph, vector<int>& component, vector<bool>& visited, int comp) {
    visited[u] = true;
    component[u] = comp;
    for (int v : graph[u]) {
        if (!visited[v]) {
            dfs(v, graph, component, visited, comp);
        }
    }
}

void ex_4() {
    int N, M;
    cin >> N >> M;

    vector<vector<int>> graph(N + 1);
    vector<int> component(N + 1);
    vector<bool> visited(N + 1, false); 

    for (int i = 0; i < M; ++i) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    int L = 0; 
    for (int u = 1; u <= N; ++u) {
        if (!visited[u]) {
            ++L;
            dfs(u, graph, component, visited, L);
        }
    }

    cout << L << endl;
    for (int i = 1; i <= N; ++i) {
        cout << component[i] << " ";
    }
    cout << endl;

}

// Функция для поиска мостов в графе
void find_bridges(const vector<vector<int>>& graph, vector<bool>& used, vector<int>& tin, vector<int>& fup, int& timer, int v, int p = -1) {
    used[v] = true;
    tin[v] = fup[v] = timer++;
    for (int to : graph[v]) {
        if (to == p) continue;
        if (used[to]) {
            fup[v] = min(fup[v], tin[to]);
        }
        else {
            find_bridges(graph, used, tin, fup, timer, to, v);
            fup[v] = min(fup[v], fup[to]);
            if (fup[to] > tin[v]) {
                cout << "Мост:" << v+1 << " " << to+1 << endl;
            }
        }
    }
}

// Основная функция для поиска мостов
void find_bridges(const vector<vector<int>>& graph, int n) {
    vector<bool> used(n, false);
    vector<int> tin(n, 0);
    vector<int> fup(n, 0);
    int timer = 0;
    for (int i = 0; i < n; ++i) {
        if (!used[i]) {
            find_bridges(graph, used, tin, fup, timer, i);
        }
    }
}


void ex_55() {
    int n, m;
    cout << "Введите количество вершин\n";
    cin >> n;
    cout << "Введите количество ребер\n";
    cin >> m;

    vector< vector<int> > g(n);
    vector<int> used(n, 0);

    cout << "Введите ребра:\n";
    for (int i = 0; i < m; i++)
    {
        int x, y;
        cin >> x >> y;
        g[x-1].push_back(y-1);
        g[y-1].push_back(x-1);
    }
    find_bridges(g, n);
}

const int MAXN = 1000;

void dfs1(const vector<vector<int>>& g, int v, int p, vector<int>& tin, vector<int>& fup, vector<bool>& used, int& timer) {
    used[v] = true;
    tin[v] = fup[v] = timer++;

    int children = 0;
    for (int to : g[v]) {
        if (to == p) continue;
        if (used[to]) {
            fup[v] = min(fup[v], tin[to]);
        }
        else {
            dfs1(g, to, v, tin, fup, used, timer);
            fup[v] = min(fup[v], fup[to]);
            if (fup[to] >= tin[v] && p != -1) {
                cout << "Точка:" << v+1 << endl;
            }
            ++children;
        }
    }
    if (p == -1 && children > 1) {
        cout << "Точка:" << v+1 << endl;
    }
}

void ex_66() {
    int n, m;
    cout << "Введите количество вершин\n";
    cin >> n;
    cout << "Введите количество ребер\n";
    cin >> m;
    vector<vector<int>> g(MAXN); // Граф

    cout << "Введите ребра:\n";
    for (int i = 0; i < m; i++)
    {
        int x, y;
        cin >> x >> y;
        g[x - 1].push_back(y - 1);
        g[y - 1].push_back(x - 1);
    }

    vector<int> tin(MAXN, -1);
    vector<int> fup(MAXN, -1);
    vector<bool> used(MAXN, false);
    int timer = 0;

    dfs1(g, 0, -1, tin, fup, used, timer);

}
void ex_7();
void ex_8();
void ex_9();
void ex_10();
void ex_11();