#include <bits/stdc++.h>

using namespace std;

bool On;
int x, y, z;
char _x, _y, _z;

char Pos(int x){
	return char(x + 'A');
}

bool Monk_mov(int &x, int y, int z, bool On, int tag){
	if(tag > 2 || tag < 0){printf("Monkey can't move to %c\n", Pos(tag)); return 0;}
	if(tag == x){printf("Monkey has already at %c\n", Pos(tag)); return 0;}
	if(On){printf("Get Down plz"); return 0;}

	printf("Monkey moves from %c to %c\n", Pos(x), Pos(tag));
	x = tag;
	return 1;
}

bool Push(int &x, int y, int &z, bool On, int tag){
	if(x != z){printf("Box != Monkey\n"); return 0;}
	if(On){printf("Get Down plz"); return 0;}
	
	printf("Monkey pushes Box from %c to %c\n", Pos(x), Pos(tag));
	x = tag, z = tag;
	return 1;
}

bool Climb(int x, int y, int z, bool &On){
	if(x != z){printf("Monkey should move to box first\n");return 0;}
	On = 1;
	printf("Monkey climbs the box at %c\n", Pos(x));
	return 1;
}

bool Grasp(int x, int y, int z, bool On){
	if(On && x == y && x == z){printf("Get the banana at %c!\n", Pos(x)); return 1;}
	return 0;
}

int main(){
	cin>>_x>>_y>>_z;
	x = _x - 'A', y = _y - 'A', z = _z - 'A';
	int way_Box = z - x, way_Ban = y - z;
	if(way_Box)if(!Monk_mov(x, y, z, On, z))return printf("ERR_Monk_mov\n"), 0;
	if(way_Ban)if(!Push(x, y, z, On, y))return printf("ERR_Push\n"), 0;
	if(!Climb(x, y, z, On))return printf("ERR_Climb\n"), 0;
	if(!Grasp(x, y, z, On))return printf("ERR_Grasp\n"), 0;
	return 0;
}
