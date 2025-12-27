from flask import Flask,render_template,request
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

#calling your  API KEY creating env 
load_dotenv()

app=Flask(__name__)
#configure gemini

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-2.5-flash")

#reading the file using the pnadas fro the framework
df=pd.read_csv("qa_data (1).csv")

#convert csv into text content 
context_text=""
for _, row in df.iterrows():
    context_text +=f"Q: {row['question']}\nA: {row['answer']}\n\n"

def ask_gemini(query):
    prompt = f"""
you are a Q&A assistant

Answer only using the context below 
if the answer is not present, say: No relevant Q&A found 

context:
{context_text}

Question: {query}
"""
    response=model.generate_content(prompt)
    return response.text.strip()

###Route Function
@app.route("/",methods=["GET","POST"])
def home():
    answer = ""
    if request.method=="POST":
        query=request.form["query"]
        answer=ask_gemini(query)
    return render_template("index.html",answer=an swer)
#run Flask app
if __name__ =="__main__":
    app.run()