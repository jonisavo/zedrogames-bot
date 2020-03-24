# zedrogames-bot
The Discord Triple-A Game Developer Bot

The ZEDROGAMES bot is something I made for my side project: Pokémon as a Service.
It is designed to be deployed on Heroku.

This bot has many features that are designed to only work on the Discord server of Pokémon as a Service.

## Configuration
The following environment variables are required to be set:
- `DISCORD_TOKEN` - Your bot's token.
- `OWNER_ID` - The id of the owner.

There's also an optional variable `PAAS_GUILD` (guild ID for the Pokémon as a Service server), which is used
for the extensions related to Pokémon as a Service.

## Structure & Features
The bot's functionality is divided into many separate extensions that can be enabled or disabled at will with the
`!addext` and `!rmext` commands. All extensions are activated by default when the bot logs in to Discord. The
`!listext` command allows you to see all active extensions.

Upon issuing a command, the bot will automatically attempt to delete it. The `manage_messages` permission is required
for this. An error will be printed out if the permission is missing, but the bot will otherwise ignore it.

The extensions bundled in zedrogames-bot are as follows:

#### `zedrogames.core.base` - Base Commands
`!help` - In the triple-A games industry, no one can hear you scream.

`!message` - Have the bot write a message to any text channel in the current server (owner only).

#### `zedrogames.core.responses` - Random Responses
With this extension active, the bot will pick a random quotes from `utils/quotes.py` and respond to messages with them.

`!quote` - Picks a random quote and sends it to the current channel (owner only).

#### `zedrogames.fun.microtransactions` - Microtransactions
With this extension active, the bot will randomly lock users out of a server until they "pay" a microtransaction
(react to a DM with the :moneybag: emoji). This should be rare. When the bot connects to Discord, it automatically
removes any locked roles it sees. **NOTE:** The locked role must be called "locked". Also, the `manage_roles`
permission is required for adding and removing the locked role.

`!purgelocks` - Manually removes locked roles from everyone who has it (owner only).

`!lockme` - Automatically locks your account for testing purposes (owner only).

#### `zedrogames.fun.rgsserrors` - RGSS Errors
This is a dumb one: with this extension active, the bot will occasionally ask for help with a randomly generated
RGSS error.

`!rgsserror` - Sends a random error help request to the current channel (owner only).

#### `zedrogames.fun.todd` - Todd Howard
With this extension active, the bot will react to all Bethesda-related keywords with the :todd: emoji, found in
the Discord server for Pokémon As A Service. **NOTE:** this extension requires the `PAAS_GUILD` environment variable 
to be set, and that the guild with the given ID has an emoji called "todd". Otherwise the extension does nothing.

#### `zedrogames.paas.download` - PAAS Download Link
**NOTE:** This extension is only usable in the Discord server for Pokémon As A Service.

`!download` - Sends a download link for PAAS. (However, since the game is not out yet, only thanks for the interest)

#### `zedrogames.paas.topup` - PAAS Topup
**NOTE:** This extension is only usable in the Discord server for Pokémon As A Service.

`!topup` - Sends a unique topup code.
