
from settings import TOKEN
from commands.bot_commands import client
import nltk

if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('stopwords')
    client.run(TOKEN)
