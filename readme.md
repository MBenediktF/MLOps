# End-to-End MLOps

This project explores Machine Learning Operations (MLOps)
as a solution to the challenges of deploying and maintaining ML models in production.
It implements a flexible multi-container system that enables
automated training, deployment, monitoring, and optimization of ML models.
The approach is demonstrated using a distance measurement application with a rearview camera
but is designed to be easily adaptable for various ML applications.
The system ensures scalability, reproducibility, and maintainability,
making it suitable for a wide range of ML use cases.

This project is closely related to my Bachelor's thesis,
which was developed in collaboration with Bosch Engineering GmbH and Hochschule Heilbronn.
The thesis explores the concept of MLOps
and its practical implementation.
You can find the full thesis [here](https://www.mbenediktf.de/end-to-end-mlops/).

I welcome any feedback, suggestions for improvement, or discussions regarding the thesis. This work is intended to serve as a foundation and knowledge base for the practical application of MLOps.

## System architecture

![Systemarchitektur](src/system_architecture.jpg)

## Quick setup for local test and dev

- Clone repo: `git clone -bare https://github.com/MBenediktF/MLOps.git`
- Navigate to cloned repo: `cd MLOps`
- (Update config in `.env`)
- Start system: `docker-compose up`

A detailed guide for setting up and testing the system
can be found in Appendix B of the thesis, on page 58.
A detailed guide for setting up and testing the system
is provided in Appendix B (Page 58) of the
[thesis](https://www.mbenediktf.de/end-to-end-mlops/)
Additionally, this section covers
how to simulate the edge device and customize the services.

## Current Status and Functionality of Available Services

### Dynamic System

- 🟡 **Inference API (Flask)**  
  - Integration test route tbd

- 🟢 **Model Training Pipeline (Dasgter)**  

- 🟢 **Config UI (HTML/Javascript)**  

- 🟢 **Experiment Tracking(MLFlow)**  

- 🟡 **Model Registry (MLFlow)**  
  - Auto-creation of models in registry tbd

- 🟢 **Object Store (MinIO)**

- 🟢 **SQL Database (MySQL)**  

- 🟢 **Time Series Database (InfluxDB)**  

- 🟡 **Monitoring (Grafana)**  
  - System utilization logging and dashboard tbd

- 🟡 **Edge Code (Python)**
  - Edge-Device reboots sometimes
  - Automated onboarding procedure tbd
  - Multiprocessing could be used to enhance drive controls
  - Remote deployment could be implemented
  - Edge Computing could be implemented

- 🔴 **Backup**
  - Current scripts not tested
  - Automated backup tbd

### Static System

- 🟢 **Central Code Repository (GitHub)**

- 🟢 **Model Code and Dagster Wrapper (Python)**

- 🟢 **Dockerfiles and Docker-Compose**

- 🟢 **1-Click local deployment (Docker)**

- 🟡 **Static Code analysis**
  - currently only using flake8 for python files
  - check of dockerfiles tbd

- 🟡 **Unit Tests (pytest)**
  - Only implemented for some model scripts

- 🔴 **Continous Integration (GH Actions)**
  - Pipeline not up to date

- 🔴 **Continous Deployment (GH Actions)**
  - Pipeline not up to date
  - Integration-Tests tbd
  - Remote deployment via ssh tbd

- 🟡 **Security**
  - Update Branch protection rules

- 🟢 **Documentation**
