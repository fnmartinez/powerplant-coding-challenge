# powerplant-coding-challenge
This is the proposed solution for the GEM SPaaS Coding Challenge. It has been built using Python 3.8 with FastAPI and 
SciPy for the optimization algorithm.

## Installation
There are two main ways prepare the environment for running the application. One is to simply install it as a Python 
project. The other is to run it as docker container.

### Basic Python installation
To install the project as a Python app you only need to install its dependencies. In order to do that, simply open a 
terminal and execute the following command from the project's root directory:

```bash
pip install -r requirements.txt
```

It is recommended to do this in a Virtual Environment.

### Docker Installation
In case of not having Python or not wanting to create an environment for the project, there is a Dockerfile that allows 
you to build an image for the project. If you have docker installed in your system, simply open a terminal and execute 
the following command from the project's root directory:

```bash
docker build -t gem/spaas .
```

This will build an image with application in it ready to run.

## Running the solution
Depending on the installation type you did, is the way you have to run the application.

### Directly with Uvicorn
One of the dependencies installed is uvicorn, which is an ASGI server implementation. It will allow you to run the 
service by simply running the following command in a terminal from the project's root directory

```bash
uvicorn spaas:app --port 8888
```

This will run the application at the port 8888.

### Using Docker
If you have chosen to use follow a Docker installation then, after building the image, you need to run the following 
command

```bash
docker run -d -p 8888:8888 gem/spaas
```

This will spin up the container and allow connections to the port 8888, where the app is listening.

## About the optimization algorithm
The basic idea behind the optimization is to find a local minima for a multivariate function of cost, given a constraint 
of a minimum power output by the energy grid. For that, what I did is to use SciPy's Differential Evolution algorithm, 
to find the local minima for such cost function. This uses evolutionary algorithms to find the variables that reach to a 
minimum in the cost function, while maintaining the constraints.

Given that the input variable (i.e.: power output of each power plant), may have a minimum and maximum amount of power 
they can output. And given that this upper and lower bounds can alter the result of the algorithm, what I did is to play
with each power plant by turning them off and on. This would make the effect of effectively using or not using a given 
power plant for the final solution.
