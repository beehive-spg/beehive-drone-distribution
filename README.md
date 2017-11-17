# Beehive-Drone-Distribution
This repository serves the purpose of the drone distribution management of project Beehive.

## General Description
The Distribution Management is responsible for commanding drones to change their current hive in order to respond to current or future orders. This prediction is done by the Workload Prediction component, which sends future peaks in demand. For sending and receiving the prediction data, CloudAMQP is used to host RabbitMQ server messaging queues.

A REST Service enables to fetch detailed information of different hives to analyze which drone ports are qualified for being part of the distribution process.

As a drone logistics network can be quite large, a Machine Learning algorithm is included to enhance future decision making and to increase general distribution performance capabilities.

After all the data is properly evaluated, it is prepared to be sent to the Routing Engine, which is in charge of the route planning, scheduling and executing the deliveries.

## Basic System Architecture
![System Architecture][architecture]

## Requirements

###### Disclaimer
This README only covers commands for apt package mangager performed by Debian Stretch. To adjust the commands to your OS use the provided links.

### [rabbitmq server](https://www.rabbitmq.com/download.html)
> RabbitMQ is the most widely deployed open source message broker.
```
apt install rabbitmq-server
```

### [pip](https://pip.pypa.io/en/stable/installing/)
> The PyPA recommended tool for installing Python packages.
```
# python 2
apt install python-pip
```
```
# python 3
apt install python3-pip
```

### packages
documented in the requirements.txt
```
# python 2
pip install -r requirements.txt
```
```
# python 3
python3 -m pip install -r requirements.txt
```
or manually

```
# python 2
pip install <package-name>
```

```
# python 3
python3 -m pip install <package-name>
```

## List of packages
#### [pika](http://pika.readthedocs.io/en/latest/)
> Pika is a pure-Python implementation of the AMQP 0-9-1 protocol that tries to stay fairly independent of the underlying network support library.


[architecture]: /home/jonas/Documents/git/github/beehive-drone-distribution/assets/beehive_distribution_architecture.png "System Architecture"