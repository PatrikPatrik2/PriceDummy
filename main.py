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
Part Number;Part Description;Price;Pkg.Qty.
1007355;H-Insulation Kit, 5.5\", 6.9\", 7.9\";2150;1
1007357;Reducer Bushing 5.5\" to 2.7\";90,1;1
1007358;Compression Wall Seal for 2.7\" Jacket;505;1
1007360;Compression Wall Seal for 5.5\" Jacket;595;1
1007361;Compression Wall Seal for 6.9\" Jacket;715;1
1007362;Compression Wall Seal for 7.9\" Jacket;760;1
1018245;Twin End Cap, 1\", 1¼\", 1½\" PEX Pipe with 5.5\" Jacket (25mm, 32mm and 40mm);140;1
1018266;Wall Sleeve with Heat Shrink for 2.7\" Jacket;160;1
1018268;Wall Sleeve with Heat Shrink for 6.9\" and 7.9\" Jackets;396;1
1018269;Wall Sleeve with Heat Shrink for 5.5\" Jacket;354;1
1018378;Uponor Shrinkable Tape 9\" x 9' roll;239;1
1018379;Vault Shrink Sleeve for 5.5\" Jacket;135;1
1018381;Vault Shrink Sleeve for 7.9\" Jacket;160;1
1021990;Tee Insulation Kit, 5.5\", 6.9\", 7.9\";1390;1
1021991;Elbow Insulation Kit, 5.5\", 6.9\", 7.9\";1210;1
1021992;Straight Insulation Kit, 5.5\", 6.9\", 7.9\";1180;1
5012710;1\" Thermal Single with 2.7\" Jacket, 1,000-ft. coil;12,33;1
5012775;¾\" Thermal Single with 2.7\" Jacket, 1,000-ft. coil;10,97;1
5015510;1\" Thermal Single with 5.5\" Jacket, 600-ft. coil;37,72;1
5015513;1¼\" Thermal Single with 5.5\" Jacket, 500-ft. coil;43,79;1
5016915;1½\" Thermal Single with 6.9\" Jacket, 300-ft. coil;59,15;1
5016920;2\" Thermal Single with 6.9\" Jacket, 300-ft. coil;67,61;1
5016925;2½\" Thermal Single with 6.9\" Jacket, 300-ft. coil;76,81;1
5017930;3\" Thermal Single with 7.9\" Jacket, 300-ft. coil;99,59;1
5017940;4\" Thermal Single with 7.9\" Jacket, 300-ft. coil;127,49;1
5025513;1¼\" Thermal Twin Jr. with 5.5\" Jacket, 600-ft. coil;29,26;1
5026910;1\" Thermal Twin with 6.9\" Jacket, 600-ft. coil;52,56;1
5026913;1¼\" Thermal Twin with 6.9\" Jacket, 500-ft. coil;57,68;1
5026915;1½\" Thermal Twin with 6.9\" Jacket, 300-ft. coil;73,67;1
5027920;2\" Thermal Twin with 7.9\" Jacket, 300-ft. coil;106,59;1
5027925;2½\" Thermal Twin with 7.9\" Jacket, 300-ft. coil;134,81;1
5212710;1\" Potable PEX with 2.7\" Jacket, 1,000-ft. coil;12,33;1
5212775;¾\" Potable PEX with 2.7\" Jacket, 1,000-ft. coil;10,97;1
5215510;1\" Potable PEX with 5.5\" Jacket, 600-ft. coil;37,72;1
5215513;1¼\" Potable PEX with 5.5\" Jacket, 500-ft. coil;43,79;1
5216915;1½\" Potable PEX with 6.9\" Jacket, 300-ft. coil;59,04;1
5216920;2\" Potable PEX with 6.9\" Jacket, 300-ft. coil;65,73;1
5217930;3\" Potable PEX with 7.9\" Jacket, 300-ft. coil;99,59;1
5226910;1\" Potable PEX Twin with 6.9\" Jacket, 600-ft. coil;52,56;1
5226913;1¼\" Potable PEX Twin with 6.9\" Jacket, 500-ft. coil;57,68;1
5226915;1½\" Potable PEX Twin with 6.9\" Jacket, 300-ft. coil;73,67;1
5227920;2\" Potable PEX Twin with 7.9\" Jacket, 300-ft. coil;105,55;1
5550040;WIPEX Fitting 4\" x 4\" NPT;342;1
5550103;WIPEX Sleeve Pliers 3½\" - 4\";242,05;1
5852710;End Cap, ¾\" and 1\" Pipe with 2.7\" Jacket;67,9;1
5855513;End Cap, 1\" and 1¼\" PEX Pipe with 5.5\" Jacket;144;1
5855520;End Cap, 1¼\", 1½\" and 2\" HDPE Pipe with 5.5\" Jacket;155;1
5856930;End Cap, 1½\", 2\", 2½\" PEX and 3\" HDPE Pipe with 6.9\" Jacket;171;1
5857940;End Cap 3\", 3½\", 4\" PEX and 4\" HDPE pipe, 7.9\" Jacket;193;1
5956915;Twin End Cap, 1\", 1¼\" and 1½\" PEX Pipe with 6.9\" Jacket;196;1
5957925;Twin End Cap, 2\" and 2½\" PEX Pipe with 7.9\" Jacket;226;1
5992000;Heat-trace Power Terminal Block;472;1
5993000;Heat-trace End Seal, SF-E;63;1
5994000;Heat-trace Tee Splice, SF-T;478;1
54555513;1¼\" Potable PEX Plus with 5.5\" Jacket, 5 W/ft. 240VAC;61,34;1
A1140313;5/16\" Wirsbo hePEX, 100-ft. coil;154,02;1
A1140375;?\" Wirsbo hePEX, 100-ft. coil;166,26;1
A1140500;½\" Wirsbo hePEX, 100-ft. coil;154,02;1
A1140625;?\" Wirsbo hePEX, 100-ft. coil;206,04;1
A1140750;¾\" Wirsbo hePEX, 100-ft. coil;253,98;1
A1141000;1\" Wirsbo hePEX, 100-ft. coil;427,38;1
A1141250;1¼\" Wirsbo hePEX, 100-ft. coil;765;1
A1141500;1½\" Wirsbo hePEX, 100-ft. coil;1014,9;1
A1142000;2\" Wirsbo hePEX, 100-ft. coil;1591,2;1
A1180313;5/16\" Wirsbo hePEX, 250-ft. coil;382,5;1
A1210375;?\" Wirsbo hePEX, 400-ft. coil;673,2;1
A1210625;?\" Wirsbo hePEX, 400-ft. coil;826,2;1
A1220313;5/16\" Wirsbo hePEX, 1,000-ft. coil;1540,2;1
A1220375;?\" Wirsbo hePEX, 1,000-ft. coil;1662,6;1
A1220500;½\" Wirsbo hePEX, 1,000-ft. coil;1540,2;1
A1220625;?\" Wirsbo hePEX, 1,000-ft. coil;2060,4;1
A1220750;¾\" Wirsbo hePEX, 1,000-ft. coil;2539,8;1
A1240750;¾\" Wirsbo hePEX, 500-ft. coil;1275;1
A1241000;1\" Wirsbo hePEX, 500-ft. coil;2142;1
A1250500;½\" Wirsbo hePEX, 300-ft. coil;459;1
A1250625;?\" Wirsbo hePEX, 300-ft. coil;622,2;1
A1250750;¾\" Wirsbo hePEX, 300-ft. coil;765;1
A1251000;1\" Wirsbo hePEX, 300-ft. coil;1295,4;1
A1251250;1¼\" Wirsbo hePEX, 300-ft. coil;2295;1
A1251500;1½\" Wirsbo hePEX, 300-ft. coil;3029,4;1
A1252000;2\" Wirsbo hePEX, 300-ft. coil;4732,8;1
A1260500;½\" Wirsbo hePEX, 500-ft. coil;770,1;1
A1921000;1\" Wirsbo hePEX, 20-ft. straight length, 200 ft. (10 per bundle);948,6;1
A1921250;1¼\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);790,5;1
A1921500;1½\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);1050,6;1
A1922000;2\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);1642,2;1
A1922500;2½\" Wirsbo hePEX 20-ft. straight length, 60 ft.(3 per bundle);1295,4;1
A1923000;3\" Wirsbo hePEX 20-ft. straight length, 40 ft.(2 per bundle);1173;1
A1930500;½\" Wirsbo hePEX, 20-ft. straight length, 500 ft. (25 per bundle);846,6;1
A1930625;?\" Wirsbo hePEX, 20-ft. straight length, 300 ft. (15 per bundle);683,4;1
A1930750;¾\" Wirsbo hePEX, 20-ft. straight length, 300 ft. (15 per bundle);841,5;1
A2080020;Brass Manifold Loop End Cap, R20;14,16;10
A2080032;Basic End Cap, R32;28,74;10
A2123210;Threaded Brass Manifold Bushing, R32 Male x 1\" Female NPT;25,03;10
A2133275;Threaded Brass Manifold Bushing, R32 Male x ¾\" Female NPT;30,93;10
A2400020;Brass Manifold Loop End Cap Gasket, spare part;4,34;10
A2400032;Basic End Cap Gasket, spare part, R32;4,7;10
A2402000;2\" Copper End Cap Spun End with drain and vent connections;220,5;1
A2603524;Manifold Wall Cabinet, 35.5\" H x 24\" W x 3.5\" D;444;1
A2603530;Manifold Wall Cabinet, 35.5\" H x 30.5\" W x 3.5\" D;494;1
A2603539;Manifold Wall Cabinet, 35.5\" H x 39\" W x 3.5\" D;540;1
A2610020;TruFLOW Manifold Loop Temperature Gauge;51,8;10
A2620090;TruFLOW Classic Manifold Elbow Union, R32 Union x 1¼\" BSP;32,6;10
A2621010;TruFLOW Manifold Coupling Nipple, 1¼\" BSP x 1¼\" BSP;26,23;10
A2631250;Manifold Supply and Return Ball Valves with Filter and Temperature Gauge, set of 2;345,9;1
A2631251;Manifold Supply and Return Ball Valves with Temperature Gauges, set of 2;268,57;1
A2631252;Manifold Supply and Return Ball Valves, set of 2;138;1
A2640015;TruFLOW Visual Flow Meter, 0.15 to 0.8 gpm;49,12;10
A2640027;TruFLOW Visual Flow Meter, 0.25 to 2.0 gpm;49,12;10
A2670001;EP Heating Manifold Single Section with Isolation Valve;43,96;1
A2670003;EP Heating Manifold Single Section with Balancing Valve and Flow Meter;61,1;1
A2670090;EP Heating Manifold Elbow, set of 2;49,47;1
A2670201;EP Heating Manifold Assembly with Flow Meter, 2-loop;395,76;1
A2670301;EP Heating Manifold Assembly with Flow Meter, 3-loop;457,98;1
A2670401;EP Heating Manifold Assembly with Flow Meter, 4-loop;545,7;1
A2670501;EP Heating Manifold Assembly with Flow Meter, 5-loop;632,4;1
A2670601;EP Heating Manifold Assembly with Flow Meter, 6-loop;708,9;1
A2670701;EP Heating Manifold Assembly with Flow Meter, 7-loop;765;1
A2670801;EP Heating Manifold Assembly with Flow Meter, 8-loop;877,2;1
A2671300;EP Heating Manifold Actuator Adapter;7,91;10
A2700202;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 2 loops;461;1
A2700302;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 3 loops;540;1
A2700402;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 4 loops;645;1
A2700502;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 5 loops;735;1
A2700602;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 6 loops;835;1
A2700702;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 7 loops;900;1
A2700802;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 8 loops;1030;1
A2701002;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 10 loops;1290;1
A2701202;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 12 loops;1510;1
A2720202;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 2 loops;520;1
A2720302;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 3 loops;655;1
A2720402;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 4 loops;785;1
A2720502;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 5 loops;935;1
A2720602;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 6 loops;1070;1
A2720702;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 7 loops;1190;1
A2720802;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 8 loops;1380;1
A2721002;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 10 loops;1690;1
A2721202;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 12 loops;1940;1
A2740302;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 3 loops;1910,01;1
A2740402;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 4 loops;2088,01;1
A2740502;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 5 loops;2322;1
A2740602;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 6 loops;2510,01;1
A2740702;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 7 loops;2789,01;1
A2740802;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 8 loops;3001;1
A2741002;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 10 loops;3266,01;1
A2741202;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 12 loops;3702;1
A2771035;O-ring for Stainless-steel Manifold Isolation Valve Body;12,75;10
A2771050;Stainless-steel Manifold Temperature Gauge, set of 2;44,3;1
A2771060;Spacer Ring VA10 for Thermal Actuators;2,34;5
A2771251;Stainless-steel Manifold Supply and Return 1\" FNPT Ball Valve with Temperature Gauge, set of 2;130,63;1
A2771252;Stainless-steel Manifold Supply and Return 1¼\" FNPT Ball Valve with Temperature Gauge, set of 2;178,7;1
A2791000;Commercial Stainless-steel Manifold Loop Cap;21;12
A2791515;Commercial Stainless-steel Manifold ProPEX Male Elbow Adapter, 1 ½\" PEX x 1 ½\" NPT;61,1;2
A2803250;End Cap with Vent, R32;114,95;1
A2870100;Spacer Ring VA31H for Thermal Actuators;8,7;10
A3010100;Single-zone Pump Relay;185;1
A3011075;¾\" and 1\" Thermal Zone Valve;223;1
A3019900;Spacer Ring VA33 for White Thermal Actuators;8,7;5
A3023522;Thermal Actuator, four-wire;127;1
A3030522;Two-wire Thermal Actuator for EP Heating Manifolds;78,7;1
A3030523;Two-wire Thermal Actuator for TruFLOW Classic and Jr. Valved Manifolds;83,9;1
A3030524;Two-wire Thermal Actuator for Stainless-steel Manifolds;79,4;1
A3031003;Three-zone Control Module for Two and Four-wire Operation;170;1
A3031004;Four-zone Control Module for Two and Four-wire Operation;189;1
A3040073;Slab Sensor for Aerial Snow Sensor;474;1
A3040090;Pavement Snow and Ice Sensor;1850;1
A3040091;Pavement Snow and Ice Sensor Cup;425;1
A3040095;Aerial Snow Sensor;440;1
A3040521;SetPoint 521, Programmable Thermostat with floor sensor;472;1
A3040654;Single-zone Snow Melt Control;1290;1
A3050050;50 VA Transformer;64,9;1
A3080301;Three-zone Multi-pump Relay;461;1
A3080404;Powered Four-zone Controller;352;1
A3080406;Powered Six-zone Controller;452;1
A3100101;Heat-only Thermostat with Touchscreen;198;1
A3800161;Smatrix Pulse Mini Sensor (T-161);101;1
A3800165;Wireless Dial Thermostat (T-165);92,4;1
A3800167;Wireless Digital Thermostat (T-167);144;1
A3800169;Smatrix Pulse Digital Thermostat (T-169);152;1
A3801160;Wireless Base Unit Expansion Module, 6 zones (M-160);137;1
A3801165;Wireless Base Unit, 6 zones (X-165);433;1
A3801262;Smatrix Pulse Expansion Module (M-262);152;1
A3801263;Smatrix Pulse Relay Module (M-263);152;1
A380265A;Smatrix Pulse Controller (X-265) with Antenna (A-265);515;1
A380265C;Smatrix Pulse Controller (X-265) with Communication Module (R-208);770;1
A4010313;5/16\" Repair Coupling;38,77;10
A4020313;5/16\" QS-style Compression Fitting Assembly, R20 thread;23,36;10
A4020375;?\" QS-style Compression Fitting Assembly, R20 thread;22,52;10
A4020500;½\" QS-style Compression Fitting Assembly, R20 thread;18,18;10
A4020625;?\" QS-style Compression Fitting Assembly, R20 thread;22,05;10
A4020750;¾\" QS-style Compression Fitting Assembly, R25 thread;30,41;10
A4030625;?\" QS-style Compression Fitting Assembly, R25 thread;24,45;10
A4050625;?\" QS-style Compression Fitting Assembly for Commercial Manifold, R25 thread;31,9;10
A4050750;¾\" QS-style Compression Fitting Assembly for Commercial Manifold, R25 thread;34,65;10
A4123215;Brass Manifold Adapter, R32 to 1¼\" Adapter or 1½\" Fitting Adapter;63,75;10
A4133210;Brass Manifold Adapter, R32 x 1\" Adapter or 1¼\" Fitting Adapter;35,53;10
A4143210;Brass Manifold Adapter, R32 x ¾\" Adapter or 1\" Fitting Adapter;42,11;10
A4322020;QS-style Coupling Nipple, R20 x R20;15,99;10
A4322050;QS-style Conversion Nipple, R20 x ½\" NPT;15,99;10
A4322075;QS-style Conversion Nipple, R20 x ¾\" NPT;16,56;10
A4332050;QS-style Copper Adapter, R20 x ½\" Copper;17,03;10
A4332075;QS-style Copper Adapter, R20 x ¾\" Copper;13,32;10
A4332575;QS-style Copper Adapter, R25 x ¾\" Copper (for ¾\" and ?\" tubing only);29,57;10
A4342050;QS-style Copper Fitting Adapter, R20 x ½\" Copper;16,93;10
A4342510;QS-style Copper Fitting Adapter, R25 X 1\" Copper (for ¾\" and ?\" tubing only);17,61;10
A5060701;Quik Trak 7\" x 48\" Panels;24,42;10
A5060702;Quik Trak 7\" x 48\" Return Panels;32,45;10
A5060712;Quik Trak 12\" x 48\" Combo Panel, 6 runs with return;74,36;5
A5060722;Quik Trak 12\" x 12\" Combo 90, 6 runs;20,68;5
A5060732;Quik Trak 7\" x 12\" Combo Access Panel, 6 runs with 1 access;19,91;6
A5060761;Quik Trak 7\" x 48\" x 6 Panels (fully assembled set);158,7;1
A5070641;Xpress Trak Radiant Panel, 6\" o.c., 4 runs;118;14
A5080375;Joist Trak, ?\" Heat Transfer Panel;17,55;20
A5080500;Joist Trak, ½\" Heat Transfer Panel;17,55;20
A5090313;Fast Trak 0.5;37,9;20
A5090500;Fast Trak 1.3i;42,6;18
A5091000;Fast Trak Edge Strip, 65-ft. roll;47;10
A5110375;?\" Metal Bend Support;3,48;50
A5110500;½\" Metal Bend Support;3,36;50
A5110625;?\" Metal Bend Support;4,32;50
A5110750;¾\" Metal Bend Support;6,3;25
A5150375;?\" Plastic Bend Support;2,34;25
A5150500;½\" Plastic Bend Support (not for use with wall support bracket A5750500);2,46;25
A5150745;¾\" 45-degree Plastic Bend Support;4,6;50
A5150750;¾\" Plastic Bend Support;5,45;50
A5250500;½\" Plastic Bend Support;2,46;25
A5250545;½\" 45-degree Plastic Bend Support;3,2;25
A5402112;1\" Thermal Mixing Valve with Union;214;1
A5500500;¾\" PVC Elbow for ?\" and ½\" PEX Bend Support;4,77;25
A5500625;1\" PVC Elbow for ?\" PEX Bend Support;6,35;25
A5500750;1¼\" PVC Elbow for ¾\" PEX Bend Support;13,4;20
A5501000;1½\" PVC Elbow for 1\" PEX Bend Support;14,8;25
A5700500;½\" PEX Rail, 6.5 ft.;16,55;16
A5700625;?\" PEX Rail, 6.5 ft.;15,9;16
A5700750;¾\" PEX Rail, 6.5 ft.;25,1;16
A5750001;Mounting Bracket for ?\" to 1\" Water Meters;14,15;1
A5750500;PEX Wall Support Bracket, ½\" and ¾\";8,85;25
A5802575;Ball Valve, R25 Thread x ¾\" Copper Adapter;51,9;10
A5902075;Ball and Balancing Valve, R20 Thread x ¾\" Copper Adapter;93,32;10
A5902575;Ball and Balancing Valve, R25 Thread x ¾\" Copper Adapter;93,8;10
A6140500;½\" Pre-insulated Wirsbo hePEX with ½\" insulation, 100-ft. coil;535,6;1
A6140750;¾\" Pre-insulated Wirsbo hePEX with ½\" insulation, 100-ft. coil;655,2;1
A6141000;1\" Pre-insulated Wirsbo hePEX with ½\" insulation, 100-ft. coil;790,4;1
A6150750;¾\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;960,75;1
A6151000;1\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;1176;1
A6151250;1¼\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;1680;1
A6160750;¾\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 100-ft. coil;1378;1
A6161000;1\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 100-ft. coil;1600,6;1
A6161250;1¼\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 100-ft. coil;2162,4;1
A6161500;1½\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 75-ft. coil;1971,6;1
A7012000;2\" Blue Foam Staples, 300/pkg.;76;1
A7015050;1½\" Plastic Foam Staples, 300/pkg.;132;1
A7015075;2½\" Plastic Foam Staples, 300/pkg.;151;1
A7031000;Fixing Wire, 1,000/bundle;39,8;1
A7250500;Tube Clamp Suspension (½ PEX), 100/pkg.;61,4;1
A7250750;Tube Clamp Suspension (¾ PEX), 50/pkg.;31,3;1
A7350500;Tube Clamp Standard (½ PEX), 100/pkg.;48,7;1
A7350750;Tube Clamp Standard (¾ PEX), 50/pkg.;25,6;1
A7750700;Fire Sprinkler Adapter Mounting Bracket, ¾\" and 1\";11,8;5
A9010599;Slab Sensor, 10k;61,8;1
B2253751;3\" x 10' HDPE Valveless Manifold (12\" o.c.), 10 outlet, ¾\" ProPEX;1560;1
B2253752;3\" x 20' HDPE Valveless Manifold (12\" o.c.), 20 outlet, ¾\" ProPEX;3100;1
B2254751;4\" x 10' HDPE Valveless Manifold (12\" o.c.), 10 outlet, ¾\" ProPEX;1630;1
B2254752;4\" x 20' HDPE Valveless Manifold (12\" o.c.), 20 outlet, ¾\" ProPEX;3370;1
B2273101;3\" x 10' HDPE Valveless Manifold (12\" o.c.), 10 outlet, 1\" ProPEX;1850;1
B2273102;3\" x 20' HDPE Valveless Manifold (12\" o.c.), 20 outlet, 1\" ProPEX;3680;1
B2274101;4\" x 10' HDPE Valveless Manifold (12\" o.c.), 10 outlet, 1\" ProPEX;1920;1
B2274102;4\" x 20' HDPE Valveless Manifold (12\" o.c.), 20 outlet, 1\" ProPEX;3820;1
CP4501300;ProPEX LF Brass x CPVC Spigot Adapter Kit, 1¼\" PEX x 1¼\" CPVC (IPS or CTS);91,5;1
CP4501313;ProPEX LF Brass x CPVC Spigot Adapter, 1¼\" PEX x 1¼\" CPVC (CTS);86,8;1
CP4501500;ProPEX LF Brass x CPVC Spigot Adapter Kit, 1½\" PEX x 1½\" CPVC (IPS or CTS);119;1
CP4501515;ProPEX LF Brass x CPVC Spigot Adapter, 1½\" PEX x 1½\" CPVC (CTS);113;1
CP4502000;ProPEX LF Brass x CPVC Spigot Adapter Kit, 2\" PEX x 2\" CPVC (IPS or CTS);191;1
CP4502020;ProPEX LF Brass x CPVC Spigot Adapter, 2\" PEX x 2\" CPVC (CTS);184;1
CP4511313;ProPEX LF Brass x CPVC Socket Adapter, 1¼\" PEX x 1¼\" CPVC (CTS);86,8;1
CP4511515;ProPEX LF Brass x CPVC Socket Adapter, 1½\" PEX x 1½\" CPVC (CTS);113;1
CP4512020;ProPEX LF Brass x CPVC Socket Adapter, 2\" PEX x 2\" CPVC (CTS);184;1
E6025000;PEX Foam Stapler;916,7;1
E6050010;Quik Trak Sealant, 10.3 fluid oz. (300 ml);23,29;24
E6051250;Quik Trak Screws (1¼\"), 2,500/pkg.;367,4;1
E6061000;Tube Uncoiler;858;1
E6062000;Select Uncoiler;4950;1
E6081125;Tube Cutter (metal) for up to 1\" PEX;57,68;1
E6081128;Tube Cutter (plastic) for up to 1\" PEX;52,9;1
E6083000;Ratchet-style PEX Pipe Cutter, 1¼\" - 3\";762,2;1
E6090005;Fixing Wire Twister;9,32;1
E6091700;Ratchet-style Fixing Wire Twister;111,24;1
E6122000;Manifold Pressure Test Kit;109,18;1
F1021250;1¼\" Uponor AquaPEX White, 300-ft. coil;1940;1
F1021500;1½\" Uponor AquaPEX White, 300-ft. coil;2260;1
F1022000;2\" Uponor AquaPEX White, 300-ft. coil;4510;1
F1023000;3\" Uponor AquaPEX White, 300-ft. coil;7990;1
F1035400;½\" HDPE Corrugated Sleeve, Red, 400-ft. coil;288;1
F1037400;¾\" HDPE Corrugated Sleeve, Red, 400 ft.;412;1
F1040250;¼\" Uponor AquaPEX White, 100-ft. coil;81,1;1
F1040500;½\" Uponor AquaPEX White, 100-ft. coil;93,8;1
F1040750;¾\" Uponor AquaPEX White, 100-ft. coil;162;1
F1041000;1\" Uponor AquaPEX White, 100-ft. coil;291;1
F1052000;2\" Uponor AquaPEX White, 200-ft. coil;3010;1
F1055400;½\" HDPE Corrugated Sleeve, Blue, 400-ft. coil;288;1
F1057400;¾\" HDPE Corrugated Sleeve, Blue, 400 ft.;412;1
F1060500;½\" Uponor AquaPEX White, 300-ft. coil;282;1
F1060502;½\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;288;1
F1060625;?\" Uponor AquaPEX White, 300-ft. coil;420;1
F1060750;¾\" Uponor AquaPEX White, 300-ft. coil;483;1
F1060752;¾\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;492;1
F1061000;1\" Uponor AquaPEX White, 300-ft. coil;875;1
F1061002;1\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;925;1
F1061250;1¼\" Uponor AquaPEX White, 100-ft. coil;650;1
F1061500;1½\" Uponor AquaPEX White, 100-ft. coil;755;1
F1062000;2\" Uponor AquaPEX White, 100-ft. coil;1510;1
F1062500;2½\" Uponor AquaPEX White, 100-ft. coil;1980;1
F1063000;3\" Uponor AquaPEX White, 100-ft. coil;2670;1
F1090375;?\" Uponor AquaPEX White, 400-ft. coil;316;1
F1091500;½\" Pre-sleeved Uponor AquaPEX Blue Sleeve, 400-ft. coil;645;1
F1091750;¾\" Pre-Sleeved Uponor AquaPEX Blue Sleeve, 400-ft. coil;990;1
F1092500;½\" Pre-sleeved Uponor AquaPEX Red Sleeve, 400-ft. coil;645;1
F1092750;¾\" Pre-Sleeved Uponor AquaPEX Red Sleeve, 400-ft. coil;990;1
F1100500;½\" Uponor AquaPEX White, 500-ft. coil;469;1
F1100750;¾\" Uponor AquaPEX White, 500-ft. coil;810;1
F1101000;1\" Uponor AquaPEX White, 500-ft. coil;1470;1
F1120375;?\" Uponor AquaPEX White, 1,000-ft. coil;835;1
F1120500;½\" Uponor AquaPEX White, 1,000-ft. coil;940;1
F1120625;?\" Uponor AquaPEX White, 1,000-ft. coil;1420;1
F1911256;1¼\" Uponor AquaPEX Purple Reclaimed Water, 10-ft. straight length, 50 ft. (5 per bundle);398;1
F1921000;1\" Uponor AquaPEX White, 20-ft. straight length, 200 ft. (10 per bundle);635;1
F1921002;1\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 200 ft. (10 per bundle);785;1
F1921250;1¼\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);670;1
F1921500;1½\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);780;1
F1922000;2\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);1560;1
F1922500;2½\" Uponor AquaPEX White, 20-ft. straight length, 60 ft. (3 per bundle);1230;1
F1923000;3\" Uponor AquaPEX White, 20-ft. straight length, 40 ft. (2 per bundle);1110;1
F1930500;½\" Uponor AquaPEX White, 20-ft. straight length, 500 ft. (25 per bundle);515;1
F1930750;¾\" Uponor AquaPEX White, 20-ft. straight length, 300 ft. (15 per bundle);530;1
F1961002;1\" Uponor AquaPEX Purple Reclaimed Water, 10-ft. straight length, 100 ft. (10 per bundle);385;1
F1961256;1¼\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);715;1
F1961502;1½\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);920;1
F1962002;2\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);1840;1
F2040500;½\" Uponor AquaPEX Red, 100-ft. coil;103;1
F2040750;¾\" Uponor AquaPEX Red, 100-ft. coil;180;1
F2041000;1\" Uponor AquaPEX Red, 100-ft. coil;319;1
F2060500;½\" Uponor AquaPEX Red, 300-ft. coil;309;1
F2060750;¾\" Uponor AquaPEX Red, 300-ft. coil;535;1
F2061000;1\" Uponor AquaPEX Red, 300-ft. coil;960;1
F2120500;½\" Uponor AquaPEX Red, 1,000-ft. coil;1030;1
F2801575;1½\" x 6' Copper Valveless Manifold with 24 outlets, ¾\" sweat;810;1
F2802075;2\" x 6' Copper Valveless Manifold with 24 outlets, ¾\" sweat;1170;1
F2811220;2\" x 4' Copper Valved Manifold with R20 Threaded Ball Valves, 12 outlets;1400;1
F2821220;2\" x 4' Copper Valved Manifold with R20 Threaded Ball and Balancing Valves, 12 outlets;2390;1
F2821225;2\" x 4' Copper Valved Manifold with R25 Threaded Ball and Balancing Valves, 12 outlets;2060;1
F2921000;1\" Uponor AquaPEX Red, 20-ft. straight length, 200 ft. (10 per bundle);715;1
F2930500;½\" Uponor AquaPEX Red, 20-ft. straight length, 500 ft. (25 per bundle);575;1
F2930750;¾\" Uponor AquaPEX Red, 20-ft. straight length, 300 ft. (15 per bundle);595;1
F3040500;½\" Uponor AquaPEX Blue, 100-ft. coil;103;1
F3040750;¾\" Uponor AquaPEX Blue, 100-ft. coil;180;1
F3041000;1\" Uponor AquaPEX Blue, 100-ft. coil;319;1
F3060500;½\" Uponor AquaPEX Blue, 300-ft. coil;309;1
F3060750;¾\" Uponor AquaPEX Blue, 300-ft. coil;535;1
F3061000;1\" Uponor AquaPEX Blue, 300-ft. coil;960;1
F3120500;½\" Uponor AquaPEX Blue, 1,000-ft. coil;1030;1
F3921000;1\" Uponor AquaPEX Blue, 20-ft. straight length, 200 ft. (10 per bundle);715;1
F3930500;½\" Uponor AquaPEX Blue, 20-ft. straight length, 500 ft. (25 per bundle);575;1
F3930750;¾\" Uponor AquaPEX Blue, 20-ft. straight length, 300 ft. (15 per bundle);595;1
F4220500;½\" Uponor AquaPEX White, Red Print, 1,000-ft. coil;940;1
F4240500;½\" Uponor AquaPEX White, Red Print, 100-ft. coil;93,8;1
F4240750;¾\" Uponor AquaPEX White, Red Print, 100-ft. coil;162;1
F4241000;1\" Uponor AquaPEX White, Red Print, 100-ft. coil;291;1
F4260500;½\" Uponor AquaPEX White, Red Print, 300-ft. coil;282;1
F4260750;¾\" Uponor AquaPEX White, Red Print, 300-ft. coil;483;1
F4261000;1\" Uponor AquaPEX White, Red Print, 300-ft. coil;875;1
F4320500;½\" Uponor AquaPEX White, Blue Print, 1,000-ft. coil;940;1
F4340500;½\" Uponor AquaPEX White, Blue Print, 100-ft. coil;93,8;1
F4340750;¾\" Uponor AquaPEX White, Blue Print, 100-ft. coil;162;1
F4341000;1\" Uponor AquaPEX White, Blue Print, 100-ft. coil;291;1
F4360500;½\" Uponor AquaPEX White, Blue Print, 300-ft. coil;282;1
F4360750;¾\" Uponor AquaPEX White, Blue Print, 300-ft. coil;483;1
F4361000;1\" Uponor AquaPEX White, Blue Print, 300-ft. coil;875;1
F4920500;½\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 500-ft. (25 per bundle);515;1
F4920750;¾\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 300-ft. (15 per bundle);530;1
F4921000;1\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 200-ft. (10 per bundle);635;1
F4930500;½\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 500-ft. (25 per bundle);515;1
F4930750;¾\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 300-ft. (15 per bundle);530;1
F4931000;1\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 200-ft. (10 per bundle);635;1
F5120375;?\" Metal Drop Ear Bend Support;8,4;25
F5120500;½\" Metal Drop Ear Bend Support;8,75;25
F5140500;½\" Metal Straight-through Support;11,7;25
F5200375;?\" Plastic Drop Ear Bend Support;4,61;25
F5200500;½\" Plastic Drop Ear Bend Support;4,66;25
F5400250;¼\" Insert (stainless steel);1,47;10
F5400500;½\" Insert (stainless steel);2,55;10
F5600500;Chrome Finishing Sleeve for ½\" PEX (11/16\" O.D.);7,85;25
F5650500;ProPEX Escutcheon for ½\" PEX (11/16\" O.D.), chrome-plated;15,45;25
F5670500;ProPEX Escutcheon for ½\" PEX (11/16\" O.D.), white;4,35;25
F5700002;Steel Plate Protector, 100/pkg.;48,5;1
F5801000;Single-tube PEX Stand-up Bracket for ½\" PEX;19,6;60
F5805000;Five-tube PEX Stand-up Bracket for ½\" PEX;74;16
F6040500;½\" Pre-insulated Uponor AquaPEX with ½\" insulation, 100-ft. coil;457;1
F6040750;¾\" Pre-insulated Uponor AquaPEX with ½\" insulation, 100-ft. coil;560;1
F6041000;1\" Pre-insulated Uponor AquaPEX with ½\" insulation, 100-ft. coil;685;1
F6150500;½\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;700;1
F6150750;¾\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;820;1
F6151000;1\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;1000;1
F6151250;1¼\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;1470;1
F6630001;LFCSS Stem Extension Kit for ½\" and ¾\" Valves;14,95;1
F6630002;LFCSS Stem Extension Kit for 1\" and 1 ¼\" Valves;17,05;1
F6630003;LFCSS Stem Extension Kit for 1 ½\" and 2\" Valves;19,65;1
F7000005;Fire Sprinkler Adapter Push-on Nut, 25/pkg.;73,5;1
F7040500;½\" PEX-a Pipe Support, 9-ft. length;15,15;5
F7040750;¾\" PEX-a Pipe Support, 9-ft. length;16,9;5
F7041000;1\" PEX-a Pipe Support, 9-ft. length;17,6;5
F7041250;1¼\" PEX-a Pipe Support, 9-ft. length;22,55;5
F7041500;1½\" PEX-a Pipe Support, 9-ft. length;24,85;5
F7042000;2\" PEX-a Pipe Support, 9-ft. length;28,9;5
F7042500;2½\" PEX-a Pipe Support, 9-ft. length;46,9;5
F7043000;3\" PEX-a Pipe Support, 9-ft. length;49,4;5
F7050375;Tube Talon (?\" PEX), 100/pkg.;40,8;1
F7050750;Tube Talon (½\", ?\", ¾\" PEX), 100/pkg.;35,7;1
F7051000;Tube Talon (1\" PEX), 50/pkg.;44,2;1
F7051001;1\" PEX Clip, 50/pkg.;215;1
F7051258;½\" PEX Clip, 100/pkg.;143;1
F7057500;¾\" PEX Clip, 100/pkg.;360;1
F7060375;?\" PEX Clip, 100/pkg.;143;1
LF2500400;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 4 outlets;323;1
LF2500600;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 6 outlets;456;1
LF2500800;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 8 outlets;615;1
LF2501000;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 10 outlets;750;1
LF2501200;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 12 outlets;865;1
LF2801050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 4 outlets;116;1
LF2811050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 6 outlets;159;1
LF2821050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 8 outlets;198;1
LF2831050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 10 outlets;246;1
LF2841050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 12 outlets;302;1
LF2855050;ProPEX LF Copper Stub Ell, ½\" PEX LF Brass x ½\" Copper (13\" x 8\");31,9;25
LF2865050;ProPEX LF Copper Stub Ell, ½\" PEX LF Brass x ½\" Copper (3½\" x 8\");22,25;25
LF2875050;ProPEX LF Copper Tub Ell, ½\" PEX LF Brass x ½\" Copper (3\" x 6\");20,2;25
LF2885050;ProPEX LF Copper Tub Ell, ½\" PEX LF Brass x ½\" Copper (3\" x 4\");18,3;25
LF2891010;ProPEX LF Copper Stub Ell, 1\" PEX x 1\" Copper (13\" x 16\");76,5;1
LF2895050;ProPEX LF Copper Stub Ell, ½\" PEX LF Brass x ½\" Copper (8\" x 13\");32,7;25
LF2897575;ProPEX LF Copper Stub Ell, ¾\" PEX LF Brass x ¾\" Copper (4\" x 8\");49,8;25
LF2935050;ProPEX LF Copper Straight Stub, ½\" PEX LF Brass x ½\" Copper (8\");22,85;25
LF2945050;ProPEX LF Copper Straight Stub, ½\" PEX LF Brass x ½\" Copper (15\");27,6;25
LF2957575;ProPEX LF Water Heater Adapter, ¾\" PEX LF Brass x ¾\" FIP x 18\";69,5;20
LF2982525;ProPEX LF Brass Flange Adapter Kit, 2½\" PEX (150 lb.);660;1
LF2983030;ProPEX LF Brass Flange Adapter Kit, 3\" PEX (150 lb.);880;1
LF4125050;ProPEX LF Brass Elbow, ½\" PEX x ½\" MIP;18,9;25
LF4231010;ProPEX LF Brass Drop Ear Elbow, 1\" PEX x 1\" FIP;72,1;4
LF4235038;ProPEX LF Brass Drop Ear Elbow, ½\" PEX x ?\" FIP;27,7;25
LF4235050;ProPEX LF Brass Drop Ear Elbow, ½\" PEX x ½\" FIP;21,9;25
LF4237575;ProPEX LF Brass Drop Ear Elbow, ¾\" PEX x ¾\" FIP;48,1;4
LF4410500;LF Brass Compression Angle Stop Valve for ½\" PEX;20,48;10
LF4420500;LF Brass Compression Straight Stop Valve for ½\" PEX;20,45;10
LF4455050;ProPEX LF Brass In-line Ice Maker Tee, ½\" PEX x ½\" PEX x ¼\" O.D. compression;62,6;10
LF4501010;ProPEX LF Brass Sweat Fitting Adapter, 1\" PEX x 1\" Copper;21,85;10
LF4501313;ProPEX LF Brass Sweat Fitting Adapter, 1¼\" PEX x 1¼\" Copper;48,3;1
LF4501515;ProPEX LF Brass Sweat Fitting Adapter, 1½\" PEX x 1½\" Copper;79,3;1
LF4502020;ProPEX LF Brass Sweat Fitting Adapter, 2\" PEX x 2\" Copper;222;1
LF4505050;ProPEX LF Brass Sweat Fitting Adapter, ½\" PEX x ½\" Copper;5,45;25
LF4505075;ProPEX LF Brass Sweat Fitting Adapter, ½\" PEX x ¾\" Copper;11;25
LF4507510;ProPEX LF Brass Sweat Fitting Adapter, ¾\" PEX x 1\" Copper;24,35;10
LF4507550;ProPEX LF Brass Sweat Fitting Adapter, ¾\" PEX x ½\" Copper;22,5;25
LF4507575;ProPEX LF Brass Sweat Fitting Adapter, ¾\" PEX x ¾\" Copper;11,95;25
LF4511010;ProPEX LF Brass Sweat Adapter, 1\" PEX x 1\" Copper;21;10
LF4511313;ProPEX LF Brass Sweat Adapter, 1¼\" PEX x 1¼\" Copper;54,5;1
LF4511515;ProPEX LF Brass Sweat Adapter, 1½\" PEX x 1½\" Copper;83,5;1
LF4512020;ProPEX LF Brass Sweat Adapter, 2\" PEX x 2\" Copper;222;1
LF4512525;ProPEX LF Brass Sweat Adapter, 2½\" PEX x 2½\" Copper;456;1
LF4513030;ProPEX LF Brass Sweat Adapter, 3\" PEX x 3\" Copper;730;1
LF4513850;ProPEX LF Brass Sweat Adapter, ?\" PEX x ½\" Copper;12,65;25
LF4515050;ProPEX LF Brass Sweat Adapter, ½\" PEX x ½\" Copper;5,6;25
LF4515075;ProPEX LF Brass Sweat Adapter, ½\" PEX x ¾\" Copper;11,15;25
LF4517510;ProPEX LF Brass Sweat Adapter, ¾\" PEX x 1\" Copper;25,3;10
LF4517550;ProPEX LF Brass Sweat Adapter, ¾\" PEX x ½\" Copper;20,6;25
LF4517575;ProPEX LF Brass Sweat Adapter, ¾\" PEX x ¾\" Copper;12,65;25
LF4521010;ProPEX LF Brass Male Threaded Adapter, 1\" PEX x 1\" NPT;28,7;10
LF4521075;ProPEX LF Brass Male Threaded Adapter, 1\" PEX x ¾\" NPT;30,1;10
LF4521313;ProPEX LF Brass Male Threaded Adapter, 1¼\" PEX x 1¼\" NPT;66,6;1
LF4521515;ProPEX LF Brass Male Threaded Adapter, 1½\" PEX x 1½\" NPT;88,8;1
LF4522020;ProPEX LF Brass Male Threaded Adapter, 2\" PEX x 2\" NPT;246;1
LF4522525;ProPEX LF Brass Male Threaded Adapter, 2½\" PEX x 2½\" NPT;535;1
LF4523030;ProPEX LF Brass Male Threaded Adapter, 3\" PEX x 3\" NPT;785;1
LF4523850;ProPEX LF Brass Male Threaded Adapter, ?\" PEX x ½\" NPT;15,65;25
LF4525050;ProPEX LF Brass Male Threaded Adapter, ½\" PEX x ½\" NPT;7,75;25
LF4525075;ProPEX LF Brass Male Threaded Adapter, ½\" PEX x ¾\" NPT;20,1;25
LF4527510;ProPEX LF Brass Male Threaded Adapter, ¾\" PEX x 1\" NPT;30,1;10
LF4527575;ProPEX LF Brass Male Threaded Adapter, ¾\" PEX x ¾\" NPT;13,95;25
LF4543850;ProPEX LF Brass Coupling, ?\" PEX x ½\" PEX;14,4;25
LF4571010;ProPEX LF Brass Female Threaded Adapter, 1\" PEX x 1\" NPT;38,8;10
LF4571313;ProPEX LF Brass Female Threaded Adapter, 1¼\" PEX x 1¼\" NPT;74,2;1
LF4571515;ProPEX LF Brass Female Threaded Adapter, 1½\" PEX x 1½\" NPT;161;1
LF4572020;ProPEX LF Brass Female Threaded Adapter, 2\" PEX x 2\" NPT;329;1
LF4575050;ProPEX LF Brass Female Threaded Adapter, ½\" PEX x ½\" NPT;15,95;25
LF4575075;ProPEX LF Brass Female Threaded Adapter, ½\" PEX x ¾\" NPT;26,6;25
LF4577510;ProPEX LF Brass Female Threaded Adapter, ¾\" PEX x 1\" NPT;59,3;10
LF4577575;ProPEX LF Brass Female Threaded Adapter, ¾\" PEX x ¾\" NPT;18,7;25
LF4585050;ProPEX LF Brass to PB Coupling, ½\" PEX x ½\" PB;16,3;25
LF4587575;ProPEX LF Brass to PB Coupling, ¾\" PEX x ¾\" PB;27;25
LF4591010;ProPEX LF Brass to PE Coupling, 1\" PEX x 1\" PE;42,5;10
LF4701010;ProPEX LF Brass Tee, 1\" PEX x 1\" PEX x 1\" PEX;44,4;10
LF4705050;ProPEX LF Brass Tee, ½\" PEX x ½\" PEX x ½\" PEX;14,75;25
LF4707575;ProPEX LF Brass Tee, ¾\" PEX x ¾\" PEX x ¾\" PEX;24,05;25
LF4707710;ProPEX LF Brass Reducing Tee, ¾\" PEX x ¾\" PEX x 1\" PEX;38,9;10
LF4710500;ProPEX LF Brass Elbow, ½\" PEX x ½\" PEX;10,4;25
LF4710750;ProPEX LF Brass Elbow, ¾\" PEX x ¾\" PEX;17,2;25
LF4730500;ProPEX LF Brass Elbow, ½\" PEX x ½\" Male CU;17,7;10
LF4785025;ProPEX LF Brass Ice Maker Valve, ½\" PEX x ¼\" O.D. (angle);27,4;10
LF4786025;ProPEX LF Brass Ice Maker Valve, ½\" PEX x ¼\" O.D. (straight);30,6;10
LF4795050;ProPEX LF Brass Ball Valve, ½\" PEX x ½\" MIP;34,2;10
LF4805050;ProPEX LF Brass Ball Valve, ½\" PEX x ½\" Copper Adapter;23,1;10
LF4807575;ProPEX LF Brass Ball Valve, ¾\" PEX x ¾\" Copper Adapter;41;10
LF4855038;ProPEX LF Brass Angle Stop Valve, ½\" PEX;13,95;10
LF4865038;ProPEX LF Brass Straight Stop Valve, ½\" PEX;14,35;10
LF5930500;ProPEX Washing Machine Outlet Box, ½\" LF Brass Valves;120;12
LF5955025;ProPEX Ice Maker Box with Support Brackets, ½\" LF Brass Valve;71,2;12
LF73000WH;LF Recessed Pendent Sprinkler, 155F, 3.0 K-factor, White;86,8;5
LF74000HS;LF Flat Concealed Horizontal Sidewall Sprinkler, 165F, 4.0 K-factor;191;5
LF74300HW;LF Recessed Horizontal Sidewall Sprinkler, 155F, 4.2 K-factor, White;88,3;5
LF74301HW;LF Recessed Horizontal Sidewall Sprinkler, 175F, 4.2 K-factor, White;88,3;5
LF74900WH;LF Recessed Pendent Sprinkler, 155F, 4.9 K-factor, White;86,8;5
LF74901WH;LF Recessed Pendent Sprinkler, 175F, 4.9 K-factor, White;86,8;5
LF74970FC;LF RC-RES (162F) Flat Concealed Sprinkler;65,3;5
LF74971FW;LF RC-RES (205F) Flat Concealed Sprinkler with White Cover Plate;116;5
LF7701010;ProPEX LF Brass Fire Sprinkler Adapter Tee, 1\" PEX x 1\" PEX x ½\" FNPT;61,3;5
LF7707575;ProPEX LF Brass Fire Sprinkler Adapter Tee, ¾\" PEX x ¾\" PEX x ½\" FNPT;57;5
LF7711050;ProPEX LF Brass Fire Sprinkler Adapter Elbow, 1\" PEX x ½\" FNPT;50,1;5
LF7717550;ProPEX LF Brass Fire Sprinkler Adapter Elbow, ¾\" PEX x ½\" FNPT;48,1;5
LFC4821010SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 1\" PEX x 1\" PEX;40,5;1
LFC4821313SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 1¼\" PEX x 1¼\" PEX;66,2;1
LFC4821515SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 1½\" PEX x 1½\" PEX;99,3;1
LFC4822020SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 2\" PEX x 2\" PEX;173;1
LFC4825050SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem ½\" PEX x ½\" PEX;17,1;10
LFC4827575SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem ¾\" PEX x ¾\" PEX;27,2;10
LFD4811010;ProPEX LF Brass Stop and Drain Ball Valve (full port), 1\" PEX x 1\" PEX;41;1
LFD4815050;ProPEX LF Brass Stop and Drain Ball Valve (full port), ½\" PEX x ½\" PEX;19,85;10
LFD4817575;ProPEX LF Brass Stop and Drain Ball Valve (full port), ¾\" PEX x ¾\" PEX;26,5;10
LFP4501010;ProPEX LF Brass Copper Press Fitting Adapter, 1\" PEX x 1\" Copper;27,9;10
LFP4501313;ProPEX LF Brass Copper Press Fitting Adapter, 1¼\" PEX x 1¼\" Copper;43,3;1
LFP4501515;ProPEX LF Brass Copper Press Fitting Adapter, 1½\" PEX x 1½\" Copper;57,2;1
LFP4502020;ProPEX LF Brass Copper Press Fitting Adapter, 2\" PEX x 2\" Copper;121;1
LFP4502525;ProPEX LF Brass Copper Press Fitting Adapter, 2½\" PEX x 2½\" Copper;311;1
LFP4503030;ProPEX LF Brass Copper Press Fitting Adapter, 3\" PEX x 3\" Copper;399;1
LFP4505050;ProPEX LF Brass Copper Press Fitting Adapter, ½\" PEX x ½\" Copper;9,35;25
LFP4507575;ProPEX LF Brass Copper Press Fitting Adapter, ¾\" PEX x ¾\" Copper;16,6;25
LFP4511010;ProPEX LF Brass Copper Press Adapter, 1\" PEX x 1\" Copper;27,9;10
LFP4511313;ProPEX LF Brass Copper Press Adapter, 1¼\" PEX x 1¼\" Copper;41,6;1
LFP4511515;ProPEX LF Brass Copper Press Adapter, 1½\" PEX x 1½\" Copper;55,1;1
LFP4512020;ProPEX LF Brass Copper Press Adapter, 2\" PEX x 2\" Copper;116;1
LFP4512525;ProPEX LF Brass Copper Press Adapter, 2½\" PEX x 2½\" Copper;300;1
LFP4513030;ProPEX LF Brass Copper Press Adapter, 3\" PEX x 3\" Copper;385;1
LFP4515050;ProPEX LF Brass Copper Press Adapter, ½\" PEX x ½\" Copper;8,9;25
LFP4517575;ProPEX LF Brass Copper Press Adapter, ¾\" PEX x ¾\" Copper;15,8;25
LFR4811010;ProPEX LF Brass Ball Valve (full port), 1\" PEX x 1\" PEX;38,4;1
LFR4815050;ProPEX LF Brass Ball Valve (full port), ½\" PEX x ½\" PEX;13,9;10
LFR4817575;ProPEX LF Brass  Ball Valve (full port), ¾\" PEX x ¾\" PEX;22,5;10
LFV2962020;ProPEX LF Groove Fitting Adapter, 2\" PEX LF Brass x 2\" CTS Groove;114;1
LFV2962525;ProPEX LF Groove Fitting Adapter, 2½\" PEX LF Brass x 2½\" CTS Groove;173;1
LFV2963030;ProPEX LF Groove Fitting Adapter, 3\" PEX LF Brass x 3\" CTS Groove;256;1
LFV2972020;ProPEX LF Groove Fitting Adapter, 2\" PEX LF Brass x 2\" IPS Groove;117;1
LFV2972525;ProPEX LF Groove Fitting Adapter, 2½\" PEX LF Brass x 2½\" IPS Groove;176;1
LFV2972530;ProPEX LF Groove Fitting Adapter, 2½\" PEX LF Brass x 3\" IPS Groove;218;1
LFV2973030;ProPEX LF Groove Fitting Adapter, 3\" PEX LF Brass x 3\" IPS Groove;256;1
M2306060000;½\" Wirsbo hePEX Radiant Rollout Mat (6\" o.c.), 5 loop;call for price;1
M2309054000;½\" Wirsbo hePEX Radiant Rollout Mat (9\" o.c.), 3 loop;call for price;1
M2312072000;½\" Wirsbo hePEX Radiant Rollout Mat (12\" o.c.), 3 loop;call for price;1
M2406060000;?\" Wirsbo hePEX Radiant Rollout Mat (6\" o.c.), 5 loop;call for price;1
M2409054000;?\" Wirsbo hePEX Radiant Rollout Mat (9\" o.c.), 3 loop;call for price;1
M2412072000;?\" Wirsbo hePEX Radiant Rollout Mat (12\" o.c.), 3 loop;call for price;1
Q2087550;¾\" EP Branch Multi-port Elbow, 8 outlets with mounting clips;91,6;1
Q2101000;1\" EP Branch Multi-port Elbow, 10 outlets with mounting clips;93,3;1
Q2101051;1\" EP Branch Multi-port Tee, 10 outlets with mounting clips;98,1;1
Q2121051;1\" EP Branch Multi-port Tee, 12 outlets with mounting clips;108;1
Q2227557;EP Flow-through Multi-port Tee, 2 outlets, ¾\" x ¾\" ProPEX;13,15;10
Q2231057;EP Flow-through Multi-port Tee, 3 outlets, 1\" x ¾\" ProPEX;44,1;10
Q2231373;EP Flow-through Multi-port Tee, 3 (¾\") outlets, 1¼\" x 1¼\" ProPEX;72,1;1
Q2231375;1¼\" EP Branch Multi-port Tee, 3 (¾\") outlets;72,1;1
Q2232102;EP Flow-through Multi-port Tee, 3 (1\") outlets, 2\" x 2\" ProPEX;268;1
Q2235577;EP Flow-through Multi-port Elbow, 3 outlets, ¾\" x ¾\" ProPEX;49,1;10
Q2237550;¾\" EP Branch Multi-port Tee, 3 outlets;15,25;10
Q2237557;EP Flow-through Multi-port Tee, 3 outlets, ¾\" x ¾\" ProPEX;17,75;10
Q2237757;EP Flow-through Multi-port Vertical Tee, 3 outlets, ¾\" x ¾\" x ¾\" ProPEX;55,6;10
Q2241050;1\" EP Branch Multi-port Tee, 4 outlets;49,8;10
Q2241051;EP Flow-through Multi-port Tee, 4 outlets, 1\" x 1\" ProPEX;47,7;10
Q2241057;EP Flow-through Multi-port Tee, 4 outlets, 1\" x ¾\" ProPEX;50,3;10
Q2245577;EP Flow-through Multi-port Elbow, 4 outlets, ¾\" x ¾\" ProPEX;48,5;10
Q2247550;¾\" EP Branch Multi-port Tee, 4 outlets;22,1;10
Q2247557;EP Flow-through Multi-port Tee, 4 outlets, ¾\" x ¾\" ProPEX;22,1;10
Q2247577;EP Flow-through Multi-port Horizontal Tee, 4 outlets, ¾\" x ¾\" x ¾\" ProPEX;58,9;10
Q2247757;EP Flow-through Multi-port Vertical Tee, 4 outlets, ¾\" x ¾\" x ¾\" ProPEX;58,9;10
Q2261050;1\" EP Branch Multi-port Tee, 6 outlets;63,8;10
Q2261051;EP Flow-through Multi-port Tee, 6 outlets, 1\" x 1\" ProPEX;65,9;10
Q2261057;EP Flow-through Multi-port Tee, 6 outlets, 1\" x ¾\" ProPEX;65,9;10
Q2267550;¾\" EP Branch Multi-port Tee, 6 outlets;25,9;10
Q2267557;EP Flow-through Multi-port Tee, 6 outlets, ¾\" x ¾\" ProPEX;26,6;10
Q2271051;1\" EP Branch Multi-port Tee, 7 outlets with mounting clips;82,8;1
Q2277550;¾\" EP Branch Multi-port Tee, 7 outlets with mounting clips;85,3;1
Q2281051;1\" EP Branch Multi-port Tee, 8 outlets with mounting clips;90,1;1
Q2287550;¾\" EP Branch Multi-port Tee, 8 outlets with mounting clips;88,1;1
Q2337550;¾\" EP Branch Opposing-port Multi-port Tee, 3 outlets;23;10
Q2337557;EP Flow-through Opposing-port Multi-port Tee, 3 outlets, ¾\" x ¾\" ProPEX;28,4;10
Q2347550;¾\" EP Branch Opposing-port Multi-port Tee, 4 outlets;38,4;10
Q2347557;EP Flow-through Opposing-port Multi-port Tee, 4 outlets, ¾\" x ¾\" ProPEX;38,6;10
Q2367557;EP Flow-through Opposing-port Multi-port Tee, 6 outlets, ¾\" x ¾\" ProPEX;58,8;10
Q2811263;2\" x 4' Copper Valved Manifold with ?\" ProPEX Ball Valves, 12 outlets;1620;1
Q2811275;2\" x 4' Copper Valved Manifold with ¾\" ProPEX Ball Valves, 12 outlets;1680;1
Q2821275;2\" x 4' Copper Valved Manifold with ¾\" ProPEX Ball and Balancing Valves, 12 outlets;2060;1
Q2831275;2\" x 4' Copper Valveless Manifold with ¾\" ProPEX, 12 outlets;1060;1
Q4020375;?\" ProPEX Fitting Assembly, R20 Thread;17,19;10
Q4020500;½\" ProPEX Fitting Assembly, R20 Thread;14,63;10
Q4020625;?\" ProPEX Fitting Assembly, R20 Thread;17,4;10
Q4020750;¾\" ProPEX Fitting Assembly, R20 Thread;28,42;10
Q4050625;?\" ProPEX Fitting Assembly for Commercial Manifold, R25 thread;26,1;10
Q4050750;¾\" ProPEX Fitting Assembly for Commercial Manifold, R25 thread;30,33;10
Q4051000;1\" ProPEX Fitting Assembly for Commercial Manifold, R25 thread;47,91;10
Q4143210;ProPEX Manifold Straight Adapter, R32 x 1\" ProPEX;46,4;10
Q4143213;ProPEX Manifold Straight Adapter, R32 x 1¼\" ProPEX;51,94;10
Q4143215;ProPEX Manifold Straight Adapter, R32 x 1½\" ProPEX;54,76;10
Q4143275;ProPEX Manifold Straight Adapter, R32 x ¾\" ProPEX;49,95;10
Q4153210;ProPEX Manifold Elbow Adapter, R32 x 1\" ProPEX;61,66;10
Q4153215;ProPEX Manifold Elbow Adapter, R32 x 1½\" ProPEX;76,81;10
Q4153275;ProPEX Manifold Elbow Adapter, R32 x ¾\" ProPEX;62,6;10
Q4350500;ProPEX EP Plug for ½\" PEX;2,23;25
Q4350750;ProPEX EP Plug for ¾\" PEX;3,45;25
Q4351000;ProPEX EP Plug for 1\" PEX;4,58;10
Q4351250;ProPEX EP Plug for 1¼\" PEX;21,55;1
Q4351500;ProPEX EP Plug for 1½\" PEX;33,5;1
Q4352000;ProPEX EP Plug for 2\" PEX;37,8;1
Q4360500;ProPEX EP Swivel Faucet Adapter, ½\" PEX x ½\" NPSM;5,5;25
Q4375075;ProPEX Baseboard Elbow, ½\" PEX x ¾\" Copper Fitting Adapter;13,32;10
Q4376375;ProPEX Baseboard Elbow, ?\" PEX x ¾\" Copper Fitting Adapter;14,16;10
Q4377575;ProPEX Baseboard Elbow, ¾\" PEX x ¾\" Copper Fitting Adapter;15,1;10
Q4385075;ProPEX Baseboard Elbow, ½\" PEX x ¾\" Copper Adapter;13,32;10
Q4386375;ProPEX Baseboard Elbow, ?\" PEX x ¾\" Copper Adapter;14,16;10
Q4387575;ProPEX Baseboard Elbow, ¾\" PEX x ¾\" Copper Adapter;15,1;10
Q4506350;ProPEX Brass Fitting Adapter, ?\" PEX x ½\" Copper;8,73;10
Q4506375;ProPEX Brass Fitting Adapter, ?\" PEX x ¾\" Copper;7,94;10
Q4516350;ProPEX Brass Sweat Adapter, ?\" PEX x ½\" Copper;12,17;10
Q4516375;ProPEX Brass Sweat Adapter, ?\" PEX x ¾\" Copper;9,3;10
Q4526375;ProPEX Brass Male Threaded Adapter, ?\" PEX x ¾\" NPT;13,95;10
Q4536363;ProPEX Brass Plug for ?\" PEX;14,94;10
Q4546363;ProPEX Brass Coupling, ?\" PEX x ?\" PEX;9,35;10
Q4576375;ProPEX Brass Female Threaded Adapter, ?\" PEX x ¾\" NPT;13,22;10
Q4621010;ProPEX EP Male Threaded Adapter, 1\" PEX x 1\" NPT;12,1;10
Q4625050;ProPEX EP Male Threaded Adapter, ½\" PEX x ½\" NPT;3,46;25
Q4627575;ProPEX EP Male Threaded Adapter, ¾\" PEX x ¾\" NPT;5,55;25
Q4690302;ProPEX Ring, ?\";0,38;50
Q4690512;ProPEX Ring with Stop, ½\";0,43;50
Q4690625;ProPEX Ring with Stop, ?\";0,69;50
Q4690756;ProPEX Ring with Stop, ¾\";0,85;50
Q4691000;ProPEX Ring with Stop, 1\";1,8;50
Q4691250;ProPEX Ring with Stop, 1¼\";1,98;10
Q4691500;ProPEX Ring with Stop, 1½\";2,62;5
Q4692000;ProPEX Ring with Stop, 2\";5,25;10
Q4692500;ProPEX Ring with Stop, 2½\";6,95;5
Q4693000;ProPEX Ring with Stop, 3\";11,4;5
Q4710625;ProPEX Brass Elbow, ?\" PEX x ?\" PEX;14,94;25
Q4751010;ProPEX EP Tee, 1\" PEX x 1\" PEX x 1\" PEX;10,25;10
Q4751113;ProPEX EP Reducing Tee, 1\" PEX x 1\" PEX x 1¼\" PEX;40,2;1
Q4751150;ProPEX EP Reducing Tee, 1\" PEX x 1\" PEX x ½\" PEX;9,4;10
Q4751175;ProPEX EP Reducing Tee, 1\" PEX x 1\" PEX x ¾\" PEX;10,35;10
Q4751311;ProPEX EP Reducing Tee, 1¼\" PEX x 1\" PEX x 1\" PEX;20,3;1
Q4751313;ProPEX EP Tee, 1¼\" PEX x 1¼\" PEX x 1¼\" PEX;22,9;1
Q4751317;ProPEX EP Reducing Tee, 1¼\" PEX x 1\" PEX x ¾\" PEX;17,3;1
Q4751331;ProPEX EP Reducing Tee, 1¼\" PEX x 1¼\" PEX x 1\" PEX;20,95;1
Q4751337;ProPEX EP Reducing Tee, 1¼\" PEX x 1¼\" PEX x ¾\" PEX;20,5;1
Q4751350;ProPEX EP Reducing Tee, 1¼\" PEX x 1¼\" PEX x ½\" PEX;16,1;1
Q4751371;ProPEX EP Reducing Tee, 1¼\" PEX x ¾\" PEX x 1\" PEX;30,7;1
Q4751373;ProPEX EP Reducing Tee, 1¼\" PEX x ¾\" PEX x 1¼\" PEX;35,3;1
Q4751377;ProPEX EP Reducing Tee, 1¼\" PEX x ¾\" PEX x ¾\" PEX;27,4;1
Q4751501;ProPEX EP Reducing Tee, 1\" PEX x ½\" PEX x 1\" PEX;17,55;10
Q4751505;ProPEX EP Reducing Tee, 1½\" PEX x 1\" PEX x 1½\" PEX;27,1;1
Q4751511;ProPEX EP Reducing Tee, 1½\" PEX x 1\" PEX x 1\" PEX;25,4;1
Q4751515;ProPEX EP Tee, 1½\" PEX x 1½\" PEX x 1½\" PEX;32;1
Q4751517;ProPEX EP Reducing Tee, 1½\" PEX x 1\" PEX x ¾\" PEX;25,4;1
Q4751531;ProPEX EP Reducing Tee, 1½\" PEX x 1¼\" PEX x 1\" PEX;30;1
Q4751533;ProPEX EP Reducing Tee, 1½\" PEX x 1¼\" PEX x 1¼\" PEX;32,1;1
Q4751537;ProPEX EP Reducing Tee, 1½\" PEX x 1¼\" PEX x ¾\" PEX;29,1;1
Q4751550;ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x ½\" PEX;23,1;1
Q4751551;ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x 1\" PEX;28,1;1
Q4751553;ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x 1¼\" PEX;28,9;1
Q4751557;ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x ¾\" PEX;27,3;1
Q4751575;ProPEX EP Reducing Tee, 1½\" PEX x ¾\" PEX x 1½\" PEX;35,3;1
Q4751577;ProPEX EP Reducing Tee, 1½\" PEX x ¾\" PEX x ¾\" PEX;35,5;1
Q4751750;ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x ½\" PEX;10,95;10
Q4751751;ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x 1\" PEX;12,35;10
Q4751753;ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x 1¼\" PEX;33,3;1
Q4751775;ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x ¾\" PEX;10;10
Q4752000;ProPEX EP Tee, 2\" PEX x 2\" PEX x 2\" PEX;103;1
Q4752051;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 1\" PEX;79,2;1
Q4752053;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 1¼\" PEX;98;1
Q4752055;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 1½\" PEX;98,6;1
Q4752110;ProPEX EP Reducing Tee, 2\" PEX x 1\" PEX x 1\" PEX;78;1
Q4752152;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 2\" PEX;97,6;1
Q4752210;ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x 1\" PEX;85;1
Q4752213;ProPEX EP Reducing Tee, 2\" x 2\" x 1¼\";89,2;1
Q4752215;ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x 1½\" PEX;99,8;1
Q4752250;ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x ½\" PEX;85,9;1
Q4752275;ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x ¾\" PEX;86,7;1
Q4752500;ProPEX EP Tee, 2½\" PEX x 2½\" PEX x 2½\" PEX;171;1
Q4752510;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 1\" PEX;140;1
Q4752513;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 1¼\" PEX;151;1
Q4752515;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 1½\" PEX;151;1
Q4752520;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 2\" PEX;151;1
Q4752522;ProPEX EP Reducing Tee, 2½\" PEX x 2\" PEX x 2\" PEX;151;1
Q4752525;ProPEX EP Reducing Tee, 2½\" PEX x 2\" PEX x 1½\" PEX;151;1
Q4752557;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x ¾\" PEX;122;1
Q4752575;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x ¾\" PEX;90,9;1
Q4753000;ProPEX EP Tee, 3\" PEX x 3\" PEX x 3\" PEX;278;1
Q4753215;ProPEX EP Reducing Tee, 3\" PEX x 2½\" PEX x 1½\" PEX;203;1
Q4753220;ProPEX EP Reducing Tee, 3\" PEX x 2\" PEX x 2\" PEX;207;1
Q4753252;ProPEX EP Reducing Tee, 3\" PEX x 2½\" PEX x 2\" PEX;232;1
Q4753310;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 1\" PEX;174;1
Q4753313;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 1¼\" PEX;185;1
Q4753315;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 1½\" PEX;197;1
Q4753320;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 2\" PEX;232;1
Q4753325;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 2½\" PEX;254;1
Q4753375;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x ¾\" PEX;174;1
Q4755050;ProPEX EP Tee, ½\" PEX x ½\" PEX x ½\" PEX;3,51;25
Q4755575;ProPEX EP Reducing Tee, ½\" PEX x ½\" PEX x ¾\" PEX;11,15;25
Q4757550;ProPEX EP Reducing Tee, ¾\" PEX x ¾\" PEX x ½\" PEX;4,58;25
Q4757555;ProPEX EP Reducing Tee, ¾\" PEX x ½\" PEX x ½\" PEX;5,45;25
Q4757557;ProPEX EP Reducing Tee, ¾\" PEX x ½\" PEX x ¾\" PEX;5,65;25
Q4757563;ProPEX EP Reducing Tee, ¾\" PEX x ¾\" PEX x ?\" PEX;10,15;10
Q4757575;ProPEX EP Tee, ¾\" PEX x ¾\" PEX x ¾\" PEX;5,65;25
Q4757710;ProPEX EP Reducing Tee, ¾\" PEX x ¾\" PEX x 1\" PEX;16,65;10
Q4760500;ProPEX EP Elbow, ½\" PEX x ½\" PEX;3,46;25
Q4760750;ProPEX EP Elbow, ¾\" PEX x ¾\" PEX;4,36;25
Q4761000;ProPEX EP Elbow, 1\" PEX x 1\" PEX;9,1;10
Q4761010;ProPEX EP 45 Elbow, 1\" PEX x 1\" PEX;13,35;10
Q4761250;ProPEX EP Elbow, 1¼\" PEX x 1¼\" PEX;19,2;1
Q4761313;ProPEX EP 45 Elbow, 1¼\" PEX x 1¼\" PEX;21;1
Q4761500;ProPEX EP Elbow, 1½\" PEX x 1½\" PEX;25,5;1
Q4761515;ProPEX EP 45 Elbow, 1½\" PEX x 1½\" PEX;23,3;1
Q4762000;ProPEX EP Elbow, 2\" PEX x 2\" PEX;83,6;1
Q4762020;ProPEX EP 45 Elbow, 2\" PEX x 2\" PEX;83,6;1
Q4762500;ProPEX EP Elbow, 2½\" PEX x 2½\" PEX;134;1
Q4762525;ProPEX EP 45 Elbow, 2½\" PEX x 2½\" PEX;134;1
Q4763000;ProPEX EP Elbow, 3\" PEX x 3\" PEX;197;1
Q4763030;ProPEX EP 45 Elbow, 3\" PEX x 3\" PEX;197;1
Q4771010;ProPEX EP Coupling, 1\" PEX x 1\" PEX;4,96;10
Q4771307;ProPEX EP Coupling, 1¼\" PEX x ¾\" PEX;10,8;1
Q4771310;ProPEX EP Coupling, 1¼\" PEX x 1\" PEX;11,3;1
Q4771313;ProPEX EP Coupling, 1¼\" PEX x 1¼\" PEX;12,75;1
Q4771507;ProPEX EP Coupling, 1½\" PEX x ¾\" PEX;13,55;1
Q4771510;ProPEX EP Coupling, 1½\" PEX x 1\" PEX;13,9;1
Q4771513;ProPEX EP Coupling, 1½\" PEX x 1¼\" PEX;14,05;1
Q4771515;ProPEX EP Coupling, 1½\" PEX x 1½\" PEX;14,3;1
Q4772015;ProPEX EP Coupling, 2\" PEX x 1½\" PEX;46,4;1
Q4772020;ProPEX EP Coupling, 2\" PEX x 2\" PEX;59,3;1
Q4772513;ProPEX EP Coupling, 2½\" PEX x 1¼\" PEX;91,2;1
Q4772515;ProPEX EP Coupling, 2½\" PEX x 1½\" PEX;93,8;1
Q4772520;ProPEX EP Coupling, 2½\" PEX x 2\" PEX;95,6;1
Q4772525;ProPEX EP Coupling, 2½\" PEX x 2½\" PEX;96,4;1
Q4773020;ProPEX EP Coupling, 3\" PEX x 2\" PEX;117;1
Q4773025;ProPEX EP Coupling, 3\" PEX x 2½\" PEX;119;1
Q4773030;ProPEX EP Coupling, 3\" PEX x 3\" PEX;126;1
Q4773838;ProPEX EP Coupling, ?\" PEX x ?\" PEX;2,65;25
Q4775050;ProPEX EP Coupling, ½\" PEX x ½\" PEX;2,81;25
Q4775075;ProPEX EP Coupling, ½\" PEX x ¾\" PEX;5,9;25
Q4776363;ProPEX EP Coupling, ?\" PEX X ?\" PEX;6,05;10
Q4777510;ProPEX EP Coupling, ¾\" PEX x 1\" PEX;7,65;25
Q4777575;ProPEX EP Coupling, ¾\" PEX x ¾\" PEX;3,34;25
Q4801075;ProPEX EP Opposing-port Tee 1\" x 1\" x ¾\" x ¾\";29,4;1
Q4801375;ProPEX EP Opposing-port Tee 1¼\" x 1¼\" x ¾\" x ¾\";36,2;1
Q4801575;ProPEX EP Opposing-port Tee 1½\" x 1½\" x ¾\" x ¾\";60,6;1
Q4802075;ProPEX EP Opposing-port Tee 2\" x 2\" x ¾\" x ¾\";94,4;1
Q5501010;ProPEX Brass Fitting Adapter, 1\" PEX x 1\" Copper;13,11;10
Q5501313;ProPEX Brass Fitting Adapter, 1¼\" PEX x 1¼\" Copper;29,16;1
Q5501515;ProPEX Brass Fitting Adapter, 1½\" PEX x 1½\" Copper;47,86;1
Q5505050;ProPEX Brass Fitting Adapter, ½\" PEX x ½\" Copper;3,19;25
Q5507510;ProPEX Brass Fitting Adapter, ¾\" PEX x 1\" Copper;14,06;10
Q5507550;ProPEX Brass Fitting Adapter, ¾\" PEX x ½\" Copper;12,96;25
Q5507575;ProPEX Brass Fitting Adapter, ¾\" PEX x ¾\" Copper;6,95;25
Q5511010;ProPEX Brass Sweat Adapter, 1\" PEX x 1\" Copper;12,07;10
Q5511313;ProPEX Brass Sweat Adapter, 1¼\" PEX x 1¼\" Copper;32,92;1
Q5511515;ProPEX Brass Sweat Adapter, 1½\" PEX x 1½\" Copper;50,37;1
Q5512020;ProPEX Brass Sweat Adapter, 2\" PEX x 2\" Copper;138,99;1
Q5515050;ProPEX Brass Sweat Adapter, ½\" PEX x ½\" Copper;3,25;25
Q5517510;ProPEX Brass Sweat Adapter, ¾\" PEX x 1\" Copper;14,58;10
Q5517550;ProPEX Brass Sweat Adapter, ¾\" PEX x ½\" Copper;11,91;25
Q5517575;ProPEX Brass Sweat Adapter, ¾\" PEX x ¾\" Copper;7,26;25
Q5521010;ProPEX Brass Male Threaded Adapter, 1\" PEX x 1\" NPT;18,08;10
Q5521075;ProPEX Brass Male Threaded Adapter, 1\" PEX x ¾\" NPT;18,13;10
Q5521313;ProPEX Brass Male Threaded Adapter, 1¼\" PEX x 1¼\" NPT;40,23;1
Q5521515;ProPEX Brass Male Threaded Adapter, 1½\" PEX x 1½\" NPT;56,12;1
Q5522020;ProPEX Brass Male Threaded Adapter, 2\" PEX x 2\" NPT;146,3;1
Q5525050;ProPEX Brass Male Threaded Adapter, ½\" PEX x ½\" NPT;4,85;25
Q5527510;ProPEX Brass Male Threaded Adapter, ¾\" PEX x 1\" NPT;18,97;10
Q5527550;ProPEX Brass Male Threaded Adapter,  ¾\" PEX x ½\" NPT;12,7;25
Q5527575;ProPEX Brass Male Threaded Adapter, ¾\" PEX x ¾\" NPT;8,83;25
Q5571010;ProPEX Brass Female Threaded Adapter, 1\" PEX x 1\" NPT;23,36;10
Q5571313;ProPEX Brass Female Threaded Adapter, 1¼\" PEX x 1¼\" NPT;43,05;1
Q5571515;ProPEX Brass Female Threaded Adapter, 1½\" PEX x 1½\" NPT;91,86;1
Q5572020;ProPEX Brass Female Threaded Adapter, 2\" PEX x 2\" NPT;178,7;1
Q5575050;ProPEX Brass Female Threaded Adapter, ½\" PEX x ½\" NPT;9,72;25
Q5577510;ProPEX Brass Female Threaded Adapter, ¾\" PEX x 1\" NPT;34,49;10
Q5577575;ProPEX Brass Female Threaded Adapter, ¾\" PEX x ¾\" NPT;10,87;25
Q5806375;ProPEX Ball Valve, ?\" PEX x ¾\" Copper Adapter;46,4;10
Q5807575;ProPEX Ball Valve, ¾\" PEX x ¾\" Copper Adapter;49,64;10
Q5906375;ProPEX Ball and Balancing Valve, ?\" PEX x ¾\" Copper Adapter;88,3;10
Q5907575;ProPEX Ball and Balancing Valve, ¾\" PEX x ¾\" Copper Adapter;92,27;10
Q70640HW;Concealed Flat Cover Plate for HSW, White, (HSW style only);53,4;5
Q70749WH;Concealed Flat Cover Plate for 162F LF RC-RES Sprinkler, White, 3¼\";33,1;100
Q71850LW;Two-piece Recessed Escutcheon for LF Recessed Pendent and LF Recessed HSW, White;11,45;5
Q7400500;Plastic Tubing Clip, ½\", 100/pkg.;66,1;1
Q7410510;PEX-a Pipe Support Strapping for ½\", ¾\" and 1\" PEX;1,51;100
Q7411220;PEX-a Pipe Support Strapping for 1¼\", 1½\" and 2\" PEX;2,58;100
Q7412540;PEX-a Pipe Support Strapping for 2½\", 3\", 3½\" PEX;4,16;100
Q7500400;Sprinkler Wrench, LF Recessed Pendent;306;1
Q7500410;Sprinkler Wrench, LF Recessed Horizontal Sidewall;345;1
Q7500700;Sprinkler Socket for LF RC-RES Sprinklers, LF74970FC and LF74971FW;287;1
Q8521010;ProPEX Stainless-steel Male Threaded Adapter, 1\" PEX x 1\" NPT;86,3;10
Q8525050;ProPEX Stainless-steel Male Threaded Adapter, ½\" PEX x ½\" NPT;38,7;25
Q8527575;ProPEX Stainless-steel Male Threaded Adapter, ¾\" PEX x ¾\" NPT;57,8;25
TF4235050;TotalFit Drop Ear Elbow, ½\" x ½\" FNPT;call for price;20
TF4237575;TotalFit Drop Ear Elbow, ¾\" x ¾\" FNPT;call for price;12
TF4350500;TotalFit Plug, ½\";call for price;50
TF4350750;TotalFit Plug, ¾\";call for price;30
TF4351000;TotalFit Plug, 1\";call for price;25
TF4521010;TotalFit Male Threaded Adapter, 1\" x 1\" NPT;call for price;15
TF4525050;TotalFit Male Threaded Adapter, ½\" x ½\" NPT;call for price;35
TF4525075;TotalFit Male Threaded Adapter, ½\" x ¾\" NPT;call for price;30
TF4527510;TotalFit Male Threaded Adapter, ¾\" x 1\" NPT;call for price;20
TF4527575;TotalFit Male Threaded Adapter, ¾\" x ¾\" NPT;call for price;25
TF4571010;TotalFit Female Threaded Adapter, 1\" x 1\" NPT;call for price;15
TF4575050;TotalFit Female Threaded Adapter, ½\" x ½\" NPT;call for price;30
TF4575075;TotalFit Female Threaded Adapter, ½\" x ¾\" NPT;call for price;25
TF4577510;TotalFit Female Threaded Adapter, ¾\" x 1\" NPT;call for price;18
TF4577575;TotalFit Female Threaded Adapter, ¾\" x ¾\" NPT;call for price;20
TF4751010;TotalFit Tee, 1\" x 1\" x 1\";call for price;8
TF4751150;TotalFit Reducing Tee, 1\" x 1\" x ½\";call for price;10
TF4751175;TotalFit Reducing Tee, 1\" x 1\" x ¾\";call for price;10
TF4755050;TotalFit Tee, ½\" x ½\" x ½\";call for price;20
TF4757550;TotalFit Reducing Tee, ¾\" x ¾\" x ½\";call for price;14
TF4757555;TotalFit Reducing Tee, ¾\" x ½\" x ½\";call for price;15
TF4757575;TotalFit Tee, ¾\" x ¾\" x ¾\";call for price;12
TF4760500;TotalFit Elbow, ½\" x ½\";call for price;25
TF4760750;TotalFit Elbow, ¾\" x ¾\";call for price;15
TF4761000;TotalFit Elbow, 1\" x 1\";call for price;10
TF4771010;TotalFit Coupling, 1\" x 1\";call for price;15
TF4775050;TotalFit Coupling, ½\" x ½\";call for price;30
TF4775075;TotalFit Coupling, ½\" x ¾\";call for price;25
TF4777510;TotalFit Coupling, ¾\" x 1\";call for price;15
TF4777575;TotalFit Coupling, ¾\" x ¾\";call for price;18
TF4781010;TotalFit Repair Coupling, 1\" x 1\";call for price;9
TF4785050;TotalFit Repair Coupling, ½\" x ½\";call for price;24
TF4787575;TotalFit Repair Coupling, ¾\" x ¾\";call for price;12
TF4800500;TotalFit Removal Tool, ½\";call for price;40
TF4800750;TotalFit Removal Tool, ¾\";call for price;40
TF4801000;TotalFit Removal Tool, 1\";call for price;40
TF4808000;TotalFit Deburr and Depth Tool;call for price;6
WS4360750;ProPEX EP Straight Water Meter Fitting, ¾\" PEX x 1\" NPSM;18,45;1
WS4360751;ProPEX EP Elbow Water Meter Fitting, ¾\" PEX x 1\" NPSM;20,6;1
WS4361000;ProPEX EP Straight Water Meter Fitting, 1\" PEX x 1¼\" NPSM;21,2;1
WS4361001;ProPEX EP Elbow Water Meter Fitting, 1\" PEX x 1¼\" NPSM;23,95;1
WS4820750;ProPEX LF Brass Straight Water Meter Valve, ¾\" PEX x 1\" NPSM;48;1
WS4820751;ProPEX LF Brass Elbow Water Meter Valve, ¾\" PEX x 1\" NPSM;48;1
WS4821000;ProPEX LF Brass Straight Water Meter Valve, 1\" PEX x 1¼\" NPSM;66,8;1
WS4821001;ProPEX LF Brass Elbow Water Meter Valve, 1\" PEX x 1¼\" NPSM;66,8;1
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
