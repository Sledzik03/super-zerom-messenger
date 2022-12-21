#include <iostream>
#include <string>
#include <math.h>
using namespace std;

int b,c;
int a = 11;
string tekst;
int delta;
int ret_data;

void szyfr(int a, int b, int c);
void deszyfr(int a, int b, int c);

int main()
{
    getline(cin,tekst);
    c = tekst.length();
    cout << c << endl;
    szyfr(a,b,c);
}
void szyfr(int a, int b, int c)
{
    for (int i=0;i<tekst.length();i++)
    {
        b = int(tekst[i]);
        delta = pow(b,2) - (4*a*c);
        ret_data = sqrt(delta+4 * a *c);
        cout << delta << endl;
    }
}
