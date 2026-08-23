# Kavi Collector App Project

A Python-based application built with **Streamlit** to manage, track, and analyze your card collection inventory.

## Features
* **Collection Analytics:** View instant portfolio summaries including total cards, total spent, current market value, and profit/loss metrics.
* **Inventory Management:** Track your items and easily add new entries.
* **Bulk Import:** Support for importing collection data via CSV.
* **Master Checklist:** Keep track of your complete collection goals.

## Project Structure
* `app.py` - The main Streamlit user interface and dashboard logic.
* `database.py` - Handles database connections, queries, and portfolio calculations.
* `collector_app.db` - Local SQLite database storing your collection data.
* `requirements.txt` - Lists the required Python packages for the app.

## Requirements & Installation
Make sure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
