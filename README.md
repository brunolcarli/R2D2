<table align="center"><tr><td align="center" width="9999">

<img src="https://i.ebayimg.com/images/g/1rQAAOSwhLJZorIU/s-l300.jpg" align="center" width="150" alt="Project icon">

# R2D2 - Civil Cultural Discord Bot

[![Generic badge](https://img.shields.io/badge/docs-blue.svg)](https://gitlab.com/civil-cultural/r2d2/wikis/home)

Help Bot for Civil Cultural project.

</td></tr></table>


# Run as developer

First of all you will have to make an account on [Discord developers portal](http://discordapp.com/developers/), start an app and include a bot on your application. Generate the `token` for the bot and paste the token on a `.env` file on the project root, like this:

```
TOKEN=iuagdsucfdshgfujsfiukshdfiosgduyfhsiuhjfnsiudhfgs
```

Engage your python virtual environment and install the requirements

```
make install
```

Run the bot locally

```
make run
```

The bot should print out `BIP BIP READY!` on the terminal.

Dont forget to add the bot to your Discord servers generating an invite link on your Developer Portal.