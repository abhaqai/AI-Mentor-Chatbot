import google.generativeai as genai

# Configure API Key
genai.configure(api_key='AIzaSyCPCw8-RxzyEsN1QbFhS03w7pC8a2dgcnM')

def sentiment_analysis(text):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    response = model.generate_content(f"""You are trained to analyze and detect the sentiment of given text.
                If you're unsure of an answer, you can say "not sure" and recommend users to review manually.
                Analyze the following text and determine if the sentiment is: positive or negative.
                Return answer in a single word as either positive or negative: {text}""")

    response_text = response.text.strip().lower()
    return response_text

# Calling the function
input_text = 'I love eating ice cream'
response = sentiment_analysis(input_text)
print(input_text, ': The Sentiment is', response)
