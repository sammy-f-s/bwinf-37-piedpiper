// Widerstände.cpp : Definiert den Einstiegspunkt für die Konsolenanwendung.
//

#include "stdafx.h"

#include "Resistor.h"

#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <tuple>

//Rendern
#include "SFML\System.hpp"
#include "SFML\Graphics.hpp"
#include "SFML\Window.hpp"

using namespace std;

//Funktionsprototypen
void drawCircuit(vector <Resistor> &used, sf::Font &font);
tuple <float, Resistor> closestSerialAdd(vector <float> &resistors, float desired, float current);
tuple <float, Resistor> closestParallelAdd(vector <float> &resistors, float desired, float current);
float parAdd(float a, float b);
float currentResistorValue(vector <Resistor> &used);
void drawRect(int x, int y, int w, int h, sf::RenderWindow &window);
void drawText(string text, int x, int y, sf::RenderWindow &window, sf::Font &font);
void drawLine(int x1, int y1, int x2, int y2, sf::RenderWindow &window);

int main()
{
	//Liste verfügbarer Widerstände
	vector <float> availResistors;
	//Liste der benutzten Widerstände
	vector <Resistor> usedResistors;

	//Laden einer Schriftart
	sf::Font font;
	font.loadFromFile("OpenSans.ttf");

	//Auslesen der Widerstände
	ifstream stream("widerstaende.txt");
	string line;

	if (stream.is_open())
	{
		while (std::getline(stream, line))
		{
			availResistors.push_back(stof(line));
		}
	}

	//k?
	int k;
	cout << "Gewuenschtes k?";
	cin >> k;
	//gewünschter Widerstand?
	float desiredRes;
	cout << "\nGewuenschter Widerstand?";
	cin >> desiredRes;
	
	for (int i = 0; i < k; i++)
	{
		float cRV = currentResistorValue(usedResistors);
		float diff = abs(desiredRes - cRV);
		if (diff < 1.0) { break; }

		//Übergabe Variablen
		float val;
		Resistor resistor_Serial;
		Resistor resistor_Parallel;

		//Serielle Annäherung
		tie(val, resistor_Serial) = closestSerialAdd(availResistors, desiredRes, cRV);
		float serialDiff = abs(val - desiredRes);
		if (serialDiff == cRV) { serialDiff == 100000; } //wenn kein kleinerer wert gefunden wird, ist val = 0, wodurch das übernächste "if" nicht anschlägt

		//Parallele Annäherung
		tie(val, resistor_Parallel) = closestParallelAdd(availResistors, desiredRes, cRV);
		float parallelDiff = abs(val - desiredRes);
		if (val == cRV) { parallelDiff == 100000; }

		if (diff < serialDiff && diff < parallelDiff)
		{
			//näher geht es nicht
			break;
		}
		else
		{
			if (serialDiff <= parallelDiff)
			{
				usedResistors.push_back(resistor_Serial);
				//Entfernen des benutzten Widerstands aus der Liste der verfügbaren
				availResistors.erase(std::remove(availResistors.begin(), availResistors.end(), resistor_Serial.ohm), availResistors.end());
			}
			else
			{
				usedResistors.push_back(resistor_Parallel);
				//Entfernen des benutzten Widerstands aus der Liste der verfügbaren
				availResistors.erase(std::remove(availResistors.begin(), availResistors.end(), resistor_Parallel.ohm), availResistors.end());
			}
		}
	}

	drawCircuit(usedResistors, font);

	system("PAUSE");
    return 0;
}

