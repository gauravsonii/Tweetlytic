import config
import requests
from openai import OpenAI
from random_id import random_id
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


def genText():

    chat = ChatGoogleGenerativeAI(
        temperature=1,
        max_tokens=90,
        model="gemini-1.5-flash",
        google_api_key=config.GOOGLEAI_API_KEY,
    )

    system = """
    You are a wise, calm, and composed being, embodying the serene wisdom of Naval Ravikant. Your task is to share profound philosophical reflections on a wide range of topics, each response uniquely crafted and under 240 characters. Build upon the ideas of history's great thinkers, maintaining a composed demeanour and avoiding unnecessary repetition or formatting. If no topic is provided, select a diverse and thought-provoking subject randomly.
    """

    human = "{query}"

    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", human)])

    chain = prompt | chat

    response = chain.invoke({"query": " "})

    return response.content


def getImagePrompt(genText):

    chat = ChatGroq(
        temperature=0.2,
        max_tokens=150,
        model="gemma2-9b-it",
        api_key=config.GROQ_API_KEY
    )

    system = """
    Generate a high-quality prompt for the DALL-E 3 model to create an image. The prompt should be concise, engaging, and describe a unique, visually appealing, and thought-provoking concept. It should capture the essence of the given text in a creative and imaginative way. The prompt should be under 50 words and comma-separated. Include keywords like high quality, 8k, photorealistic, vibrant colors, etc. Here are some examples:
    - A serene sunset over a mountain range, high quality, 8k, photorealistic, vibrant colors.
    - A bustling futuristic cityscape at night, high quality, 8k, photorealistic, vibrant colors.
    Don't write anything else in the prompt, just the sentence.
    """

    human = "{query}"

    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", human)])

    chain = prompt | chat

    response = chain.invoke({"query": genText})

    return response.content


def genImage(prompt):

    client = OpenAI(
        api_key=config.OPENAI_API_KEY,
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    image_data = requests.get(image_url).content

    image_name = random_id() + ".png"

    with open(f"images/{image_name}", "wb") as f:
        f.write(image_data)

    return image_data, image_name

# generatedText = genText()
# print(generatedText)
# imagePrompt = getImagePrompt(generatedText)
# print(imagePrompt)
