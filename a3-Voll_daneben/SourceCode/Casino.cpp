// Casino.cpp : Definiert den Einstiegspunkt für die Konsolenanwendung.
//

#include "stdafx.h"

#include <vector>
#include <fstream>
#include <iostream>
#include <string>
#include <algorithm> //std::sort

using namespace std;

float averageInRange(vector <int> &entries, int low, int high);
int getClosest(int a, vector <int> &picks);
float toPay(vector <int> &entries, vector <int> &picks);

int main()
{
	//Zahlen der Teilnehmer
	vector <int> entries;
	vector <int> picks;

	int nr;
	cout << "Beispiel Nr.?" << endl;
	cin >> nr;
	cout << "-----------------" << endl;

	ifstream stream("beispiel" + to_string(nr) + ".txt");
	string line;

	if (stream.is_open())
	{
		while (getline(stream, line))
		{
			entries.push_back(stoi(line));
		}
	}

	cout << "Anfangseinnahmen: " << entries.size() * 25 << endl << endl;

	sort(entries.begin(), entries.end());

	cout << "Al Capones Wahl: " << endl;
	for (int i = 0; i < 10; i++)
	{
		//Unterteilung von 1000 in 10 gleichgroße Bereiche, mit dem Marker in der Mitte
		//Start des Markers in der Mitte seines Bereiches
		int marker = i * 100 + 50;

		//Um möglichst dicht an möglichst vielen Leuten zu liegen wird die durchschnittlich gewählte Zahl in diesem Bereich errechnet
		float avInRange = averageInRange(entries, marker - 50, marker + 50);
		cout << (int)avInRange << ", ";

		picks.push_back((int)avInRange);
	}

	cout << endl << endl;
	cout << "Auszuzahlen: " << toPay(entries, picks) << endl;

	system("PAUSE");
    return 0;
}

float toPay(vector <int> &entries, vector <int> &picks)
{
	int sum = 0;
	for (int bet : entries)
	{
		int closest = getClosest(bet, picks);

		int diff = abs(closest - bet);

		sum += diff;
	}
	return sum;
}

int getClosest(int a, vector <int> &picks)
{
	float recdiff = 100000;
	float closestPick = 0;

	for (int pick : picks)
	{
		float newDiff = abs(pick - a);
		if (newDiff < recdiff)
		{
			recdiff = newDiff;
			closestPick = pick;
		}
	}
	return closestPick;
}

float averageInRange(vector <int> &entries, int low, int high)
{
	float av = 0;
	int amount = 0;
	for (int i : entries)
	{
		if (i >= low && i < high)
		{
			av += i;
			amount++;
		}
	}
	return(av / (float)amount);
}