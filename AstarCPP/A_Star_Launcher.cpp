// A C++ Program to implement A* Search Algorithm
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <iostream>

#include <vector>
#include <string>
#include "A_Star_Class.cpp"
using namespace std;

// Driver program to test above function
string launcher(int row, int col, vector<vector<int>> forbidden_vector, vector<int> start_arr, vector<int> finish_arr)
{
	// Creating a shortcut for int, int pair type
	typedef pair<int, int> Pair;
	// Creating a shortcut for pair<int, pair<int, int>> type
	typedef pair<double, pair<int, int> > pPair;


	//Initialize grid of zeros.
	vector<vector<int>> grid_vector;
	grid_vector.resize(row);
	for (int i = 0; i < row; ++i)
	{

		grid_vector[i].resize(col);
		for (int j = 0; j < col; ++j)
			grid_vector[i][j] = 0;
	};
	//printf("-> (%d,%d)", grid_vector.size(),grid_vector[0].size());
	

	for (int z = 0; z < forbidden_vector.size(); ++z)
		grid_vector[forbidden_vector[z][0]][forbidden_vector[z][1]] = 1;

	// Source is the left-most bottom-most corner
	Pair start = make_pair(start_arr[0], start_arr[1]);
	// Destination is the left-most top-most corner
	Pair finish = make_pair(finish_arr[0], finish_arr[1]);

    // Declare an object of class geeks
    AStar AIObj;

    // accessing member function
	printf("Starting Search\n");
	string first_move;
	first_move = AIObj.aStarSearch(row, col, grid_vector, start, finish);

	return first_move;
}

int main()
{
	int col = 10;
	int row = 9;

	vector<int>  start = {8,8};
	vector<int>  finish = {0,0};

	
	vector<vector<int>> forbidden_vector
	{       { 5, 0 },
			{ 5, 1 },
			{ 5, 2 },
			{ 5, 3 },
			{ 5, 4 },
			{ 5, 6 },
			{ 5, 7 },
			{ 5, 8 } };
	
	//vector<vector<int>> forbidden_vector {{}};

	string the_move;

	the_move = launcher(row, col, forbidden_vector, start, finish);

	printf("-> (%s) ", the_move.c_str());
	return (0);
};