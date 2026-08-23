import pandas as pd
import streamlit as st
import dataBase as db

st.set_page_config(page_title="Card Collector App", page_icon="🎴", layout="wide")
db.init_db()

st.title("🎴 Kavi Card Collector Dashboard")

tab_dashboard, tab_add_inventory, tab_master_db, tab_bulk_import = st.tabs([
    "📊 Portfolio Dashboard", 
    "➕ Add to Inventory", 
    "🗂️ Master Checklist", 
    "📥 Bulk Import CSV"
])

# --- TAB 1: DASHBOARD ---
with tab_dashboard:
    st.header("Collection Analytics")
    stats = db.get_portfolio_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cards", stats["total_cards"])
    col2.metric("Total Spent", f"${stats['total_spent']:,.2f}")
    col3.metric("Market Value", f"${stats['market_value']:,.2f}")
    col4.metric("Profit / Loss", f"${stats['profit_loss']:,.2f}", delta=stats['profit_loss'])

    st.markdown("---")
    st.subheader("Inventory")
    
    inv_df = db.get_inventory_df()
    if inv_df.empty:
        st.info("Inventory is empty. Go to 'Add to Inventory' to add your first card.")
    else:
        inv_df['Total Cost'] = inv_df['purchase_price'] * inv_df['quantity']
        inv_df['Total Value'] = inv_df['market_price'] * inv_df['quantity']
        inv_df['Profit/Loss'] = inv_df['Total Value'] - inv_df['Total Cost']
        
        st.dataframe(inv_df, use_container_width=True, hide_index=True)

        st.subheader("Manage Selected Item")
        selected_inv_id = st.selectbox("Select Inventory ID to Manage", inv_df['inventory_id'].tolist())
        item_data = inv_df[inv_df['inventory_id'] == selected_inv_id].iloc[0]
        
        c1, c2 = st.columns(2)
        with c1:
            conditions = ["Gem Mint", "Mint", "Near Mint", "Lightly Played", "Moderately Played", "Heavily Played", "Damaged"]
            curr_cond_idx = conditions.index(item_data['condition']) if item_data['condition'] in conditions else 2
            
            new_cond = st.selectbox("Condition", conditions, index=curr_cond_idx)
            new_price = st.number_input("Purchase Price ($)", min_value=0.0, value=float(item_data['purchase_price']), step=0.5)
            new_qty = st.number_input("Quantity", min_value=1, value=int(item_data['quantity']), step=1)
            
            btn1, btn2 = st.columns(2)
            if btn1.button("Update Item"):
                db.update_inventory_item(selected_inv_id, new_cond, new_price, new_qty)
                st.success("Updated!")
                st.rerun()
                
            if btn2.button("Delete Item", type="primary"):
                db.remove_from_inventory(selected_inv_id)
                st.warning("Deleted.")
                st.rerun()

# --- TAB 2: ADD TO INVENTORY ---
with tab_add_inventory:
    st.header("Add Card to Inventory")
    master_df = db.get_master_df()
    
    if master_df.empty:
        st.warning("No cards in Master Checklist. Add cards to the Master Checklist first.")
    else:
        master_df['display_name'] = master_df['set_name'] + " - #" + master_df['card_number'] + " " + master_df['card_name']
        selected_card_label = st.selectbox("Search Card", master_df['display_name'].tolist())
        selected_card_row = master_df[master_df['display_name'] == selected_card_label].iloc[0]
        
        with st.form("add_inventory_form"):
            condition = st.selectbox("Condition", ["Gem Mint", "Mint", "Near Mint", "Lightly Played", "Moderately Played", "Heavily Played", "Damaged"], index=2)
            purchase_price = st.number_input("Purchase Price ($)", min_value=0.0, value=float(selected_card_row['market_price']), step=0.5)
            quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
            
            if st.form_submit_button("Add to Inventory"):
                db.add_to_inventory(int(selected_card_row['id']), condition, purchase_price, quantity)
                st.success("Card added!")
                st.rerun()

# --- TAB 3: MASTER CHECKLIST ---
with tab_master_db:
    st.header("Master Checklist")
    with st.expander("➕ Add Single Card"):
        with st.form("add_master_form"):
            s_name = st.text_input("Set Name")
            c_num = st.text_input("Card Number")
            c_name = st.text_input("Card Name")
            m_price = st.number_input("Market Price ($)", min_value=0.0, value=0.0, step=0.5)
            
            if st.form_submit_button("Save Card"):
                if s_name and c_num and c_name:
                    db.add_master_card(s_name, c_num, c_name, m_price)
                    st.success("Card added to Master Database!")
                    st.rerun()

    m_df = db.get_master_df()
    st.dataframe(m_df, use_container_width=True, hide_index=True)
    
    if not m_df.empty:
        st.subheader("Update Market Price")
        m_id = st.selectbox("Select Card ID to Update Price", m_df['id'].tolist())
        m_row = m_df[m_id == m_df['id']].iloc[0]
        new_m_price = st.number_input("New Market Price ($)", min_value=0.0, value=float(m_row['market_price']), step=0.5)
        if st.button("Update Price"):
            db.update_market_price(m_id, new_m_price)
            st.success("Price updated!")
            st.rerun()

# --- TAB 4: BULK IMPORT ---
with tab_bulk_import:
    st.header("Bulk Import Master Cards via CSV")
    st.caption("Upload a CSV with columns: `set_name`, `card_number`, `card_name`, `market_price`")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        st.dataframe(df_upload.head())
        if st.button("Import CSV"):
            conn = db.get_connection()
            df_upload[['set_name', 'card_number', 'card_name', 'market_price']].to_sql('master_checklist', conn, if_exists='append', index=False)
            conn.close()
            st.success("Import successful!")
            st.rerun()