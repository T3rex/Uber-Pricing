# 🚕 Uber Pricing Configuration System

A configurable pricing engine built with **Django** and **Django Admin**, allowing business teams to define and manage differential ride pricing based on distance, duration, day of the week, and waiting time.

---

## Features

- Distance-Based Pricing (DBP)
- Distance Additional Pricing (DAP) slabs
- Time Multiplier Factor (TMF) slabs based on ride duration
- Waiting Charges (WC)
- Day-of-week specific pricing
- Enable/disable configurations
- Enable/Disable multiple pricing module
- Calculate final ride price using:
  > Price = (DBP + (Dn _ DAP)) + (Tn _ TMF) + WC
- Admin interface with:
- Validation
- Audit logging (who changed what, when)
- REST API to calculate pricing for a ride

## Setup Instructions

### 1.Clone the Repository

```bash
git clone https://github.com/T3rex/Uber-Pricing.git

cd Uber-Pricing
```

### 2.Create Virtual Environment

```bash
python -m venv env
source env/bin/activate
```

### 3.Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5.Create Superuser

```bash
python manage.py createsuperuser
```

### 6.Run the Development Server

```bash
python manage.py runserver
```

## API Usage

### Create a Ride and POST

```json
POST request to "http://127.0.0.1:8000/api/rides/"
{
  "pricing_module": 1,
  "start_time": "2025-06-09T10:00:00Z",
  "end_time": "2025-06-09T10:45:00Z",
  "waiting_time_minutes": 3,
  "total_distance": 7.5
}
```

### Response

```json
{
  "id": 1,
  "dap_ride": 12.50,
  "tmf_ride": 10.00,
  "wc_ride": 3.00,
  "dbp_ride": 20.00,
  "total_price": 145.50,
  ...
}
```

## Use Interface

- Visit the home page: http://127.0.0.1:8000/
- Fill in ride details via the form
- Submit to calculate pricing
- View detailed results on the results page

## Tech stack

- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite3 (default, can be changed)
- Django Admin for backend management

## TODO

- [x] Pricing configuration models
- [x] Admin interface with validation
- [x] Price calculation logic
- [x] API to trigger ride creation + price computation
- [x] Audit log model
- [ ] Add unit tests for service layer
- [ ] Swagger or Postman collection for API
