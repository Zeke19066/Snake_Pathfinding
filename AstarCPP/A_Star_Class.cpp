#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <math.h>       /* sqrt */
#include <stack>
#include <cstring>
#include <cfloat>
#include <set>
#include <iostream>
#include <vector>
#include <string>
using namespace std;
// A C++ Program to implement A* Search Algorithm

class AStar {
private:
	// Creating a shortcut for int, int pair type
	typedef pair<int, int> Pair;

	// Creating a shortcut for pair<int, pair<int, int>> type
	typedef pair<double, pair<int, int> > pPair;

	// A structure to hold the necessary parameters
	struct cell {
		// Row and Column index of its parent
		// Note that 0 <= i <= ROW-1 & 0 <= j <= COL-1
		int parent_i, parent_j;
		// f = g + h
		double f, g, h;
	};

	// A Utility Function to check whether given cell (row, col)
	// is a valid cell or not.
	bool isValid(int row, int col, int master_row, int master_col)
	{
		// Returns true if row number and column number
		// is in range
		return (row >= 0) && (row < master_row) && (col >= 0)
			&& (col < master_col);
	}

	// A Utility Function to check whether the given cell is
	// blocked or not
	bool isUnBlocked(vector<vector<int>> forbidden_grid, int row, int col)
	{
		if (forbidden_grid[row][col] == 1)
			return (false);
		else
			return (true);
	}

	// A Utility Function to check whether destination cell has
	// been reached or not
	bool isDestination(int row, int col, Pair finish)
	{
		if (row == finish.first && col == finish.second)
			return (true);
		else
			return (false);
	}

	// A Utility Function to calculate the 'h' heuristics.
	double calculateHValue(int row, int col, Pair finish)
	{
		// Return using the distance formula
		return ((double)sqrt(
			(row - finish.first) * (row - finish.first)
			+ (col - finish.second) * (col - finish.second)));
	}


	// A Utility Function to trace the path from the source
	// to destination
	string tracePath(vector<vector<cell>> cellDetails, Pair finish)
	{

		int row = finish.first;
		int col = finish.second;
		string move;

		stack<Pair> Path;

		while (!(cellDetails[row][col].parent_i == row
				&& cellDetails[row][col].parent_j == col)) {
			Path.push(make_pair(row, col));
			int temp_row = cellDetails[row][col].parent_i;
			int temp_col = cellDetails[row][col].parent_j;
			row = temp_row;
			col = temp_col;
		}

		/* For the complete path
		Path.push(make_pair(row, col));
		while (!Path.empty()) {
			pair<int, int> p = Path.top();
			Path.pop();
			printf("-> (%d,%d) ", p.first, p.second);
		}*/
		Path.push(make_pair(row, col));

		pair<int, int> start_coord = Path.top();
		Path.pop();

		pair<int, int> move_coord = Path.top();
		Path.pop();

		if (start_coord.second != move_coord.second) //+left/-right
			{
			int delta = start_coord.second - move_coord.second; //+left/-right
			if (delta > 0)
				{move = "Left";}
			else if (delta < 0)
				{move = "Right";}
			}

		else if (start_coord.first != move_coord.first) //+up/-down
			{
			int delta = start_coord.first - move_coord.first; //+up/-down
			if (delta > 0)
				{move = "Up";}
			else if (delta < 0)
				{move = "Down";}
			}

		return move;
	}

