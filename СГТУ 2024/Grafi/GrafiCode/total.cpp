#include "total.h"
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include <set>
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

void ex_33() {
    int n, m;
    cin >> n >> m;

    // Представление графа с помощью вектора векторов
    vector<vector<pair<int,int>>> graph(n + 1);
    vector<int> used(n + 1, 0);
    vector<int> dist(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int x, y, l;
        cin >> x >> y >> l;
        x--;
        y--;
        graph[x].push_back(make_pair(y, l));
    }
    set<vector<int>> q;
    q.insert({ 0,-1 });
    while (!q.empty())
    {
        auto vv = *q.begin();
        int v = vv[0], color = vv[1];
        q.erase(vv);

        for (auto i : graph[v]) {
            if (!used[i.first] && color!=i.second) {
                used[i.first] = 1;
                q.insert({ i.first, i.second});
                dist[i.first] = dist[v] + 1;
            }
        }
    }
    cout << dist[n - 1];
}

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

struct Graph {
    vector<vector<int>> g;
    vector<vector<int>> gr; // Обратный граф
};

// Функция для глубины поиска в ширину (DFS)
void dfs1(int v, vector<bool>& used, vector<int>& order, Graph& graph) {
    used[v] = true;
    for (size_t i = 0; i < graph.g[v].size(); ++i) {
        if (!used[graph.g[v][i]]) {
            dfs1(graph.g[v][i], used, order, graph);
        }
    }
    order.push_back(v);
}

// Функция для глубины поиска в ширину (DFS) на обратном графе
void dfs2(int v, vector<bool>& used, vector<int>& component, Graph& graph) {
    used[v] = true;
    component.push_back(v);
    for (size_t i = 0; i < graph.gr[v].size(); ++i) {
        if (!used[graph.gr[v][i]]) {
            dfs2(graph.gr[v][i], used, component, graph);
        }
    }
}

// Функция для поиска сильно связных компонент
vector<vector<int>> find_strongly_connected_components(Graph& graph) {
    int n = graph.g.size();
    vector<bool> used(n, false);
    vector<int> order;

    // Поиск в глубину на исходном графе
    for (int i = 0; i < n; ++i) {
        if (!used[i]) {
            dfs1(i, used, order, graph);
        }
    }

    // Инициализация переменных для хранения сильно связных компонент
    used.assign(n, false);
    vector<vector<int>> components;

    // Поиск в глубину на обратном графе
    for (int i = 0; i < n; ++i) {
        int v = order[n - 1 - i];
        if (!used[v]) {
            vector<int> component;
            dfs2(v, used, component, graph);
            components.push_back(component);
        }
    }

    return components;
}


// Основная функция
void ex_77() {
    int n, m;
    cin >> n >> m;

    // Создание графа
    Graph graph;
    graph.g.resize(n);
    graph.gr.resize(n);

    // Чтение ребер графа
    int a, b;
    for (int i = 0;i < m; i++){
        cin >> a >> b;
        a--; b--;
        graph.g[a].push_back(b);
        graph.gr[b].push_back(a);
    }

    // Поиск сильно связных компонент
    vector<vector<int>> components = find_strongly_connected_components(graph);

    // Вывод сильно связных компонент
    for (const auto& component : components) {
        cout << "Component: ";
        for (int v : component) {
            cout << v+1 << " ";
        }
        cout << endl;
    }
}
const int INF = 1000000000;

void ex_88() {
    int n, m, s,f;
    cin >> n >> m >> s >> f;
    vector < vector < pair<int, int> > > g(n);
    for (int i = 0; i < m; i++)
    {
        int a, b, c;
        cin >> a >> b >> c;
        a--;
        b--;
        g[a].push_back(make_pair(b, c));
        g[b].push_back(make_pair(a, c));
    }
    s--; f--;
    vector<int> d(n, INF), p(n);
    d[s] = 0;
    set < pair<int, int> > q;
    q.insert(make_pair(d[s], s));
    while (!q.empty()) {
        int v = q.begin()->second;
        q.erase(q.begin());

        for (size_t j = 0; j < g[v].size(); ++j) {
            int to = g[v][j].first,
                len = g[v][j].second;
            if (d[v] + len < d[to]) {
                q.erase(make_pair(d[to], to));
                d[to] = d[v] + len;
                p[to] = v;
                q.insert(make_pair(d[to], to));
            }
        }
    }
    cout << d[f];
}

