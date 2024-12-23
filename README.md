# Project Overview

- **hls-api**: Runs a program (Python Flask) to handle requests.
- **nginx**: Acts as a web server. It serves the output files created by the hls-api from a specific directory, making them accessible via a web browser at http://localhost:5001

# Requirements

- Docker (tested on v4.36.0)

# How to Run

1. Open a terminal.
2. Type: `docker-compose up --build`
3. Press Enter.
