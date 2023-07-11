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
;OTHER COMPONENTS;A2870100;Spacer Ring VA31H for Thermal Actuators;8,7;10; 30 673 372 470 071 
;2023 New Products;Category;Part Number;Part Description; List Price;Pkg. Qty.;UPC
;FTGS & ACCS;1007355;H-Insulation Kit, 5.5\", 6.9\", 7.9\";2150;1; 673 372 211 468 
;FTGS & ACCS;1007357;Reducer Bushing 5.5\" to 2.7\";90,1;1; 673 372 211 475 
;FTGS & ACCS;1007358;Compression Wall Seal for 2.7\" Jacket;505;1; 673 372 236 362 
;FTGS & ACCS;1007360;Compression Wall Seal for 5.5\" Jacket;595;1; 673 372 236 379 
;FTGS & ACCS;1007361;Compression Wall Seal for 6.9\" Jacket;715;1; 673 372 236 386 
;FTGS & ACCS;1007362;Compression Wall Seal for 7.9\" Jacket;760;1; 673 372 236 393 
;FTGS & ACCS;1018245;Twin End Cap, 1\", 1¼\", 1½\" PEX Pipe with 5.5\" Jacket (25mm, 32mm and 40mm);140;1; 673 372 455 473 
;FTGS & ACCS;1018266;Wall Sleeve with Heat Shrink for 2.7\" Jacket;160;1; 673 372 236 287 
;FTGS & ACCS;1018268;Wall Sleeve with Heat Shrink for 6.9\" and 7.9\" Jackets;396;1; 673 372 236 317 
;FTGS & ACCS;1018269;Wall Sleeve with Heat Shrink for 5.5\" Jacket;354;1; 673 372 236 294 
;FTGS & ACCS;1018378;Uponor Shrinkable Tape 9\" x 9\' roll;239;1; 673 372 236 409 
;FTGS & ACCS;1018379;Vault Shrink Sleeve for 5.5\" Jacket;135;1; 673 372 236 416 
;FTGS & ACCS;1018381;Vault Shrink Sleeve for 7.9\" Jacket;160;1; 673 372 236 430 
;FTGS & ACCS;1021990;Tee Insulation Kit, 5.5\", 6.9\", 7.9\";1390;1; 673 372 211 482 
;FTGS & ACCS;1021991;Elbow Insulation Kit, 5.5\", 6.9\", 7.9\";1210;1; 673 372 211 499 
;FTGS & ACCS;1021992;Straight Insulation Kit, 5.5\", 6.9\", 7.9\";1180;1; 673 372 211 505 
;INS HTG PIPE;5012710;1\" Thermal Single with 2.7\" Jacket, 1,000-ft. coil;12,33;1; 673 372 341 875 
;INS HTG PIPE;5012775;¾\" Thermal Single with 2.7\" Jacket, 1,000-ft. coil;10,97;1; 673 372 312 875 
;INS HTG PIPE;5015510;1\" Thermal Single with 5.5\" Jacket, 600-ft. coil;37,72;1; 673 372 215 282 
;INS HTG PIPE;5015513;1¼\" Thermal Single with 5.5\" Jacket, 500-ft. coil;43,79;1; 673 372 215 268 
;INS HTG PIPE;5016915;1½\" Thermal Single with 6.9\" Jacket, 300-ft. coil;59,15;1; 673 372 215 275 
;INS HTG PIPE;5016920;2\" Thermal Single with 6.9\" Jacket, 300-ft. coil;67,61;1; 673 372 229 708 
;INS HTG PIPE;5016925;2½\" Thermal Single with 6.9\" Jacket, 300-ft. coil;76,81;1; 673 372 236 867 
;INS HTG PIPE;5017930;3\" Thermal Single with 7.9\" Jacket, 300-ft. coil;99,59;1; 673 372 241 878 
;INS HTG PIPE;5017940;4\" Thermal Single with 7.9\" Jacket, 300-ft. coil;127,49;1; 673 372 247 887 
;INS HTG PIPE;5025513;1¼\" Thermal Twin Jr. with 5.5\" Jacket, 600-ft. coil;29,26;1; 673 372 468 473 
;INS HTG PIPE;5026910;1\" Thermal Twin with 6.9\" Jacket, 600-ft. coil;52,56;1; 673 372 215 305 
;INS HTG PIPE;5026913;1¼\" Thermal Twin with 6.9\" Jacket, 500-ft. coil;57,68;1; 673 372 215 312 
;INS HTG PIPE;5026915;1½\" Thermal Twin with 6.9\" Jacket, 300-ft. coil;73,67;1; 673 372 215 299 
;INS HTG PIPE;5027920;2\" Thermal Twin with 7.9\" Jacket, 300-ft. coil;106,59;1; 673 372 229 562 
;INS HTG PIPE;5027925;2½\" Thermal Twin with 7.9\" Jacket, 300-ft. coil;134,81;1; 673 372 243 278 
;INS PLBG PIPE;5212710;1\" Potable PEX with 2.7\" Jacket, 1,000-ft. coil;12,33;1; 673 372 291 699 
;INS PLBG PIPE;5212775;¾\" Potable PEX with 2.7\" Jacket, 1,000-ft. coil;10,97;1; 673 372 291 279 
;INS PLBG PIPE;5215510;1\" Potable PEX with 5.5\" Jacket, 600-ft. coil;37,72;1; 673 372 242 073 
;INS PLBG PIPE;5215513;1¼\" Potable PEX with 5.5\" Jacket, 500-ft. coil;43,79;1; 673 372 242 271 
;INS PLBG PIPE;5216915;1½\" Potable PEX with 6.9\" Jacket, 300-ft. coil;59,04;1; 673 372 242 479 
;INS PLBG PIPE;5216920;2\" Potable PEX with 6.9\" Jacket, 300-ft. coil;65,73;1; 673 372 242 486 
;INS PLBG PIPE;5217930;3\" Potable PEX with 7.9\" Jacket, 300-ft. coil;99,59;1; 673 372 250 092 
;INS HTG PIPE;5226910;1\" Potable PEX Twin with 6.9\" Jacket, 600-ft. coil;52,56;1; 673 372 268 271 
;INS HTG PIPE;5226913;1¼\" Potable PEX Twin with 6.9\" Jacket, 500-ft. coil;57,68;1; 673 372 268 288 
;INS HTG PIPE;5226915;1½\" Potable PEX Twin with 6.9\" Jacket, 300-ft. coil;73,67;1; 673 372 268 295 
;INS HTG PIPE;5227920;2\" Potable PEX Twin with 7.9\" Jacket, 300-ft. coil;105,55;1; 673 372 268 301 
;FTGS & ACCS;5550040;WIPEX Fitting 4\" x 4\" NPT;342;1; 673 372 229 548 
;TOOLS;5550103;WIPEX Sleeve Pliers 3½\" - 4\";242,05;1; 673 372 232 678 
;FTGS & ACCS;5852710;End Cap, ¾\" and 1\" Pipe with 2.7\" Jacket;67,9;1; 673 372 229 586 
;FTGS & ACCS;5855513;End Cap, 1\" and 1¼\" PEX Pipe with 5.5\" Jacket;144;1; 673 372 224 673 
;FTGS & ACCS;5855520;End Cap, 1¼\", 1½\" and 2\" HDPE Pipe with 5.5\" Jacket;155;1; 673 372 225 878 
;FTGS & ACCS;5856930;End Cap, 1½\", 2\", 2½\" PEX and 3\" HDPE Pipe with 6.9\" Jacket;171;1; 673 372 224 680 
;FTGS & ACCS;5857940;End Cap 3\", 3½\", 4\" PEX and 4\" HDPE pipe, 7.9\" Jacket;193;1; 673 372 229 593 
;FTGS & ACCS;5956915;Twin End Cap, 1\", 1¼\" and 1½\" PEX Pipe with 6.9\" Jacket;196;1; 673 372 224 666 
;FTGS & ACCS;5957925;Twin End Cap, 2\" and 2½\" PEX Pipe with 7.9\" Jacket;226;1; 673 372 229 609 
;FTGS & ACCS;5992000;Heat-trace Power Terminal Block;472;1; 673 372 307 871 
;FTGS & ACCS;5993000;Heat-trace End Seal, SF-E;63;1; 673 372 307 673 
;FTGS & ACCS;5994000;Heat-trace Tee Splice, SF-T;478;1; 673 372 462 273 
;INS PLBG PIPE;54555513;1¼\" Potable PEX Plus with 5.5\" Jacket, 5 W/ft. 240VAC;61,34;1; 673 372 643 078 
;PEX A;A1140313;5/16\" Wirsbo hePEX, 100-ft. coil;154,02;1; 673 372 238 687 
;PEX A;A1140375;?\" Wirsbo hePEX, 100-ft. coil;166,26;1; 673 372 238 670 
;PEX A;A1140500;½\" Wirsbo hePEX, 100-ft. coil;154,02;1; 673 372 238 694 
;PEX A;A1140625;?\" Wirsbo hePEX, 100-ft. coil;206,04;1; 673 372 238 861 
;PEX A;A1140750;¾\" Wirsbo hePEX, 100-ft. coil;253,98;1; 673 372 238 878 
;PEX A;A1141000;1\" Wirsbo hePEX, 100-ft. coil;427,38;1; 673 372 238 885 
;PEX A;A1141250;1¼\" Wirsbo hePEX, 100-ft. coil;765;1; 673 372 203 067 
;PEX A;A1141500;1½\" Wirsbo hePEX, 100-ft. coil;1014,9;1; 673 372 208 277 
;PEX A;A1142000;2\" Wirsbo hePEX, 100-ft. coil;1591,2;1; 673 372 208 062 
;PEX A;A1180313;5/16\" Wirsbo hePEX, 250-ft. coil;382,5;1; 673 372 122 535 
;PEX A;A1210375;?\" Wirsbo hePEX, 400-ft. coil;673,2;1; 673 372 123 013 
;PEX A;A1210625;?\" Wirsbo hePEX, 400-ft. coil;826,2;1; 673 372 279 079 
;PEX A;A1220313;5/16\" Wirsbo hePEX, 1,000-ft. coil;1540,2;1; 673 372 123 020 
;PEX A;A1220375;?\" Wirsbo hePEX, 1,000-ft. coil;1662,6;1; 673 372 123 037 
;PEX A;A1220500;½\" Wirsbo hePEX, 1,000-ft. coil;1540,2;1; 673 372 123 044 
;PEX A;A1220625;?\" Wirsbo hePEX, 1,000-ft. coil;2060,4;1; 673 372 123 051 
;PEX A;A1220750;¾\" Wirsbo hePEX, 1,000-ft. coil;2539,8;1; 673 372 132 251 
;PEX A;A1240750;¾\" Wirsbo hePEX, 500-ft. coil;1275;1; 673 372 123 068 
;PEX A;A1241000;1\" Wirsbo hePEX, 500-ft. coil;2142;1; 673 372 123 075 
;PEX A;A1250500;½\" Wirsbo hePEX, 300-ft. coil;459;1; 673 372 123 082 
;PEX A;A1250625;?\" Wirsbo hePEX, 300-ft. coil;622,2;1; 673 372 123 099 
;PEX A;A1250750;¾\" Wirsbo hePEX, 300-ft. coil;765;1; 673 372 123 105 
;PEX A;A1251000;1\" Wirsbo hePEX, 300-ft. coil;1295,4;1; 673 372 123 112 
;PEX A;A1251250;1¼\" Wirsbo hePEX, 300-ft. coil;2295;1; 673 372 203 074 
;PEX A;A1251500;1½\" Wirsbo hePEX, 300-ft. coil;3029,4;1; 673 372 208 260 
;PEX A;A1252000;2\" Wirsbo hePEX, 300-ft. coil;4732,8;1; 673 372 207 461 
;PEX A;A1260500;½\" Wirsbo hePEX, 500-ft. coil;770,1;1; 673 372 123 129 
;PEX A;A1921000;1\" Wirsbo hePEX, 20-ft. straight length, 200 ft. (10 per bundle);948,6;1; 673 372 256 285 
;PEX A;A1921250;1¼\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);790,5;1; 673 372 203 081 
;PEX A;A1921500;1½\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);1050,6;1; 673 372 208 284 
;PEX A;A1922000;2\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);1642,2;1; 673 372 207 867 
;PEX A;A1922500;2½\" Wirsbo hePEX 20-ft. straight length, 60 ft.(3 per bundle);1295,4;1; 673 372 504 478 
;PEX A;A1923000;3\" Wirsbo hePEX 20-ft. straight length, 40 ft.(2 per bundle);1173;1; 673 372 504 485 
;PEX A;A1930500;½\" Wirsbo hePEX, 20-ft. straight length, 500 ft. (25 per bundle);846,6;1; 673 372 256 292 
;PEX A;A1930625;?\" Wirsbo hePEX, 20-ft. straight length, 300 ft. (15 per bundle);683,4;1; 673 372 256 476 
;PEX A;A1930750;¾\" Wirsbo hePEX, 20-ft. straight length, 300 ft. (15 per bundle);841,5;1; 673 372 256 278 
;FITTINGS METAL;A2080020;Brass Manifold Loop End Cap, R20;14,16;10; 30 673 372 118 898 
;FITTINGS METAL;A2080032;Basic End Cap, R32;28,74;10; 30 673 372 118 904 
;FITTINGS METAL;A2123210;Threaded Brass Manifold Bushing, R32 Male x 1\" Female NPT;25,03;10; 30 673 372 118 911 
;FITTINGS METAL;A2133275;Threaded Brass Manifold Bushing, R32 Male x ¾\" Female NPT;30,93;10; 30 673 372 128 651 
;MANIFOLDS METAL;A2400020;Brass Manifold Loop End Cap Gasket, spare part;4,34;10; 30 673 372 118 935 
;MANIFOLDS METAL;A2400032;Basic End Cap Gasket, spare part, R32;4,7;10; 30 673 372 118 942 
;FITTINGS METAL;A2402000;2\" Copper End Cap Spun End with drain and vent connections;220,5;1; 673 372 135 603 
;MOUNTING PARTS;A2603524;Manifold Wall Cabinet, 35.5\" H x 24\" W x 3.5\" D;444;1; 673 372 144 988 
;MOUNTING PARTS;A2603530;Manifold Wall Cabinet, 35.5\" H x 30.5\" W x 3.5\" D;494;1; 673 372 145 008 
;MOUNTING PARTS;A2603539;Manifold Wall Cabinet, 35.5\" H x 39\" W x 3.5\" D;540;1; 673 372 144 995 
;FITTINGS METAL;A2610020;TruFLOW Manifold Loop Temperature Gauge;51,8;10; 30 673 372 134 195 
;FITTINGS METAL;A2620090;TruFLOW Classic Manifold Elbow Union, R32 Union x 1¼\" BSP;32,6;10; 30 673 372 142 237 
;FITTINGS METAL;A2621010;TruFLOW Manifold Coupling Nipple, 1¼\" BSP x 1¼\" BSP;26,23;10; 30 673 372 134 133 
;FITTINGS METAL;A2631250;Manifold Supply and Return Ball Valves with Filter and Temperature Gauge, set of 2;345,9;1; 673 372 134 224 
;FITTINGS METAL;A2631251;Manifold Supply and Return Ball Valves with Temperature Gauges, set of 2;268,57;1; 673 372 308 670 
;FITTINGS METAL;A2631252;Manifold Supply and Return Ball Valves, set of 2;138;1; 673 372 308 878 
;FITTINGS METAL;A2640015;TruFLOW Visual Flow Meter, 0.15 to 0.8 gpm;49,12;10; 30 673 372 182 189 
;FITTINGS METAL;A2640027;TruFLOW Visual Flow Meter, 0.25 to 2.0 gpm;49,12;10; 30 673 372 182 196 
;MANIFOLDS PLASTIC;A2670001;EP Heating Manifold Single Section with Isolation Valve;43,96;1; 673 372 223 461 
;MANIFOLDS PLASTIC;A2670003;EP Heating Manifold Single Section with Balancing Valve and Flow Meter;61,1;1; 673 372 223 669 
;FITTINGS PLASTIC;A2670090;EP Heating Manifold Elbow, set of 2;49,47;1; 673 372 223 720 
;MANIFOLDS PLASTIC;A2670201;EP Heating Manifold Assembly with Flow Meter, 2-loop;395,76;1; 673 372 223 744 
;MANIFOLDS PLASTIC;A2670301;EP Heating Manifold Assembly with Flow Meter, 3-loop;457,98;1; 673 372 223 751 
;MANIFOLDS PLASTIC;A2670401;EP Heating Manifold Assembly with Flow Meter, 4-loop;545,7;1; 673 372 223 768 
;MANIFOLDS PLASTIC;A2670501;EP Heating Manifold Assembly with Flow Meter, 5-loop;632,4;1; 673 372 223 775 
;MANIFOLDS PLASTIC;A2670601;EP Heating Manifold Assembly with Flow Meter, 6-loop;708,9;1; 673 372 223 782 
;MANIFOLDS PLASTIC;A2670701;EP Heating Manifold Assembly with Flow Meter, 7-loop;765;1; 673 372 223 799 
;MANIFOLDS PLASTIC;A2670801;EP Heating Manifold Assembly with Flow Meter, 8-loop;877,2;1; 673 372 223 805 
;MANIFOLDS PLASTIC;A2671300;EP Heating Manifold Actuator Adapter;7,91;10; 30 673 372 227 064 
;MANIFOLDS METAL;A2700202;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 2 loops;461;1; 673 372 404 679 
;MANIFOLDS METAL;A2700302;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 3 loops;540;1; 673 372 404 686 
;MANIFOLDS METAL;A2700402;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 4 loops;645;1; 673 372 404 693 
;MANIFOLDS METAL;A2700502;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 5 loops;735;1; 673 372 404 709 
;MANIFOLDS METAL;A2700602;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 6 loops;835;1; 673 372 404 716 
;MANIFOLDS METAL;A2700702;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 7 loops;900;1; 673 372 404 723 
;MANIFOLDS METAL;A2700802;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 8 loops;1030;1; 673 372 404 730 
;MANIFOLDS METAL;A2701002;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 10 loops;1290;1; 673 372 404 747 
;MANIFOLDS METAL;A2701202;Stainless-steel Manifold Assembly, 1\" with flow meter, B&I, ball valve, 12 loops;1510;1; 673 372 404 754 
;MANIFOLDS METAL;A2720202;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 2 loops;520;1; 673 372 404 761 
;MANIFOLDS METAL;A2720302;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 3 loops;655;1; 673 372 404 778 
;MANIFOLDS METAL;A2720402;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 4 loops;785;1; 673 372 404 877 
;MANIFOLDS METAL;A2720502;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 5 loops;935;1; 673 372 404 884 
;MANIFOLDS METAL;A2720602;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 6 loops;1070;1; 673 372 404 891 
;MANIFOLDS METAL;A2720702;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 7 loops;1190;1; 673 372 404 907 
;MANIFOLDS METAL;A2720802;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 8 loops;1380;1; 673 372 404 914 
;MANIFOLDS METAL;A2721002;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 10 loops;1690;1; 673 372 404 921 
;MANIFOLDS METAL;A2721202;Stainless-steel Manifold Assembly, 1¼\" with flow meter, B&I, ball valve, 12 loops;1940;1; 673 372 404 938 
New;MANIFOLDS METAL;A2740302;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 3 loops;1910,01;1; 673 372 756 488 
New;MANIFOLDS METAL;A2740402;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 4 loops;2088,01;1; 673 372 756 495 
New;MANIFOLDS METAL;A2740502;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 5 loops;2322;1; 673 372 756 501 
New;MANIFOLDS METAL;A2740602;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 6 loops;2510,01;1; 673 372 756 518 
New;MANIFOLDS METAL;A2740702;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 7 loops;2789,01;1; 673 372 756 525 
New;MANIFOLDS METAL;A2740802;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 8 loops;3001;1; 673 372 756 532 
New;MANIFOLDS METAL;A2741002;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 10 loops;3266,01;1; 673 372 756 549 
New;MANIFOLDS METAL;A2741202;Commercial Stainless-steel Manifold Assembly, 1 ½\" with Flow Meter & Ball Valve, 12 loops;3702;1; 673 372 756 556 
;FITTINGS METAL;A2771035;O-ring for Stainless-steel Manifold Isolation Valve Body;12,75;10; 30 673 372 405 127 
;OTHER COMPONENTS;A2771050;Stainless-steel Manifold Temperature Gauge, set of 2;44,3;1; 673 372 405 140 
;OTHER COMPONENTS;A2771060;Spacer Ring VA10 for Thermal Actuators;2,34;5; 30 673 372 405 271 
;FITTINGS METAL;A2771251;Stainless-steel Manifold Supply and Return 1\" FNPT Ball Valve with Temperature Gauge, set of 2;130,63;1; 673 372 404 945 
;FITTINGS METAL;A2771252;Stainless-steel Manifold Supply and Return 1¼\" FNPT Ball Valve with Temperature Gauge, set of 2;178,7;1; 673 372 404 952 
New;FITTINGS METAL;A2791000;Commercial Stainless-steel Manifold Loop Cap;21;12; 30 673 372 756 625 
New;FITTINGS METAL;A2791515;Commercial Stainless-steel Manifold ProPEX Male Elbow Adapter, 1 ½\" PEX x 1 ½\" NPT;61,1;2; 30 673 372 756 595 
;FITTINGS METAL;A2803250;End Cap with Vent, R32;114,95;1; 673 372 119 092 
;CONTROLS;A3010100;Single-zone Pump Relay;185;1; 673 372 119 139 
;CONTROLS;A3011075;¾\" and 1\" Thermal Zone Valve;223;1; 673 372 478 274 
;MOUNTING PARTS;A3019900;Spacer Ring VA33 for White Thermal Actuators;8,7;5; 30 673 372 275 478 
;CONTROLS;A3023522;Thermal Actuator, four-wire;127;1; 673 372 477 475 
;CONTROLS;A3030522;Two-wire Thermal Actuator for EP Heating Manifolds;78,7;1; 673 372 210 317 
;CONTROLS;A3030523;Two-wire Thermal Actuator for TruFLOW Classic and Jr. Valved Manifolds;83,9;1; 673 372 210 362 
;CONTROLS;A3030524;Two-wire Thermal Actuator for Stainless-steel Manifolds;79,4;1; 673 372 502 870 
;CONTROLS;A3031003;Three-zone Control Module for Two and Four-wire Operation;170;1; 673 372 296 878 
;CONTROLS;A3031004;Four-zone Control Module for Two and Four-wire Operation;189;1; 673 372 296 885 
;CONTROLS;A3040073;Slab Sensor for Aerial Snow Sensor;474;1; 673 372 469 876 
;CONTROLS;A3040090;Pavement Snow and Ice Sensor;1850;1; 673 372 130 202 
;CONTROLS;A3040091;Pavement Snow and Ice Sensor Cup;425;1; 673 372 130 189 
;CONTROLS;A3040095;Aerial Snow Sensor;440;1; 673 372 469 678 
;CONTROLS;A3040521;SetPoint 521, Programmable Thermostat with floor sensor;472;1; 673 372 512 329 
;CONTROLS;A3040654;Single-zone Snow Melt Control;1290;1; 673 372 469 074 
;CONTROLS;A3050050;50 VA Transformer;64,9;1; 673 372 119 290 
;CONTROLS;A3080301;Three-zone Multi-pump Relay;461;1; 673 372 119 351 
;CONTROLS;A3080404;Powered Four-zone Controller;352;1; 673 372 138 963 
;CONTROLS;A3080406;Powered Six-zone Controller;452;1; 673 372 138 956 
;CONTROLS;A3100101;Heat-only Thermostat with Touchscreen;198;1; 673 372 533 676 
New;CONTROLS;A3800161;Smatrix Pulse Mini Sensor (T-161);101;1; 673 372 756 082 
;CONTROLS;A3800165;Wireless Dial Thermostat (T-165);92,4;1; 673 372 549 677 
;CONTROLS;A3800167;Wireless Digital Thermostat (T-167);144;1; 673 372 549 684 
New;CONTROLS;A3800169;Smatrix Pulse Digital Thermostat (T-169);152;1; 673 372 756 075 
;CONTROLS;A3801160;Wireless Base Unit Expansion Module, 6 zones (M-160);137;1; 673 372 549 691 
;CONTROLS;A3801165;Wireless Base Unit, 6 zones (X-165);433;1; 673 372 549 707 
New;CONTROLS;A3801262;Smatrix Pulse Expansion Module (M-262);152;1; 673 372 757 317 
New;CONTROLS;A3801263;Smatrix Pulse Relay Module (M-263);152;1; 673 372 757 331 
New;CONTROLS;A380265A;Smatrix Pulse Controller (X-265) with Antenna (A-265);515;1; 673 372 757 287 
New;CONTROLS;A380265C;Smatrix Pulse Controller (X-265) with Communication Module (R-208);770;1; 673 372 757 294 
;FITTINGS METAL;A4010313;5/16\" Repair Coupling;38,77;10; 30 673 372 132 306 
;FITTINGS METAL;A4020313;5/16\" QS-style Compression Fitting Assembly, R20 thread;23,36;10; 30 673 372 118 201 
;FITTINGS METAL;A4020375;?\" QS-style Compression Fitting Assembly, R20 thread;22,52;10; 30 673 372 118 218 
;FITTINGS METAL;A4020500;½\" QS-style Compression Fitting Assembly, R20 thread;18,18;10; 30 673 372 118 225 
;FITTINGS METAL;A4020625;?\" QS-style Compression Fitting Assembly, R20 thread;22,05;10; 30 673 372 118 232 
;FITTINGS METAL;A4020750;¾\" QS-style Compression Fitting Assembly, R25 thread;30,41;10; 30 673 372 118 249 
;FITTINGS METAL;A4030625;?\" QS-style Compression Fitting Assembly, R25 thread;24,45;10; 30 673 372 168 077 
New;FITTINGS METAL;A4050625;?\" QS-style Compression Fitting Assembly for Commercial Manifold, R25 thread;31,9;10; 30 673 372 752 504 
New;FITTINGS METAL;A4050750;¾\" QS-style Compression Fitting Assembly for Commercial Manifold, R25 thread;34,65;10; 30 673 372 752 511 
;FITTINGS METAL;A4123215;Brass Manifold Adapter, R32 to 1¼\" Adapter or 1½\" Fitting Adapter;63,75;10; 30 673 372 309 487 
;FITTINGS METAL;A4133210;Brass Manifold Adapter, R32 x 1\" Adapter or 1¼\" Fitting Adapter;35,53;10; 30 673 372 118 270 
;FITTINGS METAL;A4143210;Brass Manifold Adapter, R32 x ¾\" Adapter or 1\" Fitting Adapter;42,11;10; 30 673 372 118 287 
;FITTINGS METAL;A4322020;QS-style Coupling Nipple, R20 x R20;15,99;10; 30 673 372 118 348 
;FITTINGS METAL;A4322050;QS-style Conversion Nipple, R20 x ½\" NPT;15,99;10; 30 673 372 118 355 
;FITTINGS METAL;A4322075;QS-style Conversion Nipple, R20 x ¾\" NPT;16,56;10; 30 673 372 116 757 
;FITTINGS METAL;A4332050;QS-style Copper Adapter, R20 x ½\" Copper;17,03;10; 30 673 372 116 795 
;FITTINGS METAL;A4332075;QS-style Copper Adapter, R20 x ¾\" Copper;13,32;10; 30 673 372 116 801 
;FITTINGS METAL;A4332575;QS-style Copper Adapter, R25 x ¾\" Copper (for ¾\" and ?\" tubing only);29,57;10; 30 673 372 116 818 
;FITTINGS METAL;A4342050;QS-style Copper Fitting Adapter, R20 x ½\" Copper;16,93;10; 30 673 372 116 825 
;FITTINGS METAL;A4342510;QS-style Copper Fitting Adapter, R25 X 1\" Copper (for ¾\" and ?\" tubing only);17,61;10; 30 673 372 128 910 
;PANELS;A5060701;Quik Trak 7\" x 48\" Panels;24,42;10; 30 673 372 116 887 
;PANELS;A5060702;Quik Trak 7\" x 48\" Return Panels;32,45;10; 30 673 372 116 894 
;PANELS;A5060712;Quik Trak 12\" x 48\" Combo Panel, 6 runs with return;74,36;5; 30 673 372 212 114 
;PANELS;A5060722;Quik Trak 12\" x 12\" Combo 90, 6 runs;20,68;5; 30 673 372 212 107 
;PANELS;A5060732;Quik Trak 7\" x 12\" Combo Access Panel, 6 runs with 1 access;19,91;6; 30 673 372 212 091 
;PANELS;A5060761;Quik Trak 7\" x 48\" x 6 Panels (fully assembled set);158,7;1; 673 372 125 734 
New;PANELS;A5070641;Xpress Trak Radiant Panel, 6\" o.c., 4 runs;118;14; 30 673 372 769 076 
;PANELS;A5080375;Joist Trak, ?\" Heat Transfer Panel;17,55;20; 30 673 372 129 849 
;PANELS;A5080500;Joist Trak, ½\" Heat Transfer Panel;17,55;20; 30 673 372 129 825 
;PANELS;A5090313;Fast Trak 0.5;37,9;20; 30 673 372 273 894 
;PANELS;A5090500;Fast Trak 1.3i;42,6;18; 30 673 372 273 870 
;PANELS;A5091000;Fast Trak Edge Strip, 65-ft. roll;47;10; 30 673 372 273 887 
;MOUNTING PARTS;A5110375;?\" Metal Bend Support;3,48;50; 30 673 372 116 955 
;MOUNTING PARTS;A5110500;½\" Metal Bend Support;3,36;50; 30 673 372 116 962 
;MOUNTING PARTS;A5110625;?\" Metal Bend Support;4,32;50; 30 673 372 116 979 
;MOUNTING PARTS;A5110750;¾\" Metal Bend Support;6,3;25; 30 673 372 116 986 
;MOUNTING PARTS;A5150375;?\" Plastic Bend Support;2,34;25; 30 673 372 117 884 
;MOUNTING PARTS;A5150500;½\" Plastic Bend Support (not for use with wall support bracket A5750500);2,46;25; 30 673 372 117 891 
New;MOUNTING PARTS;A5150745;¾\" 45-degree Plastic Bend Support;4,6;50; 30 673 372 732 179 
;MOUNTING PARTS;A5150750;¾\" Plastic Bend Support;5,45;50; 30 673 372 117 907 
;MOUNTING PARTS;A5250500;½\" Plastic Bend Support;2,46;25; 30 673 372 212 466 
New;MOUNTING PARTS;A5250545;½\" 45-degree Plastic Bend Support;3,2;25; 30 673 372 732 162 
;CONTROLS;A5402112;1\" Thermal Mixing Valve with Union;214;1; 673 372 524 278 
;MOUNTING PARTS;A5500500;¾\" PVC Elbow for ?\" and ½\" PEX Bend Support;4,77;25; 30 673 372 118 065 
;MOUNTING PARTS;A5500625;1\" PVC Elbow for ?\" PEX Bend Support;6,35;25; 30 673 372 118 072 
;MOUNTING PARTS;A5500750;1¼\" PVC Elbow for ¾\" PEX Bend Support;13,4;20; 30 673 372 118 089 
;MOUNTING PARTS;A5501000;1½\" PVC Elbow for 1\" PEX Bend Support;14,8;25; 30 673 372 118 096 
;MOUNTING PARTS;A5700500;½\" PEX Rail, 6.5 ft.;16,55;16; 30 673 372 118 119 
;MOUNTING PARTS;A5700625;?\" PEX Rail, 6.5 ft.;15,9;16; 30 673 372 116 511 
;MOUNTING PARTS;A5700750;¾\" PEX Rail, 6.5 ft.;25,1;16; 30 673 372 116 528 
;MOUNTING PARTS;A5750001;Mounting Bracket for ?\" to 1\" Water Meters;14,15;1; 673 372 551 274 
;MOUNTING PARTS;A5750500;PEX Wall Support Bracket, ½\" and ¾\";8,85;25; 50 673 372 203 864 
;FITTINGS METAL;A5802575;Ball Valve, R25 Thread x ¾\" Copper Adapter;51,9;10; 30 673 372 145 528 
;FITTINGS METAL;A5902075;Ball and Balancing Valve, R20 Thread x ¾\" Copper Adapter;93,32;10; 30 673 372 142 794 
;FITTINGS METAL;A5902575;Ball and Balancing Valve, R25 Thread x ¾\" Copper Adapter;93,8;10; 30 673 372 145 542 
;PEX A;A6140500;½\" Pre-insulated Wirsbo hePEX with ½\" insulation, 100-ft. coil;535,6;1; 673 372 501 484 
;PEX A;A6140750;¾\" Pre-insulated Wirsbo hePEX with ½\" insulation, 100-ft. coil;655,2;1; 673 372 507 486 
;PEX A;A6141000;1\" Pre-insulated Wirsbo hePEX with ½\" insulation, 100-ft. coil;790,4;1; 673 372 317 870 
;PEX A;A6150750;¾\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;960,75;1; 673 372 321 075 
;PEX A;A6151000;1\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;1176;1; 673 372 507 509 
;PEX A;A6151250;1¼\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;1680;1; 673 372 507 516 
;PEX A;A6160750;¾\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 100-ft. coil;1378;1; 673 372 508 094 
;PEX A;A6161000;1\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 100-ft. coil;1600,6;1; 673 372 318 075 
;PEX A;A6161250;1¼\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 100-ft. coil;2162,4;1; 673 372 508 100 
;PEX A;A6161500;1½\" Pre-insulated Wirsbo hePEX with 1½\" insulation, 75-ft. coil;1971,6;1; 673 372 507 523 
;MOUNTING PARTS;A7012000;2\" Blue Foam Staples, 300/pkg.;76;1; 673 372 455 886 
;MOUNTING PARTS;A7015050;1½\" Plastic Foam Staples, 300/pkg.;132;1; 673 372 116 565 
;MOUNTING PARTS;A7015075;2½\" Plastic Foam Staples, 300/pkg.;151;1; 673 372 116 572 
;MOUNTING PARTS;A7031000;Fixing Wire, 1,000/bundle;39,8;1; 673 372 116 589 
;MOUNTING PARTS;A7250500;Tube Clamp Suspension (½ PEX), 100/pkg.;61,4;1; 673 372 159 494 
;MOUNTING PARTS;A7250750;Tube Clamp Suspension (¾ PEX), 50/pkg.;31,3;1; 673 372 159 500 
;MOUNTING PARTS;A7350500;Tube Clamp Standard (½ PEX), 100/pkg.;48,7;1; 673 372 159 517 
;MOUNTING PARTS;A7350750;Tube Clamp Standard (¾ PEX), 50/pkg.;25,6;1; 673 372 159 524 
;MOUNTING PARTS;A7750700;Fire Sprinkler Adapter Mounting Bracket, ¾\" and 1\";11,8;5; 30 673 372 246 119 
;CONTROLS;A9010599;Slab Sensor, 10k;61,8;1; 673 372 175 098 
;MANIFOLDS PLASTIC;B2253751;3\" x 10\' HDPE Valveless Manifold (12\" o.c.), 10 outlet, ¾\" ProPEX;1560;1; 673 372 103 237 
;MANIFOLDS PLASTIC;B2253752;3\" x 20\' HDPE Valveless Manifold (12\" o.c.), 20 outlet, ¾\" ProPEX;3100;1; 673 372 103 244 
;MANIFOLDS PLASTIC;B2254751;4\" x 10\' HDPE Valveless Manifold (12\" o.c.), 10 outlet, ¾\" ProPEX;1630;1; 673 372 103 251 
;MANIFOLDS PLASTIC;B2254752;4\" x 20\' HDPE Valveless Manifold (12\" o.c.), 20 outlet, ¾\" ProPEX;3370;1; 673 372 103 268 
;MANIFOLDS PLASTIC;B2273101;3\" x 10\' HDPE Valveless Manifold (12\" o.c.), 10 outlet, 1\" ProPEX;1850;1; 673 372 103 299 
;MANIFOLDS PLASTIC;B2273102;3\" x 20\' HDPE Valveless Manifold (12\" o.c.), 20 outlet, 1\" ProPEX;3680;1; 673 372 103 305 
;MANIFOLDS PLASTIC;B2274101;4\" x 10\' HDPE Valveless Manifold (12\" o.c.), 10 outlet, 1\" ProPEX;1920;1; 673 372 103 312 
;MANIFOLDS PLASTIC;B2274102;4\" x 20\' HDPE Valveless Manifold (12\" o.c.), 20 outlet, 1\" ProPEX;3820;1; 673 372 103 329 
;FITTINGS METAL;CP4501300;ProPEX LF Brass x CPVC Spigot Adapter Kit, 1¼\" PEX x 1¼\" CPVC (IPS or CTS);91,5;1; 673 372 511 278 
;FITTINGS METAL;CP4501313;ProPEX LF Brass x CPVC Spigot Adapter, 1¼\" PEX x 1¼\" CPVC (CTS);86,8;1; 673 372 333 276 
;FITTINGS METAL;CP4501500;ProPEX LF Brass x CPVC Spigot Adapter Kit, 1½\" PEX x 1½\" CPVC (IPS or CTS);119;1; 673 372 511 285 
;FITTINGS METAL;CP4501515;ProPEX LF Brass x CPVC Spigot Adapter, 1½\" PEX x 1½\" CPVC (CTS);113;1; 673 372 333 474 
;FITTINGS METAL;CP4502000;ProPEX LF Brass x CPVC Spigot Adapter Kit, 2\" PEX x 2\" CPVC (IPS or CTS);191;1; 673 372 511 292 
;FITTINGS METAL;CP4502020;ProPEX LF Brass x CPVC Spigot Adapter, 2\" PEX x 2\" CPVC (CTS);184;1; 673 372 333 672 
;FITTINGS METAL;CP4511313;ProPEX LF Brass x CPVC Socket Adapter, 1¼\" PEX x 1¼\" CPVC (CTS);86,8;1; 673 372 335 072 
;FITTINGS METAL;CP4511515;ProPEX LF Brass x CPVC Socket Adapter, 1½\" PEX x 1½\" CPVC (CTS);113;1; 673 372 335 270 
;FITTINGS METAL;CP4512020;ProPEX LF Brass x CPVC Socket Adapter, 2\" PEX x 2\" CPVC (CTS);184;1; 673 372 335 478 
;TOOLS;E6025000;PEX Foam Stapler;916,7;1; 673 372 455 879 
;TOOLS;E6050010;Quik Trak Sealant, 10.3 fluid oz. (300 ml);23,29;24; 30 673 372 118 485 
;TOOLS;E6051250;Quik Trak Screws (1¼\"), 2,500/pkg.;367,4;1; 673 372 118 507 
;TOOLS;E6061000;Tube Uncoiler;858;1; 673 372 118 514 
;TOOLS;E6062000;Select Uncoiler;4950;1; 673 372 135 597 
;TOOLS;E6081125;Tube Cutter (metal) for up to 1\" PEX;57,68;1; 673 372 118 521 
;TOOLS;E6081128;Tube Cutter (plastic) for up to 1\" PEX;52,9;1; 673 372 133 593 
;TOOLS;E6083000;Ratchet-style PEX Pipe Cutter, 1¼\" - 3\";762,2;1; 673 372 513 272 
;TOOLS;E6090005;Fixing Wire Twister;9,32;1; 673 372 118 576 
;TOOLS;E6091700;Ratchet-style Fixing Wire Twister;111,24;1; 673 372 118 583 
;TOOLS;E6122000;Manifold Pressure Test Kit;109,18;1; 673 372 124 447 
;PEX A;F1021250;1¼\" Uponor AquaPEX White, 300-ft. coil;1940;1; 673 372 132 282 
;PEX A;F1021500;1½\" Uponor AquaPEX White, 300-ft. coil;2260;1; 673 372 132 299 
;PEX A;F1022000;2\" Uponor AquaPEX White, 300-ft. coil;4510;1; 673 372 204 262 
;PEX A;F1023000;3\" Uponor AquaPEX White, 300-ft. coil;7990;1; 673 372 248 877 
;OTHER COMPONENTS;F1035400;½\" HDPE Corrugated Sleeve, Red, 400-ft. coil;288;1; 673 372 189 040 
;OTHER COMPONENTS;F1037400;¾\" HDPE Corrugated Sleeve, Red, 400 ft.;412;1; 673 372 208 673 
;PEX A;F1040250;¼\" Uponor AquaPEX White, 100-ft. coil;81,1;1; 673 372 122 368 
;PEX A;F1040500;½\" Uponor AquaPEX White, 100-ft. coil;93,8;1; 673 372 122 382 
;PEX A;F1040750;¾\" Uponor AquaPEX White, 100-ft. coil;162;1; 673 372 122 399 
;PEX A;F1041000;1\" Uponor AquaPEX White, 100-ft. coil;291;1; 673 372 122 405 
;PEX A;F1052000;2\" Uponor AquaPEX White, 200-ft. coil;3010;1; 673 372 204 460 
;OTHER COMPONENTS;F1055400;½\" HDPE Corrugated Sleeve, Blue, 400-ft. coil;288;1; 673 372 189 057 
;OTHER COMPONENTS;F1057400;¾\" HDPE Corrugated Sleeve, Blue, 400 ft.;412;1; 673 372 208 666 
;PEX A;F1060500;½\" Uponor AquaPEX White, 300-ft. coil;282;1; 673 372 122 412 
;PEX A;F1060502;½\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;288;1; 673 372 238 069 
;PEX A;F1060625;?\" Uponor AquaPEX White, 300-ft. coil;420;1; 673 372 122 429 
;PEX A;F1060750;¾\" Uponor AquaPEX White, 300-ft. coil;483;1; 673 372 122 436 
;PEX A;F1060752;¾\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;492;1; 673 372 238 267 
;PEX A;F1061000;1\" Uponor AquaPEX White, 300-ft. coil;875;1; 673 372 122 443 
;PEX A;F1061002;1\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;925;1; 673 372 238 274 
;PEX A;F1061250;1¼\" Uponor AquaPEX White, 100-ft. coil;650;1; 673 372 122 450 
;PEX A;F1061500;1½\" Uponor AquaPEX White, 100-ft. coil;755;1; 673 372 122 467 
;PEX A;F1062000;2\" Uponor AquaPEX White, 100-ft. coil;1510;1; 673 372 195 249 
;PEX A;F1062500;2½\" Uponor AquaPEX White, 100-ft. coil;1980;1; 673 372 452 274 
;PEX A;F1063000;3\" Uponor AquaPEX White, 100-ft. coil;2670;1; 673 372 249 072 
;PEX A;F1090375;?\" Uponor AquaPEX White, 400-ft. coil;316;1; 673 372 115 742 
;PEX A;F1091500;½\" Pre-sleeved Uponor AquaPEX Blue Sleeve, 400-ft. coil;645;1; 673 372 189 453 
;PEX A;F1091750;¾\" Pre-Sleeved Uponor AquaPEX Blue Sleeve, 400-ft. coil;990;1; 673 372 211 093 
;PEX A;F1092500;½\" Pre-sleeved Uponor AquaPEX Red Sleeve, 400-ft. coil;645;1; 673 372 189 460 
;PEX A;F1092750;¾\" Pre-Sleeved Uponor AquaPEX Red Sleeve, 400-ft. coil;990;1; 673 372 211 109 
;PEX A;F1100500;½\" Uponor AquaPEX White, 500-ft. coil;469;1; 673 372 115 759 
;PEX A;F1100750;¾\" Uponor AquaPEX White, 500-ft. coil;810;1; 673 372 115 766 
;PEX A;F1101000;1\" Uponor AquaPEX White, 500-ft. coil;1470;1; 673 372 115 773 
;PEX A;F1120375;?\" Uponor AquaPEX White, 1,000-ft. coil;835;1; 673 372 115 780 
;PEX A;F1120500;½\" Uponor AquaPEX White, 1,000-ft. coil;940;1; 673 372 115 797 
;PEX A;F1120625;?\" Uponor AquaPEX White, 1,000-ft. coil;1420;1; 673 372 115 803 
;PEX A;F1911256;1¼\" Uponor AquaPEX Purple Reclaimed Water, 10-ft. straight length, 50 ft. (5 per bundle);398;1; 673 372 516 877 
;PEX A;F1921000;1\" Uponor AquaPEX White, 20-ft. straight length, 200 ft. (10 per bundle);635;1; 673 372 115 810 
;PEX A;F1921002;1\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 200 ft. (10 per bundle);785;1; 673 372 440 479 
;PEX A;F1921250;1¼\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);670;1; 673 372 115 827 
;PEX A;F1921500;1½\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);780;1; 673 372 115 834 
;PEX A;F1922000;2\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);1560;1; 673 372 183 055 
;PEX A;F1922500;2½\" Uponor AquaPEX White, 20-ft. straight length, 60 ft. (3 per bundle);1230;1; 673 372 452 298 
;PEX A;F1923000;3\" Uponor AquaPEX White, 20-ft. straight length, 40 ft. (2 per bundle);1110;1; 673 372 249 270 
;PEX A;F1930500;½\" Uponor AquaPEX White, 20-ft. straight length, 500 ft. (25 per bundle);515;1; 673 372 115 841 
;PEX A;F1930750;¾\" Uponor AquaPEX White, 20-ft. straight length, 300 ft. (15 per bundle);530;1; 673 372 115 858 
;PEX A;F1961002;1\" Uponor AquaPEX Purple Reclaimed Water, 10-ft. straight length, 100 ft. (10 per bundle);385;1; 673 372 516 679 
;PEX A;F1961256;1¼\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);715;1; 673 372 516 884 
;PEX A;F1961502;1½\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);920;1; 673 372 517 072 
;PEX A;F1962002;2\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);1840;1; 673 372 517 102 
;PEX A;F2040500;½\" Uponor AquaPEX Red, 100-ft. coil;103;1; 673 372 150 385 
;PEX A;F2040750;¾\" Uponor AquaPEX Red, 100-ft. coil;180;1; 673 372 154 352 
;PEX A;F2041000;1\" Uponor AquaPEX Red, 100-ft. coil;319;1; 673 372 154 444 
;PEX A;F2060500;½\" Uponor AquaPEX Red, 300-ft. coil;309;1; 673 372 150 378 
;PEX A;F2060750;¾\" Uponor AquaPEX Red, 300-ft. coil;535;1; 673 372 154 376 
;PEX A;F2061000;1\" Uponor AquaPEX Red, 300-ft. coil;960;1; 673 372 154 451 
;PEX A;F2120500;½\" Uponor AquaPEX Red, 1,000-ft. coil;1030;1; 673 372 150 361 
;MANIFOLDS METAL;F2801575;1½\" x 6\' Copper Valveless Manifold with 24 outlets, ¾\" sweat;810;1; 673 372 117 654 
;MANIFOLDS METAL;F2802075;2\" x 6\' Copper Valveless Manifold with 24 outlets, ¾\" sweat;1170;1; 673 372 117 661 
;MANIFOLDS METAL;F2811220;2\" x 4\' Copper Valved Manifold with R20 Threaded Ball Valves, 12 outlets;1400;1; 673 372 133 654 
;MANIFOLDS METAL;F2821220;2\" x 4\' Copper Valved Manifold with R20 Threaded Ball and Balancing Valves, 12 outlets;2390;1; 673 372 133 845 
;MANIFOLDS METAL;F2821225;2\" x 4\' Copper Valved Manifold with R25 Threaded Ball and Balancing Valves, 12 outlets;2060;1; 673 372 133 784 
;PEX A;F2921000;1\" Uponor AquaPEX Red, 20-ft. straight length, 200 ft. (10 per bundle);715;1; 673 372 154 437 
;PEX A;F2930500;½\" Uponor AquaPEX Red, 20-ft. straight length, 500 ft. (25 per bundle);575;1; 673 372 154 307 
;PEX A;F2930750;¾\" Uponor AquaPEX Red, 20-ft. straight length, 300 ft. (15 per bundle);595;1; 673 372 154 383 
;PEX A;F3040500;½\" Uponor AquaPEX Blue, 100-ft. coil;103;1; 673 372 154 291 
;PEX A;F3040750;¾\" Uponor AquaPEX Blue, 100-ft. coil;180;1; 673 372 154 345 
;PEX A;F3041000;1\" Uponor AquaPEX Blue, 100-ft. coil;319;1; 673 372 154 420 
;PEX A;F3060500;½\" Uponor AquaPEX Blue, 300-ft. coil;309;1; 673 372 154 031 
;PEX A;F3060750;¾\" Uponor AquaPEX Blue, 300-ft. coil;535;1; 673 372 154 338 
;PEX A;F3061000;1\" Uponor AquaPEX Blue, 300-ft. coil;960;1; 673 372 154 413 
;PEX A;F3120500;½\" Uponor AquaPEX Blue, 1,000-ft. coil;1030;1; 673 372 154 284 
;PEX A;F3921000;1\" Uponor AquaPEX Blue, 20-ft. straight length, 200 ft. (10 per bundle);715;1; 673 372 154 390 
;PEX A;F3930500;½\" Uponor AquaPEX Blue, 20-ft. straight length, 500 ft. (25 per bundle);575;1; 673 372 154 277 
;PEX A;F3930750;¾\" Uponor AquaPEX Blue, 20-ft. straight length, 300 ft. (15 per bundle);595;1; 673 372 154 314 
;PEX A;F4220500;½\" Uponor AquaPEX White, Red Print, 1,000-ft. coil;940;1; 673 372 725 873 
;PEX A;F4240500;½\" Uponor AquaPEX White, Red Print, 100-ft. coil;93,8;1; 673 372 505 925 
;PEX A;F4240750;¾\" Uponor AquaPEX White, Red Print, 100-ft. coil;162;1; 673 372 505 987 
;PEX A;F4241000;1\" Uponor AquaPEX White, Red Print, 100-ft. coil;291;1; 673 372 506 113 
;PEX A;F4260500;½\" Uponor AquaPEX White, Red Print, 300-ft. coil;282;1; 673 372 505 932 
;PEX A;F4260750;¾\" Uponor AquaPEX White, Red Print, 300-ft. coil;483;1; 673 372 505 994 
;PEX A;F4261000;1\" Uponor AquaPEX White, Red Print, 300-ft. coil;875;1; 673 372 506 120 
;PEX A;F4320500;½\" Uponor AquaPEX White, Blue Print, 1,000-ft. coil;940;1; 673 372 725 880 
;PEX A;F4340500;½\" Uponor AquaPEX White, Blue Print, 100-ft. coil;93,8;1; 673 372 505 895 
;PEX A;F4340750;¾\" Uponor AquaPEX White, Blue Print, 100-ft. coil;162;1; 673 372 505 956 
;PEX A;F4341000;1\" Uponor AquaPEX White, Blue Print, 100-ft. coil;291;1; 673 372 506 083 
;PEX A;F4360500;½\" Uponor AquaPEX White, Blue Print, 300-ft. coil;282;1; 673 372 505 901 
;PEX A;F4360750;¾\" Uponor AquaPEX White, Blue Print, 300-ft. coil;483;1; 673 372 505 963 
;PEX A;F4361000;1\" Uponor AquaPEX White, Blue Print, 300-ft. coil;875;1; 673 372 506 090 
;PEX A;F4920500;½\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 500-ft. (25 per bundle);515;1; 673 372 505 918 
;PEX A;F4920750;¾\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 300-ft. (15 per bundle);530;1; 673 372 505 970 
;PEX A;F4921000;1\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 200-ft. (10 per bundle);635;1; 673 372 506 106 
;PEX A;F4930500;½\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 500-ft. (25 per bundle);515;1; 673 372 505 888 
;PEX A;F4930750;¾\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 300-ft. (15 per bundle);530;1; 673 372 505 949 
;PEX A;F4931000;1\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 200-ft. (10 per bundle);635;1; 673 372 506 076 
;MOUNTING PARTS;F5120375;?\" Metal Drop Ear Bend Support;8,4;25; 30 673 372 117 709 
;MOUNTING PARTS;F5120500;½\" Metal Drop Ear Bend Support;8,75;25; 30 673 372 117 716 
;MOUNTING PARTS;F5140500;½\" Metal Straight-through Support;11,7;25; 30 673 372 117 730 
;MOUNTING PARTS;F5200375;?\" Plastic Drop Ear Bend Support;4,61;25; 30 673 372 117 747 
;MOUNTING PARTS;F5200500;½\" Plastic Drop Ear Bend Support;4,66;25; 30 673 372 117 754 
;FITTINGS METAL;F5400250;¼\" Insert (stainless steel);1,47;10; 30 673 372 117 761 
;FITTINGS METAL;F5400500;½\" Insert (stainless steel);2,55;10; 30 673 372 117 785 
;OTHER COMPONENTS;F5600500;Chrome Finishing Sleeve for ½\" PEX (11/16\" O.D.);7,85;25; 30 673 372 117 808 
;OTHER COMPONENTS;F5650500;ProPEX Escutcheon for ½\" PEX (11/16\" O.D.), chrome-plated;15,45;25; 30 673 372 212 084 
;OTHER COMPONENTS;F5670500;ProPEX Escutcheon for ½\" PEX (11/16\" O.D.), white;4,35;25; 30 673 372 212 077 
;OTHER COMPONENTS;F5700002;Steel Plate Protector, 100/pkg.;48,5;1; 673 372 117 838 
;MOUNTING PARTS;F5801000;Single-tube PEX Stand-up Bracket for ½\" PEX;19,6;60; 30 673 372 150 348 
;MOUNTING PARTS;F5805000;Five-tube PEX Stand-up Bracket for ½\" PEX;74;16; 30 673 372 150 355 
;PEX A;F6040500;½\" Pre-insulated Uponor AquaPEX with ½\" insulation, 100-ft. coil;457;1; 673 372 233 064 
;PEX A;F6040750;¾\" Pre-insulated Uponor AquaPEX with ½\" insulation, 100-ft. coil;560;1; 673 372 233 071 
;PEX A;F6041000;1\" Pre-insulated Uponor AquaPEX with ½\" insulation, 100-ft. coil;685;1; 673 372 233 088 
;PEX A;F6150500;½\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;700;1; 673 372 507 271 
;PEX A;F6150750;¾\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;820;1; 673 372 485 272 
;PEX A;F6151000;1\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;1000;1; 673 372 507 288 
;PEX A;F6151250;1¼\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;1470;1; 673 372 507 295 
;FITTINGS METAL;F6630001;LFCSS Stem Extension Kit for ½\" and ¾\" Valves;14,95;1; 673 372 693 073 
;FITTINGS METAL;F6630002;LFCSS Stem Extension Kit for 1\" and 1 ¼\" Valves;17,05;1; 673 372 693 080 
;FITTINGS METAL;F6630003;LFCSS Stem Extension Kit for 1 ½\" and 2\" Valves;19,65;1; 673 372 693 097 
;MOUNTING PARTS;F7000005;Fire Sprinkler Adapter Push-on Nut, 25/pkg.;73,5;1; 673 372 246 286 
;MOUNTING PARTS;F7040500;½\" PEX-a Pipe Support, 9-ft. length;15,15;5; 30 673 372 314 870 
;MOUNTING PARTS;F7040750;¾\" PEX-a Pipe Support, 9-ft. length;16,9;5; 30 673 372 315 075 
;MOUNTING PARTS;F7041000;1\" PEX-a Pipe Support, 9-ft. length;17,6;5; 30 673 372 299 474 
;MOUNTING PARTS;F7041250;1¼\" PEX-a Pipe Support, 9-ft. length;22,55;5; 30 673 372 299 672 
;MOUNTING PARTS;F7041500;1½\" PEX-a Pipe Support, 9-ft. length;24,85;5; 30 673 372 299 870 
;MOUNTING PARTS;F7042000;2\" PEX-a Pipe Support, 9-ft. length;28,9;5; 30 673 372 299 887 
;MOUNTING PARTS;F7042500;2½\" PEX-a Pipe Support, 9-ft. length;46,9;5; 30 673 372 461 475 
;MOUNTING PARTS;F7043000;3\" PEX-a Pipe Support, 9-ft. length;49,4;5; 30 673 372 461 673 
;MOUNTING PARTS;F7050375;Tube Talon (?\" PEX), 100/pkg.;40,8;1; 673 372 117 845 
;MOUNTING PARTS;F7050750;Tube Talon (½\", ?\", ¾\" PEX), 100/pkg.;35,7;1; 673 372 117 852 
;MOUNTING PARTS;F7051000;Tube Talon (1\" PEX), 50/pkg.;44,2;1; 673 372 117 869 
;MOUNTING PARTS;F7051001;1\" PEX Clip, 50/pkg.;215;1; 673 372 159 548 
;MOUNTING PARTS;F7051258;½\" PEX Clip, 100/pkg.;143;1; 673 372 117 876 
;MOUNTING PARTS;F7057500;¾\" PEX Clip, 100/pkg.;360;1; 673 372 159 562 
;MOUNTING PARTS;F7060375;?\" PEX Clip, 100/pkg.;143;1; 673 372 118 606 
;MANIFOLDS METAL;LF2500400;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 4 outlets;323;1; 673 372 246 729 
;MANIFOLDS METAL;LF2500600;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 6 outlets;456;1; 673 372 246 736 
;MANIFOLDS METAL;LF2500800;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 8 outlets;615;1; 673 372 246 743 
;MANIFOLDS METAL;LF2501000;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 10 outlets;750;1; 673 372 246 750 
;MANIFOLDS METAL;LF2501200;1\" Copper Manifold with LF Brass ½\" ProPEX Ball Valve, 12 outlets;865;1; 673 372 246 767 
;MANIFOLDS METAL;LF2801050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 4 outlets;116;1; 673 372 244 671 
;MANIFOLDS METAL;LF2811050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 6 outlets;159;1; 673 372 244 688 
;MANIFOLDS METAL;LF2821050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 8 outlets;198;1; 673 372 244 695 
;MANIFOLDS METAL;LF2831050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 10 outlets;246;1; 673 372 244 701 
;MANIFOLDS METAL;LF2841050;ProPEX 1\" Copper Branch Manifold with ½\" ProPEX LF brass outlets, 12 outlets;302;1; 673 372 244 718 
;FITTINGS METAL;LF2855050;ProPEX LF Copper Stub Ell, ½\" PEX LF Brass x ½\" Copper (13\" x 8\");31,9;25; 30 673 372 246 485 
;FITTINGS METAL;LF2865050;ProPEX LF Copper Stub Ell, ½\" PEX LF Brass x ½\" Copper (3½\" x 8\");22,25;25; 30 673 372 232 327 
;FITTINGS METAL;LF2875050;ProPEX LF Copper Tub Ell, ½\" PEX LF Brass x ½\" Copper (3\" x 6\");20,2;25; 30 673 372 246 676 
;FITTINGS METAL;LF2885050;ProPEX LF Copper Tub Ell, ½\" PEX LF Brass x ½\" Copper (3\" x 4\");18,3;25; 30 673 372 232 334 
;FITTINGS METAL;LF2891010;ProPEX LF Copper Stub Ell, 1\" PEX x 1\" Copper (13\" x 16\");76,5;1; 673 372 545 471 
;FITTINGS METAL;LF2895050;ProPEX LF Copper Stub Ell, ½\" PEX LF Brass x ½\" Copper (8\" x 13\");32,7;25; 30 673 372 246 683 
;FITTINGS METAL;LF2897575;ProPEX LF Copper Stub Ell, ¾\" PEX LF Brass x ¾\" Copper (4\" x 8\");49,8;25; 30 673 372 246 690 
;FITTINGS METAL;LF2935050;ProPEX LF Copper Straight Stub, ½\" PEX LF Brass x ½\" Copper (8\");22,85;25; 30 673 372 246 706 
;FITTINGS METAL;LF2945050;ProPEX LF Copper Straight Stub, ½\" PEX LF Brass x ½\" Copper (15\");27,6;25; 30 673 372 246 713 
;FITTINGS METAL;LF2957575;ProPEX LF Water Heater Adapter, ¾\" PEX LF Brass x ¾\" FIP x 18\";69,5;20; 50 673 372 232 550 
;FITTINGS METAL;LF2982525;ProPEX LF Brass Flange Adapter Kit, 2½\" PEX (150 lb.);660;1; 673 372 472 678 
;FITTINGS METAL;LF2983030;ProPEX LF Brass Flange Adapter Kit, 3\" PEX (150 lb.);880;1; 673 372 472 876 
;FITTINGS METAL;LF4125050;ProPEX LF Brass Elbow, ½\" PEX x ½\" MIP;18,9;25; 30 673 372 232 358 
;FITTINGS METAL;LF4231010;ProPEX LF Brass Drop Ear Elbow, 1\" PEX x 1\" FIP;72,1;4; 30 673 372 245 280 
;FITTINGS METAL;LF4235038;ProPEX LF Brass Drop Ear Elbow, ½\" PEX x ?\" FIP;27,7;25; 30 673 372 244 771 
;FITTINGS METAL;LF4235050;ProPEX LF Brass Drop Ear Elbow, ½\" PEX x ½\" FIP;21,9;25; 30 673 372 232 341 
;FITTINGS METAL;LF4237575;ProPEX LF Brass Drop Ear Elbow, ¾\" PEX x ¾\" FIP;48,1;4; 30 673 372 245 273 
;FITTINGS METAL;LF4410500;LF Brass Compression Angle Stop Valve for ½\" PEX;20,48;10; 30 673 372 232 280 
;FITTINGS METAL;LF4420500;LF Brass Compression Straight Stop Valve for ½\" PEX;20,45;10; 30 673 372 232 297 
;FITTINGS METAL;LF4455050;ProPEX LF Brass In-line Ice Maker Tee, ½\" PEX x ½\" PEX x ¼\" O.D. compression;62,6;10; 30 673 372 244 788 
;FITTINGS METAL;LF4501010;ProPEX LF Brass Sweat Fitting Adapter, 1\" PEX x 1\" Copper;21,85;10; 30 673 372 232 501 
;FITTINGS METAL;LF4501313;ProPEX LF Brass Sweat Fitting Adapter, 1¼\" PEX x 1¼\" Copper;48,3;1; 673 372 232 548 
;FITTINGS METAL;LF4501515;ProPEX LF Brass Sweat Fitting Adapter, 1½\" PEX x 1½\" Copper;79,3;1; 673 372 246 477 
;FITTINGS METAL;LF4502020;ProPEX LF Brass Sweat Fitting Adapter, 2\" PEX x 2\" Copper;222;1; 673 372 248 082 
;FITTINGS METAL;LF4505050;ProPEX LF Brass Sweat Fitting Adapter, ½\" PEX x ½\" Copper;5,45;25; 30 673 372 232 464 
;FITTINGS METAL;LF4505075;ProPEX LF Brass Sweat Fitting Adapter, ½\" PEX x ¾\" Copper;11;25; 30 673 372 232 525 
;FITTINGS METAL;LF4507510;ProPEX LF Brass Sweat Fitting Adapter, ¾\" PEX x 1\" Copper;24,35;10; 30 673 372 248 090 
;FITTINGS METAL;LF4507550;ProPEX LF Brass Sweat Fitting Adapter, ¾\" PEX x ½\" Copper;22,5;25; 30 673 372 248 106 
;FITTINGS METAL;LF4507575;ProPEX LF Brass Sweat Fitting Adapter, ¾\" PEX x ¾\" Copper;11,95;25; 30 673 372 232 488 
;FITTINGS METAL;LF4511010;ProPEX LF Brass Sweat Adapter, 1\" PEX x 1\" Copper;21;10; 30 673 372 232 495 
;FITTINGS METAL;LF4511313;ProPEX LF Brass Sweat Adapter, 1¼\" PEX x 1¼\" Copper;54,5;1; 673 372 232 531 
;FITTINGS METAL;LF4511515;ProPEX LF Brass Sweat Adapter, 1½\" PEX x 1½\" Copper;83,5;1; 673 372 248 075 
;FITTINGS METAL;LF4512020;ProPEX LF Brass Sweat Adapter, 2\" PEX x 2\" Copper;222;1; 673 372 248 112 
;FITTINGS METAL;LF4512525;ProPEX LF Brass Sweat Adapter, 2½\" PEX x 2½\" Copper;456;1; 673 372 454 964 
;FITTINGS METAL;LF4513030;ProPEX LF Brass Sweat Adapter, 3\" PEX x 3\" Copper;730;1; 673 372 454 971 
;FITTINGS METAL;LF4513850;ProPEX LF Brass Sweat Adapter, ?\" PEX x ½\" Copper;12,65;25; 30 673 372 246 898 
;FITTINGS METAL;LF4515050;ProPEX LF Brass Sweat Adapter, ½\" PEX x ½\" Copper;5,6;25; 30 673 372 232 457 
;FITTINGS METAL;LF4515075;ProPEX LF Brass Sweat Adapter, ½\" PEX x ¾\" Copper;11,15;25; 30 673 372 232 518 
;FITTINGS METAL;LF4517510;ProPEX LF Brass Sweat Adapter, ¾\" PEX x 1\" Copper;25,3;10; 30 673 372 248 274 
;FITTINGS METAL;LF4517550;ProPEX LF Brass Sweat Adapter, ¾\" PEX x ½\" Copper;20,6;25; 30 673 372 248 281 
;FITTINGS METAL;LF4517575;ProPEX LF Brass Sweat Adapter, ¾\" PEX x ¾\" Copper;12,65;25; 30 673 372 232 471 
;FITTINGS METAL;LF4521010;ProPEX LF Brass Male Threaded Adapter, 1\" PEX x 1\" NPT;28,7;10; 30 673 372 232 396 
;FITTINGS METAL;LF4521075;ProPEX LF Brass Male Threaded Adapter, 1\" PEX x ¾\" NPT;30,1;10; 30 673 372 246 935 
;FITTINGS METAL;LF4521313;ProPEX LF Brass Male Threaded Adapter, 1¼\" PEX x 1¼\" NPT;66,6;1; 673 372 232 432 
;FITTINGS METAL;LF4521515;ProPEX LF Brass Male Threaded Adapter, 1½\" PEX x 1½\" NPT;88,8;1; 673 372 246 903 
;FITTINGS METAL;LF4522020;ProPEX LF Brass Male Threaded Adapter, 2\" PEX x 2\" NPT;246;1; 673 372 246 941 
;FITTINGS METAL;LF4522525;ProPEX LF Brass Male Threaded Adapter, 2½\" PEX x 2½\" NPT;535;1; 673 372 454 988 
;FITTINGS METAL;LF4523030;ProPEX LF Brass Male Threaded Adapter, 3\" PEX x 3\" NPT;785;1; 673 372 454 995 
;FITTINGS METAL;LF4523850;ProPEX LF Brass Male Threaded Adapter, ?\" PEX x ½\" NPT;15,65;25; 30 673 372 246 959 
;FITTINGS METAL;LF4525050;ProPEX LF Brass Male Threaded Adapter, ½\" PEX x ½\" NPT;7,75;25; 30 673 372 232 365 
;FITTINGS METAL;LF4525075;ProPEX LF Brass Male Threaded Adapter, ½\" PEX x ¾\" NPT;20,1;25; 30 673 372 246 966 
;FITTINGS METAL;LF4527510;ProPEX LF Brass Male Threaded Adapter, ¾\" PEX x 1\" NPT;30,1;10; 30 673 372 246 973 
;FITTINGS METAL;LF4527575;ProPEX LF Brass Male Threaded Adapter, ¾\" PEX x ¾\" NPT;13,95;25; 30 673 372 232 389 
;FITTINGS METAL;LF4543850;ProPEX LF Brass Coupling, ?\" PEX x ½\" PEX;14,4;25; 30 673 372 244 733 
;FITTINGS METAL;LF4571010;ProPEX LF Brass Female Threaded Adapter, 1\" PEX x 1\" NPT;38,8;10; 30 673 372 232 426 
;FITTINGS METAL;LF4571313;ProPEX LF Brass Female Threaded Adapter, 1¼\" PEX x 1¼\" NPT;74,2;1; 673 372 232 449 
;FITTINGS METAL;LF4571515;ProPEX LF Brass Female Threaded Adapter, 1½\" PEX x 1½\" NPT;161;1; 673 372 246 927 
;FITTINGS METAL;LF4572020;ProPEX LF Brass Female Threaded Adapter, 2\" PEX x 2\" NPT;329;1; 673 372 246 989 
;FITTINGS METAL;LF4575050;ProPEX LF Brass Female Threaded Adapter, ½\" PEX x ½\" NPT;15,95;25; 30 673 372 232 402 
;FITTINGS METAL;LF4575075;ProPEX LF Brass Female Threaded Adapter, ½\" PEX x ¾\" NPT;26,6;25; 30 673 372 246 997 
;FITTINGS METAL;LF4577510;ProPEX LF Brass Female Threaded Adapter, ¾\" PEX x 1\" NPT;59,3;10; 30 673 372 247 000 
;FITTINGS METAL;LF4577575;ProPEX LF Brass Female Threaded Adapter, ¾\" PEX x ¾\" NPT;18,7;25; 30 673 372 232 419 
;FITTINGS METAL;LF4585050;ProPEX LF Brass to PB Coupling, ½\" PEX x ½\" PB;16,3;25; 30 673 372 244 740 
;FITTINGS METAL;LF4587575;ProPEX LF Brass to PB Coupling, ¾\" PEX x ¾\" PB;27;25; 30 673 372 244 757 
;FITTINGS METAL;LF4591010;ProPEX LF Brass to PE Coupling, 1\" PEX x 1\" PE;42,5;10; 30 673 372 244 764 
;FITTINGS METAL;LF4701010;ProPEX LF Brass Tee, 1\" PEX x 1\" PEX x 1\" PEX;44,4;10; 30 673 372 242 678 
;FITTINGS METAL;LF4705050;ProPEX LF Brass Tee, ½\" PEX x ½\" PEX x ½\" PEX;14,75;25; 30 673 372 242 685 
;FITTINGS METAL;LF4707575;ProPEX LF Brass Tee, ¾\" PEX x ¾\" PEX x ¾\" PEX;24,05;25; 30 673 372 242 876 
;FITTINGS METAL;LF4707710;ProPEX LF Brass Reducing Tee, ¾\" PEX x ¾\" PEX x 1\" PEX;38,9;10; 30 673 372 243 675 
;FITTINGS METAL;LF4710500;ProPEX LF Brass Elbow, ½\" PEX x ½\" PEX;10,4;25; 30 673 372 269 873 
;FITTINGS METAL;LF4710750;ProPEX LF Brass Elbow, ¾\" PEX x ¾\" PEX;17,2;25; 30 673 372 242 883 
;FITTINGS METAL;LF4730500;ProPEX LF Brass Elbow, ½\" PEX x ½\" Male CU;17,7;10; 30 673 372 342 675 
;FITTINGS METAL;LF4785025;ProPEX LF Brass Ice Maker Valve, ½\" PEX x ¼\" O.D. (angle);27,4;10; 30 673 372 341 272 
;FITTINGS METAL;LF4786025;ProPEX LF Brass Ice Maker Valve, ½\" PEX x ¼\" O.D. (straight);30,6;10; 30 673 372 342 071 
;FITTINGS METAL;LF4795050;ProPEX LF Brass Ball Valve, ½\" PEX x ½\" MIP;34,2;10; 30 673 372 232 310 
;FITTINGS METAL;LF4805050;ProPEX LF Brass Ball Valve, ½\" PEX x ½\" Copper Adapter;23,1;10; 30 673 372 232 266 
;FITTINGS METAL;LF4807575;ProPEX LF Brass Ball Valve, ¾\" PEX x ¾\" Copper Adapter;41;10; 30 673 372 244 924 
;FITTINGS METAL;LF4855038;ProPEX LF Brass Angle Stop Valve, ½\" PEX;13,95;10; 30 673 372 232 600 
;FITTINGS METAL;LF4865038;ProPEX LF Brass Straight Stop Valve, ½\" PEX;14,35;10; 30 673 372 232 594 
;FITTINGS METAL;LF5930500;ProPEX Washing Machine Outlet Box, ½\" LF Brass Valves;120;12; 50 673 372 232 567 
;FITTINGS METAL;LF5955025;ProPEX Ice Maker Box with Support Brackets, ½\" LF Brass Valve;71,2;12; 50 673 372 232 574 
;FITTINGS METAL;LF73000WH;LF Recessed Pendent Sprinkler, 155F, 3.0 K-factor, White;86,8;5; 30 673 372 285 675 
;FITTINGS METAL;LF74000HS;LF Flat Concealed Horizontal Sidewall Sprinkler, 165F, 4.0 K-factor;191;5; 30 673 372 286 474 
;FITTINGS METAL;LF74300HW;LF Recessed Horizontal Sidewall Sprinkler, 155F, 4.2 K-factor, White;88,3;5; 30 673 372 285 873 
;FITTINGS METAL;LF74301HW;LF Recessed Horizontal Sidewall Sprinkler, 175F, 4.2 K-factor, White;88,3;5; 30 673 372 286 078 
;FITTINGS METAL;LF74900WH;LF Recessed Pendent Sprinkler, 155F, 4.9 K-factor, White;86,8;5; 30 673 372 285 279 
;FITTINGS METAL;LF74901WH;LF Recessed Pendent Sprinkler, 175F, 4.9 K-factor, White;86,8;5; 30 673 372 285 477 
;FITTINGS METAL;LF74970FC;LF RC-RES (162F) Flat Concealed Sprinkler;65,3;5; 30 673 372 262 874 
;FITTINGS METAL;LF74971FW;LF RC-RES (205F) Flat Concealed Sprinkler with White Cover Plate;116;5; 30 673 372 326 279 
;FITTINGS METAL;LF7701010;ProPEX LF Brass Fire Sprinkler Adapter Tee, 1\" PEX x 1\" PEX x ½\" FNPT;61,3;5; 30 673 372 246 072 
;FITTINGS METAL;LF7707575;ProPEX LF Brass Fire Sprinkler Adapter Tee, ¾\" PEX x ¾\" PEX x ½\" FNPT;57;5; 30 673 372 246 089 
;FITTINGS METAL;LF7711050;ProPEX LF Brass Fire Sprinkler Adapter Elbow, 1\" PEX x ½\" FNPT;50,1;5; 30 673 372 246 096 
;FITTINGS METAL;LF7717550;ProPEX LF Brass Fire Sprinkler Adapter Elbow, ¾\" PEX x ½\" FNPT;48,1;5; 30 673 372 246 102 
;FITTINGS METAL;LFC4821010SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 1\" PEX x 1\" PEX;40,5;1; 673 372 660 877 
;FITTINGS METAL;LFC4821313SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 1¼\" PEX x 1¼\" PEX;66,2;1; 673 372 660 884 
;FITTINGS METAL;LFC4821515SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 1½\" PEX x 1½\" PEX;99,3;1; 673 372 660 891 
;FITTINGS METAL;LFC4822020SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem 2\" PEX x 2\" PEX;173;1; 673 372 660 907 
;FITTINGS METAL;LFC4825050SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem ½\" PEX x ½\" PEX;17,1;10; 30 673 372 660 915 
;FITTINGS METAL;LFC4827575SS;ProPEX LF Brass Commercial Ball Valve (full port), SS Ball and Stem ¾\" PEX x ¾\" PEX;27,2;10; 30 673 372 660 922 
;FITTINGS METAL;LFD4811010;ProPEX LF Brass Stop and Drain Ball Valve (full port), 1\" PEX x 1\" PEX;41;1; 673 372 674 270 
;FITTINGS METAL;LFD4815050;ProPEX LF Brass Stop and Drain Ball Valve (full port), ½\" PEX x ½\" PEX;19,85;10; 30 673 372 674 288 
;FITTINGS METAL;LFD4817575;ProPEX LF Brass Stop and Drain Ball Valve (full port), ¾\" PEX x ¾\" PEX;26,5;10; 30 673 372 674 295 
;FITTINGS METAL;LFP4501010;ProPEX LF Brass Copper Press Fitting Adapter, 1\" PEX x 1\" Copper;27,9;10; 30 673 372 545 489 
;FITTINGS METAL;LFP4501313;ProPEX LF Brass Copper Press Fitting Adapter, 1¼\" PEX x 1¼\" Copper;43,3;1; 673 372 545 495 
;FITTINGS METAL;LFP4501515;ProPEX LF Brass Copper Press Fitting Adapter, 1½\" PEX x 1½\" Copper;57,2;1; 673 372 545 501 
;FITTINGS METAL;LFP4502020;ProPEX LF Brass Copper Press Fitting Adapter, 2\" PEX x 2\" Copper;121;1; 673 372 545 518 
;FITTINGS METAL;LFP4502525;ProPEX LF Brass Copper Press Fitting Adapter, 2½\" PEX x 2½\" Copper;311;1; 673 372 545 525 
;FITTINGS METAL;LFP4503030;ProPEX LF Brass Copper Press Fitting Adapter, 3\" PEX x 3\" Copper;399;1; 673 372 545 532 
;FITTINGS METAL;LFP4505050;ProPEX LF Brass Copper Press Fitting Adapter, ½\" PEX x ½\" Copper;9,35;25; 30 673 372 545 540 
;FITTINGS METAL;LFP4507575;ProPEX LF Brass Copper Press Fitting Adapter, ¾\" PEX x ¾\" Copper;16,6;25; 30 673 372 545 557 
;FITTINGS METAL;LFP4511010;ProPEX LF Brass Copper Press Adapter, 1\" PEX x 1\" Copper;27,9;10; 30 673 372 545 564 
;FITTINGS METAL;LFP4511313;ProPEX LF Brass Copper Press Adapter, 1¼\" PEX x 1¼\" Copper;41,6;1; 673 372 545 570 
;FITTINGS METAL;LFP4511515;ProPEX LF Brass Copper Press Adapter, 1½\" PEX x 1½\" Copper;55,1;1; 673 372 545 587 
;FITTINGS METAL;LFP4512020;ProPEX LF Brass Copper Press Adapter, 2\" PEX x 2\" Copper;116;1; 673 372 545 594 
;FITTINGS METAL;LFP4512525;ProPEX LF Brass Copper Press Adapter, 2½\" PEX x 2½\" Copper;300;1; 673 372 545 600 
;FITTINGS METAL;LFP4513030;ProPEX LF Brass Copper Press Adapter, 3\" PEX x 3\" Copper;385;1; 673 372 545 617 
;FITTINGS METAL;LFP4515050;ProPEX LF Brass Copper Press Adapter, ½\" PEX x ½\" Copper;8,9;25; 30 673 372 545 625 
;FITTINGS METAL;LFP4517575;ProPEX LF Brass Copper Press Adapter, ¾\" PEX x ¾\" Copper;15,8;25; 30 673 372 545 632 
;FITTINGS METAL;LFR4811010;ProPEX LF Brass Ball Valve (full port), 1\" PEX x 1\" PEX;38,4;1; 673 372 695 886 
;FITTINGS METAL;LFR4815050;ProPEX LF Brass Ball Valve (full port), ½\" PEX x ½\" PEX;13,9;10; 30 673 372 695 894 
;FITTINGS METAL;LFR4817575;ProPEX LF Brass  Ball Valve (full port), ¾\" PEX x ¾\" PEX;22,5;10; 30 673 372 695 900 
;FITTINGS METAL;LFV2962020;ProPEX LF Groove Fitting Adapter, 2\" PEX LF Brass x 2\" CTS Groove;114;1; 673 372 536 271 
;FITTINGS METAL;LFV2962525;ProPEX LF Groove Fitting Adapter, 2½\" PEX LF Brass x 2½\" CTS Groove;173;1; 673 372 536 295 
;FITTINGS METAL;LFV2963030;ProPEX LF Groove Fitting Adapter, 3\" PEX LF Brass x 3\" CTS Groove;256;1; 673 372 536 301 
;FITTINGS METAL;LFV2972020;ProPEX LF Groove Fitting Adapter, 2\" PEX LF Brass x 2\" IPS Groove;117;1; 673 372 552 479 
;FITTINGS METAL;LFV2972525;ProPEX LF Groove Fitting Adapter, 2½\" PEX LF Brass x 2½\" IPS Groove;176;1; 673 372 552 509 
;FITTINGS METAL;LFV2972530;ProPEX LF Groove Fitting Adapter, 2½\" PEX LF Brass x 3\" IPS Groove;218;1; 673 372 552 516 
;FITTINGS METAL;LFV2973030;ProPEX LF Groove Fitting Adapter, 3\" PEX LF Brass x 3\" IPS Groove;256;1; 673 372 552 530 
;MATS;M2306060000;½\" Wirsbo hePEX Radiant Rollout Mat (6\" o.c.), 5 loop;call for price;1; 673 372 336 871 
;MATS;M2309054000;½\" Wirsbo hePEX Radiant Rollout Mat (9\" o.c.), 3 loop;call for price;1; 673 372 337 076 
;MATS;M2312072000;½\" Wirsbo hePEX Radiant Rollout Mat (12\" o.c.), 3 loop;call for price;1; 673 372 337 274 
;MATS;M2406060000;?\" Wirsbo hePEX Radiant Rollout Mat (6\" o.c.), 5 loop;call for price;1; 673 372 337 472 
;MATS;M2409054000;?\" Wirsbo hePEX Radiant Rollout Mat (9\" o.c.), 3 loop;call for price;1; 673 372 337 670 
;MATS;M2412072000;?\" Wirsbo hePEX Radiant Rollout Mat (12\" o.c.), 3 loop;call for price;1; 673 372 337 878 
;MANIFOLDS PLASTIC;Q2087550;¾\" EP Branch Multi-port Elbow, 8 outlets with mounting clips;91,6;1; 673 372 201 247 
;MANIFOLDS PLASTIC;Q2101000;1\" EP Branch Multi-port Elbow, 10 outlets with mounting clips;93,3;1; 673 372 201 049 
;MANIFOLDS PLASTIC;Q2101051;1\" EP Branch Multi-port Tee, 10 outlets with mounting clips;98,1;1; 673 372 202 046 
;MANIFOLDS PLASTIC;Q2121051;1\" EP Branch Multi-port Tee, 12 outlets with mounting clips;108;1; 673 372 202 053 
;MANIFOLDS PLASTIC;Q2227557;EP Flow-through Multi-port Tee, 2 outlets, ¾\" x ¾\" ProPEX;13,15;10; 30 673 372 135 123 
;MANIFOLDS PLASTIC;Q2231057;EP Flow-through Multi-port Tee, 3 outlets, 1\" x ¾\" ProPEX;44,1;10; 30 673 372 314 276 
;MANIFOLDS PLASTIC;Q2231373;EP Flow-through Multi-port Tee, 3 (¾\") outlets, 1¼\" x 1¼\" ProPEX;72,1;1; 673 372 328 678 
;MANIFOLDS PLASTIC;Q2231375;1¼\" EP Branch Multi-port Tee, 3 (¾\") outlets;72,1;1; 673 372 328 876 
;MANIFOLDS PLASTIC;Q2232102;EP Flow-through Multi-port Tee, 3 (1\") outlets, 2\" x 2\" ProPEX;268;1; 673 372 317 276 
;MANIFOLDS PLASTIC;Q2235577;EP Flow-through Multi-port Elbow, 3 outlets, ¾\" x ¾\" ProPEX;49,1;10; 30 673 372 190 856 
;MANIFOLDS PLASTIC;Q2237550;¾\" EP Branch Multi-port Tee, 3 outlets;15,25;10; 30 673 372 188 068 
;MANIFOLDS PLASTIC;Q2237557;EP Flow-through Multi-port Tee, 3 outlets, ¾\" x ¾\" ProPEX;17,75;10; 30 673 372 135 130 
;MANIFOLDS PLASTIC;Q2237757;EP Flow-through Multi-port Vertical Tee, 3 outlets, ¾\" x ¾\" x ¾\" ProPEX;55,6;10; 30 673 372 190 863 
;MANIFOLDS PLASTIC;Q2241050;1\" EP Branch Multi-port Tee, 4 outlets;49,8;10; 30 673 372 314 672 
;MANIFOLDS PLASTIC;Q2241051;EP Flow-through Multi-port Tee, 4 outlets, 1\" x 1\" ProPEX;47,7;10; 30 673 372 314 474 
;MANIFOLDS PLASTIC;Q2241057;EP Flow-through Multi-port Tee, 4 outlets, 1\" x ¾\" ProPEX;50,3;10; 30 673 372 135 147 
;MANIFOLDS PLASTIC;Q2245577;EP Flow-through Multi-port Elbow, 4 outlets, ¾\" x ¾\" ProPEX;48,5;10; 30 673 372 191 044 
;MANIFOLDS PLASTIC;Q2247550;¾\" EP Branch Multi-port Tee, 4 outlets;22,1;10; 30 673 372 135 154 
;MANIFOLDS PLASTIC;Q2247557;EP Flow-through Multi-port Tee, 4 outlets, ¾\" x ¾\" ProPEX;22,1;10; 30 673 372 119 383 
;MANIFOLDS PLASTIC;Q2247577;EP Flow-through Multi-port Horizontal Tee, 4 outlets, ¾\" x ¾\" x ¾\" ProPEX;58,9;10; 30 673 372 191 051 
;MANIFOLDS PLASTIC;Q2247757;EP Flow-through Multi-port Vertical Tee, 4 outlets, ¾\" x ¾\" x ¾\" ProPEX;58,9;10; 30 673 372 190 849 
;MANIFOLDS PLASTIC;Q2261050;1\" EP Branch Multi-port Tee, 6 outlets;63,8;10; 30 673 372 135 161 
;MANIFOLDS PLASTIC;Q2261051;EP Flow-through Multi-port Tee, 6 outlets, 1\" x 1\" ProPEX;65,9;10; 30 673 372 135 178 
;MANIFOLDS PLASTIC;Q2261057;EP Flow-through Multi-port Tee, 6 outlets, 1\" x ¾\" ProPEX;65,9;10; 30 673 372 135 185 
;MANIFOLDS PLASTIC;Q2267550;¾\" EP Branch Multi-port Tee, 6 outlets;25,9;10; 30 673 372 188 044 
;MANIFOLDS PLASTIC;Q2267557;EP Flow-through Multi-port Tee, 6 outlets, ¾\" x ¾\" ProPEX;26,6;10; 30 673 372 188 051 
;MANIFOLDS PLASTIC;Q2271051;1\" EP Branch Multi-port Tee, 7 outlets with mounting clips;82,8;1; 673 372 299 275 
;MANIFOLDS PLASTIC;Q2277550;¾\" EP Branch Multi-port Tee, 7 outlets with mounting clips;85,3;1; 673 372 201 650 
;MANIFOLDS PLASTIC;Q2281051;1\" EP Branch Multi-port Tee, 8 outlets with mounting clips;90,1;1; 673 372 299 282 
;MANIFOLDS PLASTIC;Q2287550;¾\" EP Branch Multi-port Tee, 8 outlets with mounting clips;88,1;1; 673 372 201 643 
;MANIFOLDS PLASTIC;Q2337550;¾\" EP Branch Opposing-port Multi-port Tee, 3 outlets;23;10; 30 673 372 202 665 
;MANIFOLDS PLASTIC;Q2337557;EP Flow-through Opposing-port Multi-port Tee, 3 outlets, ¾\" x ¾\" ProPEX;28,4;10; 30 673 372 202 672 
;MANIFOLDS PLASTIC;Q2347550;¾\" EP Branch Opposing-port Multi-port Tee, 4 outlets;38,4;10; 30 673 372 202 245 
;MANIFOLDS PLASTIC;Q2347557;EP Flow-through Opposing-port Multi-port Tee, 4 outlets, ¾\" x ¾\" ProPEX;38,6;10; 30 673 372 202 443 
;MANIFOLDS PLASTIC;Q2367557;EP Flow-through Opposing-port Multi-port Tee, 6 outlets, ¾\" x ¾\" ProPEX;58,8;10; 30 673 372 202 641 
;MANIFOLDS METAL;Q2811263;2\" x 4\' Copper Valved Manifold with ?\" ProPEX Ball Valves, 12 outlets;1620;1; 673 372 133 715 
;MANIFOLDS METAL;Q2811275;2\" x 4\' Copper Valved Manifold with ¾\" ProPEX Ball Valves, 12 outlets;1680;1; 673 372 133 685 
;MANIFOLDS METAL;Q2821275;2\" x 4\' Copper Valved Manifold with ¾\" ProPEX Ball and Balancing Valves, 12 outlets;2060;1; 673 372 133 876 
;MANIFOLDS METAL;Q2831275;2\" x 4\' Copper Valveless Manifold with ¾\" ProPEX, 12 outlets;1060;1; 673 372 158 992 
;FITTINGS METAL;Q4020375;?\" ProPEX Fitting Assembly, R20 Thread;17,19;10; 30 673 372 119 840 
;FITTINGS METAL;Q4020500;½\" ProPEX Fitting Assembly, R20 Thread;14,63;10; 30 673 372 119 857 
;FITTINGS METAL;Q4020625;?\" ProPEX Fitting Assembly, R20 Thread;17,4;10; 30 673 372 119 864 
;FITTINGS METAL;Q4020750;¾\" ProPEX Fitting Assembly, R20 Thread;28,42;10; 30 673 372 124 462 
New;FITTINGS METAL;Q4050625;?\" ProPEX Fitting Assembly for Commercial Manifold, R25 thread;26,1;10; 30 673 372 752 474 
New;FITTINGS METAL;Q4050750;¾\" ProPEX Fitting Assembly for Commercial Manifold, R25 thread;30,33;10; 30 673 372 752 481 
New;FITTINGS METAL;Q4051000;1\" ProPEX Fitting Assembly for Commercial Manifold, R25 thread;47,91;10; 30 673 372 752 498 
;FITTINGS METAL;Q4143210;ProPEX Manifold Straight Adapter, R32 x 1\" ProPEX;46,4;10; 30 673 372 119 895 
;FITTINGS METAL;Q4143213;ProPEX Manifold Straight Adapter, R32 x 1¼\" ProPEX;51,94;10; 30 673 372 309 074 
;FITTINGS METAL;Q4143215;ProPEX Manifold Straight Adapter, R32 x 1½\" ProPEX;54,76;10; 30 673 372 309 081 
;FITTINGS METAL;Q4143275;ProPEX Manifold Straight Adapter, R32 x ¾\" ProPEX;49,95;10; 30 673 372 138 759 
;FITTINGS METAL;Q4153210;ProPEX Manifold Elbow Adapter, R32 x 1\" ProPEX;61,66;10; 30 673 372 129 191 
;FITTINGS METAL;Q4153215;ProPEX Manifold Elbow Adapter, R32 x 1½\" ProPEX;76,81;10; 30 673 372 309 470 
;FITTINGS METAL;Q4153275;ProPEX Manifold Elbow Adapter, R32 x ¾\" ProPEX;62,6;10; 30 673 372 129 252 
;FITTINGS PLASTIC;Q4350500;ProPEX EP Plug for ½\" PEX;2,23;25; 30 673 372 119 963 
;FITTINGS PLASTIC;Q4350750;ProPEX EP Plug for ¾\" PEX;3,45;25; 30 673 372 119 970 
;FITTINGS PLASTIC;Q4351000;ProPEX EP Plug for 1\" PEX;4,58;10; 30 673 372 119 987 
;FITTINGS PLASTIC;Q4351250;ProPEX EP Plug for 1¼\" PEX;21,55;1; 673 372 198 042 
;FITTINGS PLASTIC;Q4351500;ProPEX EP Plug for 1½\" PEX;33,5;1; 673 372 198 059 
;FITTINGS PLASTIC;Q4352000;ProPEX EP Plug for 2\" PEX;37,8;1; 673 372 198 066 
;FITTINGS PLASTIC;Q4360500;ProPEX EP Swivel Faucet Adapter, ½\" PEX x ½\" NPSM;5,5;25; 30 673 372 120 006 
;FITTINGS METAL;Q4375075;ProPEX Baseboard Elbow, ½\" PEX x ¾\" Copper Fitting Adapter;13,32;10; 30 673 372 138 261 
;FITTINGS METAL;Q4376375;ProPEX Baseboard Elbow, ?\" PEX x ¾\" Copper Fitting Adapter;14,16;10; 30 673 372 138 230 
;FITTINGS METAL;Q4377575;ProPEX Baseboard Elbow, ¾\" PEX x ¾\" Copper Fitting Adapter;15,1;10; 30 673 372 138 223 
;FITTINGS METAL;Q4385075;ProPEX Baseboard Elbow, ½\" PEX x ¾\" Copper Adapter;13,32;10; 30 673 372 120 013 
;FITTINGS METAL;Q4386375;ProPEX Baseboard Elbow, ?\" PEX x ¾\" Copper Adapter;14,16;10; 30 673 372 120 020 
;FITTINGS METAL;Q4387575;ProPEX Baseboard Elbow, ¾\" PEX x ¾\" Copper Adapter;15,1;10; 30 673 372 138 254 
;FITTINGS METAL;Q4506350;ProPEX Brass Fitting Adapter, ?\" PEX x ½\" Copper;8,73;10; 30 673 372 120 167 
;FITTINGS METAL;Q4506375;ProPEX Brass Fitting Adapter, ?\" PEX x ¾\" Copper;7,94;10; 30 673 372 120 174 
;FITTINGS METAL;Q4516350;ProPEX Brass Sweat Adapter, ?\" PEX x ½\" Copper;12,17;10; 30 673 372 120 273 
;FITTINGS METAL;Q4516375;ProPEX Brass Sweat Adapter, ?\" PEX x ¾\" Copper;9,3;10; 30 673 372 120 280 
;FITTINGS METAL;Q4526375;ProPEX Brass Male Threaded Adapter, ?\" PEX x ¾\" NPT;13,95;10; 30 673 372 120 396 
;FITTINGS METAL;Q4536363;ProPEX Brass Plug for ?\" PEX;14,94;10; 30 673 372 120 457 
;FITTINGS METAL;Q4546363;ProPEX Brass Coupling, ?\" PEX x ?\" PEX;9,35;10; 30 673 372 120 549 
;FITTINGS METAL;Q4576375;ProPEX Brass Female Threaded Adapter, ?\" PEX x ¾\" NPT;13,22;10; 30 673 372 107 892 
;FITTINGS PLASTIC;Q4621010;ProPEX EP Male Threaded Adapter, 1\" PEX x 1\" NPT;12,1;10; 30 673 372 693 678 
;FITTINGS PLASTIC;Q4625050;ProPEX EP Male Threaded Adapter, ½\" PEX x ½\" NPT;3,46;25; 30 673 372 693 685 
;FITTINGS PLASTIC;Q4627575;ProPEX EP Male Threaded Adapter, ¾\" PEX x ¾\" NPT;5,55;25; 30 673 372 693 692 
;RINGS;Q4690302;ProPEX Ring, ?\";0,38;50; 30 673 372 120 761 
;RINGS;Q4690512;ProPEX Ring with Stop, ½\";0,43;50; 30 673 372 210 530 
;RINGS;Q4690625;ProPEX Ring with Stop, ?\";0,69;50; 30 673 372 315 471 
;RINGS;Q4690756;ProPEX Ring with Stop, ¾\";0,85;50; 30 673 372 223 134 
;RINGS;Q4691000;ProPEX Ring with Stop, 1\";1,8;50; 30 673 372 268 876 
;RINGS;Q4691250;ProPEX Ring with Stop, 1¼\";1,98;10; 30 673 372 269 286 
;RINGS;Q4691500;ProPEX Ring with Stop, 1½\";2,62;5; 30 673 372 269 279 
;RINGS;Q4692000;ProPEX Ring with Stop, 2\";5,25;10; 30 673 372 269 156 
;RINGS;Q4692500;ProPEX Ring with Stop, 2½\";6,95;5; 30 673 372 452 312 
;RINGS;Q4693000;ProPEX Ring with Stop, 3\";11,4;5; 30 673 372 452 893 
;FITTINGS METAL;Q4710625;ProPEX Brass Elbow, ?\" PEX x ?\" PEX;14,94;25; 30 673 372 164 864 
;FITTINGS PLASTIC;Q4751010;ProPEX EP Tee, 1\" PEX x 1\" PEX x 1\" PEX;10,25;10; 30 673 372 120 976 
;FITTINGS PLASTIC;Q4751113;ProPEX EP Reducing Tee, 1\" PEX x 1\" PEX x 1¼\" PEX;40,2;1; 673 372 656 887 
;FITTINGS PLASTIC;Q4751150;ProPEX EP Reducing Tee, 1\" PEX x 1\" PEX x ½\" PEX;9,4;10; 30 673 372 120 983 
;FITTINGS PLASTIC;Q4751175;ProPEX EP Reducing Tee, 1\" PEX x 1\" PEX x ¾\" PEX;10,35;10; 30 673 372 120 990 
;FITTINGS PLASTIC;Q4751311;ProPEX EP Reducing Tee, 1¼\" PEX x 1\" PEX x 1\" PEX;20,3;1; 673 372 129 589 
;FITTINGS PLASTIC;Q4751313;ProPEX EP Tee, 1¼\" PEX x 1¼\" PEX x 1¼\" PEX;22,9;1; 673 372 129 565 
;FITTINGS PLASTIC;Q4751317;ProPEX EP Reducing Tee, 1¼\" PEX x 1\" PEX x ¾\" PEX;17,3;1; 673 372 129 664 
;FITTINGS PLASTIC;Q4751331;ProPEX EP Reducing Tee, 1¼\" PEX x 1¼\" PEX x 1\" PEX;20,95;1; 673 372 129 541 
;FITTINGS PLASTIC;Q4751337;ProPEX EP Reducing Tee, 1¼\" PEX x 1¼\" PEX x ¾\" PEX;20,5;1; 673 372 129 527 
;FITTINGS PLASTIC;Q4751350;ProPEX EP Reducing Tee, 1¼\" PEX x 1¼\" PEX x ½\" PEX;16,1;1; 673 372 313 674 
;FITTINGS PLASTIC;Q4751371;ProPEX EP Reducing Tee, 1¼\" PEX x ¾\" PEX x 1\" PEX;30,7;1; 673 372 656 894 
;FITTINGS PLASTIC;Q4751373;ProPEX EP Reducing Tee, 1¼\" PEX x ¾\" PEX x 1¼\" PEX;35,3;1; 673 372 656 900 
;FITTINGS PLASTIC;Q4751377;ProPEX EP Reducing Tee, 1¼\" PEX x ¾\" PEX x ¾\" PEX;27,4;1; 673 372 656 917 
;FITTINGS PLASTIC;Q4751501;ProPEX EP Reducing Tee, 1\" PEX x ½\" PEX x 1\" PEX;17,55;10; 30 673 372 656 925 
;FITTINGS PLASTIC;Q4751505;ProPEX EP Reducing Tee, 1½\" PEX x 1\" PEX x 1½\" PEX;27,1;1; 673 372 314 084 
;FITTINGS PLASTIC;Q4751511;ProPEX EP Reducing Tee, 1½\" PEX x 1\" PEX x 1\" PEX;25,4;1; 673 372 129 503 
;FITTINGS PLASTIC;Q4751515;ProPEX EP Tee, 1½\" PEX x 1½\" PEX x 1½\" PEX;32;1; 673 372 129 466 
;FITTINGS PLASTIC;Q4751517;ProPEX EP Reducing Tee, 1½\" PEX x 1\" PEX x ¾\" PEX;25,4;1; 673 372 129 640 
;FITTINGS PLASTIC;Q4751531;ProPEX EP Reducing Tee, 1½\" PEX x 1¼\" PEX x 1\" PEX;30;1; 673 372 233 668 
;FITTINGS PLASTIC;Q4751533;ProPEX EP Reducing Tee, 1½\" PEX x 1¼\" PEX x 1¼\" PEX;32,1;1; 673 372 233 675 
;FITTINGS PLASTIC;Q4751537;ProPEX EP Reducing Tee, 1½\" PEX x 1¼\" PEX x ¾\" PEX;29,1;1; 673 372 233 682 
;FITTINGS PLASTIC;Q4751550;ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x ½\" PEX;23,1;1; 673 372 313 681 
;FITTINGS PLASTIC;Q4751551;ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x 1\" PEX;28,1;1; 673 372 129 480 
;FITTINGS PLASTIC;Q4751553;ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x 1¼\" PEX;28,9;1; 673 372 129 442 
;FITTINGS PLASTIC;Q4751557;ProPEX EP Reducing Tee, 1½\" PEX x 1½\" PEX x ¾\" PEX;27,3;1; 673 372 129 428 
;FITTINGS PLASTIC;Q4751575;ProPEX EP Reducing Tee, 1½\" PEX x ¾\" PEX x 1½\" PEX;35,3;1; 673 372 656 931 
;FITTINGS PLASTIC;Q4751577;ProPEX EP Reducing Tee, 1½\" PEX x ¾\" PEX x ¾\" PEX;35,5;1; 673 372 656 948 
;FITTINGS PLASTIC;Q4751750;ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x ½\" PEX;10,95;10; 30 673 372 656 871 
;FITTINGS PLASTIC;Q4751751;ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x 1\" PEX;12,35;10; 30 673 372 121 003 
;FITTINGS PLASTIC;Q4751753;ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x 1¼\" PEX;33,3;1; 673 372 656 955 
;FITTINGS PLASTIC;Q4751775;ProPEX EP Reducing Tee, 1\" PEX x ¾\" PEX x ¾\" PEX;10;10; 30 673 372 121 010 
;FITTINGS PLASTIC;Q4752000;ProPEX EP Tee, 2\" PEX x 2\" PEX x 2\" PEX;103;1; 673 372 217 699 
;FITTINGS PLASTIC;Q4752051;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 1\" PEX;79,2;1; 673 372 217 668 
;FITTINGS PLASTIC;Q4752053;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 1¼\" PEX;98;1; 673 372 233 262 
;FITTINGS PLASTIC;Q4752055;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 1½\" PEX;98,6;1; 673 372 233 279 
;FITTINGS PLASTIC;Q4752110;ProPEX EP Reducing Tee, 2\" PEX x 1\" PEX x 1\" PEX;78;1; 673 372 656 962 
;FITTINGS PLASTIC;Q4752152;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x 2\" PEX;97,6;1; 673 372 314 077 
;FITTINGS PLASTIC;Q4752210;ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x 1\" PEX;85;1; 673 372 217 729 
;FITTINGS PLASTIC;Q4752213;ProPEX EP Reducing Tee, 2\" x 2\" x 1¼\";89,2;1; 673 372 233 286 
;FITTINGS PLASTIC;Q4752215;ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x 1½\" PEX;99,8;1; 673 372 217 712 
;FITTINGS PLASTIC;Q4752250;ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x ½\" PEX;85,9;1; 673 372 313 872 
;FITTINGS PLASTIC;Q4752275;ProPEX EP Reducing Tee, 2\" PEX x 2\" PEX x ¾\" PEX;86,7;1; 673 372 217 705 
;FITTINGS PLASTIC;Q4752500;ProPEX EP Tee, 2½\" PEX x 2½\" PEX x 2½\" PEX;171;1; 673 372 454 728 
;FITTINGS PLASTIC;Q4752510;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 1\" PEX;140;1; 673 372 454 681 
;FITTINGS PLASTIC;Q4752513;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 1¼\" PEX;151;1; 673 372 454 698 
;FITTINGS PLASTIC;Q4752515;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 1½\" PEX;151;1; 673 372 454 704 
;FITTINGS PLASTIC;Q4752520;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x 2\" PEX;151;1; 673 372 454 711 
;FITTINGS PLASTIC;Q4752522;ProPEX EP Reducing Tee, 2½\" PEX x 2\" PEX x 2\" PEX;151;1; 673 372 453 080 
;FITTINGS PLASTIC;Q4752525;ProPEX EP Reducing Tee, 2½\" PEX x 2\" PEX x 1½\" PEX;151;1; 673 372 453 073 
;FITTINGS PLASTIC;Q4752557;ProPEX EP Reducing Tee, 2½\" PEX x 2½\" PEX x ¾\" PEX;122;1; 673 372 454 674 
;FITTINGS PLASTIC;Q4752575;ProPEX EP Reducing Tee, 2\" PEX x 1½\" PEX x ¾\" PEX;90,9;1; 673 372 233 293 
;FITTINGS PLASTIC;Q4753000;ProPEX EP Tee, 3\" PEX x 3\" PEX x 3\" PEX;278;1; 673 372 454 827 
;FITTINGS PLASTIC;Q4753215;ProPEX EP Reducing Tee, 3\" PEX x 2½\" PEX x 1½\" PEX;203;1; 673 372 454 742 
;FITTINGS PLASTIC;Q4753220;ProPEX EP Reducing Tee, 3\" PEX x 2\" PEX x 2\" PEX;207;1; 673 372 454 735 
;FITTINGS PLASTIC;Q4753252;ProPEX EP Reducing Tee, 3\" PEX x 2½\" PEX x 2\" PEX;232;1; 673 372 454 759 
;FITTINGS PLASTIC;Q4753310;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 1\" PEX;174;1; 673 372 454 773 
;FITTINGS PLASTIC;Q4753313;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 1¼\" PEX;185;1; 673 372 454 780 
;FITTINGS PLASTIC;Q4753315;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 1½\" PEX;197;1; 673 372 454 797 
;FITTINGS PLASTIC;Q4753320;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 2\" PEX;232;1; 673 372 454 803 
;FITTINGS PLASTIC;Q4753325;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x 2½\" PEX;254;1; 673 372 454 810 
;FITTINGS PLASTIC;Q4753375;ProPEX EP Reducing Tee, 3\" PEX x 3\" PEX x ¾\" PEX;174;1; 673 372 454 766 
;FITTINGS PLASTIC;Q4755050;ProPEX EP Tee, ½\" PEX x ½\" PEX x ½\" PEX;3,51;25; 30 673 372 121 027 
;FITTINGS PLASTIC;Q4755575;ProPEX EP Reducing Tee, ½\" PEX x ½\" PEX x ¾\" PEX;11,15;25; 30 673 372 188 860 
;FITTINGS PLASTIC;Q4757550;ProPEX EP Reducing Tee, ¾\" PEX x ¾\" PEX x ½\" PEX;4,58;25; 30 673 372 121 034 
;FITTINGS PLASTIC;Q4757555;ProPEX EP Reducing Tee, ¾\" PEX x ½\" PEX x ½\" PEX;5,45;25; 30 673 372 121 041 
;FITTINGS PLASTIC;Q4757557;ProPEX EP Reducing Tee, ¾\" PEX x ½\" PEX x ¾\" PEX;5,65;25; 30 673 372 121 058 
;FITTINGS PLASTIC;Q4757563;ProPEX EP Reducing Tee, ¾\" PEX x ¾\" PEX x ?\" PEX;10,15;10; 30 673 372 264 076 
;FITTINGS PLASTIC;Q4757575;ProPEX EP Tee, ¾\" PEX x ¾\" PEX x ¾\" PEX;5,65;25; 30 673 372 121 065 
;FITTINGS PLASTIC;Q4757710;ProPEX EP Reducing Tee, ¾\" PEX x ¾\" PEX x 1\" PEX;16,65;10; 30 673 372 188 877 
;FITTINGS PLASTIC;Q4760500;ProPEX EP Elbow, ½\" PEX x ½\" PEX;3,46;25; 30 673 372 121 072 
;FITTINGS PLASTIC;Q4760750;ProPEX EP Elbow, ¾\" PEX x ¾\" PEX;4,36;25; 30 673 372 121 089 
;FITTINGS PLASTIC;Q4761000;ProPEX EP Elbow, 1\" PEX x 1\" PEX;9,1;10; 30 673 372 121 096 
New;FITTINGS PLASTIC;Q4761010;ProPEX EP 45 Elbow, 1\" PEX x 1\" PEX;13,35;10; 30 673 372 751 477 
;FITTINGS PLASTIC;Q4761250;ProPEX EP Elbow, 1¼\" PEX x 1¼\" PEX;19,2;1; 673 372 142 007 
New;FITTINGS PLASTIC;Q4761313;ProPEX EP 45 Elbow, 1¼\" PEX x 1¼\" PEX;21;1; 673 372 751 483 
;FITTINGS PLASTIC;Q4761500;ProPEX EP Elbow, 1½\" PEX x 1½\" PEX;25,5;1; 673 372 142 014 
;FITTINGS PLASTIC;Q4761515;ProPEX EP 45 Elbow, 1½\" PEX x 1½\" PEX;23,3;1; 673 372 313 278 
;FITTINGS PLASTIC;Q4762000;ProPEX EP Elbow, 2\" PEX x 2\" PEX;83,6;1; 673 372 217 682 
;FITTINGS PLASTIC;Q4762020;ProPEX EP 45 Elbow, 2\" PEX x 2\" PEX;83,6;1; 673 372 313 476 
;FITTINGS PLASTIC;Q4762500;ProPEX EP Elbow, 2½\" PEX x 2½\" PEX;134;1; 673 372 454 834 
;FITTINGS PLASTIC;Q4762525;ProPEX EP 45 Elbow, 2½\" PEX x 2½\" PEX;134;1; 673 372 454 858 
;FITTINGS PLASTIC;Q4763000;ProPEX EP Elbow, 3\" PEX x 3\" PEX;197;1; 673 372 454 841 
;FITTINGS PLASTIC;Q4763030;ProPEX EP 45 Elbow, 3\" PEX x 3\" PEX;197;1; 673 372 454 865 
;FITTINGS PLASTIC;Q4771010;ProPEX EP Coupling, 1\" PEX x 1\" PEX;4,96;10; 30 673 372 121 102 
;FITTINGS PLASTIC;Q4771307;ProPEX EP Coupling, 1¼\" PEX x ¾\" PEX;10,8;1; 673 372 233 866 
;FITTINGS PLASTIC;Q4771310;ProPEX EP Coupling, 1¼\" PEX x 1\" PEX;11,3;1; 673 372 234 061 
;FITTINGS PLASTIC;Q4771313;ProPEX EP Coupling, 1¼\" PEX x 1¼\" PEX;12,75;1; 673 372 234 078 
;FITTINGS PLASTIC;Q4771507;ProPEX EP Coupling, 1½\" PEX x ¾\" PEX;13,55;1; 673 372 234 085 
;FITTINGS PLASTIC;Q4771510;ProPEX EP Coupling, 1½\" PEX x 1\" PEX;13,9;1; 673 372 234 092 
;FITTINGS PLASTIC;Q4771513;ProPEX EP Coupling, 1½\" PEX x 1¼\" PEX;14,05;1; 673 372 234 108 
;FITTINGS PLASTIC;Q4771515;ProPEX EP Coupling, 1½\" PEX x 1½\" PEX;14,3;1; 673 372 234 269 
;FITTINGS PLASTIC;Q4772015;ProPEX EP Coupling, 2\" PEX x 1½\" PEX;46,4;1; 673 372 233 309 
;FITTINGS PLASTIC;Q4772020;ProPEX EP Coupling, 2\" PEX x 2\" PEX;59,3;1; 673 372 217 675 
;FITTINGS PLASTIC;Q4772513;ProPEX EP Coupling, 2½\" PEX x 1¼\" PEX;91,2;1; 673 372 454 872 
;FITTINGS PLASTIC;Q4772515;ProPEX EP Coupling, 2½\" PEX x 1½\" PEX;93,8;1; 673 372 454 889 
;FITTINGS PLASTIC;Q4772520;ProPEX EP Coupling, 2½\" PEX x 2\" PEX;95,6;1; 673 372 454 896 
;FITTINGS PLASTIC;Q4772525;ProPEX EP Coupling, 2½\" PEX x 2½\" PEX;96,4;1; 673 372 454 902 
;FITTINGS PLASTIC;Q4773020;ProPEX EP Coupling, 3\" PEX x 2\" PEX;117;1; 673 372 454 919 
;FITTINGS PLASTIC;Q4773025;ProPEX EP Coupling, 3\" PEX x 2½\" PEX;119;1; 673 372 454 926 
;FITTINGS PLASTIC;Q4773030;ProPEX EP Coupling, 3\" PEX x 3\" PEX;126;1; 673 372 454 933 
;FITTINGS PLASTIC;Q4773838;ProPEX EP Coupling, ?\" PEX x ?\" PEX;2,65;25; 30 673 372 121 119 
;FITTINGS PLASTIC;Q4775050;ProPEX EP Coupling, ½\" PEX x ½\" PEX;2,81;25; 30 673 372 121 126 
;FITTINGS PLASTIC;Q4775075;ProPEX EP Coupling, ½\" PEX x ¾\" PEX;5,9;25; 30 673 372 188 846 
;FITTINGS PLASTIC;Q4776363;ProPEX EP Coupling, ?\" PEX X ?\" PEX;6,05;10; 30 673 372 128 255 
;FITTINGS PLASTIC;Q4777510;ProPEX EP Coupling, ¾\" PEX x 1\" PEX;7,65;25; 30 673 372 188 853 
;FITTINGS PLASTIC;Q4777575;ProPEX EP Coupling, ¾\" PEX x ¾\" PEX;3,34;25; 30 673 372 121 133 
;MANIFOLDS PLASTIC;Q4801075;ProPEX EP Opposing-port Tee 1\" x 1\" x ¾\" x ¾\";29,4;1; 673 372 534 673 
;MANIFOLDS PLASTIC;Q4801375;ProPEX EP Opposing-port Tee 1¼\" x 1¼\" x ¾\" x ¾\";36,2;1; 673 372 534 680 
;MANIFOLDS PLASTIC;Q4801575;ProPEX EP Opposing-port Tee 1½\" x 1½\" x ¾\" x ¾\";60,6;1; 673 372 534 697 
;MANIFOLDS PLASTIC;Q4802075;ProPEX EP Opposing-port Tee 2\" x 2\" x ¾\" x ¾\";94,4;1; 673 372 534 703 
;FITTINGS METAL;Q5501010;ProPEX Brass Fitting Adapter, 1\" PEX x 1\" Copper;13,11;10; 30 673 372 530 386 
;FITTINGS METAL;Q5501313;ProPEX Brass Fitting Adapter, 1¼\" PEX x 1¼\" Copper;29,16;1; 673 372 530 392 
;FITTINGS METAL;Q5501515;ProPEX Brass Fitting Adapter, 1½\" PEX x 1½\" Copper;47,86;1; 673 372 530 408 
;FITTINGS METAL;Q5505050;ProPEX Brass Fitting Adapter, ½\" PEX x ½\" Copper;3,19;25; 30 673 372 530 348 
;FITTINGS METAL;Q5507510;ProPEX Brass Fitting Adapter, ¾\" PEX x 1\" Copper;14,06;10; 30 673 372 530 379 
;FITTINGS METAL;Q5507550;ProPEX Brass Fitting Adapter, ¾\" PEX x ½\" Copper;12,96;25; 30 673 372 530 355 
;FITTINGS METAL;Q5507575;ProPEX Brass Fitting Adapter, ¾\" PEX x ¾\" Copper;6,95;25; 30 673 372 530 362 
;FITTINGS METAL;Q5511010;ProPEX Brass Sweat Adapter, 1\" PEX x 1\" Copper;12,07;10; 30 673 372 530 300 
;FITTINGS METAL;Q5511313;ProPEX Brass Sweat Adapter, 1¼\" PEX x 1¼\" Copper;32,92;1; 673 372 530 316 
;FITTINGS METAL;Q5511515;ProPEX Brass Sweat Adapter, 1½\" PEX x 1½\" Copper;50,37;1; 673 372 530 323 
;FITTINGS METAL;Q5512020;ProPEX Brass Sweat Adapter, 2\" PEX x 2\" Copper;138,99;1; 673 372 530 330 
;FITTINGS METAL;Q5515050;ProPEX Brass Sweat Adapter, ½\" PEX x ½\" Copper;3,25;25; 30 673 372 529 960 
;FITTINGS METAL;Q5517510;ProPEX Brass Sweat Adapter, ¾\" PEX x 1\" Copper;14,58;10; 30 673 372 530 294 
;FITTINGS METAL;Q5517550;ProPEX Brass Sweat Adapter, ¾\" PEX x ½\" Copper;11,91;25; 30 673 372 530 270 
;FITTINGS METAL;Q5517575;ProPEX Brass Sweat Adapter, ¾\" PEX x ¾\" Copper;7,26;25; 30 673 372 530 287 
;FITTINGS METAL;Q5521010;ProPEX Brass Male Threaded Adapter, 1\" PEX x 1\" NPT;18,08;10; 30 673 372 529 670 
;FITTINGS METAL;Q5521075;ProPEX Brass Male Threaded Adapter, 1\" PEX x ¾\" NPT;18,13;10; 30 673 372 529 519 
;FITTINGS METAL;Q5521313;ProPEX Brass Male Threaded Adapter, 1¼\" PEX x 1¼\" NPT;40,23;1; 673 372 529 686 
;FITTINGS METAL;Q5521515;ProPEX Brass Male Threaded Adapter, 1½\" PEX x 1½\" NPT;56,12;1; 673 372 529 877 
;FITTINGS METAL;Q5522020;ProPEX Brass Male Threaded Adapter, 2\" PEX x 2\" NPT;146,3;1; 673 372 529 884 
;FITTINGS METAL;Q5525050;ProPEX Brass Male Threaded Adapter, ½\" PEX x ½\" NPT;4,85;25; 30 673 372 529 489 
;FITTINGS METAL;Q5527510;ProPEX Brass Male Threaded Adapter, ¾\" PEX x 1\" NPT;18,97;10; 30 673 372 529 502 
;FITTINGS METAL;Q5527550;ProPEX Brass Male Threaded Adapter,  ¾\" PEX x ½\" NPT;12,7;25; 30 673 372 740 075 
;FITTINGS METAL;Q5527575;ProPEX Brass Male Threaded Adapter, ¾\" PEX x ¾\" NPT;8,83;25; 30 673 372 529 496 
;FITTINGS METAL;Q5571010;ProPEX Brass Female Threaded Adapter, 1\" PEX x 1\" NPT;23,36;10; 30 673 372 529 922 
;FITTINGS METAL;Q5571313;ProPEX Brass Female Threaded Adapter, 1¼\" PEX x 1¼\" NPT;43,05;1; 673 372 529 938 
;FITTINGS METAL;Q5571515;ProPEX Brass Female Threaded Adapter, 1½\" PEX x 1½\" NPT;91,86;1; 673 372 529 945 
;FITTINGS METAL;Q5572020;ProPEX Brass Female Threaded Adapter, 2\" PEX x 2\" NPT;178,7;1; 673 372 529 952 
;FITTINGS METAL;Q5575050;ProPEX Brass Female Threaded Adapter, ½\" PEX x ½\" NPT;9,72;25; 30 673 372 529 892 
;FITTINGS METAL;Q5577510;ProPEX Brass Female Threaded Adapter, ¾\" PEX x 1\" NPT;34,49;10; 30 673 372 529 915 
;FITTINGS METAL;Q5577575;ProPEX Brass Female Threaded Adapter, ¾\" PEX x ¾\" NPT;10,87;25; 30 673 372 529 908 
;FITTINGS METAL;Q5806375;ProPEX Ball Valve, ?\" PEX x ¾\" Copper Adapter;46,4;10; 30 673 372 145 498 
;FITTINGS METAL;Q5807575;ProPEX Ball Valve, ¾\" PEX x ¾\" Copper Adapter;49,64;10; 30 673 372 145 504 
;FITTINGS METAL;Q5906375;ProPEX Ball and Balancing Valve, ?\" PEX x ¾\" Copper Adapter;88,3;10; 30 673 372 145 481 
;FITTINGS METAL;Q5907575;ProPEX Ball and Balancing Valve, ¾\" PEX x ¾\" Copper Adapter;92,27;10; 30 673 372 145 559 
;OTHER COMPONENTS;Q70640HW;Concealed Flat Cover Plate for HSW, White, (HSW style only);53,4;5; 30 673 372 287 075 
;OTHER COMPONENTS;Q70749WH;Concealed Flat Cover Plate for 162F LF RC-RES Sprinkler, White, 3¼\";33,1;100; 30 673 372 518 070 
;OTHER COMPONENTS;Q71850LW;Two-piece Recessed Escutcheon for LF Recessed Pendent and LF Recessed HSW, White;11,45;5; 30 673 372 287 273 
;OTHER COMPONENTS;Q7400500;Plastic Tubing Clip, ½\", 100/pkg.;66,1;1; 673 372 127 653 
;MOUNTING PARTS;Q7410510;PEX-a Pipe Support Strapping for ½\", ¾\" and 1\" PEX;1,51;100; 30 673 372 423 077 
;MOUNTING PARTS;Q7411220;PEX-a Pipe Support Strapping for 1¼\", 1½\" and 2\" PEX;2,58;100; 30 673 372 423 275 
;OTHER COMPONENTS;Q7412540;PEX-a Pipe Support Strapping for 2½\", 3\", 3½\" PEX;4,16;100; 30 673 372 462 076 
;TOOLS;Q7500400;Sprinkler Wrench, LF Recessed Pendent;306;1; 673 372 262 903 
;TOOLS;Q7500410;Sprinkler Wrench, LF Recessed Horizontal Sidewall;345;1; 673 372 286 671 
;TOOLS;Q7500700;Sprinkler Socket for LF RC-RES Sprinklers, LF74970FC and LF74971FW;287;1; 673 372 326 070 
;FITTINGS METAL;Q8521010;ProPEX Stainless-steel Male Threaded Adapter, 1\" PEX x 1\" NPT;86,3;10; 30 673 372 124 899 
;FITTINGS METAL;Q8525050;ProPEX Stainless-steel Male Threaded Adapter, ½\" PEX x ½\" NPT;38,7;25; 30 673 372 124 905 
;FITTINGS METAL;Q8527575;ProPEX Stainless-steel Male Threaded Adapter, ¾\" PEX x ¾\" NPT;57,8;25; 30 673 372 124 912 
New;FITTINGS PLASTIC;TF4235050;TotalFit Drop Ear Elbow, ½\" x ½\" FNPT;call for price;20; 30 673 372 736 672 
New;FITTINGS PLASTIC;TF4237575;TotalFit Drop Ear Elbow, ¾\" x ¾\" FNPT;call for price;12; 30 673 372 736 689 
New;FITTINGS PLASTIC;TF4350500;TotalFit Plug, ½\";call for price;50; 30 673 372 736 696 
New;FITTINGS PLASTIC;TF4350750;TotalFit Plug, ¾\";call for price;30; 30 673 372 736 702 
New;FITTINGS PLASTIC;TF4351000;TotalFit Plug, 1\";call for price;25; 30 673 372 736 719 
New;FITTINGS PLASTIC;TF4521010;TotalFit Male Threaded Adapter, 1\" x 1\" NPT;call for price;15; 30 673 372 736 726 
New;FITTINGS PLASTIC;TF4525050;TotalFit Male Threaded Adapter, ½\" x ½\" NPT;call for price;35; 30 673 372 736 733 
New;FITTINGS PLASTIC;TF4525075;TotalFit Male Threaded Adapter, ½\" x ¾\" NPT;call for price;30; 30 673 372 736 740 
New;FITTINGS PLASTIC;TF4527510;TotalFit Male Threaded Adapter, ¾\" x 1\" NPT;call for price;20; 30 673 372 736 757 
New;FITTINGS PLASTIC;TF4527575;TotalFit Male Threaded Adapter, ¾\" x ¾\" NPT;call for price;25; 30 673 372 736 764 
New;FITTINGS PLASTIC;TF4571010;TotalFit Female Threaded Adapter, 1\" x 1\" NPT;call for price;15; 30 673 372 736 771 
New;FITTINGS PLASTIC;TF4575050;TotalFit Female Threaded Adapter, ½\" x ½\" NPT;call for price;30; 30 673 372 736 788 
New;FITTINGS PLASTIC;TF4575075;TotalFit Female Threaded Adapter, ½\" x ¾\" NPT;call for price;25; 30 673 372 736 795 
New;FITTINGS PLASTIC;TF4577510;TotalFit Female Threaded Adapter, ¾\" x 1\" NPT;call for price;18; 30 673 372 736 801 
New;FITTINGS PLASTIC;TF4577575;TotalFit Female Threaded Adapter, ¾\" x ¾\" NPT;call for price;20; 30 673 372 736 818 
New;FITTINGS PLASTIC;TF4751010;TotalFit Tee, 1\" x 1\" x 1\";call for price;8; 30 673 372 736 825 
New;FITTINGS PLASTIC;TF4751150;TotalFit Reducing Tee, 1\" x 1\" x ½\";call for price;10; 30 673 372 736 832 
New;FITTINGS PLASTIC;TF4751175;TotalFit Reducing Tee, 1\" x 1\" x ¾\";call for price;10; 30 673 372 736 849 
New;FITTINGS PLASTIC;TF4755050;TotalFit Tee, ½\" x ½\" x ½\";call for price;20; 30 673 372 736 856 
New;FITTINGS PLASTIC;TF4757550;TotalFit Reducing Tee, ¾\" x ¾\" x ½\";call for price;14; 30 673 372 736 863 
New;FITTINGS PLASTIC;TF4757555;TotalFit Reducing Tee, ¾\" x ½\" x ½\";call for price;15; 30 673 372 736 870 
New;FITTINGS PLASTIC;TF4757575;TotalFit Tee, ¾\" x ¾\" x ¾\";call for price;12; 30 673 372 736 887 
New;FITTINGS PLASTIC;TF4760500;TotalFit Elbow, ½\" x ½\";call for price;25; 30 673 372 736 894 
New;FITTINGS PLASTIC;TF4760750;TotalFit Elbow, ¾\" x ¾\";call for price;15; 30 673 372 736 900 
New;FITTINGS PLASTIC;TF4761000;TotalFit Elbow, 1\" x 1\";call for price;10; 30 673 372 736 917 
New;FITTINGS PLASTIC;TF4771010;TotalFit Coupling, 1\" x 1\";call for price;15; 30 673 372 736 924 
New;FITTINGS PLASTIC;TF4775050;TotalFit Coupling, ½\" x ½\";call for price;30; 30 673 372 736 931 
New;FITTINGS PLASTIC;TF4775075;TotalFit Coupling, ½\" x ¾\";call for price;25; 30 673 372 736 948 
New;FITTINGS PLASTIC;TF4777510;TotalFit Coupling, ¾\" x 1\";call for price;15; 30 673 372 736 955 
New;FITTINGS PLASTIC;TF4777575;TotalFit Coupling, ¾\" x ¾\";call for price;18; 30 673 372 736 962 
New;FITTINGS PLASTIC;TF4781010;TotalFit Repair Coupling, 1\" x 1\";call for price;9; 30 673 372 736 979 
New;FITTINGS PLASTIC;TF4785050;TotalFit Repair Coupling, ½\" x ½\";call for price;24; 30 673 372 736 986 
New;FITTINGS PLASTIC;TF4787575;TotalFit Repair Coupling, ¾\" x ¾\";call for price;12; 30 673 372 736 993 
New;TOOLS;TF4800500;TotalFit Removal Tool, ½\";call for price;40; 30 673 372 737 006 
New;TOOLS;TF4800750;TotalFit Removal Tool, ¾\";call for price;40; 30 673 372 737 013 
New;TOOLS;TF4801000;TotalFit Removal Tool, 1\";call for price;40; 30 673 372 737 020 
New;TOOLS;TF4808000;TotalFit Deburr and Depth Tool;call for price;6; 30 673 372 737 037 
;FITTINGS PLASTIC;WS4360750;ProPEX EP Straight Water Meter Fitting, ¾\" PEX x 1\" NPSM;18,45;1; 673 372 536 677 
;FITTINGS PLASTIC;WS4360751;ProPEX EP Elbow Water Meter Fitting, ¾\" PEX x 1\" NPSM;20,6;1; 673 372 536 691 
;FITTINGS PLASTIC;WS4361000;ProPEX EP Straight Water Meter Fitting, 1\" PEX x 1¼\" NPSM;21,2;1; 673 372 536 684 
;FITTINGS PLASTIC;WS4361001;ProPEX EP Elbow Water Meter Fitting, 1\" PEX x 1¼\" NPSM;23,95;1; 673 372 536 707 
;FITTINGS METAL;WS4820750;ProPEX LF Brass Straight Water Meter Valve, ¾\" PEX x 1\" NPSM;48;1; 673 372 536 714 
;FITTINGS METAL;WS4820751;ProPEX LF Brass Elbow Water Meter Valve, ¾\" PEX x 1\" NPSM;48;1; 673 372 536 738 
;FITTINGS METAL;WS4821000;ProPEX LF Brass Straight Water Meter Valve, 1\" PEX x 1¼\" NPSM;66,8;1; 673 372 536 721 
;FITTINGS METAL;WS4821001;ProPEX LF Brass Elbow Water Meter Valve, 1\" PEX x 1¼\" NPSM;66,8;1; 673 372 536 745 
;Uponor reserves the right to increase quantities to the next package allowable.;;;;;;

    """

    



    
    messages = [{"role": "user", "content": query}, {"role": "system", "content": system_message} ] 

    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo-0613",
        model="gpt-4",
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
