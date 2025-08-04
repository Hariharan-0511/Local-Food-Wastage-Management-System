import pandas as pd
import streamlit as st
import psycopg2

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="food_wastage",
    user="postgres",
    password="Haridb"
)
cursor = conn.cursor()

# Sidebar navigation
page = st.sidebar.radio("Go to", [
    "Project Introduction",
    "View Tables",
    "CRUD Operations",
    "SQL Queries & Visualization",
    "Learner SQL Queries",
    "User Introduction"
])

# Page: Project Introduction
if page == "Project Introduction":
    st.title("📊 Food Wastage Management System")
    st.image("fooddonation.jpg", width=400, caption="Join the Movement!")
    st.text("This project helps manage surplus food and reduce wastage by connecting providers to needy")
    st.markdown("**Providers**: Restaurants, households, and businesses list surplus food.")
    st.markdown("**Receivers**: NGOs and individuals claim available food.")
    st.markdown("**Geolocation**: Helps locate nearby food.")
    st.markdown("**SQL Analysis**: Powerful insights using SQL queries.")

# Page: View Tables
if page == "View Tables":
    st.title("📑 Database Tables")
    
    table_files = {
        "Providers": "providers_data.csv",
        "Receivers": "receivers_data.csv",
        "Food Listings": "food_listings_data.csv",
        "Claims": "claims_data.csv"
    }

    selected_table = st.selectbox("📋 Select Table", list(table_files.keys()))
    df = pd.read_csv(table_files[selected_table])
    df.columns = df.columns.str.lower()

    st.markdown("### 🔍 Filter Options")

    if selected_table == "Providers":
        filter_input = st.text_input("Enter Provider ID to filter")
        filter_column = "provider_id"
    elif selected_table == "Receivers":
        filter_input = st.text_input("Enter Phone or Receiver ID to filter")
        filter_column = "receiver_id"
    elif selected_table == "Claims":
        filter_input = st.text_input("Enter Receiver ID to filter")
        filter_column = "receiver_id"
    elif selected_table == "Food Listings":
        filter_input = st.text_input("Enter Provider ID to filter")
        filter_column = "provider_id"
    
    if filter_input:
        try:
            df_filtered = df[df[filter_column] == int(filter_input)]
            st.dataframe(df_filtered)
        except (ValueError, KeyError):
            st.warning("⚠️ Invalid input or column not found.")
    else:
        st.dataframe(df)

