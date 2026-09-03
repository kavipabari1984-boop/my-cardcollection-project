
How to run the app

📊 Portfolio Dashboard: Real-time financial analytics tracking total spent, market valuation, profit/loss, and inventory management with item update and delete capabilities.

➕ Add to Inventory: Link acquired cards from the master database with custom purchase prices, conditions (e.g., Gem Mint, Near Mint), and quantities.

🗂️ Master Checklist: Central catalog of all available card sets, custom single-card additions, and manual market pricing updates.

📥 Bulk Import CSV: Batch upload structured comma-separated files to rapidly populate or expand the master database.

Repository Topics
streamlit · python · portfolio-tracker · inventory-management · tcg · trading-cards · dashboard · pandas · sqlite · collectibles

How to Run Locally
1. Clone the Repository

Bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Install Dependencies
Ensure you have Python installed, then install the required packages:

Bash
pip install streamlit pandas
(Alternatively, if a requirements file is available: pip install -r requirements.txt)

3. Ensure Project Structure
Verify your project folder contains your main application file (e.g., app.py) and your database module (dataBase.py).

4. Run the Streamlit App
Launch the local development server:

Bash
streamlit run app.py
5. View the App
Open your browser and navigate to the local URL provided in the terminal (typically http://localhost:8501).