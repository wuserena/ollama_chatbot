# Retrieve From: https://ollama.com/blog/embedding-models

import ollama
import chromadb

# Sample documents
documents = [
    "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels.",
    "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands.",
    "Llamas can grow as much as 6 feet tall, though the average llama is between 5 feet 6 inches and 5 feet 9 inches tall.",
    "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight.",
    "Llamas are vegetarians and have very efficient digestive systems.",
    "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old."
]

# Initialize ChromaDB client
client = chromadb.PersistentClient()  # Use HttpClient() if running a server
collection = client.get_or_create_collection(name="docs")

# Store documents in the vector database
for i, d in enumerate(documents):
  response = ollama.embed(model="mxbai-embed-large", input=d)
  embeddings = response["embeddings"]
  collection.add(
    ids=[str(i)],
    embeddings=embeddings,
    documents=[d]
  )

# Example query
prompt = "What animals are llamas related to?"

## generate an embedding for the input and retrieve the most relevant doc
response = ollama.embed(
  model="mxbai-embed-large",
  input=prompt
)
results = collection.query(
  query_embeddings=response["embeddings"],
  n_results=1
)
data = results["documents"][0][0]  # Retrieve the best match

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="llama3",
  prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

print(output['response'])
