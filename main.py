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
