
#include <iostream>
#include <vector>
#include <algorithm>
#include "Lesson15.h"

using namespace std;

int n, k;
vector < vector<int> > g;
vector<int> mt;
vector<char> used;

bool try_kuhn(int v) {
    if (used[v])  return false;
    used[v] = true;
    for (size_t i = 0; i < g[v].size(); ++i) {
        int to = g[v][i];
        if (mt[to] == -1 || try_kuhn(mt[to])) {
            mt[to] = v;
            return true;
        }
    }
    return false;
}

void ex() {
    // Чтение графа
    cin >> n >> k; // Количество вершин и ребер
    g.resize(n); // Инициализация вектора графа

    for (int i = 0; i < k; ++i) {
        int u, v;
        cout << i << ": ";
        cin >> u >> v; // Чтение ребра
        u--; v--; // Индексы начинаются с 0
        g[u].push_back(v); // Добавление ребра в граф
    }

    mt.assign(k, -1);
    for (int v = 0; v < n; ++v) {
        used.assign(n, false);
        try_kuhn(v);
    }

    for (int i = 0; i < k; ++i)
        if (mt[i] != -1)
            printf("%d %d\n", mt[i]+1, i+1);
}