void drawCircuit(vector <Resistor> &used, sf::Font &font)
{
	sf::RenderWindow window(sf::VideoMode(800, 600), "Aufgabe 5");
	window.setFramerateLimit(1);

	//Hilfsvariablen zum Rendern
	int parallelen = 1;
	int len = 10;
	int ylen = 100;

	sf::Vector2i start = sf::Vector2i(50, 100);
	sf::Vector2i end = sf::Vector2i(50, 100);
	
	while (window.isOpen())
	{
		sf::Event event;
		if (window.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
			{
				window.close();
			}
		}
		window.clear();

		drawLine(0, 100, 50, 100, window);

		for (Resistor r : used)
		{
			if (r.wtype == Serial)
			{
				drawLine(end.x, end.y, end.x + len, end.y, window);

				drawRect(end.x + len, end.y - 20, 100, 40, window);
				drawText(to_string(r.ohm), end.x + len + 2.5, end.y, window, font);

				drawLine(end.x + 100 + len, end.y, end.x + 100 + len + len + 10 * parallelen, end.y, window);

				end.x += 100 + len + len;
			}
			else if (r.wtype == Parallel)
			{
				drawLine(start.x - 10 * parallelen, start.y, start.x - 10 * parallelen, start.y + ylen * parallelen, window);
				drawLine(start.x - 10 * parallelen, start.y + ylen * parallelen, start.x + len - 10 * parallelen, start.y + ylen * parallelen, window);

				drawRect(start.x + len - 10 * parallelen, start.y + ylen * parallelen - 20, 100, 40, window);
				drawText(to_string(r.ohm), start.x + len + 2.5 - 10 * parallelen, start.y + ylen * parallelen, window, font);

				drawLine(start.x + len + 100 - 10 * parallelen, start.y + ylen * parallelen, end.x + 10 * parallelen, end.y + ylen * parallelen, window);
				drawLine(end.x + 10 * parallelen, end.y + ylen * parallelen, end.x + 10 * parallelen, end.y, window);

				end.x += 10;

				parallelen++;
			}
		}

		drawLine(end.x, end.y, end.x + 50, end.y, window);
		drawText("Gesamtwiderstand = " + to_string(currentResistorValue(used)), 0, 0, window, font);

		//Rendervariablen zurücksetzen für nächsten Frame
		parallelen = 1;
		start = sf::Vector2i(50, 100);
		end = sf::Vector2i(50, 100);

		window.display();
	}
}

tuple<float, Resistor> closestSerialAdd(vector <float> &resistors, float desired, float current)
{
	float recordDiff = abs(desired - current);
	float recordResistorValue = 0.0;

	//Ermitteln des Widerstands, welcher als Parallel-Addition mit der vorhandenen Schaltung, am nächsten am gewünschten Wert liegt
	for (float f : resistors)
	{
		float newDiff = abs(desired - (current + f));
		if (newDiff < recordDiff)
		{
			recordDiff = newDiff;
			recordResistorValue = f;
		}
	}

	//Zurückgeben des erreichten Wertes (welcher am nächsten am gesuchten liegt), sowie dem dazugehörigen Widerstand als Tupel
	return tuple<float, Resistor>(current + recordResistorValue, Resistor(recordResistorValue, Serial));
}

tuple<float, Resistor> closestParallelAdd(vector <float> &resistors, float desired, float current)
{
	float recordDiff = abs(desired - current);
	float recordResistorValue = 0.0;

	//Ermitteln des Widerstands, welcher als Parallel-Addition mit der vorhandenen Schaltung, am nächsten am gewünschten Wert liegt
	for (float f : resistors)
	{
		float newDiff = abs(desired - parAdd(current, f));
		if (newDiff < recordDiff)
		{
			recordDiff = newDiff;
			recordResistorValue = f;
		}
	}

	//Zurückgeben des erreichten Wertes (welcher am nächsten am gesuchten liegt), sowie dem dazugehörigen Widerstand als Tupel
	return tuple<float, Resistor>(parAdd(current, recordResistorValue), Resistor(recordResistorValue, Parallel));
}

float parAdd(float a, float b)
{
	return (1 / ((1 / a) + (1 / b)));
}

float currentResistorValue(vector <Resistor> &used)
{
	float sum = 0;
	for (int i = 0; i < used.size(); i++)
	{
		if (used[i].wtype == Serial)
		{
			sum += used[i].ohm;
		}
		else if (used[i].wtype == Parallel)
		{
			sum = parAdd(sum, used[i].ohm);
		}
	}

	return sum;
}

void drawRect(int x, int y, int w, int h, sf::RenderWindow &window)
{
	sf::RectangleShape r;
	r.setOutlineColor(sf::Color::White);
	r.setOutlineThickness(1);
	r.setFillColor(sf::Color::Transparent);
	r.setPosition(x, y);
	r.setSize(sf::Vector2f(w, h));
	window.draw(r);
}

void drawText(string text, int x, int y, sf::RenderWindow &window, sf::Font &font)
{
	sf::Text t;
	t.setPosition(x, y);
	t.setFont(font);
	t.setString(text);
	t.setCharacterSize(15);
	window.draw(t);
}

void drawLine(int x1, int y1, int x2, int y2, sf::RenderWindow &window)
{
	sf::VertexArray line(sf::Lines, 2);
	line[0] = sf::Vector2f(x1, y1);
	line[1] = sf::Vector2f(x2, y2);
	window.draw(line);
}