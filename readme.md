# Django GraphQL Celery Async Application with React, Docker, Kubernetes & Jenkins

This project is a full-stack web application that includes a Django backend with GraphQL, PostgreSQL (with JSONB support), Redis-based caching, Celery for asynchronous tasks, and a React frontend. It is containerized using Docker, orchestrated with Kubernetes, and integrated with Jenkins for CI/CD.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Local Development with Docker Compose](#local-development-with-docker-compose)
- [Kubernetes Deployment](#kubernetes-deployment)
  - [Kubernetes Manifests](#kubernetes-manifests)
- [Jenkins Pipeline Integration](#jenkins-pipeline-integration)
- [Monitoring](#monitoring)
- [Caching and Asynchronous Tasks](#caching-and-asynchronous-tasks)
- [License](#license)

## Overview

This application provides a quick way to set up a scalable and robust environment that includes:
- **Django** with GraphQL API.
- **React** for the frontend.
- **PostgreSQL** for the database.
- **Redis** for caching.
- **Celery** to process asynchronous tasks.
- **Celery Exporter** to export Celery metrics.
- **Prometheus** and **Grafana** for monitoring.
- Deployment using **Docker** and orchestration with **Kubernetes**.
- Continuous Integration and Deployment (CI/CD) using **Jenkins**.

## Features

- **GraphQL API**: Query and mutate user data (create, update, delete).
- **Caching**: Redis cache is used to optimize read performance.
- **Asynchronous Task Processing**: Celery processes background tasks.
- **Frontend in React**: Displays data and provides interactive UI for CRUD operations.
- **Containerization**: Dockerized services for easy local development.
- **Kubernetes Orchestration**: Deploys the application using Kubernetes deployments, services, and ingress.
- **Monitoring**: Prometheus scrapes metrics from various services, and Grafana displays them in dashboards.
- **CI/CD Pipeline**: Jenkins automates builds, pushes images to DockerHub, and deploys to Kubernetes.

## Architecture

The project is structured as follows:

- **Backend (Django)**: Handles API logic, GraphQL schema, and caching. Uses Gunicorn as the production server.
- **Frontend (React)**: Provides an interactive UI for users.
- **Celery Worker**: Processes asynchronous tasks.
- **Celery Exporter**: Exports Celery metrics to Prometheus.
- **Database (PostgreSQL)**: Stores application data.
- **Redis**: Provides caching and serves as the broker for Celery.
- **Monitoring**: Prometheus collects metrics and Grafana visualizes them.
- **CI/CD**: Jenkins pipeline builds and deploys the application.

## Prerequisites

- Docker and Docker Compose installed.
- Kubernetes cluster (Minikube, Docker Desktop Kubernetes, or a managed cluster).
- kubectl configured to access your cluster.
- Jenkins installed and configured (or a Jenkins server available).
- DockerHub account (username: `thiagocmach`) for pushing images.

## Local Development with Docker Compose

The project is containerized with Docker. The key services are defined in the `docker-compose.yml` file.

### Steps

1. **Build and Run Containers**

   ```bash
   docker-compose up --build



This command builds the images for the backend, frontend, and celery exporter, then starts all services including PostgreSQL, Redis, Django, Celery, React, Prometheus, and Grafana.

Accessing the Application

Django (Backend): http://localhost:8000
React (Frontend): http://localhost:3000
Prometheus: http://localhost:9090
Grafana: http://localhost:3001
Kubernetes Deployment
After local development, the application can be deployed to a Kubernetes cluster.

Deploying with Kubernetes
The Kubernetes manifests are located in the k8s/ directory. These include deployments and services for each component.

Kubernetes Manifests
backend-deployment.yaml & backend-service.yaml: Deploy the Django backend.
frontend-deployment.yaml & frontend-service.yaml: Deploy the React frontend.
db-deployment.yaml & db-service.yaml: Deploy PostgreSQL.
redis-deployment.yaml & redis-service.yaml: Deploy Redis.
celery-deployment.yaml: Deploy the Celery worker (using the same image as the backend or a dedicated one).
celery-exporter-deployment.yaml & celery-exporter-service.yaml: Deploy the Celery exporter.
prometheus-deployment.yaml, prometheus-service.yaml & prometheus-configmap.yaml: Deploy Prometheus and provide its configuration.
grafana-deployment.yaml & grafana-service.yaml: Deploy Grafana.
ingress.yaml (optional): Define an Ingress resource to expose services externally.
Applying the Kubernetes Manifests
From the root of the project, run:

bash
Copiar
kubectl apply -f k8s/
This command creates all the Kubernetes resources. You can check the status of pods using:

bash
Copiar
kubectl get pods
Jenkins Pipeline Integration
A Jenkinsfile is included in the root directory to define the CI/CD pipeline.

Jenkinsfile Overview
Checkout: Retrieves the code from the repository.
Build: Builds Docker images for the backend and frontend.
Push: Pushes images to DockerHub (ensure you’re logged in with your DockerHub credentials).
Deploy: Uses kubectl apply -f k8s/ to deploy updates to the Kubernetes cluster.
Steps
Configure Jenkins with the necessary plugins (Docker Pipeline, Kubernetes CLI).
Add credentials for DockerHub and the Kubernetes cluster.
Create a new pipeline job that uses the Jenkinsfile.
Run the pipeline to build, push, and deploy your application.
Monitoring
Prometheus: Scrapes metrics from the Django, Celery exporter, and other endpoints as defined in the prometheus.yml configuration (stored in a ConfigMap).
Grafana: Connects to Prometheus as a data source and displays dashboards for system and application metrics.
Caching and Asynchronous Tasks
Caching: The Django application caches query results (e.g., user data) using Redis. Cache invalidation is triggered in GraphQL mutations (create, update, delete).
Celery: Processes asynchronous tasks using Redis as the broker. The Celery worker and its exporter are deployed, allowing Prometheus to monitor task metrics.
License
This project is provided "as is" without any warranty. Feel free to modify and use it for your own purposes.

Note:
Make sure to adjust image names, environment variables, and other configuration details to suit your production environment. This README serves as a baseline documentation for setting up, developing, and deploying the application with Docker, Kubernetes, and Jenkins.

Happy coding!


---





