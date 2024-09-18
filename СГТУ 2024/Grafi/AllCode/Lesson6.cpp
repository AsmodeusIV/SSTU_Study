#include "Lesson6.h"

#include <iostream>
#include <vector>
#include <unordered_map>
#include <set>

using namespace std;

vector<int> pruferCode(const vector<vector<int>>& edges) {
    unordered_map<int, int> degree;
    set<int> leaves;

    // Подсчет степени каждой вершины
    for (const auto& edge : edges) {
        degree[edge[0]]++;
        degree[edge[1]]++;
    }

    // Инициализация множества листьев
    for (int i = 0; i < degree.size(); ++i) {
        if (degree[i] == 1) {
            leaves.insert(i);
        }
    }

    vector<int> code;

    // Построение кода Прюфера
    for (int i = 0; i < edges.size() - 1; ++i) {
        int leaf = *leaves.begin(); // Наименьший лист
        leaves.erase(leaf);

        // Находим соседей листа
        for (const auto& edge : edges) {
            if (edge[0] == leaf || edge[1] == leaf) {
                int neighbor = (edge[0] == leaf) ? edge[1] : edge[0];
                code.push_back(neighbor);

                // Уменьшаем степень соседа
                degree[neighbor]--;

                // Если степень соседа стала равной 1, добавляем его в листья
                if (degree[neighbor] == 1) {
                    leaves.insert(neighbor);
                }
                break;
            }
        }
    }

    return code;
}


/*
vector<vector<int>> decodePrufer(const vector<int>& code) {
    unordered_map<int, int> degree;
    vector<vector<int>> edges;
    int n = code.size() + 2;

    // Подсчет степени для каждой вершины
    for (int node : code) {
        degree[node]++;
    }

    // Добавляем дополнительные вершины
    for (int i = 1; i <= n; ++i) {
        degree[i]++; // Каждая вершина будет иметь степень как минимум 1
    }

    set<int> leaves;
    for (const auto& [node, deg] : degree) {
        if (deg == 1) {
            leaves.insert(node);
        }
    }

    // Дешифровка кода Прюфера
    for (int node : code) {
        int leaf = *leaves.begin();
        leaves.erase(leaf);

        edges.push_back({ leaf, node });

        // Уменьшаем степень узла
        degree[node]--;

        if (degree[node] == 1) {
            leaves.insert(node);
        }
    }

    // Добавляем последние два узла
    auto it = leaves.begin();
    int u = *it++;
    int v = *it;
    edges.push_back({ u, v });

    return edges;
}

void printAdjacencyList(const vector<vector<int>>& edges) {
    unordered_map<int, vector<int>> adjacencyList;

    for (const auto& edge : edges) {
        adjacencyList[edge[0]].push_back(edge[1]);
        adjacencyList[edge[1]].push_back(edge[0]);
    }

    for (const auto& [node, neighbors] : adjacencyList) {
        cout << "Node " << node << ": ";
        for (int neighbor : neighbors) {
            cout << neighbor << " ";
        }
        cout << endl;
    }
}
*/

