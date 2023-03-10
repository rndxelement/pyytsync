# pyytsync - A simple web app for watching Youtube videos synchronized over multiple user sessions

![Sample image](sample.png)

:heavy_check_mark: User interface: Fast and responsive, implemented with Bootstrap 5 and JavaScript  
:heavy_check_mark: Managing a queue of videos: Add, delete and adjust order via Drag & Drop  
:heavy_check_mark: Deployment: Easily deployable via Docker and Docker-compose  
:heavy_plus_sign: No User-management: The server can only handle a single "Room" of clients, which might be a pro or a con depending on your use case  
:heavy_exclamation_mark: This app is supposed to be used in private watch-party sessions, thus hosting a public instance is not recommended/feasible 

# Install

1. `git clone git@github.com:rndxelement/pyytsync.git`
2. Copy `.env.dev` to `.env` and adjust the environment variables
3. Set your Youtube Data API key in `pyytsync/pyytsync/settings.py`

# Build and run

`docker-compose build && docker-compose up -d`

# Contribute

I'd be happy and grateful about any kind of contributions or even forks.  
Areas which might improved:  
- Documentation  
- JavaScript code for client synchronisation
- Improving and/or adding advanced techniques to the deployment process  
- General front-end refactoring/improvement
