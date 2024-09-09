#include <iostream>
#include <vector>
#include <queue>
#include "Lesson7.h"

using namespace std;

void dfs(vector< vector<int> >& g, vector<int>& used, int v)
{
	cout << v << " ";
	used[v] = 1;
	for (int& i : g[v]) {
		//cout << i;
		if (used[i]==0)
			dfs(g, used, i);
	}
}

void ex_6() {
	int n, m;
	
	cout << "¬ведите количество вершин\n";
	cin >> n;
	cout << "¬ведите количество ребер\n";
	cin >> m;

	vector< vector<int> > g(n);
	vector<int> used(n, 0);

	cout << "¬ведите ребра:\n";
	for (int i = 0; i < m; i++)
	{
		int x, y;
		cin >> x >> y;
		g[x].push_back(y);
		g[y].push_back(x);
	}
	dfs(g, used, 0);
}
/*
0 3
3 1
3 7
3 6
2 6
5 6
8 4
4 1
7 4
*/

void ex_7() {
	int n, m;

	cout << "¬ведите количество вершин\n";
	cin >> n;
	cout << "¬ведите количество ребер\n";
	cin >> m;

	vector< vector<int> > g(n);
	vector<int> used(n, 0);

	cout << "¬ведите ребра:\n";
	for (int i = 0; i < m; i++)
	{
		int x, y;
		cin >> x >> y;
		g[x].push_back(y);
		g[y].push_back(x);
	}

	queue<int> vertix;
	vertix.push(0);
	used[0] = 1;
	while (!vertix.empty()) {
		int v = vertix.front();
		cout << v << " ";
		vertix.pop();

		for (int& i : g[v]) {
			if (!used[i]) {
				used[i] = 1; 
				vertix.push(i);
			}
		}
	}
}

void ex_8() {
	int n, m, d;

	cout << "¬ведите количество вершин\n";
	cin >> n;
	cout << "¬ведите количество ребер\n";
	cin >> m;
	cout << "¬ведите дистанцию\n";
	cin >> d;

	vector< vector<int> > g(n);
	vector<int> used(n, 0);

	cout << "¬ведите ребра:\n";
	for (int i = 0; i < m; i++)
	{
		int x, y;
		cin >> x >> y;
		g[x].push_back(y);
		g[y].push_back(x);
	}

	queue<vector<int>> vertix;
	vertix.push({0,0});
	used[0] = 1;
	while (!vertix.empty()) {
		auto t = vertix.front();
		int v = t[0];
		int dist = t[1];
		vertix.pop();

		if (dist == d)
			cout << v << " ";

		for (int& i : g[v]) {
			if (!used[i]) {
				used[i] = 1; 
				vertix.push({i, dist+1});
			}
		}
	}
}