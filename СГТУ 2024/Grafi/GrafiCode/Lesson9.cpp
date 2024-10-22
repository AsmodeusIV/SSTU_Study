#include "Lesson9.h"
#include <iostream>
#include <vector>

using namespace std;

void ex_9() {

}

int sum = 80000;

void go(int **g, int *ans,int *cur,int *used, int k)
{
	if (k == 8) {
		if (ans[0] == -1) {
			for (int i = 0; i < 8; i++) {
				ans[i] = cur[i];
			}
		}
		else {
			int s1 = 0, s2 = 0;
			for (int i = 0; i < 7; i++) {
				s1 += g[ans[i]][ans[i+1]];
				s2 += g[cur[i]][cur[i+1]];
			}
			if (s2 < s1) {
				for (int i = 0; i < 8; i++) {
					ans[i] = cur[i];
				}
			}
		}
		return;
	}
	for(int i = 0; i < 8; i++) {
		if (used[i] == 0) {
			used[i] = 1;
			cur[k] = i;
			go(g, ans, cur, used, k + 1);
			used[i] = 0;
		}
	}
}

void ex_10() {
	int** g = new int*[8];
	g[0] = new int[8] {-1,190,210,680,690,460,780,750};
	g[1] = new int[8] {190, -1, 380, 760, 790, 610, 670, 450};
	g[2] = new int[8] {210, 380, -1, 890, 900, 340, 410, 600};
	g[3] = new int[8] {680, 760, 890, -1, 480, 760, 510, 250};
	g[4] = new int[8] {690, 790, 900, 480, -1, 890, 490, 560};
	g[5] = new int[8] {460, 610, 340, 760, 890, -1, 720, 600};
	g[6] = new int[8] {780, 670, 410, 510, 490, 720, -1, 500};
	g[7] = new int[8] {750, 450, 600, 250, 560, 600, 500, -1};
	int* a_cur = new int[8];
	int* used = new int[8];
	int* a_ans = new int[8];
	for (int i = 0;i < 8;i++)
	{
		a_cur[i] = -1;
		used[i] = 0;
		a_ans[i] = -1;
	}

	string names[] = {"Saratov", "Akapyliko", "Gonolulu", "Tokio", "Gonkong", "London", "Sidney", "Rim"};

	go(g, a_ans, a_cur, used, 0);
	for (int i = 0; i < 8; i++) {
		 cout << names[a_ans[i]] << " ";
	}
	int s1 = 0;
	for (int i = 0; i < 7; i++) {
		s1 += g[a_ans[i]][a_ans[i + 1]];
	}
	printf("\nSum len: %d", s1);
}
