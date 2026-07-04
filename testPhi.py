from ollama import Client
from pydantic import BaseModel

# 1. Define the exact JSON structure you want using Pydantic
class MathProblem(BaseModel):
    question: str
    step_by_step_solution: list[str]
    final_answer: str

print("Connecting to local Ollama engine...")

try:
    # 2. Initialize the client 
    # (No API key needed! It talks directly to your local machine)
    client = Client(host='http://localhost:11434')
    
    model_name = "phi4-mini"

    # 3. Make the request with the JSON format enforced
    response = client.chat(
        model=model_name,
        messages=[
            {
                "role": "system", 
                "content": "You are a math problem generator. Provide realistic word problems."
            },
            {
                "role": "user", 
                "content": "Generate a 9th-grade algebra word problem."
            }
        ],
        # This one line forces the AI to output valid JSON matching your class above
        format=MathProblem.model_json_schema()
    )
    
    print("\n✅ Success!")
    print("Phi-4-mini says:\n")
    
    # The output will be a clean JSON string
    print(response.message.content)

except Exception as e:
    print("\n❌ Error connecting to Ollama:")
    print(e)
    print("Tip: Make sure the Ollama app is open and running in the background!")