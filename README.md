# BRAUM: Analyzing and Protecting Autonomous Machine Software Stack

This repository contains the code for error injection and analysis for Autoware, an open-source autonomous vehicle driving software, which helps us on figuring out the robustness of each individual nodes in Autoware. Based on the analysis results, we can provide selectively protection to ensure reliability while save protection overhead. 

## Installation

We use CARLA as the simulator and Autoware as the AV software instance. First, the user need to set up the CARLA and Autoware. 

### Install Autoware with docker

```bash
sudo apt install git-lfs
git clone --recurse-submodules https://github.com/carla-simulator/carla-autoware
cd carla-autoware && ./build.sh
./run.sh
```
After finishing the above steps, there should be a docker container running which includes the source code of Autoware.
### Install CARLA with docker
```bash
sudo apt-get install x11-xserver-utils
xhost +
docker run --rm --name carla_server --network host --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=0 -e DISPLAY=${DISPLAY} carlasim/carla:0.9.10.1 /bin/bash CarlaUE4.sh -fps=20 -opengl
```
After finishing the above, the CARLA simulator version 0.9.10.1 is running. 

## Run a scenario in Autoware

The scripts for error injection are in /injection folder. To inject errors into a running instance of Autoware, we first create a scenario of a car starting from point A to point B.

In the docker container with Autoware source code, start Autoware at a fixed point.
```bash
export ROS_HOSTNAME=localhost
export ROS_MASTER_URI=http://localhost:11311
roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 spawn_point:="107,59,0.5,0,0,0"
```
In another terminal of the docker container, set up the finish point.
```bash
rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped "{'header': {'seq': 0, 'stamp': {'secs': 0, 'nsecs': 0}, 'frame_id': "world" }, 'pose': {'position': {'x': 170, 'y': 0, 'z': 0.0}, 'orientation': {'x': 0.0, 'y': 0.0, 'z': -0.00720201027314, 'w': 0.999974065188}}}" --once
```

## Error Injection
To collect results without error injection, use the script ```baseline.py``` inside ```/injection``` folder. First copy the script into the Autoware container. 
```bash
docker cp baseline.py $CONTAINER_ID:/home/autoware/
```
Run the ```baseline.py``` script inside the Autoware container.
```bash
python baseline.py
```
Use other scripts in the ```/injection``` to inject errors into different nodes. For example, use the ```inject_trraw.py``` to inject errors into the output of ```twist_filter``` node
```bash
python inject_trraw.py -signal=xl -delta=0.5 -time=5.0 -iter=false
```
This means to inject an error into the signal ```xl``` for an amplitude of ```0.5``` at the time of ```5.0``` seconds during the scenario running, the error injection only happens ***once***. 

## Error Analysis
After collecting the results from baseline and error injection, use the script inside ```/analysis``` folder. First we create a database from the baseline results, and then analysis the results using the baseline.
```bash
python create_dataset_frombaseline.py
python traceback_twist_raw.py
```



## Publication
This work is published in ISSRE 2022. The citation information is updated later. 

## License
[MIT](https://choosealicense.com/licenses/mit/)
