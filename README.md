# Prerequisites

Before you run the project, please make sure you have set up all the following:

1.  This project uses Docker to run. If you have not installed Docker Desktop, please install from [here](https://www.docker.com/products/docker-desktop/).

2.  At the root directory, create a `data` and `out` folder. Put all relevant data in the `data` folder. The `out` folder should be kept empty.
3.

# Running the Project

```bash
# Run the services
docker-compose up --build

# Stop the services
docker-compose stop

# Remove the services
docker-compose down
```
