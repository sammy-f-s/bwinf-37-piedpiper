#pragma once

//Art der Verkabelung
enum WiringType
{
	Serial,
	Parallel,
	None
};

struct Resistor{
	float ohm;
	WiringType wtype;

	Resistor()
	{
		ohm = 0;
		wtype = None;
	}
	Resistor(float o, WiringType w){
		ohm = o;
		wtype = w;
	}
};