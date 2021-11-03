#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <iostream>

// A C++ Program to implement A* Search Algorithm
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
	
	for (int z = 0; z < forbidden_vector.size(); ++z)
		grid_vector[forbidden_vector[z][0]][forbidden_vector[z][1]] = 1;

	// Source is the left-most bottom-most corner
	Pair start = make_pair(start_arr[0], start_arr[1]);
	// Destination is the left-most top-most corner
	Pair finish = make_pair(finish_arr[0], finish_arr[1]);

    // Declare an object of class geeks
    AStar AIObj;

    // accessing member function
	string first_move;
	first_move = AIObj.aStarSearch(row, col, grid_vector, start, finish);

	return first_move;
}

struct MyData
{
    float x, y;

    MyData() : x(0), y(0)
    {
    }

    MyData(float x, float y) : x(x), y(y)
    {
    }

    void print()
    {
        printf("%f, %f\n", x, y);
    }
};

PYBIND11_MODULE (pybind11module, module)
{   // optional module docstring
    module.doc () = "Astar";
    // define add function
    module.def("launcher", &launcher, "launcher");


    pybind11::class_<MyData>(module, "MyData")
        .def(pybind11::init<>())
        .def(pybind11::init<float, float>(), "constructor 2", pybind11::arg("x"), pybind11::arg("y"))
        .def("print", &MyData::print)
        .def_readwrite("x", &MyData::x)
        .def_readwrite("y", &MyData::y)
    ;
}