const int inf = 1000 * 1000 * 1000;


typedef vector<int> graf_line;
typedef vector<graf_line> graf;

typedef vector<int> vint;
typedef vector<vint> vvint;


void push(int u, int v, vvint& f, vint& e, const vvint& c)
{
    int d = min(e[u], c[u][v] - f[u][v]);
    f[u][v] += d;
    f[v][u] = -f[u][v];
    e[u] -= d;
    e[v] += d;
}

void lift(int u, vint& h, const vvint& f, const vvint& c)
{
    int d = inf;
    for (int i = 0; i < (int)f.size(); i++)
        if (c[u][i] - f[u][i] > 0)
            d = min(d, h[i]);
    if (d == inf)
        return;
    h[u] = d + 1;
}

void ex_99() {
    int n;
    cin >> n;
    vvint c(n, vint(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            cin >> c[i][j];
    // исток - вершина 0, сток - вершина n-1

    vvint f(n, vint(n));
    for (int i = 1; i < n; i++)
    {
        f[0][i] = c[0][i];
        f[i][0] = -c[0][i];
    }

    vint h(n);
    h[0] = n;

    vint e(n);
    for (int i = 1; i < n; i++)
        e[i] = f[0][i];

    for (; ; )
    {
        int i;
        for (i = 1; i < n - 1; i++)
            if (e[i] > 0)
                break;
        if (i == n - 1)
            break;

        int j;
        for (j = 0; j < n; j++)
            if (c[i][j] - f[i][j] > 0 && h[i] == h[j] + 1)
                break;
        if (j < n)
            push(i, j, f, e, c);
        else
            lift(i, h, f, c);
    }

    int flow = 0;
    for (int i = 0; i < n; i++)
        if (c[0][i])
            flow += f[0][i];

    cout << max(flow, 0);

}

vector<int> fordBellman(const vector<vector<int>>& graph, int source, int n) {
    // Инициализация массива расстояний
    vector<int> distances(n + 1, INF);
    distances[source] = 0;

    // Выполнение релаксации ребер n - 1 раз
    for (int i = 0; i < n - 1; i++) {
        for (int from = 1; from <= n; from++) {
            for (int j = 0; j < graph[from].size(); j += 2) {
                int to = graph[from][j];
                int weight = graph[from][j + 1];

                if (distances[from] != INF &&
                    distances[to] > distances[from] + weight) {
                    distances[to] = distances[from] + weight;
                }
            }
        }
    }

    // Проверка на наличие циклов отрицательного веса
    for (int from = 1; from <= n; from++) {
        for (int j = 0; j < graph[from].size(); j += 2) {
            int to = graph[from][j];
            int weight = graph[from][j + 1];

            if (distances[from] != INF &&
                distances[to] > distances[from] + weight) {
                return vector<int>(n + 1, -1); // Возвращаем вектор с -1, если есть цикл
            }
        }
    }

    return distances;
}

void ex_100()
{
    int n, m;
    cin >> n >> m;

    // Представление графа с помощью вектора векторов
    vector<vector<int>> graph(n + 1);

    for (int i = 0; i < m; i++) {
        int x, y, l;
        cin >> x >> y >> l;
        graph[x].push_back(y); // Добавляем конечную вершину
        graph[x].push_back(l); // Добавляем вес ребра
    }

    // Вызов алгоритма Форда-Беллмана и вывод результатов
    vector<int> distances = fordBellman(graph, 1, n); // Стартовая вершина - 1

    for (int i = 2; i <= n; i++) {
        if (distances[i] == INF) {
            cout << "NO" << endl;
        }
        else {
            cout << distances[i] << endl;
        }
    }
}