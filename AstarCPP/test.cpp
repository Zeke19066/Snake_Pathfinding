#include <iostream>
#include <vector>

using namespace std;

int main(void) {
   vector<int> v;

   cout << "Initial vector size = " << v.size() << endl;

   v.resize(5);
   cout << "Vector size after resize = " << v.size() << endl;

   cout << "Vector contains following elements" << endl;
   for (int i = 0; i < v.size(); ++i)
      cout << v[i] << endl;

   return 0;
}