import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()



class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"From the mail below, extract what shall be quoted using the Price List, select the items that yields the lowest total cost, only the quantities from the price list should be used and combined to fulfill the requested items. A general rule of thumb, for a 1000 square foot area, you would need approximately 1000 feet of pipe if you're planning on 12-inch spacing between the pipes. This is the most common spacing used for underfloor heating systems. You are working at the sales office at Uponor and your name in Pamela Anderson, write a friendly quotation to the person signing the mail. If there are items in the request that are not included in the price list note that the price for those items will be given later. Include the price for the items that could be found in the price list. If the request is using meters, convert it to ft before calculating the cost: {content} "
    #system_message="price list: \n AquaPEX Pex pipe 1/2\": 1 usd/ft \n  AquaPEX Pex pipe 3/4\" : 1.3 usd/ft \n AquaPEX Pex pipe 3\" : 2 usd/ft \n Fitting 1/2\" : 2 usd/ft \n Fitting 3/4\" : 3 usd/ft \n Fitting 1\" : 4 usd/ft \n"
    system_message="""
Price List:
Part Description;List Price
5/16\" Wirsbo hePEX, 100-ft. coil;$154,02
3/8\" Wirsbo hePEX, 100-ft. coil;$166,26
 1/2\" Wirsbo hePEX, 100-ft. coil;$154,02
5/8\" Wirsbo hePEX, 100-ft. coil;$206,04
 3/4\" Wirsbo hePEX, 100-ft. coil;$253,98
1\" Wirsbo hePEX, 100-ft. coil;$427,38
1 1/4\" Wirsbo hePEX, 100-ft. coil;$765,00
1 1/2\" Wirsbo hePEX, 100-ft. coil;$1 014,90
2\" Wirsbo hePEX, 100-ft. coil;$1 591,20
5/16\" Wirsbo hePEX, 250-ft. coil;$382,50
3/8\" Wirsbo hePEX, 400-ft. coil;$673,20
5/8\" Wirsbo hePEX, 400-ft. coil;$826,20
5/16\" Wirsbo hePEX, 1,000-ft. coil;$1 540,20
3/8\" Wirsbo hePEX, 1,000-ft. coil;$1 662,60
 1/2\" Wirsbo hePEX, 1,000-ft. coil;$1 540,20
5/8\" Wirsbo hePEX, 1,000-ft. coil;$2 060,40
 3/4\" Wirsbo hePEX, 1,000-ft. coil;$2 539,80
 3/4\" Wirsbo hePEX, 500-ft. coil;$1 275,00
1\" Wirsbo hePEX, 500-ft. coil;$2 142,00
 1/2\" Wirsbo hePEX, 300-ft. coil;$459,00
5/8\" Wirsbo hePEX, 300-ft. coil;$622,20
 3/4\" Wirsbo hePEX, 300-ft. coil;$765,00
1\" Wirsbo hePEX, 300-ft. coil;$1 295,40
1 1/4\" Wirsbo hePEX, 300-ft. coil;$2 295,00
1 1/2\" Wirsbo hePEX, 300-ft. coil;$3 029,40
2\" Wirsbo hePEX, 300-ft. coil;$4 732,80
 1/2\" Wirsbo hePEX, 500-ft. coil;$770,10
1\" Wirsbo hePEX, 20-ft. straight length, 200 ft. (10 per bundle);$948,60
1 1/4\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);$790,50
1 1/2\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);$1 050,60
2\" Wirsbo hePEX, 20-ft. straight length, 100 ft. (5 per bundle);$1 642,20
2 1/2\" Wirsbo hePEX 20-ft. straight length, 60 ft.(3 per bundle);$1 295,40
3\" Wirsbo hePEX 20-ft. straight length, 40 ft.(2 per bundle);$1 173,00
 1/2\" Wirsbo hePEX, 20-ft. straight length, 500 ft. (25 per bundle);$846,60
5/8\" Wirsbo hePEX, 20-ft. straight length, 300 ft. (15 per bundle);$683,40
 3/4\" Wirsbo hePEX, 20-ft. straight length, 300 ft. (15 per bundle);$841,50
 1/2\" Pre-insulated Wirsbo hePEX with  1/2\" insulation, 100-ft. coil;$535,60
 3/4\" Pre-insulated Wirsbo hePEX with  1/2\" insulation, 100-ft. coil;$655,20
1\" Pre-insulated Wirsbo hePEX with  1/2\" insulation, 100-ft. coil;$790,40
 3/4\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;$960,75
1\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;$1 176,00
1 1/4\" Pre-insulated Wirsbo hePEX with 1\" insulation, 100-ft. coil;$1 680,00
 3/4\" Pre-insulated Wirsbo hePEX with 1 1/2\" insulation, 100-ft. coil;$1 378,00
1\" Pre-insulated Wirsbo hePEX with 1 1/2\" insulation, 100-ft. coil;$1 600,60
1 1/4\" Pre-insulated Wirsbo hePEX with 1 1/2\" insulation, 100-ft. coil;$2 162,40
1 1/2\" Pre-insulated Wirsbo hePEX with 1 1/2\" insulation, 75-ft. coil;$1 971,60
1 1/4\" Uponor AquaPEX White, 300-ft. coil;$1 940,00
1 1/2\" Uponor AquaPEX White, 300-ft. coil;$2 260,00
2\" Uponor AquaPEX White, 300-ft. coil;$4 510,00
3\" Uponor AquaPEX White, 300-ft. coil;$7 990,00
 1/4\" Uponor AquaPEX White, 100-ft. coil;$81,10
 1/2\" Uponor AquaPEX White, 100-ft. coil;$93,80
 3/4\" Uponor AquaPEX White, 100-ft. coil;$162,00
1\" Uponor AquaPEX White, 100-ft. coil;$291,00
2\" Uponor AquaPEX White, 200-ft. coil;$3 010,00
 1/2\" Uponor AquaPEX White, 300-ft. coil;$282,00
 1/2\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;$288,00
5/8\" Uponor AquaPEX White, 300-ft. coil;$420,00
 3/4\" Uponor AquaPEX White, 300-ft. coil;$483,00
 3/4\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;$492,00
1\" Uponor AquaPEX White, 300-ft. coil;$875,00
1\" Uponor AquaPEX Purple Reclaimed Water, 300-ft. coil;$925,00
1 1/4\" Uponor AquaPEX White, 100-ft. coil;$650,00
1 1/2\" Uponor AquaPEX White, 100-ft. coil;$755,00
2\" Uponor AquaPEX White, 100-ft. coil;$1 510,00
2 1/2\" Uponor AquaPEX White, 100-ft. coil;$1 980,00
3\" Uponor AquaPEX White, 100-ft. coil;$2 670,00
3/8\" Uponor AquaPEX White, 400-ft. coil;$316,00
 1/2\" Pre-sleeved Uponor AquaPEX Blue Sleeve, 400-ft. coil;$645,00
 3/4\" Pre-Sleeved Uponor AquaPEX Blue Sleeve, 400-ft. coil;$990,00
 1/2\" Pre-sleeved Uponor AquaPEX Red Sleeve, 400-ft. coil;$645,00
 3/4\" Pre-Sleeved Uponor AquaPEX Red Sleeve, 400-ft. coil;$990,00
 1/2\" Uponor AquaPEX White, 500-ft. coil;$469,00
 3/4\" Uponor AquaPEX White, 500-ft. coil;$810,00
1\" Uponor AquaPEX White, 500-ft. coil;$1 470,00
3/8\" Uponor AquaPEX White, 1,000-ft. coil;$835,00
 1/2\" Uponor AquaPEX White, 1,000-ft. coil;$940,00
5/8\" Uponor AquaPEX White, 1,000-ft. coil;$1 420,00
1 1/4\" Uponor AquaPEX Purple Reclaimed Water, 10-ft. straight length, 50 ft. (5 per bundle);$398,00
1\" Uponor AquaPEX White, 20-ft. straight length, 200 ft. (10 per bundle);$635,00
1\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 200 ft. (10 per bundle);$785,00
1 1/4\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);$670,00
1 1/2\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);$780,00
2\" Uponor AquaPEX White, 20-ft. straight length, 100 ft. (5 per bundle);$1 560,00
2 1/2\" Uponor AquaPEX White, 20-ft. straight length, 60 ft. (3 per bundle);$1 230,00
3\" Uponor AquaPEX White, 20-ft. straight length, 40 ft. (2 per bundle);$1 110,00
 1/2\" Uponor AquaPEX White, 20-ft. straight length, 500 ft. (25 per bundle);$515,00
 3/4\" Uponor AquaPEX White, 20-ft. straight length, 300 ft. (15 per bundle);$530,00
1\" Uponor AquaPEX Purple Reclaimed Water, 10-ft. straight length, 100 ft. (10 per bundle);$385,00
1 1/4\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);$715,00
1 1/2\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);$920,00
2\" Uponor AquaPEX Purple Reclaimed Water, 20-ft. straight length, 100 ft. (5 per bundle);$1 840,00
 1/2\" Uponor AquaPEX Red, 100-ft. coil;$103,00
 3/4\" Uponor AquaPEX Red, 100-ft. coil;$180,00
1\" Uponor AquaPEX Red, 100-ft. coil;$319,00
 1/2\" Uponor AquaPEX Red, 300-ft. coil;$309,00
 3/4\" Uponor AquaPEX Red, 300-ft. coil;$535,00
1\" Uponor AquaPEX Red, 300-ft. coil;$960,00
 1/2\" Uponor AquaPEX Red, 1,000-ft. coil;$1 030,00
1\" Uponor AquaPEX Red, 20-ft. straight length, 200 ft. (10 per bundle);$715,00
 1/2\" Uponor AquaPEX Red, 20-ft. straight length, 500 ft. (25 per bundle);$575,00
 3/4\" Uponor AquaPEX Red, 20-ft. straight length, 300 ft. (15 per bundle);$595,00
 1/2\" Uponor AquaPEX Blue, 100-ft. coil;$103,00
 3/4\" Uponor AquaPEX Blue, 100-ft. coil;$180,00
1\" Uponor AquaPEX Blue, 100-ft. coil;$319,00
 1/2\" Uponor AquaPEX Blue, 300-ft. coil;$309,00
 3/4\" Uponor AquaPEX Blue, 300-ft. coil;$535,00
1\" Uponor AquaPEX Blue, 300-ft. coil;$960,00
 1/2\" Uponor AquaPEX Blue, 1,000-ft. coil;$1 030,00
1\" Uponor AquaPEX Blue, 20-ft. straight length, 200 ft. (10 per bundle);$715,00
 1/2\" Uponor AquaPEX Blue, 20-ft. straight length, 500 ft. (25 per bundle);$575,00
 3/4\" Uponor AquaPEX Blue, 20-ft. straight length, 300 ft. (15 per bundle);$595,00
 1/2\" Uponor AquaPEX White, Red Print, 1,000-ft. coil;$940,00
 1/2\" Uponor AquaPEX White, Red Print, 100-ft. coil;$93,80
 3/4\" Uponor AquaPEX White, Red Print, 100-ft. coil;$162,00
1\" Uponor AquaPEX White, Red Print, 100-ft. coil;$291,00
 1/2\" Uponor AquaPEX White, Red Print, 300-ft. coil;$282,00
 3/4\" Uponor AquaPEX White, Red Print, 300-ft. coil;$483,00
1\" Uponor AquaPEX White, Red Print, 300-ft. coil;$875,00
 1/2\" Uponor AquaPEX White, Blue Print, 1,000-ft. coil;$940,00
 1/2\" Uponor AquaPEX White, Blue Print, 100-ft. coil;$93,80
 3/4\" Uponor AquaPEX White, Blue Print, 100-ft. coil;$162,00
1\" Uponor AquaPEX White, Blue Print, 100-ft. coil;$291,00
 1/2\" Uponor AquaPEX White, Blue Print, 300-ft. coil;$282,00
 3/4\" Uponor AquaPEX White, Blue Print, 300-ft. coil;$483,00
1\" Uponor AquaPEX White, Blue Print, 300-ft. coil;$875,00
 1/2\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 500-ft. (25 per bundle);$515,00
 3/4\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 300-ft. (15 per bundle);$530,00
1\" Uponor AquaPEX White, Red Print, 20-ft. straight length, 200-ft. (10 per bundle);$635,00
 1/2\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 500-ft. (25 per bundle);$515,00
 3/4\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 300-ft. (15 per bundle);$530,00
1\" Uponor AquaPEX White, Blue Print, 20-ft. straight length, 200-ft. (10 per bundle);$635,00
 1/2\" Pre-insulated Uponor AquaPEX with  1/2\" insulation, 100-ft. coil;$457,00
 3/4\" Pre-insulated Uponor AquaPEX with  1/2\" insulation, 100-ft. coil;$560,00
1\" Pre-insulated Uponor AquaPEX with  1/2\" insulation, 100-ft. coil;$685,00
 1/2\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;$700,00
 3/4\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;$820,00
1\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;$1 000,00
1 1/4\" Pre-insulated Uponor AquaPEX with 1\" insulation, 100-ft. coil;$1 470,00

"""
    



    
    messages = [{"role": "user", "content": query}, {"role": "system", "content": system_message} ] 

    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo-16k",
        model="gpt-4",
        temperature=0.5,
        messages=messages
    )

    arguments = response.choices[0]["message"]["content"]
    #response['choices'][0]['message']['content']})
    companyName ="z"
    cost = "0"
    mail_reply = arguments
    

    return {
        "companyName": companyName,
        "cost": cost,
        "mail_reply": mail_reply
    }
