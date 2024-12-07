![StatCrafter Logo](statcrafter.png)

# StatCrafter

A python-based web application that pulls and displays real-time statistics from Minecraft servers. This project gathers data about players, the world, and player achievements, showcasing them in an easily readable format.

## Features

- **Player Stats**: View detailed statistics for each player, including their UUID, username, skin, cape, and all in-game stats
- **Server Stats**: Access server-related data like the version, player count, and currently online players
- **Player Advancements**: Display the advancements each player has gotten on the server
- **Real-Time Data**: Information is pulled directly from the Minecraft server, ensuring up-to-date stats.

# Setup

### Python 3 is **required**

## Standalone Server
Clone the repository into the root directory of your server
```
git clone https://github.com/Yeetoxic/StatCrafter.git
```
- Execute 'InstallDependencies.bat' to set up the requirements
- Execute 'RunStatCrafter.bat' to start the program

## Docker Compose Server Package
Download 'docker-compose.yml' and place it where you would like to build your server
```
docker-compose up -d
```
You may start and stop the server and app the same you would any other docker container

## Additional Setup
- Set `enable-query` to `true` in the `server.properties` file!
- Edit values in 'StatCrafterConfig.json' to set website name, server name, and IP address
- Open port 5000 on your router if you want your players to be able to view the webserver

## Live Example
- https://meteorcraft.serveminecraft.net/
