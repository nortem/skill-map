# Skill map
Skill map application is designed to create a list of classes and objects.

## Usage (docker)

Example for debian-based system:
'''
apt-get install docker docker.io docker-compose
'''
Alternatively, you can visit Docker documentation (https://docs.master.dockerproject.org/desktop/windows/) for the installation instructions.

When you have installed docker, you need to clone the repository and run docker-compose in the terminal:
'''
git clone 
cd 
docker-compose up
'''
The app will be available on http://localhost:5000/ (port = 5000).

## Usage (no docker) 
The app can be launch without docker. 
Requirements:
- Python 3.7.
- Python packages specified in the requirements.txt (/web/requirements.txt).
- Redis server 

You need set the correct host:port settings for the redis db. (/web/app/my_config.py).
