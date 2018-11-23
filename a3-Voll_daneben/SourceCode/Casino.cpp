// Casino.cpp : Definiert den Einstiegspunkt f�r die Konsolenanwendung.
//

#define PBSTR "============================================================"
#define PBWIDTH 40

#include "stdafx.h"

#include <vector>
#include <fstream>
#include <iostream>
#include <string>
#include <algorithm> //std::sort
#include <time.h> //time(NULL)

using namespace std;

float averageInRange(vector <int> &entries, int low, int high);
float evaluate(vector <int> &entries);
void printProgress(double percentage);
void fillRandomly(vector <int> &vec);
int getClosest(int a, vector <int> &picks);
float toPay(vector <int> &entries, vector <int> &picks);

int main()
{
	//Zahlen der Teilnehmer
	vector <int> entries;
    //Al Capones Zahlen
	vector <int> picks;

    //Zufall initialisieren
	srand(time(NULL));

    //Nummer der Beispieldatei
	int nr;
	cout << "Beispiel Nr.?" << "    (0 f�r zuf�llige Zahlen)" << endl;
	cin >> nr;
	cout << "-----------------" << endl;
    
    //Null um beliebige Anzahl zufälliger Spiele zu machen
	if (nr != 0)
	{
		ifstream stream("beispiel" + to_string(nr) + ".txt");
		string line;

		if (stream.is_open())
		{
			while (getline(stream, line))
			{
				entries.push_back(stoi(line));
			}
		}
		else
		{
			cerr << "File not found" << endl;
			system("PAUSE");
			return 0;
		}

		cout << "Anfangseinnahmen: " << entries.size() * 25 << endl << endl;

		cout << "Al Capones Wahl: " << endl;
		for (int i = 0; i < 10; i++)
		{
			//Unterteilung von 1000 in 10 gleichgro�e Bereiche, mit dem Marker in der Mitte
			//Start des Markers in der Mitte seines Bereiches
			int marker = i * 100 + 50;

			//Um m�glichst dicht an m�glichst vielen Leuten zu liegen wird die durchschnittlich gew�hlte Zahl in diesem Bereich errechnet
			float avInRange = averageInRange(entries, marker - 50, marker + 50);
			cout << (int)avInRange << ", ";

			picks.push_back((int)avInRange);
		}

		cout << endl << endl;
		cout << "Auszuzahlen: " << toPay(entries, picks) << endl;
	}
	else
	{
		cout << "Durchl�ufe?" << endl;
		int iterations;
		cin >> iterations;

		float dGewinn = 0;
		for (int i = 0; i < iterations; i++)
		{
			printProgress((float)i / (float)iterations);
			entries.clear();
			fillRandomly(entries);
			float einzelGewinn = evaluate(entries);
			//cout << einzelGewinn << endl;
			dGewinn += einzelGewinn;
		}

		dGewinn /= iterations;

		cout << endl << "Durchschnittlicher Gewinn: " << dGewinn << endl;
	}

	system("PAUSE");
	return 0;
}

void printProgress(double p)
{
	int val = (int)(p * 100);
	int left = (int)(p * PBWIDTH);
	int right = PBWIDTH - left;
	printf("\r%3d%% [%.*s%*s]", val, left, PBSTR, right, "");
	fflush(stdout);
}

void fillRandomly(vector <int> &vec)
{
	for (int i = 0; i < 100; i++)
	{
		vec.push_back(rand() % 1000 + 1);
	}
}

//zur Quantifizierun (bilden des durchschnittlichen Gewinns)
float evaluate(vector <int> &entries)
{
	vector <int> picks;
	
	float anfangsEinnahmen = entries.size() * 25;

	for (int i = 0; i < 10; i++)
	{
		//Unterteilung von 1000 in 10 gleichgro�e Bereiche, mit dem Marker in der Mitte
		//Start des Markers in der Mitte seines Bereiches
		int marker = i * 100 + 50;

		//Um m�glichst dicht an m�glichst vielen Leuten zu liegen wird die durchschnittlich gew�hlte Zahl in diesem Bereich errechnet
		float avInRange = averageInRange(entries, marker - 50, marker + 50);

		picks.push_back((int)avInRange);
	}

	float zuZahlen = toPay(entries, picks);
	float gewinn = anfangsEinnahmen - zuZahlen;

	return gewinn;
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