# Page: CRUD Operations
if page == "CRUD Operations":
    st.title("🍽️ Manage Food Data")

    action = st.selectbox("Choose an Action", ["Add", "Update", "Delete"])

    food_id = st.number_input("Food ID (for Update/Delete)", min_value=1, step=1)
    food_name = st.text_input("Food Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    provider_id = st.number_input("Provider ID", min_value=1, step=1)

    button_label = {
        "Add": "➕ Add Food",
        "Update": "🔁 Update Food",
        "Delete": "🗑️ Delete Food"
    }[action]

    if st.button(button_label):
        try:
            if action == "Add":
                cursor.execute(
    "INSERT INTO food_listings (food_id, food_name, quantity, provider_id) VALUES (%s, %s, %s, %s)",
    (food_id, food_name, quantity, provider_id)
                )
                conn.commit()
                st.success("✅ Food added successfully.")

            elif action == "Update":
                cursor.execute(
                    "UPDATE food_listings SET food_name = %s, quantity = %s, provider_id = %s WHERE id = %s",
                    (food_name, quantity, provider_id, food_id)
                )
                if cursor.rowcount:
                    conn.commit()
                    st.success(f"✅ Food ID {food_id} updated.")
                else:
                    st.warning("⚠️ No record found to update.")

            elif action == "Delete":
                cursor.execute("""DELETE FROM food_listings  WHERE food_id = %s AND provider_id = %s AND food_name = %s AND quantity = %s""",
                (food_id, provider_id, food_name, quantity))
                if cursor.rowcount:
                    conn.commit()
                    st.success(f"🗑️ Deleted Food ID {food_id}.")
                else:
                    st.warning("⚠️ No record found to delete.")

        except Exception as e:
                conn.rollback()  # <-- CRITICAL LINE
                st.error(f"❌ Error: {e}")
    st.markdown("### 📋 View Food Listings")
    

if page == "SQL Queries & Visualization":
    st.title("SQL Analysis")

    action = st.selectbox("Choose a query", [
        "How many food providers and receivers are there in each city",
        "Which type of food provider (restaurant, grocery store, etc.) contributes the most food",
        "What is the contact information of food providers in a specific city",
        "Which receivers have claimed the most food",
        "What is the total quantity of food available from all providers",
        "Which city has the highest number of food listings",
        "What are the most commonly available food types",
        "How many food claims have been made for each food item",
        "Which provider has had the highest number of successful food claims",
        "What percentage of food claims are completed vs. pending vs. canceled",
        "What is the average quantity of food claimed per receiver",
        "Which meal type (breakfast, lunch, dinner, snacks) is claimed the most",
        "What is the total quantity of food donated by each provider"
    ])

    if action == "How many food providers and receivers are there in each city":
        query = '''
        SELECT receiver_id, COUNT(*) AS total
        FROM claims
        GROUP BY receiver_id
        ORDER BY total DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)


    elif action == "Which type of food provider (restaurant, grocery store, etc.) contributes the most food":
        query = '''
        SELECT type, COUNT(*) AS type_count
        FROM providers
        GROUP BY type 
        ORDER BY type_count DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)


    elif action == "What is the contact information of food providers in a specific city":
        query = '''
        SELECT name, contact, city
        FROM providers
        WHERE city = 'Alexanderchester';
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)


    elif action == "Which receivers have claimed the most food":
        query = '''
        SELECT receiver_id, COUNT(*) AS total
        FROM claims
        GROUP BY receiver_id
        ORDER BY total DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "What is the total quantity of food available from all providers":
        query = '''
        SELECT SUM(quantity) AS total_quantity
        FROM food_listings;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)


    elif action == "Which city has the highest number of food listings":
        query = '''
        SELECT location, COUNT(*) AS loc_count
        FROM food_listings
        GROUP BY location
        ORDER BY loc_count DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)


    elif action == "What are the most commonly available food types":
        query = '''
        SELECT food_type, COUNT(*) AS total_food_type
        FROM food_listings
        GROUP BY food_type
        ORDER BY total_food_type DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)


    elif action == "How many food claims have been made for each food item":
        query = '''
        SELECT food_id, COUNT(*) AS food_count
        FROM claims
        GROUP BY food_id
        ORDER BY food_count DESC;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "Which provider has had the highest number of successful food claims":
        query = '''
        SELECT f.provider_id, COUNT(*) AS successful_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        WHERE c.status = 'Completed'
        GROUP BY f.provider_id
        ORDER BY successful_claims DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df,hide_index = True)

    elif action == "What percentage of food claims are completed vs. pending vs. canceled":
        query = '''
        SELECT 
            status,
            COUNT(*) AS total_claims,
            ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM claims), 2) AS percentage
        FROM claims
        GROUP BY status
        ORDER BY percentage DESC;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "What is the average quantity of food claimed per receiver":
        query = '''
        SELECT c.receiver_id, AVG(f.quantity) AS avg_quantity
        FROM claims c
        JOIN food_listings f ON f.food_id = c.food_id
        WHERE c.status = 'Completed'
        GROUP BY c.receiver_id;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "Which meal type (breakfast, lunch, dinner, snacks) is claimed the most":
        query = '''
        SELECT f.meal_type, COUNT(*) AS status_count
        FROM claims c
        JOIN food_listings f ON f.food_id = c.food_id
        WHERE c.status = 'Completed'
        GROUP BY f.meal_type
        ORDER BY status_count DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "What is the total quantity of food donated by each provider":
        query = '''
        SELECT 
            f.provider_id, 
            p.name AS provider_name, 
            SUM(f.quantity) AS total_quantity
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
        GROUP BY f.provider_id, p.name
        ORDER BY total_quantity DESC;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

if page == "Learner SQL Queries":
    st.title("Learner SQL Queries")

    action = st.selectbox("Choose a query to explore", [
        "List all providers who have never posted any food listing",
        "Show food items with a quantity greater than the average quantity",
        "Find the city with the most food receivers",
        "List receivers who have never claimed any food",
        "Which provider posted the earliest food listing",
        "Which food type is least available",
        "Find the average quantity of food per food type",
        "Which receiver has canceled the most claims",
        "List food listings that haven't been claimed",
        "Which provider has the most pending claims",
        "What is the most frequently donated meal type by each provider",
        "How many unique providers have donated each food type",
        "List all claims along with provider name and receiver name",
        "Find top 3 cities by total quantity of food donated",
        "Get the total number of claims made per month",
        "Which food items have been claimed multiple times",
        "How many listings are added per provider on average",
        "Which food listing has the highest number of claims",
        "Find providers who operate in more than one city",
        "Which day of the week sees the most food claims"
    ])

    if action == "List all providers who have never posted any food listing":
        query = '''
        SELECT p.provider_id, p.name
        FROM providers p
        LEFT JOIN food_listings f ON p.provider_id = f.provider_id
        WHERE f.food_id IS NULL;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "Show food items with a quantity greater than the average quantity":
        query = '''
        SELECT food_id, quantity
        FROM food_listings
        WHERE quantity > (SELECT AVG(quantity) FROM food_listings);
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "Find the city with the most food receivers":
        query = '''
        SELECT city, COUNT(*) AS receiver_count
        FROM receivers
        GROUP BY city
        ORDER BY receiver_count DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "List receivers who have never claimed any food":
        query = '''
        SELECT r.receiver_id, r.name
        FROM receivers r
        LEFT JOIN claims c ON r.receiver_id = c.receiver_id
        WHERE c.claim_id IS NULL;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "Which provider posted the earliest food listing":
        query = '''
        SELECT f.provider_id, p.name, MIN(f.posted_at) AS earliest_post
        FROM food_listings f
        JOIN providers p ON p.provider_id = f.provider_id
        GROUP BY f.provider_id, p.name
        ORDER BY earliest_post ASC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "Which food type is least available":
        query = '''
        SELECT food_type, COUNT(*) AS total
        FROM food_listings
        GROUP BY food_type
        ORDER BY total ASC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "Find the average quantity of food per food type":
        query = '''
        SELECT food_type, ROUND(AVG(quantity), 2) AS avg_quantity
        FROM food_listings
        GROUP BY food_type;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "Which receiver has canceled the most claims":
        query = '''
        SELECT receiver_id, COUNT(*) AS cancel_count
        FROM claims
        WHERE status = 'Canceled'
        GROUP BY receiver_id
        ORDER BY cancel_count DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "List food listings that haven't been claimed":
        query = '''
        SELECT f.food_id, f.description
        FROM food_listings f
        LEFT JOIN claims c ON f.food_id = c.food_id
        WHERE c.claim_id IS NULL;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "Which provider has the most pending claims":
        query = '''
        SELECT f.provider_id, COUNT(*) AS pending_count
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        WHERE c.status = 'Pending'
        GROUP BY f.provider_id
        ORDER BY pending_count DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "What is the most frequently donated meal type by each provider":
        query = '''
        SELECT provider_id, meal_type, COUNT(*) AS donation_count
        FROM food_listings
        GROUP BY provider_id, meal_type
        QUALIFY ROW_NUMBER() OVER (PARTITION BY provider_id ORDER BY COUNT(*) DESC) = 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "How many unique providers have donated each food type":
        query = '''
        SELECT food_type, COUNT(DISTINCT provider_id) AS unique_providers
        FROM food_listings
        GROUP BY food_type;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "List all claims along with provider name and receiver name":
        query = '''
        SELECT c.claim_id, p.name AS provider_name, r.name AS receiver_name
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        JOIN receivers r ON c.receiver_id = r.receiver_id;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "Find top 3 cities by total quantity of food donated":
        query = '''
        SELECT f.location AS city, SUM(f.quantity) AS total_quantity
        FROM food_listings f
        GROUP BY f.location
        ORDER BY total_quantity DESC
        LIMIT 3;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "Get the total number of claims made per month":
        query = '''
        SELECT DATE_TRUNC('month', claimed_at) AS month, COUNT(*) AS total_claims
        FROM claims
        GROUP BY month
        ORDER BY month;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "Which food items have been claimed multiple times":
        query = '''
        SELECT food_id, COUNT(*) AS claim_count
        FROM claims
        GROUP BY food_id
        HAVING COUNT(*) > 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "How many listings are added per provider on average":
        query = '''
        SELECT ROUND(AVG(listing_count), 2) AS avg_listings
        FROM (
            SELECT provider_id, COUNT(*) AS listing_count
            FROM food_listings
            GROUP BY provider_id
        ) AS sub;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "Which food listing has the highest number of claims":
        query = '''
        SELECT food_id, COUNT(*) AS claim_count
        FROM claims
        GROUP BY food_id
        ORDER BY claim_count DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)

    elif action == "Find providers who operate in more than one city":
        query = '''
        SELECT provider_id, COUNT(DISTINCT city) AS city_count
        FROM providers
        GROUP BY provider_id
        HAVING COUNT(DISTINCT city) > 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df.head())

    elif action == "Which day of the week sees the most food claims":
        query = '''
        SELECT TO_CHAR(claimed_at, 'Day') AS day_of_week, COUNT(*) AS claim_count
        FROM claims
        GROUP BY day_of_week
        ORDER BY claim_count DESC
        LIMIT 1;
        '''
        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True)


# Page: User Introduction
if page == "User Introduction":
    st.title("👨‍💻 About the creator")
    st.markdown("**Name:** Hariharan  &nbsp;&nbsp;&nbsp;&nbsp;  **Role:** Associate Software Engineer")
