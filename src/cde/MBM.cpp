#include "..\lib\Image.h"
#include "..\lib\Object.h"
#include <bits/stdc++.h>
using namespace std;

typedef pair <int, int> ii;
typedef tuple <int, int, int> iii;
typedef vector <ii> vii;
typedef set <iii> siii;
typedef vector <vii> vvii;
typedef vector <int> vi;
typedef vector <vi> vvi;
typedef vector <vvi> vvvi;

#define INF  1e9
#define endl '\n'

vector <vector <double>> G;
double mc = INF;
vi mM;

void rec(vi &M, vi &V, int p, double c){
    if((unsigned int) p == M.size()){
        if(mc > c){
            mc = c;
            mM = M;
        }
        return;
    }
    for(int i=0; (unsigned int) i<M.size(); i++){
        if(V[i] == 0){
            V[i] = 1;
            M[p] = i;
            
            rec(M, V, p+1, c + G[p][i]);

            V[i] = 0;
            M[p] = -1;
        }
    }
}

int lim = 240;

void sweep(Image &I, vector<Object> &O){
    for(int i = 1; i+1 < I.W; i++){
        for(int j = 1; j+1 < I.H; j++){
            int s = 0;
            s += I.pix[i-1][j-1];
            s += I.pix[ i ][j-1];
            s += I.pix[i+1][j-1];

            s += I.pix[i-1][ j ];
            s += I.pix[ i ][ j ];
            s += I.pix[i+1][ j ];

            s += I.pix[i-1][j+1];
            s += I.pix[ i ][j+1];
            s += I.pix[i+1][j+1];

            s /= 9;

            if(s > lim and I.pix[i][j] > lim and I.pixSeen[i][j] == 0){
                O.push_back(Object(1));
                I.DFSFill(i, j, O[O.size()-1].inObj[0], O[O.size()-1].exObj[0]);
            }
        }
        for(auto &x : O) x.findCenter(0);
        for(auto &x : O) x.findLum(0);
    }    
}

void tagObjectsHungarian(){
	int ni, W, H;
	cin >> ni >> W >> H;

    vector <Image> IM(ni, Image(W, H, lim));    
    for(auto &x : IM) x.inputImage();

    vector <vector <Object>> oIM(ni);

	for(int i=0; i<ni; i++) sweep(IM[i], oIM[i]);
    
    int ms = 0;
	for(auto x : oIM) ms = max(ms, (int) x.size());
	for(auto &x : oIM){
		while(x.size() < (unsigned int) ms){
		    x.push_back(Object(1));
		   	x[x.size()-1].center[0] = {INF, INF};
		}
    }

    int no = ms;

    for(int k = ni-2; k >= 0; k--){
    	//Objects to Graph
	    G = vector <vector <double>> (no, vector<double> (no));
	    
	    for(int i=0; (unsigned int) i<G.size(); i++){
	        for(int j=0; (unsigned int) j<G[i].size(); j++){
	        	G[i][j] = hypot(oIM[k][i].center[0].first  - oIM[k+1][j].center[0].first,
	        					oIM[k][i].center[0].second - oIM[k+1][j].center[0].second);
	        }
	    }
	    
	    /*
			Hungarian Implementation
	    */


	    /*
	    	Backtracking Implementation
		*/
	    
	    vi M(no, -1); vi V(no, 0);
	    mc = INF;
  		if(no > 10){
  			// Backtrack should only be used to debug
  			cout << "TOO MANY OBJECTS" << endl;
  		}
  		else rec(M, V, 0, 0);


  		// Graph back to objects & proper re-taging
	    for(int i=0; (unsigned int) i<mM.size(); i++){
	    	oIM[k][i].append(oIM[k+1][mM[i]]);
		}
	}
	// O contains all the objects during the images
    vector <Object> O = oIM[0];
    for(auto &x : O){
		x.findSpeedDecl();
		cerr << x.speed << " " << x.decl << endl;
    }
}

int main(){
	tagObjectsHungarian();
}
