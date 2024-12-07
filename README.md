![StatCrafter Logo](statcrafter.png)

# StatCrafter

A python-based web application that pulls and displays real-time statistics from Minecraft servers. This project gathers data about players, the world, and player achievements, showcasing them in an easily readable format.

## Features

- **Player Stats**: View detailed statistics for each player, including their UUID, username, skin, cape, all in-game stats, and achievements.
- **Server Stats**: Access server-related data like the version, player count, and currently online players
- **Player Advancements**: Display the advancements each player has gotten on the server
- **Real-Time Data**: Information is pulled directly from the Minecraft server, ensuring up-to-date stats.

# Setup

# Standalone Server
```
git clone https://github.com/Yeetoxic/StatCrafter.git
```

# Docker Compose Server Package
Download 'docker-compose.yml' and place it where you would like to build your server
```
docker-compose up -d
```
from here you can start and stop the server and app the same you would any other docker container

# Additional Setup
- Note: please set `enable-query` to `true` in the `server.properties` file!