	// A Function to find the shortest path between
	// a given source cell to a destination cell according
	// to A* Search Algorithm
public:
	string aStarSearch(int master_row, int master_col, vector<vector<int>> forbidden_grid, Pair start, Pair finish)
	{
		string move;
		int longest_length;
		vector<vector<cell>> longest_cell;
		longest_cell.resize(master_row);
		for (int i = 0; i < master_row; ++i)
			longest_cell[i].resize(master_col);

		// If the source is out of range
		if (isValid(start.first, start.second, master_row, master_col) == false) {
			move = "Source is invalid";
			return move;
		}

		// If the destination is out of range
		if (isValid(finish.first, finish.second, master_row, master_col) == false) {
			move = "Destination is invalid";
			return move;
		}

		// Either the source or the destination is blocked
		if (isUnBlocked(forbidden_grid, start.first, start.second) == false
			|| isUnBlocked(forbidden_grid, finish.first, finish.second)
				== false) {
			move = "Source or the destination is blocked";
			return move;
		}

		// If the destination cell is the same as source cell
		if (isDestination(start.first, start.second, finish)
			== true) {
			move = "We are already at the destination";
			return move;
		}

		// Create a closed list and initialise it to false which
		// means that no cell has been included yet This closed
		// list is implemented as a boolean 2D array
		vector<vector<bool>> closedList;
		closedList.resize(master_row);
		for (int i = 0; i < master_row; ++i)
			closedList[i].resize(master_col);

		//bool closedList[master_row][master_col];
		//memset(closedList, false, sizeof(closedList));

		// Declare a 2D vector with the cells as data,
		// then resize to appropriate proportions.

		vector<vector<cell>> cellDetails;
		cellDetails.resize(master_row);
		for (int i = 0; i < master_row; ++i)
			cellDetails[i].resize(master_col);

		//cell cellDetails[master_row][master_col];

		int i, j;

		for (i = 0; i < master_row; i++) {
			for (j = 0; j < master_col; j++) {
				cellDetails[i][j].f = FLT_MAX;
				cellDetails[i][j].g = FLT_MAX;
				cellDetails[i][j].h = FLT_MAX;
				cellDetails[i][j].parent_i = -1;
				cellDetails[i][j].parent_j = -1;
			}
		}

		// Initialising the parameters of the starting node
		i = start.first, j = start.second;
		cellDetails[i][j].f = 0.0;
		cellDetails[i][j].g = 0.0;
		cellDetails[i][j].h = 0.0;
		cellDetails[i][j].parent_i = i;
		cellDetails[i][j].parent_j = j;

		/*
		Create an open list having information as-
		<f, <i, j>>
		where f = g + h,
		and i, j are the row and column index of that cell
		Note that 0 <= i <= ROW-1 & 0 <= j <= COL-1
		This open list is implemented as a set of pair of
		pair.*/
		set<pPair> openList;

		// Put the starting cell on the open list and set its
		// 'f' as 0
		openList.insert(make_pair(0.0, make_pair(i, j)));

		// We set this boolean value as false as initially
		// the destination is not reached.
		bool foundDest = false;

		while (!openList.empty()) {
			pPair p = *openList.begin();

			// Remove this vertex from the open list
			openList.erase(openList.begin());

			// Add this vertex to the closed list
			i = p.second.first;
			j = p.second.second;
			closedList[i][j] = true;

			/*
			Generating all the 8 successor of this cell

				N.W N N.E
				\ | /
					\ | /
				W----Cell----E
					/ | \
					/ | \
				S.W S S.E

			Cell-->Popped Cell (i, j)
			N --> North	 (i-1, j)
			S --> South	 (i+1, j)
			E --> East	 (i, j+1)
			W --> West	(i, j-1)
			*/

			// To store the 'g', 'h' and 'f' of the 8 successors
			double gNew, hNew, fNew;


			longest_length++;


			//----------- 1st Successor (North) ------------

			// Only process this cell if this is a valid one
			if (isValid(i - 1, j, master_row, master_col) == true) {
				// If the destination cell is the same as the
				// current successor
				if (isDestination(i - 1, j, finish) == true) {
					// Set the Parent of the destination cell
					cellDetails[i - 1][j].parent_i = i;
					cellDetails[i - 1][j].parent_j = j;
					move = tracePath(cellDetails, finish);
					foundDest = true;
					return move;
				}
				// If the successor is already on the closed
				// list or if it is blocked, then ignore it.
				// Else do the following
				else if (closedList[i - 1][j] == false
						&& isUnBlocked(forbidden_grid, i - 1, j)
								== true) {
					gNew = cellDetails[i][j].g + 1.0;
					hNew = calculateHValue(i - 1, j, finish);
					fNew = gNew + hNew;

					// If it isn???t on the open list, add it to
					// the open list. Make the current square
					// the parent of this square. Record the
					// f, g, and h costs of the square cell
					//			 OR
					// If it is on the open list already, check
					// to see if this path to that square is
					// better, using 'f' cost as the measure.
					if (cellDetails[i - 1][j].f == FLT_MAX
						|| cellDetails[i - 1][j].f > fNew) {
						openList.insert(make_pair(
							fNew, make_pair(i - 1, j)));

						// Update the details of this cell
						cellDetails[i - 1][j].f = fNew;
						cellDetails[i - 1][j].g = gNew;
						cellDetails[i - 1][j].h = hNew;
						cellDetails[i - 1][j].parent_i = i;
						cellDetails[i - 1][j].parent_j = j;
					}
				}
			}

			//----------- 2nd Successor (South) ------------

			// Only process this cell if this is a valid one
			if (isValid(i + 1, j, master_row, master_col) == true) {
				// If the destination cell is the same as the
				// current successor
				if (isDestination(i + 1, j, finish) == true) {
					// Set the Parent of the destination cell
					cellDetails[i + 1][j].parent_i = i;
					cellDetails[i + 1][j].parent_j = j;
					move = tracePath(cellDetails, finish);
					foundDest = true;
					return move;
				}
				// If the successor is already on the closed
				// list or if it is blocked, then ignore it.
				// Else do the following
				else if (closedList[i + 1][j] == false
						&& isUnBlocked(forbidden_grid, i + 1, j)
								== true) {
					gNew = cellDetails[i][j].g + 1.0;
					hNew = calculateHValue(i + 1, j, finish);
					fNew = gNew + hNew;

					// If it isn???t on the open list, add it to
					// the open list. Make the current square
					// the parent of this square. Record the
					// f, g, and h costs of the square cell
					//			 OR
					// If it is on the open list already, check
					// to see if this path to that square is
					// better, using 'f' cost as the measure.
					if (cellDetails[i + 1][j].f == FLT_MAX
						|| cellDetails[i + 1][j].f > fNew) {
						openList.insert(make_pair(
							fNew, make_pair(i + 1, j)));
						// Update the details of this cell
						cellDetails[i + 1][j].f = fNew;
						cellDetails[i + 1][j].g = gNew;
						cellDetails[i + 1][j].h = hNew;
						cellDetails[i + 1][j].parent_i = i;
						cellDetails[i + 1][j].parent_j = j;
					}
				}
			}

			//----------- 3rd Successor (East) ------------

			// Only process this cell if this is a valid one
			if (isValid(i, j + 1, master_row, master_col) == true) {
				// If the destination cell is the same as the
				// current successor
				if (isDestination(i, j + 1, finish) == true) {
					// Set the Parent of the destination cell
					cellDetails[i][j + 1].parent_i = i;
					cellDetails[i][j + 1].parent_j = j;
					move = tracePath(cellDetails, finish);
					foundDest = true;
					return move;
				}

				// If the successor is already on the closed
				// list or if it is blocked, then ignore it.
				// Else do the following
				else if (closedList[i][j + 1] == false
						&& isUnBlocked(forbidden_grid, i, j + 1)
								== true) {
					gNew = cellDetails[i][j].g + 1.0;
					hNew = calculateHValue(i, j + 1, finish);
					fNew = gNew + hNew;

					// If it isn???t on the open list, add it to
					// the open list. Make the current square
					// the parent of this square. Record the
					// f, g, and h costs of the square cell
					//			 OR
					// If it is on the open list already, check
					// to see if this path to that square is
					// better, using 'f' cost as the measure.
					if (cellDetails[i][j + 1].f == FLT_MAX
						|| cellDetails[i][j + 1].f > fNew) {
						openList.insert(make_pair(
							fNew, make_pair(i, j + 1)));

						// Update the details of this cell
						cellDetails[i][j + 1].f = fNew;
						cellDetails[i][j + 1].g = gNew;
						cellDetails[i][j + 1].h = hNew;
						cellDetails[i][j + 1].parent_i = i;
						cellDetails[i][j + 1].parent_j = j;
					}
				}
			}

			//----------- 4th Successor (West) ------------

			// Only process this cell if this is a valid one
			if (isValid(i, j - 1, master_row, master_col) == true) {
				// If the destination cell is the same as the
				// current successor
				if (isDestination(i, j - 1, finish) == true) {
					// Set the Parent of the destination cell
					cellDetails[i][j - 1].parent_i = i;
					cellDetails[i][j - 1].parent_j = j;
					move = tracePath(cellDetails, finish);
					foundDest = true;
					return move;
				}

				// If the successor is already on the closed
				// list or if it is blocked, then ignore it.
				// Else do the following
				else if (closedList[i][j - 1] == false
						&& isUnBlocked(forbidden_grid, i, j - 1)
								== true) {
					gNew = cellDetails[i][j].g + 1.0;
					hNew = calculateHValue(i, j - 1, finish);
					fNew = gNew + hNew;

					// If it isn???t on the open list, add it to
					// the open list. Make the current square
					// the parent of this square. Record the
					// f, g, and h costs of the square cell
					//			 OR
					// If it is on the open list already, check
					// to see if this path to that square is
					// better, using 'f' cost as the measure.
					if (cellDetails[i][j - 1].f == FLT_MAX
						|| cellDetails[i][j - 1].f > fNew) {
						openList.insert(make_pair(
							fNew, make_pair(i, j - 1)));

						// Update the details of this cell
						cellDetails[i][j - 1].f = fNew;
						cellDetails[i][j - 1].g = gNew;
						cellDetails[i][j - 1].h = hNew;
						cellDetails[i][j - 1].parent_i = i;
						cellDetails[i][j - 1].parent_j = j;
					}
				}
			}

		}

		// When the destination cell is not found and the open
		// list is empty, then we conclude that we failed to
		// reach the destination cell. This may happen when the
		// there is no way to destination cell (due to
		// blockages)
		if (foundDest == false)
			move = "Failed to find the Destination Cell";

		return move;
	}
};
