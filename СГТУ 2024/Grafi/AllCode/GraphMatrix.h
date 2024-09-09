#include <iostream>
#include <vector>

class GraphMatrix {
private:
    int vertices;
    std::vector<std::vector<int>> adjMatrix;

public:
    GraphMatrix(int v) : vertices(v) {
        adjMatrix.resize(vertices, std::vector<int>(vertices, 0));
    }

    void addEdge(int u, int v) {
        if (u >= 0 && u < vertices && v >= 0 && v < vertices) {
            adjMatrix[u][v] = 1;
        }
        else {
            std::cerr << "Ошибка: неверные вершины." << std::endl;
        }
    }

    void printAdjMatrix() const {
        std::cout << "Матрица смежности:" << std::endl;
        for (const auto& row : adjMatrix) {
            for (int val : row) {
                std::cout << val << " ";
            }
            std::cout << std::endl;
        }
    }

    std::vector<std::vector<int>> getIncidenceMatrix() const {
        int edges = 0;
        for (int i = 0; i < vertices; ++i) {
            for (int j = 0; j < vertices; ++j) {
                if (adjMatrix[i][j] == 1) {
                    edges++;
                }
            }
        }

        std::vector<std::vector<int>> incidenceMatrix(vertices, std::vector<int>(edges, 0));
        int edgeIndex = 0;

        for (int i = 0; i < vertices; ++i) {
            for (int j = 0; j < vertices; ++j) {
                if (adjMatrix[i][j] == 1) {
                    incidenceMatrix[i][edgeIndex] = 1;
                    incidenceMatrix[j][edgeIndex] = -1;
                    edgeIndex++;
                }
            }
        }

        return incidenceMatrix;
    }

    std::vector<std::vector<int>> getKirchhoffMatrix() const {
        std::vector<std::vector<int>> kirchhoffMatrix(vertices, std::vector<int>(vertices, 0));

        for (int i = 0; i < vertices; ++i) {
            int degree = 0;
            for (int j = 0; j < vertices; ++j) {
                degree += adjMatrix[i][j];
            }
            kirchhoffMatrix[i][i] = degree;
        }

        for (int i = 0; i < vertices; ++i) {
            for (int j = 0; j < vertices; ++j) {
                if (i != j && adjMatrix[i][j] == 1) {
                    kirchhoffMatrix[i][j] = -1;
                }
            }
        }

        return kirchhoffMatrix;
    }

    void printMatrix(const std::vector<std::vector<int>>& matrix) const {
        for (const auto& row : matrix) {
            for (int val : row) {
                std::cout << val << " ";
            }
            std::cout << std::endl;
        }
    }
};