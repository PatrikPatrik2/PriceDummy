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
;FTGS & ACCS;1007361;Fitting 1/2\";715;1; 673 372 236 386 
;FTGS & ACCS;1007362;AquaPEX Pex pipe 1/2\";760;1; 673 372 236 393 
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
