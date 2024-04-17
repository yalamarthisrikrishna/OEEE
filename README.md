# OEE (Overall Equipment Effectiveness) App

## Description
The OEE App is a Django web application designed to calculate and monitor the Overall Equipment Effectiveness of machines in a manufacturing environment. It allows users to track production logs, view OEE metrics, add new machines, and filter OEE data based on specific criteria.

## Features
- **Dashboard**: Provides an overview of machinery logs and OEE metrics.
- **Production Log Management**: Allows users to add, view, and filter production logs for each machine.
- **Machine Management**: Enables users to add new machines to the system.
- **OEE Calculation**: Automatically calculates OEE metrics based on production logs.
- **Filtering**: Allows users to filter OEE data by machine, start date, and end date.

## Installation
1. Clone the repository to your local machine:git clone https://github.com/yourusername/OEEE.git
2. Navigate to the project directory:cd OEEE
3. Install dependencies using pip:pip install -r requirements.txt
4. Run migrations to create the database schema:python manage.py migrate
5. Start the development server:python manage.py runserver
6. Access the application at [http://localhost:8000](http://localhost:8000) in your web browser.

## Usage
- **Adding Machines**: Navigate to the "Machine View" page and use the "Add Machine" button to add new machines.
- **Adding Production Logs**: Navigate to the "Logs View" page and use the "Add Log" button to add production logs for each machine.
- **Viewing OEE Data**: Access the OEE data at [http://localhost:8000/oee/](http://localhost:8000/oee/).
- **Filtering OEE Data**: Use the filtering options to filter OEE data by machine, start date, and end date.



