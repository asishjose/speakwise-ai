from speakwise.agents.workflow import process_request


# user_input = """
# Write an email to my manager requesting two days of leave.
# Make it polite and professional.
# """

user_input = """
I have already written an email. Make it more polite 
and correct its grammar.
"""

result = process_request(user_input)

print("\nIDENTIFIED INTENT")
print(result["intent"].model_dump_json(indent=2))

print("\nEXECUTION PLAN")
print(result["plan"].model_dump_json(indent=2))