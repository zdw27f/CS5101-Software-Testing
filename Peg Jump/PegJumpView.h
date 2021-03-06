//Group Members: Alfonso Miguel Santos-Tankia and Zachary Wileman
#ifndef PegJumpView_h
#define PegJumpView_h

#include <iostream>
#include <cstdlib>
#include <vector>
using namespace std;

class PegJumpView {
public:
	// Null constructor
	PegJumpView() {}

	void printStart();

	void gameSelect();

	void invalidChoice();

	void playAgain();

	void menu();

	void printScores(int numGames, const string gameNames[], int gameScore[]);

	void firstPeg();

	void selectDifficulty();

	void twoPeg();

	void solutionFound(vector<char> &solutionList);

	void noSolution();

	void win();

	void lose();

	void cumScore(int gameScore[], int gameSelected);
};

#endif
