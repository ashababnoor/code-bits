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

bool isPrime(long n){
    if (n < 2) return false;
    else if (n == 2) return true;
    else if(n%2 == 0) return false;     
    else {
        long upperlimit = (int)sqrt(n) + 1;
        // cout << "Upperlimit on checking prime " << upperlimit << endl;
        for(long i=3; i<=upperlimit; i=i+2){
            if (n % i == 0){
               return false; 
            }
        }
        return true;
    }
}

int main(){
    int t;
    cin >> t;
    for(int a0 = 0; a0 < t; a0++){
        long n;
        cin >> n;
        if (isPrime(n)){
            cout << n << endl;
        }
        else {
            long upperlimit = n >> 1;
            for(long i=upperlimit; i > 2; i--){
                if (n%i == 0 && isPrime(i)) {
                    cout << i << endl;
                    break;
                }
            }
        }
    }
    return 0;
}


#include <iostream>
using namespace std;

bool isPrime(long n){
    if (n < 2) return false;
    else if (n == 2 || n == 3) return true;
    else{
        long upper = n+1;
        long lower = n-1;
        if(upper%6 == 0 || lower%6 == 0)
            return true;
    }
    return false;
}

int main() {
	// your code goes here
	int t;
	cin >> t;
	for(int i=0; i<t; i++){
	    long n;
	    cin >> n;
	    if (isPrime(n))
	        cout << "yes" << endl;
	    else
	        cout << "no" << endl;
	}
	return 0;
}
