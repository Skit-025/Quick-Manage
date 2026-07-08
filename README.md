<div align="center">

# 💰 Personal Finance & Expense Intelligence Dashboard

### Transforming Financial Data into Actionable Insights

*A Full-Stack Python Application for Intelligent Expense Tracking, Analytics & Machine Learning Predictions.*

---

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458?style=for-the-badge&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical-013243?style=for-the-badge&logo=numpy)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?style=for-the-badge&logo=scikitlearn)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

**Engineering Project • Data Analytics • Machine Learning • Software Engineering • Visualization**

</div>

---

# 📖 Table of Contents

- About
- Why this Project
- Features
- System Overview
- Five Layer Architecture
- System Flow
- Request Lifecycle
- Data Flow
- Architecture Philosophy

---

# 🚀 About

The **Personal Finance & Expense Intelligence Dashboard** is a production-inspired full-stack Python application that helps users monitor, analyze, and predict their financial spending.

Unlike traditional expense trackers that simply store transactions, this platform combines:

- Intelligent analytics
- Statistical analysis
- Interactive dashboards
- Machine Learning predictions
- Budget monitoring
- Spending anomaly detection

to convert raw financial records into meaningful insights.

The application demonstrates modern software engineering principles while solving a real-world financial management problem.

---

# 🎯 Why this Project?

Managing personal finances is often reduced to manually recording expenses without understanding spending behavior.

This project bridges that gap by combining:

✔ Expense Management

✔ Budget Tracking

✔ Financial Analytics

✔ Interactive Data Visualization

✔ Machine Learning

✔ Modular Software Engineering

into a single intelligent platform.

---

# ✨ Core Features

## 📊 Expense Management

- Add Daily Expenses
- Edit Existing Records
- Delete Transactions
- Categorize Expenses
- Budget Management

---

## 📈 Financial Analytics

- Monthly Reports
- Category-wise Spending
- Spending Trends
- Income vs Expense Analysis
- Average Monthly Expenses
- Expense Heatmaps

---

## 🤖 Machine Learning

- Predict Next Month Expenses
- Spending Forecast
- Budget Overspending Prediction
- Expense Trend Learning
- Anomaly Detection

---

## 📉 Data Visualization

- Pie Charts
- Monthly Bar Charts
- Trend Lines
- Category Comparison
- Heat Maps

---

## ⚙ Engineering Features

- Object-Oriented Design
- SQLite Database
- REST APIs
- Streamlit Dashboard
- Flask Backend
- Logging
- Exception Handling
- CSV Export
- Multithreading
- Modular Architecture

---

# 🏗 Five Layer Architecture

```mermaid
flowchart LR

A["🎨 Presentation Layer<br/>Streamlit Dashboard"]

B["🌐 API Layer<br/>Flask REST API"]

C["⚙ Business Logic Layer<br/>Analytics Engine<br/>Expense Engine"]

D["💾 Data Layer<br/>SQLite Database"]

E["🤖 Machine Learning Layer<br/>Prediction Engine"]

A --> B

B --> C

C --> D

C --> E

E --> B

B --> A
```

---

# 🌍 High Level System Architecture

```mermaid
graph TD

User

Streamlit

Flask

Analytics

Database

ML

Charts

Prediction

User --> Streamlit

Streamlit --> Flask

Flask --> Database

Flask --> Analytics

Analytics --> Charts

Analytics --> ML

ML --> Prediction

Prediction --> Streamlit

Charts --> Streamlit
```

---

# 🔄 Complete Request Lifecycle

```mermaid
sequenceDiagram

participant User

participant Dashboard

participant FlaskAPI

participant Database

participant Analytics

participant ML

User->>Dashboard: Add Expense

Dashboard->>FlaskAPI: POST Expense

FlaskAPI->>Database: Store Data

Database-->>FlaskAPI: Success

FlaskAPI->>Analytics: Refresh Reports

Analytics->>ML: Retrain Prediction

ML-->>Analytics: Predicted Values

Analytics-->>Dashboard: Updated Charts

Dashboard-->>User: New Dashboard
```

---

# 📊 Expense Processing Flow

```mermaid
flowchart TD

Start

Expense

Validation

Database

Analytics

Visualization

Prediction

Dashboard

Start --> Expense

Expense --> Validation

Validation --> Database

Database --> Analytics

Analytics --> Visualization

Analytics --> Prediction

Visualization --> Dashboard

Prediction --> Dashboard
```

---

# 🧠 Machine Learning Pipeline

```mermaid
flowchart LR

Expense_Data

Cleaning

Feature_Engineering

Training

Prediction

Dashboard

Expense_Data --> Cleaning

Cleaning --> Feature_Engineering

Feature_Engineering --> Training

Training --> Prediction

Prediction --> Dashboard
```

---

# 📂 Internal Module Communication

```mermaid
graph LR

Dashboard

API

Database

Analytics

ML

Logs

Reports

Dashboard --> API

API --> Database

Database --> Analytics

Analytics --> Reports

Analytics --> ML

ML --> Dashboard

API --> Logs
```

---

# 🎯 Architecture Philosophy

The project follows a **layered architecture**, ensuring each component has a clearly defined responsibility.

```
Presentation Layer
        │
        ▼
API Layer
        │
        ▼
Business Logic
        │
        ▼
Database Layer
        │
        ▼
Machine Learning Layer
```

Each layer communicates only through well-defined interfaces, improving maintainability, scalability, and testability.

---

# ⭐ Highlights

- Modular Python Architecture
- Production Inspired Design
- REST API Driven Backend
- Interactive Dashboard
- Predictive Analytics
- Financial Intelligence
- Machine Learning Integration
- Extensible Codebase
- Engineering Best Practices
- Resume-Ready Full Stack Project

---

> **"Track smarter. Analyze deeper. Predict the future of your finances."**

---