from openai import AzureOpenAI
import os 
import requests
import json

client = AzureOpenAI(
	api_key = os.getenv("AZURE_KEY"),
	azure_endpoint = os.getenv("AZURE_ENDPOINT"),
	api_version ="2023-10-01-preview",
)


with open("news_key.txt", 'r') as key_file:
	news_key = key_file.read().strip()

def get_top_headlines(country="us", category="entertainment"):
	url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={news_key}"
	response = requests.get(url)
	data = response.json()

	if "articles" in data:
		return [article["title"] for article in data["articles"][:5]]
	return []


def get_pun_joke(keyword):
	url = f"https://v2.jokeapi.dev/joke/Pun?type=single"
	response = requests.get(url)
	data = response.json()

#getting the pun jokes based on a keyword
	if "jokes" in data:
		return data["jokes"]
	return "no joke founded"


#combine headlines with the jokes

def generate_headline_jokes():
	headlines = get_top_headlines()
	if not headlines:
		return []

# genarate joke for each headline 
	jokes = []
	for headline in headlines:
		joke = get_pun_joke(keyword)
		jokes.append({"headline": headline,"joke":joke})
	
	return jokes


messages = [
	{"role": "system", "content": "You are a helpful assistant that combines entertainment news and humor."},
	{"role": "user","content": "Tell me the top 5 enternainment healines with pun jokes!"}

]



functions = [
	{
		"type":"function",
		"function": {
			"name": "generate_headline_jokes",
			"description": "Get the top entertainment headlines and genarate pun jokes for each headline.",
			"parameters": {
				"type":"object",
				"properties":{},
				"required":[],
			}
		}
	}

]

response = client.chat.completions.create(model = "GPT-4", messages=messages)


gpt_tools = response.choices[0].message.tool_calls

if gpt_tools:

	for gpt_tool in gpt_tools:
		function_name = gpt_tool.function.name
		function_parameters = json.loads(gpt_tool.function.arguments)


	if function_name == "generate_headline_jokes":
		jokes_with_headlines = generate_headline_jokes()
		for item in jokes_with_headlines:
			print(f"Headline: {item['headline']}")
			print(f"joke: {item['joke']}")
	

else:
	print(response.choices[0].message.content)
