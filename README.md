# ndn3-test

## Overview
This repository provides a docker-compose project for setting up a NDN network.
The network consists of 3 NFDs and 3 client nodes.

![Topology](./ndn3-test.png "ndn3-test.png")

## Deploy
### 1. Clone the repository
```bash
git clone https://hydrokhoos/ndn3-test.git
cd ndn3-test
```

### 2. Deploy containers using Docker-compose
```bash
docker-compose up -d
```

### 3. Check logs and NLSR status
```bash
docker logs router1
docker logs pc1
docker exec router1 nlsrc status
```

## Usage
### Retrieve content
```bash
docker exec pc1 ndnpeek -pf /pc2
# Hello, my name is pc2.
```

## Destroy
```bash
docker-compose down -v
```
