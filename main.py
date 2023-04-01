
from settings import TOKEN
from commands.bot_commands import client
from commands.keep_alive import keep_aive


if __name__ == "__main__":
    keep_alive()
    client.run(TOKEN)