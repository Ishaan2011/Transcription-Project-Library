######## USING TEXTBLOB FOR SENTIMENT ANALYSIS ########

# from textblob import TextBlob

# def analyze_sentiment(text):

#     blob = TextBlob(text)
#     sentiment_score = blob.sentiment.polarity
#     if sentiment_score > 0:
#         print("Positive")
#     elif sentiment_score < 0:
#         print("Negative")
#     else:
#         print("Neutral")


####### USING OLLAMA FOR SENTIMENT ANALYSIS ########
import ollama

def analyze_emotion(text):
    model = "llama3.2:1b"  # Choose an appropriate model compatible with Ollama
    prompt = f"Classify the emotion of the following text: '{text}'. Possible emotions include: happy, very happy, annoyed, sad, very sad, neutral, jeolous, angry, excited. Dont give the answer of u being an AI model as this is just for educational purposes. "
    
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    
    print(response['message']['content'] if 'message' in response else "Error in analysis")

# analyze_emotion("why are good things happening to u not me")