#include <map>
#include <set>
#include <list>
#include <cmath>
#include <ctime>
#include <deque>
#include <queue>
#include <stack>
#include <string>
#include <bitset>
#include <cstdio>
#include <limits>
#include <vector>
#include <climits>
#include <cstring>
#include <cstdlib>
#include <fstream>
#include <numeric>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <unordered_map>

using namespace std;


int main(){
    int t;
    cin >> t;
    for(int a0 = 0; a0 < t; a0++){
        int n;
        cin >> n;
        long num_of_three = int((n-1)/3);
        long num_of_five = int((n-1)/5);
        long num_of_common = int((n-1)/15);
        
        long a = num_of_three, b = num_of_five, c = num_of_common;
        
        long long sum = ((a*(a+1)*3) + (b*(b+1)*5) - (c*(c+1)*15));
        sum = sum >> 1;
        cout << sum << endl;
    }
    return 0;
}
