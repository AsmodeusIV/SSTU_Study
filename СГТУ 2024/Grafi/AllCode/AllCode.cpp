#include <iostream>
#include <vector>
#include "Lesson6.h"

using namespace std;

int main() {
    // Пример списка смежности для дерева
    vector<vector<int>> edges = { {1, 2}, {2, 5}, {5, 4}, {10, 5}, {6,5}, {6, 3}, {6,9}, {9, 8}, {8, 7}, {8, 11} };

    // Построение кода Прюфера
    vector<int> code = pruferCode(edges);

    cout << "Prufer Code: ";
    for (int node : code) {
        cout << node << " ";
    }
    cout << endl;

    /*// Дешифровка кода Прюфера
    vector<vector<int>> decodedEdges = decodePrufer(code);

    cout << "Decoded Adjacency List:" << endl;
    printAdjacencyList(decodedEdges);
    */
    return 0;
}