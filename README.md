# Distributed Applications

Welcome to the **Distributed Applications** repository! This repository contains three projects focusing on distributed computing principles with Python.

Este README tambem existe em [Português](README_PT.md)

## Table of Contents
1. [Project 1](#project-1)
2. [Project 2](#project-2)
3. [Project 3](#project-3)

---

## Project 1

### Overview
**Project 1** builds a distributed Coin Center application that simulates basic functionalities such as managing assets, performing transactions, and keeping track of client balances. It introduces fundamental client-server communication concepts over a network.

### Features
- Implementation of TCP client-server sockets for communication.
- Basic functionality to add, remove, and fetch asset information.
- Supports multiple asset interactions.
- Includes manager and user roles with distinct functions.

### Key Files
- [`sock_utils.py`](project1/sock_utils.py): Utilities for creating TCP sockets.
- [`coincenter_client.py`](project1/coincenter_client.py): Implements a client for the Coin Center.
- [`coincenter_server.py`](project1/coincenter_server.py): Server-side implementation handling requests.

---

## Project 2

### Overview
In **Project 2**, the Coin Center is extended with skeletonized design patterns and refined communication logic. This project emphasizes the decoupling of business logic and handling of distributed messages.

### Features
- Introduces a `CoinCenterSkeleton` for core logic management.
- Implements a `NetServer` class for managing network events.
- Enhanced modularity with the separation of network and application logic.
- Support for handling asset additions, removals, and user requests effectively.

### Key Files
- [`coincenter_skel.py`](project2/coincenter_skel.py): Skeleton handling business logic.
- [`coincenter_server.py`](project2/coincenter_server.py): Implements the server by integrating the skeleton with networking.
- [`sock_utils.py`](project2/sock_utils.py): TCP socket utility for networking.

---

## Project 3

### Overview
**Project 3** transforms the Coin Center to a RESTful microservice using Flask. It evolves into a production-ready distributed system with persistent storage and API endpoints.

### Features
- Flask-based RESTful architecture managing HTTP requests.
- Integration with SQLite for persistent database storage.
- API endpoints for managing clients, assets, and transactions.
- Incorporates Zookeeper (`KazooClient`) for distributed synchronization and management.

### Key Files
- [`coincenter_flask.py`](project3/coincenter_flask.py): Flask application server handling API routes.
- [`setup_db.py`](project3/setup_db.py): Handles database setup and connections.
- [`coincenter_data.py`](project3/coincenter_data.py): Contains database functions such as queries and asset management.

---

## Contributing
Contributions are welcome! If you have any ideas or issues, feel free to open a pull request or raise an issue.

## License
This project is currently not licensed. Please contact the repository owner for usage rights.

---

**Repository Owner:** [vitoriateixeiracorreia](https://github.com/vitoriateixeiracorreia)
