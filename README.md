# Pivotal Analytics Dashboard

Welcome to the Pivotal Analytics Dashboard project! This project aims to provide insightful analytics and visualizations for Pivotal data through a customizable dashboard. It leverages Python scripts to interact with the Pivotal APIs, SQLite for data storage and manipulation, and Grafana for visualization and dashboard creation.

Live Dashboard [link](https://andrekef.github.io/dashboards_demo.github.io/) here hosted over at GH pages

## Overview

The Pivotal Analytics Dashboard project consists of several components:

1. **Python Scripts**: Python scripts are used to interact with the Pivotal APIs, retrieve data, and perform data processing tasks.
   
2. **SQLite Database**: Data retrieved from the Pivotal APIs is stored in an SQLite database. The database schema is designed to support efficient data storage and retrieval.

3. **SQL Queries**: SQL queries are utilized to reshape the raw data into a wide format suitable for analysis. These queries transform the data and aggregate it for meaningful insights.

4. **Grafana Dashboard**: Grafana is employed to create dynamic and interactive dashboards for visualizing Pivotal analytics. The dashboard provides various metrics and visualizations to monitor project progress, track key performance indicators, and identify trends.

## Getting Started

To get started with the Pivotal Analytics Dashboard project:

1. Clone this repository to your local machine.
2. Set up the necessary Python environment and install dependencies listed in `requirements.txt`.
3. Configure API tokens and other credentials required for accessing Pivotal APIs.
4. Run the Python scripts to retrieve data from Pivotal and populate the SQLite database.
5. Execute SQL queries to reshape and aggregate the data as needed.
6. Import the provided Grafana dashboard template or create custom dashboards based on your requirements.
7. Customize the dashboard layout, panels, and visualizations to suit your analytics needs.

## Repository Structure

- `scripts/`: Contains Python scripts for interacting with Pivotal APIs and processing data.
- `queries/`: Includes SQL queries for data manipulation and aggregation.
- `dashboard/`: Holds configuration files and templates for Grafana dashboards.
- `data/`: Reserved for storing SQLite database files and any additional data files.
- `README.md`: This file provides an overview of the project and instructions for getting started.

## Contribution Guidelines

Contributions to the Pivotal Analytics Dashboard project are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request. Make sure to follow the contribution guidelines outlined in `CONTRIBUTING.md`.

## License

This project is licensed under the [MIT License](LICENSE).
