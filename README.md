# PX4 Drone Flight Log Analysis & Data Pipeline
In this project, as a data engineer working in a smart agriculture company using a px4 drone, we will create a data pipeline that processes the data in this ulog file. Let's briefly talk about what we will do. 
We will add the ulog file to a bucket in minio, and airflow will parse this ulog file for us, convert the data in it to csv format, and then write it to another bucket. Using Nifi, we will ETL these csv files and write them to opensearch. Later, we will present the data we obtained using the dashboard offered by Opensearch to the business units.
These will be needed to process the data.

## Prerequisites
- Docker - Docker compose
- Python dependency(Pyulog,Minio)
- Apache Airflow
- Apache Nifi
- Opensearch
- Prometheus
- Grafana

## System Architecture
![Architecture](https://cdn-images-1.medium.com/max/1000/1*soRNYZQhaMrfL3eAX9SrpA.png)

## Installation
### Docker
```sh
docker compose up --build
```

## License

MIT

## Plugins

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

|  | Container Name | URL |
| ------ | ------ | ------ |
| ![](https://w7.pngwing.com/pngs/937/843/png-transparent-airflow-airbnb-data-engineering-workflow-reflection-miscellaneous-symmetry-engineering-thumbnail.png) | Apache Airflow | http://192.168.1.149:8080/home |
| ![](https://cdn.icon-icons.com/icons2/2699/PNG/512/apache_nifi_logo_icon_168614.png)| Apache Nifi | http://localhost:8081/nifi/ |
| ![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9C5mI76jKNtkjrLpIAHMJdcGSO0f7e_ZAmA&s) | MinIO | http://192.168.1.149:9001/login |
| ![](https://opensearch.org/assets/media/partners/improving/resource-blog-1.png) | Opensearch Dashboard | http://192.168.1.149:5601/app/home |
| ![](https://banner2.cleanpng.com/20190423/os/kisspng-prometheus-grafana-kubernetes-application-software-1713896726589.webp)| Prometheus | http://192.168.1.149:9090/ |
| ![](https://w7.pngwing.com/pngs/434/923/png-transparent-grafana-hd-logo.png) | Grafana | http://192.168.1.149:3000/?orgId=1 |
