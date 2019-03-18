# Table of Contents 
1. [Introduction](README.md#introduction)
2. [Pipeline](README.md#pipeline)
3. [Requirements](README.md#requirements)
4. [Environment Set Up](README.md#Environment\ Setup)
5. [Repository Structure and Run Instructions](README.md#Repository\ Structure\ and\ Run\ Instructions)


# Introduction
**Trend Factor: Visualizing web trends using the Common Crawl**

This is a project I completed in 3 weeks during the Insight Data Engineering Program (New York, 19A Session). The goal of this project is to count the number of web pages that mention a set of terms between January and December 2018. The program uses a subset (~20TB) of the [Common Crawl](https://commoncrawl.org/), an archive of web page content. The results can be used to help companies measure brand recognition over a period of time or compare the popularity of different products. A sample batch job has been executed with a set of database names and the UI with the results is temporarily displayed at [techwebtrends.xyz](http://techwebtrends.xyz). A recording of the WebUI is also available [here](https://www.youtube.com/watch?v=vcIkcN4rYcI). 

# Pipeline
The data was ingested from Amazon S3 using Spark Scala and the final results containing the search terms and their frequencies were saved to PostgreSQL database. Apache Airflow was used for scheduling the batch processing tasks corresponding to each month of the Common Crawl data. The front-end Web UI, showing the results of the batch processing jobs, was build with the Python Dash framework. 

![alt text](./images/pipeline.png)

# Requirements
Languages 
*Python 2.7
*Scala 2.11.8

Technologies
*Spark
*Airflow 
*PostgreSQL

Third-Party Libraries
*AWS CLI

# Environment Setup
Install and configure [AWS](https://aws.amazon.com/cli/) and the open-source tool [Pegasus](https://github.com/InsightDataScience/pegasus) on your local machine and clone this repository `git clone https://github.com/Marinela09/Insight-DE-Project`. Configure a VPC with a security group and subnet on AWS and add your local IP address to the VPC inbound rules. 

**AWS Clusters Setup**
For my project, I used the following cluster structure: 
* 7-node Spark Cluster for Batch Processing
* 1-node Database Cluster for Postgres and front-end Dash application

To deploy each cluster, use pegasus tool. Configure the master and worker yml files and use `peg up <yml filename>` command. For example, the master file for the spark cluster can be configured using the following yml template: 

```
purchase_type: on_demand
subnet_id: subnet-XXXX
price: string
num_instances: 1
key_name: XXXX-keypair
security_group_ids: sg-XXXX
instance_type: m4.large
tag_name: SparkCluster
vol_size: 100
role: master 
use_eips: true
```

For the workers, change the number of instances to 6, and the role to worker. 


**Installing the required technologies**
**1.Spark and Hadoop**
Use the following peg commands to install and start spark on the cluster

```
peg install SparkCluster ssh
peg install SparkCluster aws
peg install SparkCluster environment
peg install SparkCluster spark
peg install SparkCluster hadoop
peg service SparkCluster hadoop start
peg service SparkCluster spark start
```

**2.Apache Airflow**
SSH into the master node (`peg ssh SparkCluster 1`) of the SparkCluster and install Apache Airflow tool following the instructions in [this guide](https://medium.com/a-r-g-o/installing-apache-airflow-on-ubuntu-aws-6ebac15db211). 


**3.PostgreSQL**
SSH into the master node of the database cluster and install PostgresSQL. [Configure the database to allow remote connections](https://blog.bigbinary.com/2016/01/23/configure-postgresql-to-allow-remote-connection.html).


# Repository Structure and Run Instructions

`./airflow/` contains the python script for the Airflow Directed Acyclic Graph (DAG) definition. This file is used to schedule the batch processing jobs for each month of the common crawl data from 2018. 

`./dashapp/` contains the python script necessary for running the front-end web application. 

`./project/` contains all configuration files and the spark scala scripts for replicating my batch processing jobs

`build.sbt` file is used for the compilation of the spark scala scripts located in the project folder


To replicate my results: 
Copy the project folder inside the master node of the spark cluster. Download Postgres JDBC driver 42.2.5 jar files inside the project folder. Run `sbt package` command. 

Copy the airflow dag definition file into the master node of the spark cluster in airflow/dags folder. Run the python script `python schedule_batch.py`, start the Airflow Web UI, and trigger DAG execution: 
```
airflow webserver
airflow scheduler
airflow worker
```
To run the front-end visualization tool after the batch processing job is done, place the dash app script `ranking_app.py` into the database cluster and execute `python ranking_app.py`.















