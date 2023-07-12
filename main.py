import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as use case, company name, contact details, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "mail_reply": {
                    "type": "string",
                    "description": "You work at Uponor Sales department, your name is Eva Anderson. write a friendly mail response. Get the mane of the person that sent the response and use that name, Your answer should be very friendly and include the cost of the requested items"
                },                        
                "cost": {
                    "type": "number",
                    "description": "The total cost of the items that were requested"
                },
                 "companyName": {
                    "type": "string",
                    "description": "the name of the company from which the mail was sent to, the company requesting the sales or service"
                }
            },
            "required": ["companyName", "cost", "mail_reply"]
        }
    }
]

class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key information from this email and prepare an answer: {content} "
    #system_message="prices: \n AquaPEX Pex pipe 1/2\": 1 usd/ft \n  AquaPEX Pex pipe 3/4\" : 1.3 usd/ft \n AquaPEX Pex pipe 3\" : 2 usd/ft \n Fitting 1/2\" : 2 usd/ft \n Fitting 3/4\" : 3 usd/ft \n Fitting 1\" : 4 usd/ft \n"
    system_message="""
Part Description;Price;Pkg.Qty.
H-Insulation Kit, 5.5\", 6.9\", 7.9\";2150;1
Reducer Bushing 5.5\" to 2.7\";90,1;1
Compression Wall Seal for 2.7\" Jacket;505;1
Compression Wall Seal for 5.5\" Jacket;595;1
Compression Wall Seal for 6.9\" Jacket;715;1
Compression Wall Seal for 7.9\" Jacket;760;1
Twin End Cap, 1\", 1¼\", 1½\" PEX Pipe with 5.5\" Jacket (25mm, 32mm and 40mm);140;1
Wall Sleeve with Heat Shrink for 2.7\" Jacket;160;1
Wall Sleeve with Heat Shrink for 6.9\" and 7.9\" Jackets;396;1
Wall Sleeve with Heat Shrink for 5.5\" Jacket;354;1
Uponor Shrinkable Tape 9\" x 9' roll;239;1
Vault Shrink Sleeve for 5.5\" Jacket;135;1
Vault Shrink Sleeve for 7.9\" Jacket;160;1
Tee Insulation Kit, 5.5\", 6.9\", 7.9\";1390;1
Elbow Insulation Kit, 5.5\", 6.9\", 7.9\";1210;1
Straight Insulation Kit, 5.5\", 6.9\", 7.9\";1180;1
1\" Thermal Single with 2.7\" Jacket, 1,000-ft. coil;12,33;1
¾\" Thermal Single with 2.7\" Jacket, 1,000-ft. coil;10,97;1
1\" Thermal Single with 5.5\" Jacket, 600-ft. coil;37,72;1
1¼\" Thermal Single with 5.5\" Jacket, 500-ft. coil;43,79;1
1½\" Thermal Single with 6.9\" Jacket, 300-ft. coil;59,15;1
2\" Thermal Single with 6.9\" Jacket, 300-ft. coil;67,61;1
2½\" Thermal Single with 6.9\" Jacket, 300-ft. coil;76,81;1
3\" Thermal Single with 7.9\" Jacket, 300-ft. coil;99,59;1
4\" Thermal Single with 7.9\" Jacket, 300-ft. coil;127,49;1
1¼\" Thermal Twin Jr. with 5.5\" Jacket, 600-ft. coil;29,26;1
1\" Thermal Twin with 6.9\" Jacket, 600-ft. coil;52,56;1
1¼\" Thermal Twin with 6.9\" Jacket, 500-ft. coil;57,68;1
1½\" Thermal Twin with 6.9\" Jacket, 300-ft. coil;73,67;1
2\" Thermal Twin with 7.9\" Jacket, 300-ft. coil;106,59;1
2½\" Thermal Twin with 7.9\" Jacket, 300-ft. coil;134,81;1
1\" Potable PEX with 2.7\" Jacket, 1,000-ft. coil;12,33;1
¾\" Potable PEX with 2.7\" Jacket, 1,000-ft. coil;10,97;1
1\" Potable PEX with 5.5\" Jacket, 600-ft. coil;37,72;1
1¼\" Potable PEX with 5.5\" Jacket, 500-ft. coil;43,79;1
1½\" Potable PEX with 6.9\" Jacket, 300-ft. coil;59,04;1
2\" Potable PEX with 6.9\" Jacket, 300-ft. coil;65,73;1
3\" Potable PEX with 7.9\" Jacket, 300-ft. coil;99,59;1
1\" Potable PEX Twin with 6.9\" Jacket, 600-ft. coil;52,56;1
1¼\" Potable PEX Twin with 6.9\" Jacket, 500-ft. coil;57,68;1
1½\" Potable PEX Twin with 6.9\" Jacket, 300-ft. coil;73,67;1
2\" Potable PEX Twin with 7.9\" Jacket, 300-ft. coil;105,55;1
WIPEX Fitting 4\" x 4\" NPT;342;1
WIPEX Sleeve Pliers 3½\" - 4\";242,05;1
End Cap, ¾\" and 1\" Pipe with 2.7\" Jacket;67,9;1
End Cap, 1\" and 1¼\" PEX Pipe with 5.5\" Jacket;144;1
End Cap, 1¼\", 1½\" and 2\" HDPE Pipe with 5.5\" Jacket;155;1
End Cap, 1½\", 2\", 2½\" PEX and 3\" HDPE Pipe with 6.9\" Jacket;171;1
End Cap 3\", 3½\", 4\" PEX and 4\" HDPE pipe, 7.9\" Jacket;193;1
Twin End Cap, 1\", 1¼\" and 1½\" PEX Pipe with 6.9\" Jacket;196;1
Twin End Cap, 2\" and 2½\" PEX Pipe with 7.9\" Jacket;226;1
Heat-trace Power Terminal Block;472;1
Heat-trace End Seal, SF-E;63;1
Heat-trace Tee Splice, SF-T;478;1
1¼\" Potable PEX Plus with 5.5\" Jacket, 5 W/ft. 240VAC;61,34;1
5/16\" Wirsbo hePEX, 100-ft. coil;154,02;1
?\" Wirsbo hePEX, 100-ft. coil;166,26;1
½\" Wirsbo hePEX, 100-ft. coil;154,02;1
?\" Wirsbo hePEX, 100-ft. coil;206,04;1
¾\" Wirsbo hePEX, 100-ft. coil;253,98;1
1\" Wirsbo hePEX, 100-ft. coil;427,38;1
1¼\" Wirsbo hePEX, 100-ft. coil;765;1
1½\" Wirsbo hePEX, 100-ft. coil;1014,9;1
2\" Wirsbo hePEX, 100-ft. coil;1591,2;1
5/16\" Wirsbo hePEX, 250-ft. coil;382,5;1
?\" Wirsbo hePEX, 400-ft. coil;673,2;1
?\" Wirsbo hePEX, 400-ft. coil;826,2;1
5/16\" Wirsbo hePEX, 1,000-ft. coil;1540,2;1
?\" Wirsbo hePEX, 1,000-ft. coil;1662,6;1
½\" Wirsbo hePEX, 1,000-ft. coil;1540,2;1
?\" Wirsbo hePEX, 1,000-ft. coil;2060,4;1
¾\" Wirsbo hePEX, 1,000-ft. coil;2539,8;1
¾\" Wirsbo hePEX, 500-ft. coil;1275;1
1\" Wirsbo hePEX, 500-ft. coil;2142;1
½\" Wirsbo hePEX, 300-ft. coil;459;1
?\" Wirsbo hePEX, 300-ft. coil;622,2;1
¾\" Wirsbo hePEX, 300-ft. coil;765;1
1\" Wirsbo hePEX, 300-ft. coil;1295,4;1
1¼\" Wirsbo hePEX, 300-ft. coil;2295;1
1½\" Wirsbo hePEX, 300-ft. coil;3029,4;1
2\" Wirsbo hePEX, 300-ft. coil;4732,8;1
½\" Wirsbo hePEX, 500-ft. coil;770,1;1
1\" Wirsbo hePEX, 20-ft. straight length, 200 ft. (10 per bundle);948,6;1
1¼\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);790,5;1
1½\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);1050,6;1
2\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);1642,2;1
2½\" Wirsbo hePEX 20-ft. straight length, 60 ft.(3 per bundle);1295,4;1
3\" Wirsbo hePEX 20-ft. straight length, 40 ft.(2 per bundle);1173;1
½\" Wirsbo hePEX, 20-ft. straight length, 500 ft. (25 per bundle);846,6;1
?\" Wirsbo hePEX, 20-ft. straight length, 300 ft. (15 per bundle);683,4;1
¾\" Wirsbo hePEX, 20-ft. straight length, 300 ft. (15 per bundle);841,5;1
Brass Manifold Loop End Cap, R20;14,16;10
Basic End Cap, R32;28,74;10
Threaded Brass Manifold Bushing, R32 Male x 1\" Female NPT;25,03;10
Threaded Brass Manifold Bushing, R32 Male x ¾\" Female NPT;30,93;10
Brass Manifold Loop End Cap Gasket, spare part;4,34;10
Basic End Cap Gasket, spare part, R32;4,7;10
2\" Copper End Cap Spun End with drain and vent connections;220,5;1
Manifold Wall Cabinet, 35.5\" H x 24\" W x 3.5\" D;444;1
Manifold Wall Cabinet, 35.5\" H x 30.5\" W x 3.5\" D;494;1
Manifold Wall Cabinet, 35.5\" H x 39\" W x 3.5\" D;540;1
TruFLOW Manifold Loop Temperature Gauge;51,8;10
TruFLOW Classic Manifold Elbow Union, R32 Union x 1¼\" BSP;32,6;10
TruFLOW Manifold Coupling Nipple, 1¼\" BSP x 1¼\" BSP;26,23;10
Manifold Supply and Return Ball Valves with Filter and Temperature Gauge, set of 2;345,9;1
Manifold Supply and Return Ball Valves with Temperature Gauges, set of 2;268,57;1
Manifold Supply and Return Ball Valves, set of 2;138;1
TruFLOW Visual Flow Meter, 0.15 to 0.8 gpm;49,12;10
TruFLOW Visual Flow Meter, 0.25 to 2.0 gpm;49,12;10
EP Heating Manifold Single Section with Isolation Valve;43,96;1
EP Heating Manifold Single Section with Balancing Valve and Flow Meter;61,1;1
EP Heating Manifold Elbow, set of 2;49,47;1
EP Heating Manifold Assembly with Flow Meter, 2-loop;395,76;1
EP Heating Manifold Assembly with Flow Meter, 3-loop;457,98;1
EP Heating Manifold Assembly with Flow Meter, 4-loop;545,7;1
EP Heating Manifold Assembly with Flow Meter, 5-loop;632,4;1
EP Heating Manifold Assembly with Flow Meter, 6-loop;708,9;1
EP Heating Manifold Assembly with Flow Meter, 7-loop;765;1
EP Heating Manifold Assembly with Flow Meter, 8-loop;877,2;1
EP Heating Manifold Actuator Adapter;7,91;10
Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 2 loops;461;1
Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 3 loops;540;1
Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 4 loops;645;1
Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 5 loops;735;1
Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 6 loops;835;1
Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 7 loops;900;1
Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 8 loops;1030;1
Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 10 loops;1290;1
Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 12 loops;1510;1
Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 2 loops;520;1
Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 3 loops;655;1
Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 4 loops;785;1
Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 5 loops;935;1
Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 6 loops;1070;1
Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 7 loops;1190;1
Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 8 loops;1380;1
Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 10 loops;1690;1
Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 12 loops;1940;1
Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 3 loops;1910,01;1
Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 4 loops;2088,01;1
Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 5 loops;2322;1
Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 6 loops;2510,01;1
Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 7 loops;2789,01;1
Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 8 loops;3001;1
Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 10 loops;3266,01;1
Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 12 loops;3702;1
O-ring for Stainless-steel Manifold Isolation Valve Body;12,75;10
Stainless-steel Manifold Temperature Gauge, set of 2;44,3;1
Spacer Ring VA10 for Thermal Actuators;2,34;5
Stainless-steel Manifold Supply and Return 1\" FNPT Ball Valve with Temperature Gauge, set of 2;130,63;1
Stainless-steel Manifold Supply and Return 1¼\" FNPT Ball Valve with Temperature Gauge, set of 2;178,7;1
Commercial Stainless-steel Manifold Loop Cap;21;12
Commercial Stainless-steel Manifold ProPEX Male Elbow Adapter, 1 ½\" PEX x 1 ½\" NPT;61,1;2
End Cap with Vent, R32;114,95;1
Spacer Ring VA31H for Thermal Actuators;8,7;10
Single-zone Pump Relay;185;1
¾\" and 1\" Thermal Zone Valve;223;1
Spacer Ring VA33 for White Thermal Actuators;8,7;5
Thermal Actuator, four-wire;127;1
Two-wire Thermal Actuator for EP Heating Manifolds;78,7;1
Two-wire Thermal Actuator for TruFLOW Classic and Jr. Valved Manifolds;83,9;1
Two-wire Thermal Actuator for Stainless-steel Manifolds;79,4;1
Three-zone Control Module for Two and Four-wire Operation;170;1
Four-zone Control Module for Two and Four-wire Operation;189;1
Slab Sensor for Aerial Snow Sensor;474;1
Pavement Snow and Ice Sensor;1850;1
Pavement Snow and Ice Sensor Cup;425;1
Aerial Snow Sensor;440;1
SetPoint 521, Programmable Thermostat with floor sensor;472;1
Single-zone Snow Melt Control;1290;1
50 VA Transformer;64,9;1
Three-zone Multi-pump Relay;461;1
Powered Four-zone Controller;352;1
Powered Six-zone Controller;452;1
Heat-only Thermostat with Touchscreen;198;1
Smatrix Pulse Mini Sensor (T-161);101;1
Wireless Dial Thermostat (T-165);92,4;1
Wireless Digital Thermostat (T-167);144;1
Smatrix Pulse Digital Thermostat (T-169);152;1
Wireless Base Unit Expansion Module, 6 zones (M-160);137;1
Wireless Base Unit, 6 zones (X-165);433;1
Smatrix Pulse Expansion Module (M-262);152;1
Smatrix Pulse Relay Module (M-263);152;1
Smatrix Pulse Controller (X-265) with Antenna (A-265);515;1
Smatrix Pulse Controller (X-265) with Communication Module (R-208);770;1
5/16\" Repair Coupling;38,77;10
5/16\" QS-style Compression Fitting Assembly, R20 thread;23,36;10
?\" QS-style Compression Fitting Assembly, R20 thread;22,52;10
½\" QS-style Compression Fitting Assembly, R20 thread;18,18;10
?\" QS-style Compression Fitting Assembly, R20 thread;22,05;10
¾\" QS-style Compression Fitting Assembly, R25 thread;30,41;10
?\" QS-style Compression Fitting Assembly, R25 thread;24,45;10
?\" QS-style Compression Fitting Assembly for Commercial Manifold, R25 thread;31,9;10
¾\" QS-style Compression Fitting Assembly for Commercial Manifold, R25 thread;34,65;10
Brass Manifold Adapter, R32 to 1¼\" Adapter or 1½\" Fitting Adapter;63,75;10
Brass Manifold Adapter, R32 x 1\" Adapter or 1¼\" Fitting Adapter;35,53;10
Brass Manifold Adapter, R32 x ¾\" Adapter or 1\" Fitting Adapter;42,11;10
QS-style Coupling Nipple, R20 x R20;15,99;10
QS-style Conversion Nipple, R20 x ½\" NPT;15,99;10
QS-style Conversion Nipple, R20 x ¾\" NPT;16,56;10
QS-style Copper Adapter, R20 x ½\" Copper;17,03;10
QS-style Copper Adapter, R20 x ¾\" Copper;13,32;10
QS-style Copper Adapter, R25 x ¾\" Copper (for ¾\" and ?\" tubing only);29,57;10
QS-style Copper Fitting Adapter, R20 x ½\" Copper;16,93;10
QS-style Copper Fitting Adapter, R25 X 1\" Copper (for ¾\" and ?\" tubing only);17,61;10
Quik Trak 7\" x 48\" Panels;24,42;10
Quik Trak 7\" x 48\" Return Panels;32,45;10
Quik Trak 12\" x 48\" Combo Panel, 6 runs with return;74,36;5
Quik Trak 12\" x 12\" Combo 90, 6 runs;20,68;5
Quik Trak 7\" x 12\" Combo Access Panel, 6 runs with 1 access;19,91;6
Quik Trak 7\" x 48\" x 6 Panels (fully assembled set);158,7;1
Xpress Trak Radiant Panel, 6\" o.c., 4 runs;118;14
Joist Trak, ?\" Heat Transfer Panel;17,55;20
Joist Trak, ½\" Heat Transfer Panel;17,55;20
Fast Trak 0.5;37,9;20
Fast Trak 1.3i;42,6;18
Fast Trak Edge Strip, 65-ft. roll;47;10
?\" Metal Bend Support;3,48;50
½\" Metal Bend Support;3,36;50
?\" Metal Bend Support;4,32;50
¾\" Metal Bend Support;6,3;25
?\" Plastic Bend Support;2,34;25
½\" Plastic Bend Support (not for use with wall support bracket A5750500);2,46;25
¾\" 45-degree Plastic Bend Support;4,6;50
¾\" Plastic Bend Support;5,45;50
½\" Plastic Bend Support;2,46;25
½\" 45-degree Plastic Bend Support;3,2;25
1\" Thermal Mixing Valve with Union;214;1
¾\" PVC Elbow for ?\" and ½\" PEX Bend Support;4,77;25
1\" PVC Elbow for ?\" PEX Bend Support;6,35;25
1¼\" PVC Elbow for ¾\" PEX Bend Support;13,4;20
1½\" PVC Elbow for 1\" PEX Bend Support;14,8;25
½\" PEX Rail, 6.5 ft.;16,55;16
?\" PEX Rail, 6.5 ft.;15,9;16
¾\" PEX Rail, 6.5 ft.;25,1;16
Mounting Bracket for ?\" to 1\" Water Meters;14,15;1
PEX Wall Support Bracket, ½\" and ¾\";8,85;25
Ball Valve, R25 Thread x ¾\" Copper Adapter;51,9;10
Ball and Balancing Valve, R20 Thread x ¾\" Copper Adapter;93,32;10
Ball and Balancing Valve, R25 Thread x ¾\" Copper Adapter;93,8;10
½\" Pre-insulated Wirsbo hePEX with ½\" insulation, 100-ft. coil;535,6;1
¾\" Pre-insulated Wirsbo hePEX with ½\" insulation, 100-ft. coil;655,2;1
1\" Pre-insulated Wirsbo hePEX with ½\" insulation, 100-ft. coil;790,4;1
¾\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;960,75;1
1\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;1176;1
1¼\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;1680;1
¾\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 100-ft. coil;1378;1
1\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 100-ft. coil;1600,6;1
1¼\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 100-ft. coil;2162,4;1
1½\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 75-ft. coil;1971,6;1
2\" Blue Foam Staples, 300/pkg.;76;1
1½\" Plastic Foam Staples, 300/pkg.;132;1
2½\" Plastic Foam Staples, 300/pkg.;151;1
Fixing Wire, 1,000/bundle;39,8;1
Tube Clamp Suspension (½ PEX), 100/pkg.;61,4;1
Tube Clamp Suspension (¾ PEX), 50/pkg.;31,3;1
Tube Clamp Standard (½ PEX), 100/pkg.;48,7;1
Tube Clamp Standard (¾ PEX), 50/pkg.;25,6;1
Fire Sprinkler Adapter Mounting Bracket, ¾\" and 1\";11,8;5
Slab Sensor, 10k;61,8;1
3\" x 10' HDPE Valveless Manifold (12\" o.c.), 10 outlet, ¾\" ProPEX;1560;1
3\" x 20' HDPE Valveless Manifold (12\" o.c.), 20 outlet, ¾\" ProPEX;3100;1
4\" x 10' HDPE Valveless Manifold (12\" o.c.), 10 outlet, ¾\" ProPEX;1630;1
4\" x 20' HDPE Valveless Manifold (12\" o.c.), 20 outlet, ¾\" ProPEX;3370;1
3\" x 10' HDPE Valveless Manifold (12\" o.c.), 10 outlet, 1\" ProPEX;1850;1
3\" x 20' HDPE Valveless Manifold (12\" o.c.), 20 outlet, 1\" ProPEX;3680;1
4\" x 10' HDPE Valveless Manifold (12\" o.c.), 10 outlet, 1\" ProPEX;1920;1
4\" x 20' HDPE Valveless Manifold (12\" o.c.), 20 outlet, 1\" ProPEX;3820;1
ProPEX LF Brass x CPVC Spigot Adapter Kit, 1¼\" PEX x 1¼\" CPVC (IPS or CTS);91,5;1
ProPEX LF Brass x CPVC Spigot Adapter, 1¼\" PEX x 1¼\" CPVC (CTS);86,8;1
ProPEX LF Brass x CPVC Spigot Adapter Kit, 1½\" PEX x 1½\" CPVC (IPS or CTS);119;1
ProPEX LF Brass x CPVC Spigot Adapter, 1½\" PEX x 1½\" CPVC (CTS);113;1
ProPEX LF Brass x CPVC Spigot Adapter Kit, 2\" PEX x 2\" CPVC (IPS or CTS);191;1
ProPEX LF Brass x CPVC Spigot Adapter, 2\" PEX x 2\" CPVC (CTS);184;1
ProPEX LF Brass x CPVC Socket Adapter, 1¼\" PEX x 1¼\" CPVC (CTS);86,8;1
ProPEX LF Brass x CPVC Socket Adapter, 1½\" PEX x 1½\" CPVC (CTS);113;1
ProPEX LF Brass x CPVC Socket Adapter, 2\" PEX x 2\" CPVC (CTS);184;1
PEX Foam Stapler;916,7;1
Quik Trak Sealant, 10.3 fluid oz. (300 ml);23,29;24
Quik Trak Screws (1¼\"), 2,500/pkg.;367,4;1
Tube Uncoiler;858;1
Select Uncoiler;4950;1
Tube Cutter (metal) for up to 1\" PEX;57,68;1
Tube Cutter (plastic) for up to 1\" PEX;52,9;1
Ratchet-style PEX Pipe Cutter, 1¼\" - 3\";762,2;1
Fixing Wire Twister;9,32;1
Ratchet-style Fixing Wire Twister;111,24;1
Manifold Pressure Test Kit;109,18;1
1¼\" Uponor AquaPEX White, 300-ft. coil;1940;1
1½\" Uponor AquaPEX White, 300-ft. coil;2260;1
2\" Uponor AquaPEX White, 300-ft. coil;4510;1
3\" Uponor AquaPEX White, 300-ft. coil;7990;1
½\" HDPE Corrugated Sleeve, Red, 400-ft. coil;288;1
¾\" HDPE Corrugated Sleeve, Red, 400 ft.;412;1
¼\" Uponor AquaPEX White, 100-ft. coil;81,1;1
½\" Uponor AquaPEX White, 100-ft. coil;93,8;1
¾\" Uponor AquaPEX White, 100-ft. coil;162;1
1\" Uponor AquaPEX White, 100-ft. coil;291;1
2\" Uponor AquaPEX White, 200-ft. coil;3010;1
½\" HDPE Corrugated Sleeve, Blue, 400-ft. coil;288;1
¾\" HDPE Corrugated Sleeve, Blue, 400 ft.;412;1
½\" Uponor AquaPEX White, 300-ft. coil;282;1
½\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;288;1
?\" Uponor AquaPEX White, 300-ft. coil;420;1
¾\" Uponor AquaPEX White, 300-ft. coil;483;1
¾\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;492;1
1\" Uponor AquaPEX White, 300-ft. coil;875;1
1\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;925;1
1¼\" Uponor AquaPEX White, 100-ft. coil;650;1
1½\" Uponor AquaPEX White, 100-ft. coil;755;1
2\" Uponor AquaPEX White, 100-ft. coil;1510;1
2½\" Uponor AquaPEX White, 100-ft. coil;1980;1
3\" Uponor AquaPEX White, 100-ft. coil;2670;1
?\" Uponor AquaPEX White, 400-ft. coil;316;1
½\" Pre-sleeved Uponor AquaPEX Blue Sleeve, 400-ft. coil;645;1
¾\" Pre-Sleeved Uponor AquaPEX Blue Sleeve, 400-ft. coil;990;1
½\" Pre-sleeved Uponor AquaPEX Red Sleeve, 400-ft. coil;645;1
¾\" Pre-Sleeved Uponor AquaPEX Red Sleeve, 400-ft. coil;990;1
½\" Uponor AquaPEX White, 500-ft. coil;469;1
¾\" Uponor AquaPEX White, 500-ft. coil;810;1
1\" Uponor AquaPEX White, 500-ft. coil;1470;1
?\" Uponor AquaPEX White, 1,000-ft. coil;835;1
½\" Uponor AquaPEX White, 1,000-ft. coil;940;1
?\" Uponor AquaPEX White, 1,000-ft. coil;1420;1
1¼\" Uponor AquaPEX Purple Reclaimed Water, 10-ft. straight length, 50 ft. (5 per bundle);398;1
1\" Uponor AquaPEX White, 20-ft. straight length, 200 ft. (10 per bundle);635;1
1\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 200 ft. (10 per bundle);785;1
1¼\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);670;1
1½\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);780;1
2\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);1560;1
2½\" Uponor AquaPEX White, 20-ft. straight length, 60 ft. (3 per bundle);1230;1
3\" Uponor AquaPEX White, 20-ft. straight length, 40 ft. (2 per bundle);1110;1
½\" Uponor AquaPEX White, 20-ft. straight length, 500 ft. (25 per bundle);515;1
¾\" Uponor AquaPEX White, 20-ft. straight length, 300 ft. (15 per bundle);530;1
1\" Uponor AquaPEX Purple Reclaimed Water, 10-ft. straight length, 100 ft. (10 per bundle);385;1
1¼\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);715;1
1½\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);920;1
2\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);1840;1
½\" Uponor AquaPEX Red, 100-ft. coil;103;1
¾\" Uponor AquaPEX Red, 100-ft. coil;180;1
1\" Uponor AquaPEX Red, 100-ft. coil;319;1
½\" Uponor AquaPEX Red, 300-ft. coil;309;1
¾\" Uponor AquaPEX Red, 300-ft. coil;535;1
1\" Uponor AquaPEX Red, 300-ft. coil;960;1
½\" Uponor AquaPEX Red, 1,000-ft. coil;1030;1
1½\" x 6' Copper Valveless Manifold with 24 outlets, ¾\" sweat;810;1
2\" x 6' Copper Valveless Manifold with 24 outlets, ¾\" sweat;1170;1
2\" x 4' Copper Valved Manifold with R20 Threaded Ball Valves, 12 outlets;1400;1
2\" x 4' Copper Valved Manifold with R20 Threaded Ball and Balancing Valves, 12 outlets;2390;1
2\" x 4' Copper Valved Manifold with R25 Threaded Ball and Balancing Valves, 12 outlets;2060;1
1\" Uponor AquaPEX Red, 20-ft. straight length, 200 ft. (10 per bundle);715;1
½\" Uponor AquaPEX Red, 20-ft. straight length, 500 ft. (25 per bundle);575;1
¾\" Uponor AquaPEX Red, 20-ft. straight length, 300 ft. (15 per bundle);595;1
½\" Uponor AquaPEX Blue, 100-ft. coil;103;1
¾\" Uponor AquaPEX Blue, 100-ft. coil;180;1
1\" Uponor AquaPEX Blue, 100-ft. coil;319;1
½\" Uponor AquaPEX Blue, 300-ft. coil;309;1
¾\" Uponor AquaPEX Blue, 300-ft. coil;535;1
1\" Uponor AquaPEX Blue, 300-ft. coil;960;1
½\" Uponor AquaPEX Blue, 1,000-ft. coil;1030;1
1\" Uponor AquaPEX Blue, 20-ft. straight length, 200 ft. (10 per bundle);715;1
½\" Uponor AquaPEX Blue, 20-ft. straight length, 500 ft. (25 per bundle);575;1
¾\" Uponor AquaPEX Blue, 20-ft. straight length, 300 ft. (15 per bundle);595;1
½\" Uponor AquaPEX White, Red Print, 1,000-ft. coil;940;1
½\" Uponor AquaPEX White, Red Print, 100-ft. coil;93,8;1
¾\" Uponor AquaPEX White, Red Print, 100-ft. coil;162;1
1\" Uponor AquaPEX White, Red Print, 100-ft. coil;291;1
½\" Uponor AquaPEX White, Red Print, 300-ft. coil;282;1
¾\" Uponor AquaPEX White, Red Print, 300-ft. coil;483;1
1\" Uponor AquaPEX White, Red Print, 300-ft. coil;875;1
½\" Uponor AquaPEX White, Blue Print, 1,000-ft. coil;940;1
½\" Uponor AquaPEX White, Blue Print, 100-ft. coil;93,8;1
¾\" Uponor AquaPEX White, Blue Print, 100-ft. coil;162;1
1\" Uponor AquaPEX White, Blue Print, 100-ft. coil;291;1
½\" Uponor AquaPEX White, Blue Print, 300-ft. coil;282;1
¾\" Uponor AquaPEX White, Blue Print, 300-ft. coil;483;1
1\" Uponor AquaPEX White, Blue Print, 300-ft. coil;875;1
½\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 500-ft. (25 per bundle);515;1
¾\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 300-ft. (15 per bundle);530;1
1\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 200-ft. (10 per bundle);635;1
½\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 500-ft. (25 per bundle);515;1
¾\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 300-ft. (15 per bundle);530;1
1\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 200-ft. (10 per bundle);635;1
?\" Metal Drop Ear Bend Support;8,4;25
½\" Metal Drop Ear Bend Support;8,75;25
½\" Metal Straight-through Support;11,7;25
?\" Plastic Drop Ear Bend Support;4,61;25
½\" Plastic Drop Ear Bend Support;4,66;25
¼\" Insert (stainless steel);1,47;10
½\" Insert (stainless steel);2,55;10
Chrome Finishing Sleeve for ½\" PEX (11/16\" O.D.);7,85;25
ProPEX Escutcheon for ½\" PEX (11/16\" O.D.), chrome-plated;15,45;25
ProPEX Escutcheon for ½\" PEX (11/16\" O.D.), white;4,35;25
Steel Plate Protector, 100/pkg.;48,5;1
Single-tube PEX Stand-up Bracket for ½\" PEX;19,6;60
Five-tube PEX Stand-up Bracket for ½\" PEX;74;16
½\" Pre-insulated Uponor AquaPEX with ½\" insulation, 100-ft. coil;457;1
¾\" Pre-insulated Uponor AquaPEX with ½\" insulation, 100-ft. coil;560;1
1\" Pre-insulated Uponor AquaPEX with ½\" insulation, 100-ft. coil;685;1
½\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;700;1
¾\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;820;1
1\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;1000;1
1¼\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;1470;1
LFCSS Stem Extension Kit for ½\" and ¾\" Valves;14,95;1
LFCSS Stem Extension Kit for 1\" and 1 ¼\" Valves;17,05;1
LFCSS Stem Extension Kit for 1 ½\" and 2\" Valves;19,65;1
Fire Sprinkler Adapter Push-on Nut, 25/pkg.;73,5;1
½\" PEX-a Pipe Support, 9-ft. length;15,15;5
¾\" PEX-a Pipe Support, 9-ft. length;16,9;5
1\" PEX-a Pipe Support, 9-ft. length;17,6;5
1¼\" PEX-a Pipe Support, 9-ft. length;22,55;5
1½\" PEX-a Pipe Support, 9-ft. length;24,85;5
2\" PEX-a Pipe Support, 9-ft. length;28,9;5
2½\" PEX-a Pipe Support, 9-ft. length;46,9;5
3\" PEX-a Pipe Support, 9-ft. length;49,4;5
Tube Talon (?\" PEX), 100/pkg.;40,8;1
Tube Talon (½\", ?\", ¾\" PEX), 100/pkg.;35,7;1
Tube Talon (1\" PEX), 50/pkg.;44,2;1
1\" PEX Clip, 50/pkg.;215;1
½\" PEX Clip, 100/pkg.;143;1
¾\" PEX Clip, 100/pkg.;360;1
?\" PEX Clip, 100/pkg.;143;1
1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 4 outlets;323;1
1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 6 outlets;456;1
1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 8 outlets;615;1
1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 10 outlets;750;1
1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 12 outlets;865;1
ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 4 outlets;116;1
ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 6 outlets;159;1
ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 8 outlets;198;1
ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 10 outlets;246;1
ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 12 outlets;302;1
ProPEX LF Copper Stub Ell, ½\" PEX LF Brass x ½\" Copper (13\" x 8\");31,9;25
ProPEX LF Copper Stub Ell, ½\" PEX LF Brass x ½\" Copper (3½\" x 8\");22,25;25
ProPEX LF Copper Tub Ell, ½\" PEX LF Brass x ½\" Copper (3\" x 6\");20,2;25
ProPEX LF Copper Tub Ell, ½\" PEX LF Brass x ½\" Copper (3\" x 4\");18,3;25
ProPEX LF Copper Stub Ell, 1\" PEX x 1\" Copper (13\" x 16\");76,5;1
ProPEX LF Copper Stub Ell, ½\" PEX LF Brass x ½\" Copper (8\" x 13\");32,7;25
ProPEX LF Copper Stub Ell, ¾\" PEX LF Brass x ¾\" Copper (4\" x 8\");49,8;25
ProPEX LF Copper Straight Stub, ½\" PEX LF Brass x ½\" Copper (8\");22,85;25
ProPEX LF Copper Straight Stub, ½\" PEX LF Brass x ½\" Copper (15\");27,6;25
ProPEX LF Water Heater Adapter, ¾\" PEX LF Brass x ¾\" FIP x 18\";69,5;20
ProPEX LF Brass Flange Adapter Kit, 2½\" PEX (150 lb.);660;1
ProPEX LF Brass Flange Adapter Kit, 3\" PEX (150 lb.);880;1
ProPEX LF Brass Elbow, ½\" PEX x ½\" MIP;18,9;25
ProPEX LF Brass Drop Ear Elbow, 1\" PEX x 1\" FIP;72,1;4
ProPEX LF Brass Drop Ear Elbow, ½\" PEX x ?\" FIP;27,7;25
ProPEX LF Brass Drop Ear Elbow, ½\" PEX x ½\" FIP;21,9;25
ProPEX LF Brass Drop Ear Elbow, ¾\" PEX x ¾\" FIP;48,1;4
LF Brass Compression Angle Stop Valve for ½\" PEX;20,48;10
LF Brass Compression Straight Stop Valve for ½\" PEX;20,45;10
ProPEX LF Brass In-line Ice Maker Tee, ½\" PEX x ½\" PEX x ¼\" O.D. compression;62,6;10
ProPEX LF Brass Sweat Fitting Adapter, 1\" PEX x 1\" Copper;21,85;10
ProPEX LF Brass Sweat Fitting Adapter, 1¼\" PEX x 1¼\" Copper;48,3;1
ProPEX LF Brass Sweat Fitting Adapter, 1½\" PEX x 1½\" Copper;79,3;1
ProPEX LF Brass Sweat Fitting Adapter, 2\" PEX x 2\" Copper;222;1
ProPEX LF Brass Sweat Fitting Adapter, ½\" PEX x ½\" Copper;5,45;25
ProPEX LF Brass Sweat Fitting Adapter, ½\" PEX x ¾\" Copper;11;25
ProPEX LF Brass Sweat Fitting Adapter, ¾\" PEX x 1\" Copper;24,35;10
ProPEX LF Brass Sweat Fitting Adapter, ¾\" PEX x ½\" Copper;22,5;25
ProPEX LF Brass Sweat Fitting Adapter, ¾\" PEX x ¾\" Copper;11,95;25
ProPEX LF Brass Sweat Adapter, 1\" PEX x 1\" Copper;21;10
ProPEX LF Brass Sweat Adapter, 1¼\" PEX x 1¼\" Copper;54,5;1
ProPEX LF Brass Sweat Adapter, 1½\" PEX x 1½\" Copper;83,5;1
ProPEX LF Brass Sweat Adapter, 2\" PEX x 2\" Copper;222;1
ProPEX LF Brass Sweat Adapter, 2½\" PEX x 2½\" Copper;456;1
ProPEX LF Brass Sweat Adapter, 3\" PEX x 3\" Copper;730;1
ProPEX LF Brass Sweat Adapter, ?\" PEX x ½\" Copper;12,65;25
ProPEX LF Brass Sweat Adapter, ½\" PEX x ½\" Copper;5,6;25
ProPEX LF Brass Sweat Adapter, ½\" PEX x ¾\" Copper;11,15;25
ProPEX LF Brass Sweat Adapter, ¾\" PEX x 1\" Copper;25,3;10
ProPEX LF Brass Sweat Adapter, ¾\" PEX x ½\" Copper;20,6;25
ProPEX LF Brass Sweat Adapter, ¾\" PEX x ¾\" Copper;12,65;25
ProPEX LF Brass Male Threaded Adapter, 1\" PEX x 1\" NPT;28,7;10
ProPEX LF Brass Male Threaded Adapter, 1\" PEX x ¾\" NPT;30,1;10
ProPEX LF Brass Male Threaded Adapter, 1¼\" PEX x 1¼\" NPT;66,6;1
ProPEX LF Brass Male Threaded Adapter, 1½\" PEX x 1½\" NPT;88,8;1
ProPEX LF Brass Male Threaded Adapter, 2\" PEX x 2\" NPT;246;1
ProPEX LF Brass Male Threaded Adapter, 2½\" PEX x 2½\" NPT;535;1
ProPEX LF Brass Male Threaded Adapter, 3\" PEX x 3\" NPT;785;1
ProPEX LF Brass Male Threaded Adapter, ?\" PEX x ½\" NPT;15,65;25
ProPEX LF Brass Male Threaded Adapter, ½\" PEX x ½\" NPT;7,75;25
ProPEX LF Brass Male Threaded Adapter, ½\" PEX x ¾\" NPT;20,1;25
ProPEX LF Brass Male Threaded Adapter, ¾\" PEX x 1\" NPT;30,1;10
ProPEX LF Brass Male Threaded Adapter, ¾\" PEX x ¾\" NPT;13,95;25
ProPEX LF Brass Coupling, ?\" PEX x ½\" PEX;14,4;25
ProPEX LF Brass Female Threaded Adapter, 1\" PEX x 1\" NPT;38,8;10
ProPEX LF Brass Female Threaded Adapter, 1¼\" PEX x 1¼\" NPT;74,2;1
ProPEX LF Brass Female Threaded Adapter, 1½\" PEX x 1½\" NPT;161;1
ProPEX LF Brass Female Threaded Adapter, 2\" PEX x 2\" NPT;329;1
ProPEX LF Brass Female Threaded Adapter, ½\" PEX x ½\" NPT;15,95;25
ProPEX LF Brass Female Threaded Adapter, ½\" PEX x ¾\" NPT;26,6;25
ProPEX LF Brass Female Threaded Adapter, ¾\" PEX x 1\" NPT;59,3;10
ProPEX LF Brass Female Threaded Adapter, ¾\" PEX x ¾\" NPT;18,7;25
ProPEX LF Brass to PB Coupling, ½\" PEX x ½\" PB;16,3;25
ProPEX LF Brass to PB Coupling, ¾\" PEX x ¾\" PB;27;25
ProPEX LF Brass to PE Coupling, 1\" PEX x 1\" PE;42,5;10
ProPEX LF Brass Tee, 1\" PEX x 1\" PEX x 1\" PEX;44,4;10
ProPEX LF Brass Tee, ½\" PEX x ½\" PEX x ½\" PEX;14,75;25
ProPEX LF Brass Tee, ¾\" PEX x ¾\" PEX x ¾\" PEX;24,05;25
ProPEX LF Brass Reducing Tee, ¾\" PEX x ¾\" PEX x 1\" PEX;38,9;10
ProPEX LF Brass Elbow, ½\" PEX x ½\" PEX;10,4;25
ProPEX LF Brass Elbow, ¾\" PEX x ¾\" PEX;17,2;25
ProPEX LF Brass Elbow, ½\" PEX x ½\" Male CU;17,7;10
ProPEX LF Brass Ice Maker Valve, ½\" PEX x ¼\" O.D. (angle);27,4;10
ProPEX LF Brass Ice Maker Valve, ½\" PEX x ¼\" O.D. (straight);30,6;10
ProPEX LF Brass Ball Valve, ½\" PEX x ½\" MIP;34,2;10
ProPEX LF Brass Ball Valve, ½\" PEX x ½\" Copper Adapter;23,1;10
ProPEX LF Brass Ball Valve, ¾\" PEX x ¾\" Copper Adapter;41;10
ProPEX LF Brass Angle Stop Valve, ½\" PEX;13,95;10
ProPEX LF Brass Straight Stop Valve, ½\" PEX;14,35;10
ProPEX Washing Machine Outlet Box, ½\" LF Brass Valves;120;12
ProPEX Ice Maker Box with Support Brackets, ½\" LF Brass Valve;71,2;12
LF Recessed Pendent Sprinkler, 155F, 3.0 K-factor, White;86,8;5
LF Flat Concealed Horizontal Sidewall Sprinkler, 165F, 4.0 K-factor;191;5
LF Recessed Horizontal Sidewall Sprinkler, 155F, 4.2 K-factor, White;88,3;5
LF Recessed Horizontal Sidewall Sprinkler, 175F, 4.2 K-factor, White;88,3;5
LF Recessed Pendent Sprinkler, 155F, 4.9 K-factor, White;86,8;5
LF Recessed Pendent Sprinkler, 175F, 4.9 K-factor, White;86,8;5
LF RC-RES (162F) Flat Concealed Sprinkler;65,3;5
LF RC-RES (205F) Flat Concealed Sprinkler with White Cover Plate;116;5
ProPEX LF Brass Fire Sprinkler Adapter Tee, 1\" PEX x 1\" PEX x ½\" FNPT;61,3;5
ProPEX LF Brass Fire Sprinkler Adapter Tee, ¾\" PEX x ¾\" PEX x ½\" FNPT;57;5
ProPEX LF Brass Fire Sprinkler Adapter Elbow, 1\" PEX x ½\" FNPT;50,1;5
ProPEX LF Brass Fire Sprinkler Adapter Elbow, ¾\" PEX x ½\" FNPT;48,1;5
ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 1\" PEX x 1\" PEX;40,5;1
ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 1¼\" PEX x 1¼\" PEX;66,2;1
ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 1½\" PEX x 1½\" PEX;99,3;1
ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 2\" PEX x 2\" PEX;173;1
ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem ½\" PEX x ½\" PEX;17,1;10
ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem ¾\" PEX x ¾\" PEX;27,2;10
ProPEX LF Brass Stop and Drain Ball Valve (full port), 1\" PEX x 1\" PEX;41;1
ProPEX LF Brass Stop and Drain Ball Valve (full port), ½\" PEX x ½\" PEX;19,85;10
ProPEX LF Brass Stop and Drain Ball Valve (full port), ¾\" PEX x ¾\" PEX;26,5;10
ProPEX LF Brass Copper Press Fitting Adapter, 1\" PEX x 1\" Copper;27,9;10
ProPEX LF Brass Copper Press Fitting Adapter, 1¼\" PEX x 1¼\" Copper;43,3;1
ProPEX LF Brass Copper Press Fitting Adapter, 1½\" PEX x 1½\" Copper;57,2;1
ProPEX LF Brass Copper Press Fitting Adapter, 2\" PEX x 2\" Copper;121;1
ProPEX LF Brass Copper Press Fitting Adapter, 2½\" PEX x 2½\" Copper;311;1
ProPEX LF Brass Copper Press Fitting Adapter, 3\" PEX x 3\" Copper;399;1
ProPEX LF Brass Copper Press Fitting Adapter, ½\" PEX x ½\" Copper;9,35;25
ProPEX LF Brass Copper Press Fitting Adapter, ¾\" PEX x ¾\" Copper;16,6;25
ProPEX LF Brass Copper Press Adapter, 1\" PEX x 1\" Copper;27,9;10
ProPEX LF Brass Copper Press Adapter, 1¼\" PEX x 1¼\" Copper;41,6;1
ProPEX LF Brass Copper Press Adapter, 1½\" PEX x 1½\" Copper;55,1;1
ProPEX LF Brass Copper Press Adapter, 2\" PEX x 2\" Copper;116;1
ProPEX LF Brass Copper Press Adapter, 2½\" PEX x 2½\" Copper;300;1
ProPEX LF Brass Copper Press Adapter, 3\" PEX x 3\" Copper;385;1
ProPEX LF Brass Copper Press Adapter, ½\" PEX x ½\" Copper;8,9;25
ProPEX LF Brass Copper Press Adapter, ¾\" PEX x ¾\" Copper;15,8;25
ProPEX LF Brass Ball Valve (full port), 1\" PEX x 1\" PEX;38,4;1
ProPEX LF Brass Ball Valve (full port), ½\" PEX x ½\" PEX;13,9;10
ProPEX LF Brass  Ball Valve (full port), ¾\" PEX x ¾\" PEX;22,5;10
ProPEX LF Groove Fitting Adapter, 2\" PEX LF Brass x 2\" CTS Groove;114;1
ProPEX LF Groove Fitting Adapter, 2½\" PEX LF Brass x 2½\" CTS Groove;173;1
ProPEX LF Groove Fitting Adapter, 3\" PEX LF Brass x 3\" CTS Groove;256;1
ProPEX LF Groove Fitting Adapter, 2\" PEX LF Brass x 2\" IPS Groove;117;1
ProPEX LF Groove Fitting Adapter, 2½\" PEX LF Brass x 2½\" IPS Groove;176;1
ProPEX LF Groove Fitting Adapter, 2½\" PEX LF Brass x 3\" IPS Groove;218;1
ProPEX LF Groove Fitting Adapter, 3\" PEX LF Brass x 3\" IPS Groove;256;1
½\" Wirsbo hePEX Radiant Rollout Mat (6\" o.c.), 5 loop;call for price;1
½\" Wirsbo hePEX Radiant Rollout Mat (9\" o.c.), 3 loop;call for price;1
½\" Wirsbo hePEX Radiant Rollout Mat (12\" o.c.), 3 loop;call for price;1
?\" Wirsbo hePEX Radiant Rollout Mat (6\" o.c.), 5 loop;call for price;1
?\" Wirsbo hePEX Radiant Rollout Mat (9\" o.c.), 3 loop;call for price;1
?\" Wirsbo hePEX Radiant Rollout Mat (12\" o.c.), 3 loop;call for price;1
¾\" EP Branch Multi-port Elbow, 8 outlets with mounting clips;91,6;1
1\" EP Branch Multi-port Elbow, 10 outlets with mounting clips;93,3;1
1\" EP Branch Multi-port Tee, 10 outlets with mounting clips;98,1;1
1\" EP Branch Multi-port Tee, 12 outlets with mounting clips;108;1
EP Flow-through Multi-port Tee, 2 outlets, ¾\" x ¾\" ProPEX;13,15;10
EP Flow-through Multi-port Tee, 3 outlets, 1\" x ¾\" ProPEX;44,1;10
EP Flow-through Multi-port Tee, 3 (¾\") outlets, 1¼\" x 1¼\" ProPEX;72,1;1
1¼\" EP Branch Multi-port Tee, 3 (¾\") outlets;72,1;1
EP Flow-through Multi-port Tee, 3 (1\") outlets, 2\" x 2\" ProPEX;268;1
EP Flow-through Multi-port Elbow, 3 outlets, ¾\" x ¾\" ProPEX;49,1;10
¾\" EP Branch Multi-port Tee, 3 outlets;15,25;10
EP Flow-through Multi-port Tee, 3 outlets, ¾\" x ¾\" ProPEX;17,75;10
EP Flow-through Multi-port Vertical Tee, 3 outlets, ¾\" x ¾\" x ¾\" ProPEX;55,6;10
1\" EP Branch Multi-port Tee, 4 outlets;49,8;10
EP Flow-through Multi-port Tee, 4 outlets, 1\" x 1\" ProPEX;47,7;10
EP Flow-through Multi-port Tee, 4 outlets, 1\" x ¾\" ProPEX;50,3;10
EP Flow-through Multi-port Elbow, 4 outlets, ¾\" x ¾\" ProPEX;48,5;10
¾\" EP Branch Multi-port Tee, 4 outlets;22,1;10
EP Flow-through Multi-port Tee, 4 outlets, ¾\" x ¾\" ProPEX;22,1;10
EP Flow-through Multi-port Horizontal Tee, 4 outlets, ¾\" x ¾\" x ¾\" ProPEX;58,9;10
EP Flow-through Multi-port Vertical Tee, 4 outlets, ¾\" x ¾\" x ¾\" ProPEX;58,9;10
1\" EP Branch Multi-port Tee, 6 outlets;63,8;10
EP Flow-through Multi-port Tee, 6 outlets, 1\" x 1\" ProPEX;65,9;10
EP Flow-through Multi-port Tee, 6 outlets, 1\" x ¾\" ProPEX;65,9;10
¾\" EP Branch Multi-port Tee, 6 outlets;25,9;10
EP Flow-through Multi-port Tee, 6 outlets, ¾\" x ¾\" ProPEX;26,6;10
1\" EP Branch Multi-port Tee, 7 outlets with mounting clips;82,8;1
¾\" EP Branch Multi-port Tee, 7 outlets with mounting clips;85,3;1
1\" EP Branch Multi-port Tee, 8 outlets with mounting clips;90,1;1
¾\" EP Branch Multi-port Tee, 8 outlets with mounting clips;88,1;1
¾\" EP Branch Opposing-port Multi-port Tee, 3 outlets;23;10
EP Flow-through Opposing-port Multi-port Tee, 3 outlets, ¾\" x ¾\" ProPEX;28,4;10
¾\" EP Branch Opposing-port Multi-port Tee, 4 outlets;38,4;10
EP Flow-through Opposing-port Multi-port Tee, 4 outlets, ¾\" x ¾\" ProPEX;38,6;10
EP Flow-through Opposing-port Multi-port Tee, 6 outlets, ¾\" x ¾\" ProPEX;58,8;10
2\" x 4' Copper Valved Manifold with ?\" ProPEX Ball Valves, 12 outlets;1620;1
2\" x 4' Copper Valved Manifold with ¾\" ProPEX Ball Valves, 12 outlets;1680;1
2\" x 4' Copper Valved Manifold with ¾\" ProPEX Ball and Balancing Valves, 12 outlets;2060;1
2\" x 4' Copper Valveless Manifold with ¾\" ProPEX, 12 outlets;1060;1
?\" ProPEX Fitting Assembly, R20 Thread;17,19;10
½\" ProPEX Fitting Assembly, R20 Thread;14,63;10
?\" ProPEX Fitting Assembly, R20 Thread;17,4;10
¾\" ProPEX Fitting Assembly, R20 Thread;28,42;10
?\" ProPEX Fitting Assembly for Commercial Manifold, R25 thread;26,1;10
¾\" ProPEX Fitting Assembly for Commercial Manifold, R25 thread;30,33;10
1\" ProPEX Fitting Assembly for Commercial Manifold, R25 thread;47,91;10
ProPEX Manifold Straight Adapter, R32 x 1\" ProPEX;46,4;10
ProPEX Manifold Straight Adapter, R32 x 1¼\" ProPEX;51,94;10
ProPEX Manifold Straight Adapter, R32 x 1½\" ProPEX;54,76;10
ProPEX Manifold Straight Adapter, R32 x ¾\" ProPEX;49,95;10
ProPEX Manifold Elbow Adapter, R32 x 1\" ProPEX;61,66;10
ProPEX Manifold Elbow Adapter, R32 x 1½\" ProPEX;76,81;10
ProPEX Manifold Elbow Adapter, R32 x ¾\" ProPEX;62,6;10
ProPEX EP Plug for ½\" PEX;2,23;25
ProPEX EP Plug for ¾\" PEX;3,45;25
ProPEX EP Plug for 1\" PEX;4,58;10
ProPEX EP Plug for 1¼\" PEX;21,55;1
ProPEX EP Plug for 1½\" PEX;33,5;1
ProPEX EP Plug for 2\" PEX;37,8;1
ProPEX EP Swivel Faucet Adapter, ½\" PEX x ½\" NPSM;5,5;25
ProPEX Baseboard Elbow, ½\" PEX x ¾\" Copper Fitting Adapter;13,32;10
ProPEX Baseboard Elbow, ?\" PEX x ¾\" Copper Fitting Adapter;14,16;10
ProPEX Baseboard Elbow, ¾\" PEX x ¾\" Copper Fitting Adapter;15,1;10
ProPEX Baseboard Elbow, ½\" PEX x ¾\" Copper Adapter;13,32;10
ProPEX Baseboard Elbow, ?\" PEX x ¾\" Copper Adapter;14,16;10
ProPEX Baseboard Elbow, ¾\" PEX x ¾\" Copper Adapter;15,1;10
ProPEX Brass Fitting Adapter, ?\" PEX x ½\" Copper;8,73;10
ProPEX Brass Fitting Adapter, ?\" PEX x ¾\" Copper;7,94;10
ProPEX Brass Sweat Adapter, ?\" PEX x ½\" Copper;12,17;10
ProPEX Brass Sweat Adapter, ?\" PEX x ¾\" Copper;9,3;10
ProPEX Brass Male Threaded Adapter, ?\" PEX x ¾\" NPT;13,95;10
ProPEX Brass Plug for ?\" PEX;14,94;10
ProPEX Brass Coupling, ?\" PEX x ?\" PEX;9,35;10
ProPEX Brass Female Threaded Adapter, ?\" PEX x ¾\" NPT;13,22;10
ProPEX EP Male Threaded Adapter, 1\" PEX x 1\" NPT;12,1;10
ProPEX EP Male Threaded Adapter, ½\" PEX x ½\" NPT;3,46;25
ProPEX EP Male Threaded Adapter, ¾\" PEX x ¾\" NPT;5,55;25
ProPEX Ring, ?\";0,38;50
ProPEX Ring with Stop, ½\";0,43;50
ProPEX Ring with Stop, ?\";0,69;50
ProPEX Ring with Stop, ¾\";0,85;50
ProPEX Ring with Stop, 1\";1,8;50
ProPEX Ring with Stop, 1¼\";1,98;10
ProPEX Ring with Stop, 1½\";2,62;5
ProPEX Ring with Stop, 2\";5,25;10
ProPEX Ring with Stop, 2½\";6,95;5
ProPEX Ring with Stop, 3\";11,4;5
ProPEX Brass Elbow, ?\" PEX x ?\" PEX;14,94;25
ProPEX EP Tee, 1\" PEX x 1\" PEX x 1\" PEX;10,25;10
ProPEX EP Reducing Tee, 1\" PEX x 1\" PEX x 1¼\" PEX;40,2;1
ProPEX EP Reducing Tee, 1\" PEX x 1\" PEX x ½\" PEX;9,4;10
ProPEX EP Reducing Tee, 1\" PEX x 1\" PEX x ¾\" PEX;10,35;10
ProPEX EP Reducing Tee, 1¼\" PEX x 1\" PEX x 1\" PEX;20,3;1
ProPEX EP Tee, 1¼\" PEX x 1¼\" PEX x 1¼\" PEX;22,9;1
ProPEX EP Reducing Tee, 1¼\" PEX x 1\" PEX x ¾\" PEX;17,3;1
ProPEX EP Reducing Tee, 1¼\" PEX x 1¼\" PEX x 1\" PEX;20,95;1
ProPEX EP Reducing Tee, 1¼\" PEX x 1¼\" PEX x ¾\" PEX;20,5;1
ProPEX EP Reducing Tee, 1¼\" PEX x 1¼\" PEX x ½\" PEX;16,1;1
ProPEX EP Reducing Tee, 1¼\" PEX x ¾\" PEX x 1\" PEX;30,7;1
ProPEX EP Reducing Tee, 1¼\" PEX x ¾\" PEX x 1¼\" PEX;35,3;1
ProPEX EP Reducing Tee, 1¼\" PEX x ¾\" PEX x ¾\" PEX;27,4;1
ProPEX EP Reducing Tee, 1\" PEX x ½\" PEX x 1\" PEX;17,55;10
ProPEX EP Reducing Tee, 1½\" PEX x 1\" PEX x 1½\" PEX;27,1;1
ProPEX EP Reducing Tee, 1½\" PEX x 1\" PEX x 1\" PEX;25,4;1
ProPEX EP Tee, 1½\" PEX x 1½\" PEX x 1½\" PEX;32;1
ProPEX EP Reducing Tee, 1½\" PEX x 1\" PEX x ¾\" PEX;25,4;1
ProPEX EP Reducing Tee, 1½\" PEX x 1¼\" PEX x 1\" PEX;30;1
ProPEX EP Reducing Tee, 1½\" PEX x 1¼\" PEX x 1¼\" PEX;32,1;1
ProPEX EP Reducing Tee, 1½\" PEX x 1¼\" PEX x ¾\" PEX;29,1;1
ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x ½\" PEX;23,1;1
ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x 1\" PEX;28,1;1
ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x 1¼\" PEX;28,9;1
ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x ¾\" PEX;27,3;1
ProPEX EP Reducing Tee, 1½\" PEX x ¾\" PEX x 1½\" PEX;35,3;1
ProPEX EP Reducing Tee, 1½\" PEX x ¾\" PEX x ¾\" PEX;35,5;1
ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x ½\" PEX;10,95;10
ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x 1\" PEX;12,35;10
ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x 1¼\" PEX;33,3;1
ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x ¾\" PEX;10;10
ProPEX EP Tee, 2\" PEX x 2\" PEX x 2\" PEX;103;1
ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 1\" PEX;79,2;1
ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 1¼\" PEX;98;1
ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 1½\" PEX;98,6;1
ProPEX EP Reducing Tee, 2\" PEX x 1\" PEX x 1\" PEX;78;1
ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 2\" PEX;97,6;1
ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x 1\" PEX;85;1
ProPEX EP Reducing Tee, 2\" x 2\" x 1¼\";89,2;1
ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x 1½\" PEX;99,8;1
ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x ½\" PEX;85,9;1
ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x ¾\" PEX;86,7;1
ProPEX EP Tee, 2½\" PEX x 2½\" PEX x 2½\" PEX;171;1
ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 1\" PEX;140;1
ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 1¼\" PEX;151;1
ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 1½\" PEX;151;1
ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 2\" PEX;151;1
ProPEX EP Reducing Tee, 2½\" PEX x 2\" PEX x 2\" PEX;151;1
ProPEX EP Reducing Tee, 2½\" PEX x 2\" PEX x 1½\" PEX;151;1
ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x ¾\" PEX;122;1
ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x ¾\" PEX;90,9;1
ProPEX EP Tee, 3\" PEX x 3\" PEX x 3\" PEX;278;1
ProPEX EP Reducing Tee, 3\" PEX x 2½\" PEX x 1½\" PEX;203;1
ProPEX EP Reducing Tee, 3\" PEX x 2\" PEX x 2\" PEX;207;1
ProPEX EP Reducing Tee, 3\" PEX x 2½\" PEX x 2\" PEX;232;1
ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 1\" PEX;174;1
ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 1¼\" PEX;185;1
ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 1½\" PEX;197;1
ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 2\" PEX;232;1
ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 2½\" PEX;254;1
ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x ¾\" PEX;174;1
ProPEX EP Tee, ½\" PEX x ½\" PEX x ½\" PEX;3,51;25
ProPEX EP Reducing Tee, ½\" PEX x ½\" PEX x ¾\" PEX;11,15;25
ProPEX EP Reducing Tee, ¾\" PEX x ¾\" PEX x ½\" PEX;4,58;25
ProPEX EP Reducing Tee, ¾\" PEX x ½\" PEX x ½\" PEX;5,45;25
ProPEX EP Reducing Tee, ¾\" PEX x ½\" PEX x ¾\" PEX;5,65;25
ProPEX EP Reducing Tee, ¾\" PEX x ¾\" PEX x ?\" PEX;10,15;10
ProPEX EP Tee, ¾\" PEX x ¾\" PEX x ¾\" PEX;5,65;25
ProPEX EP Reducing Tee, ¾\" PEX x ¾\" PEX x 1\" PEX;16,65;10
ProPEX EP Elbow, ½\" PEX x ½\" PEX;3,46;25
ProPEX EP Elbow, ¾\" PEX x ¾\" PEX;4,36;25
ProPEX EP Elbow, 1\" PEX x 1\" PEX;9,1;10
ProPEX EP 45 Elbow, 1\" PEX x 1\" PEX;13,35;10
ProPEX EP Elbow, 1¼\" PEX x 1¼\" PEX;19,2;1
ProPEX EP 45 Elbow, 1¼\" PEX x 1¼\" PEX;21;1
ProPEX EP Elbow, 1½\" PEX x 1½\" PEX;25,5;1
ProPEX EP 45 Elbow, 1½\" PEX x 1½\" PEX;23,3;1
ProPEX EP Elbow, 2\" PEX x 2\" PEX;83,6;1
ProPEX EP 45 Elbow, 2\" PEX x 2\" PEX;83,6;1
ProPEX EP Elbow, 2½\" PEX x 2½\" PEX;134;1
ProPEX EP 45 Elbow, 2½\" PEX x 2½\" PEX;134;1
ProPEX EP Elbow, 3\" PEX x 3\" PEX;197;1
ProPEX EP 45 Elbow, 3\" PEX x 3\" PEX;197;1
ProPEX EP Coupling, 1\" PEX x 1\" PEX;4,96;10
ProPEX EP Coupling, 1¼\" PEX x ¾\" PEX;10,8;1
ProPEX EP Coupling, 1¼\" PEX x 1\" PEX;11,3;1
ProPEX EP Coupling, 1¼\" PEX x 1¼\" PEX;12,75;1
ProPEX EP Coupling, 1½\" PEX x ¾\" PEX;13,55;1
ProPEX EP Coupling, 1½\" PEX x 1\" PEX;13,9;1
ProPEX EP Coupling, 1½\" PEX x 1¼\" PEX;14,05;1
ProPEX EP Coupling, 1½\" PEX x 1½\" PEX;14,3;1
ProPEX EP Coupling, 2\" PEX x 1½\" PEX;46,4;1
ProPEX EP Coupling, 2\" PEX x 2\" PEX;59,3;1
ProPEX EP Coupling, 2½\" PEX x 1¼\" PEX;91,2;1
ProPEX EP Coupling, 2½\" PEX x 1½\" PEX;93,8;1
ProPEX EP Coupling, 2½\" PEX x 2\" PEX;95,6;1
ProPEX EP Coupling, 2½\" PEX x 2½\" PEX;96,4;1
ProPEX EP Coupling, 3\" PEX x 2\" PEX;117;1
ProPEX EP Coupling, 3\" PEX x 2½\" PEX;119;1
ProPEX EP Coupling, 3\" PEX x 3\" PEX;126;1
ProPEX EP Coupling, ?\" PEX x ?\" PEX;2,65;25
ProPEX EP Coupling, ½\" PEX x ½\" PEX;2,81;25
ProPEX EP Coupling, ½\" PEX x ¾\" PEX;5,9;25
ProPEX EP Coupling, ?\" PEX X ?\" PEX;6,05;10
ProPEX EP Coupling, ¾\" PEX x 1\" PEX;7,65;25
ProPEX EP Coupling, ¾\" PEX x ¾\" PEX;3,34;25
ProPEX EP Opposing-port Tee 1\" x 1\" x ¾\" x ¾\";29,4;1
ProPEX EP Opposing-port Tee 1¼\" x 1¼\" x ¾\" x ¾\";36,2;1
ProPEX EP Opposing-port Tee 1½\" x 1½\" x ¾\" x ¾\";60,6;1
ProPEX EP Opposing-port Tee 2\" x 2\" x ¾\" x ¾\";94,4;1
ProPEX Brass Fitting Adapter, 1\" PEX x 1\" Copper;13,11;10
ProPEX Brass Fitting Adapter, 1¼\" PEX x 1¼\" Copper;29,16;1
ProPEX Brass Fitting Adapter, 1½\" PEX x 1½\" Copper;47,86;1
ProPEX Brass Fitting Adapter, ½\" PEX x ½\" Copper;3,19;25
ProPEX Brass Fitting Adapter, ¾\" PEX x 1\" Copper;14,06;10
ProPEX Brass Fitting Adapter, ¾\" PEX x ½\" Copper;12,96;25
ProPEX Brass Fitting Adapter, ¾\" PEX x ¾\" Copper;6,95;25
ProPEX Brass Sweat Adapter, 1\" PEX x 1\" Copper;12,07;10
ProPEX Brass Sweat Adapter, 1¼\" PEX x 1¼\" Copper;32,92;1
ProPEX Brass Sweat Adapter, 1½\" PEX x 1½\" Copper;50,37;1
ProPEX Brass Sweat Adapter, 2\" PEX x 2\" Copper;138,99;1
ProPEX Brass Sweat Adapter, ½\" PEX x ½\" Copper;3,25;25
ProPEX Brass Sweat Adapter, ¾\" PEX x 1\" Copper;14,58;10
ProPEX Brass Sweat Adapter, ¾\" PEX x ½\" Copper;11,91;25
ProPEX Brass Sweat Adapter, ¾\" PEX x ¾\" Copper;7,26;25
ProPEX Brass Male Threaded Adapter, 1\" PEX x 1\" NPT;18,08;10
ProPEX Brass Male Threaded Adapter, 1\" PEX x ¾\" NPT;18,13;10
ProPEX Brass Male Threaded Adapter, 1¼\" PEX x 1¼\" NPT;40,23;1
ProPEX Brass Male Threaded Adapter, 1½\" PEX x 1½\" NPT;56,12;1
ProPEX Brass Male Threaded Adapter, 2\" PEX x 2\" NPT;146,3;1
ProPEX Brass Male Threaded Adapter, ½\" PEX x ½\" NPT;4,85;25
ProPEX Brass Male Threaded Adapter, ¾\" PEX x 1\" NPT;18,97;10
ProPEX Brass Male Threaded Adapter,  ¾\" PEX x ½\" NPT;12,7;25
ProPEX Brass Male Threaded Adapter, ¾\" PEX x ¾\" NPT;8,83;25
ProPEX Brass Female Threaded Adapter, 1\" PEX x 1\" NPT;23,36;10
ProPEX Brass Female Threaded Adapter, 1¼\" PEX x 1¼\" NPT;43,05;1
ProPEX Brass Female Threaded Adapter, 1½\" PEX x 1½\" NPT;91,86;1
ProPEX Brass Female Threaded Adapter, 2\" PEX x 2\" NPT;178,7;1
ProPEX Brass Female Threaded Adapter, ½\" PEX x ½\" NPT;9,72;25
ProPEX Brass Female Threaded Adapter, ¾\" PEX x 1\" NPT;34,49;10
ProPEX Brass Female Threaded Adapter, ¾\" PEX x ¾\" NPT;10,87;25
ProPEX Ball Valve, ?\" PEX x ¾\" Copper Adapter;46,4;10
ProPEX Ball Valve, ¾\" PEX x ¾\" Copper Adapter;49,64;10
ProPEX Ball and Balancing Valve, ?\" PEX x ¾\" Copper Adapter;88,3;10
ProPEX Ball and Balancing Valve, ¾\" PEX x ¾\" Copper Adapter;92,27;10
Concealed Flat Cover Plate for HSW, White, (HSW style only);53,4;5
Concealed Flat Cover Plate for 162F LF RC-RES Sprinkler, White, 3¼\";33,1;100
Two-piece Recessed Escutcheon for LF Recessed Pendent and LF Recessed HSW, White;11,45;5
Plastic Tubing Clip, ½\", 100/pkg.;66,1;1
PEX-a Pipe Support Strapping for ½\", ¾\" and 1\" PEX;1,51;100
PEX-a Pipe Support Strapping for 1¼\", 1½\" and 2\" PEX;2,58;100
PEX-a Pipe Support Strapping for 2½\", 3\", 3½\" PEX;4,16;100
Sprinkler Wrench, LF Recessed Pendent;306;1
Sprinkler Wrench, LF Recessed Horizontal Sidewall;345;1
Sprinkler Socket for LF RC-RES Sprinklers, LF74970FC and LF74971FW;287;1
ProPEX Stainless-steel Male Threaded Adapter, 1\" PEX x 1\" NPT;86,3;10
ProPEX Stainless-steel Male Threaded Adapter, ½\" PEX x ½\" NPT;38,7;25
ProPEX Stainless-steel Male Threaded Adapter, ¾\" PEX x ¾\" NPT;57,8;25
TotalFit Drop Ear Elbow, ½\" x ½\" FNPT;call for price;20
TotalFit Drop Ear Elbow, ¾\" x ¾\" FNPT;call for price;12
TotalFit Plug, ½\";call for price;50
TotalFit Plug, ¾\";call for price;30
TotalFit Plug, 1\";call for price;25
TotalFit Male Threaded Adapter, 1\" x 1\" NPT;call for price;15
TotalFit Male Threaded Adapter, ½\" x ½\" NPT;call for price;35
TotalFit Male Threaded Adapter, ½\" x ¾\" NPT;call for price;30
TotalFit Male Threaded Adapter, ¾\" x 1\" NPT;call for price;20
TotalFit Male Threaded Adapter, ¾\" x ¾\" NPT;call for price;25
TotalFit Female Threaded Adapter, 1\" x 1\" NPT;call for price;15
TotalFit Female Threaded Adapter, ½\" x ½\" NPT;call for price;30
TotalFit Female Threaded Adapter, ½\" x ¾\" NPT;call for price;25
TotalFit Female Threaded Adapter, ¾\" x 1\" NPT;call for price;18
TotalFit Female Threaded Adapter, ¾\" x ¾\" NPT;call for price;20
TotalFit Tee, 1\" x 1\" x 1\";call for price;8
TotalFit Reducing Tee, 1\" x 1\" x ½\";call for price;10
TotalFit Reducing Tee, 1\" x 1\" x ¾\";call for price;10
TotalFit Tee, ½\" x ½\" x ½\";call for price;20
TotalFit Reducing Tee, ¾\" x ¾\" x ½\";call for price;14
TotalFit Reducing Tee, ¾\" x ½\" x ½\";call for price;15
TotalFit Tee, ¾\" x ¾\" x ¾\";call for price;12
TotalFit Elbow, ½\" x ½\";call for price;25
TotalFit Elbow, ¾\" x ¾\";call for price;15
TotalFit Elbow, 1\" x 1\";call for price;10
TotalFit Coupling, 1\" x 1\";call for price;15
TotalFit Coupling, ½\" x ½\";call for price;30
TotalFit Coupling, ½\" x ¾\";call for price;25
TotalFit Coupling, ¾\" x 1\";call for price;15
TotalFit Coupling, ¾\" x ¾\";call for price;18
TotalFit Repair Coupling, 1\" x 1\";call for price;9
TotalFit Repair Coupling, ½\" x ½\";call for price;24
TotalFit Repair Coupling, ¾\" x ¾\";call for price;12
TotalFit Removal Tool, ½\";call for price;40
TotalFit Removal Tool, ¾\";call for price;40
TotalFit Removal Tool, 1\";call for price;40
TotalFit Deburr and Depth Tool;call for price;6
ProPEX EP Straight Water Meter Fitting, ¾\" PEX x 1\" NPSM;18,45;1
ProPEX EP Elbow Water Meter Fitting, ¾\" PEX x 1\" NPSM;20,6;1
ProPEX EP Straight Water Meter Fitting, 1\" PEX x 1¼\" NPSM;21,2;1
ProPEX EP Elbow Water Meter Fitting, 1\" PEX x 1¼\" NPSM;23,95;1
ProPEX LF Brass Straight Water Meter Valve, ¾\" PEX x 1\" NPSM;48;1
ProPEX LF Brass Elbow Water Meter Valve, ¾\" PEX x 1\" NPSM;48;1
ProPEX LF Brass Straight Water Meter Valve, 1\" PEX x 1¼\" NPSM;66,8;1
ProPEX LF Brass Elbow Water Meter Valve, 1\" PEX x 1¼\" NPSM;66,8;1
"""
    



    
    messages = [{"role": "user", "content": query}, {"role": "system", "content": system_message} ] 

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        #model="gpt-4",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    companyName = eval(arguments).get("companyName")
    cost = eval(arguments).get("cost")
    mail_reply = eval(arguments).get("mail_reply")
    

    return {
        "companyName": companyName,
        "cost": cost,
        "mail_reply": mail_reply
    }
