# StatCrafter

A python-based web application that pulls and displays real-time statistics from Minecraft servers. This project gathers data about players, the world, and player achievements, showcasing them in an easily readable format.

## Features

- **Player Stats**: View detailed statistics for each player, including their UUID, username, and achievements.
- **World Stats**: Access world-related data like the current environment, time, and weather conditions.
- **Player Achievements**: Display the achievements earned by players on the server.
- **Real-Time Data**: Information is pulled directly from the Minecraft server, ensuring up-to-date stats.

## Technology Stack

- **Python**: Used for scripting and interacting with the Minecraft server.
- **Flask**: A lightweight framework for serving the stats on a webpage.
- **Docker**: Containerizes the application to ensure a consistent environment across deployments.
- **JSON**: Data is exported in JSON format for easy parsing and display.

- Note: please set `enable-query` to `true` in the `server.properties` file!
