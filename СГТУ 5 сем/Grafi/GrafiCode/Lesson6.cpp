#include "Lesson6.h"



void ex_5()
{
	int n;
	cout << "¬ведите длину кода ѕпрюфера: ";
	cin >> n;
	vector<int> nums(n);
	for (int i = 0; i < n; i++) {
		cin >> nums[i];
		nums[i]--;
	}
	prufer_decode(nums);
}

void prufer_decode(const vector<int>& prufer_code) {
	int n = (int)prufer_code.size() + 2;
	vector<int> degree(n, 1);
	for (int i = 0; i < n - 2; ++i)
		++degree[prufer_code[i]];

	set<int> leaves;
	for (int i = 0; i < n; ++i)
		if (degree[i] == 1)
			leaves.insert(i);

	vector < pair<int, int> > result;
	for (int i = 0; i < n - 2; ++i) {
		int leaf = *leaves.begin();
		leaves.erase(leaves.begin());

		int v = prufer_code[i];
		result.push_back(make_pair(leaf, v));
		if (--degree[v] == 1)
			leaves.insert(v);
	}
	result.push_back(make_pair(*leaves.begin(), *--leaves.end()));

	vector< vector<int> > g(prufer_code.size()+2);

	for (auto& i : result)
	{
		g[i.first].push_back(i.second);
		g[i.second].push_back(i.first);
	}

	for (int i = 0; i < prufer_code.size() + 2; i++)
	{
		cout << i + 1 << ": ";
		for (int j = 0; j < g[i].size(); j++)
			cout << g[i][j] + 1 << " ";
		cout << endl;
	}
}