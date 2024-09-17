#include "Lesson10.h"

#include <iostream>
#include <vector>

using namespace std;

class Point
{
public:
	double x, y;
};

std::istream& operator >> (std::istream& os, Point& p)
{
	double x, y;
	os >> x >> y;
	p.x = x;
	p.y = y;
	return os;
}

double dist(Point a, Point b)
{
	return sqrt( (a.x-b.x)*(a.x - b.x) + (a.y - b.y)*(a.y - b.y) );
}

class Edge
{
public:
	int s, e;
	double len;
	Edge(int a, int b, double c)
	{
		s = a;
		e = b;
		len = c;
	}
};

std::ostream& operator << (std::ostream& os, const Edge& person)
{
	return os << person.s << " " << person.e << " dist: " << person.len;
}

void ex_2()
{
	int n;
	cout << "¬ведите кол-во вершин" << endl;
	cin >> n;
	vector<Point> points(n);
	cout << "¬ведиет координаты каждой точки (x, y)" << endl;
	for (Point& i : points)
		cin >> i;
	vector<Edge> edges;
	for (int i = 0; i < n - 1; i++)
		for (int j = i + 1; j < n; j++)
			edges.push_back(Edge(i,j,dist(points[i],points[j])));

	for (Edge& i : edges)
		cout << i << endl;

}