import streamlit as st
import pandas as pd
from datetime import datetime

# כותרת ראשית
st.set_page_config(page_title="קניין חכם", layout="wide")
st.title("🛒 קניין חכם - הסוכן החכם שלך לקניות")

# --- נתונים מדומים למלאי והיסטוריה ---
data = {
    "מוצר": ["חלב תנובה 3%", "עגבנייה", "טונה בשמן זית", "שוקולד פרה"],
    "קטגוריה": ["חלב ומוצריו", "ירקות", "שימורים", "חטיפים ומתוקים"],
    "תאריך קנייה אחרון": ["2025-03-17", "2025-03-11", "2025-03-17", "2025-03-17"],
    "תדירות רכישה": [5, 6, 5, 4],
    "מחיר ממוצע": [5.73, 6.5, 29.9, 8.5],
    "סטטוס במלאי": ["קיים", "אזל", "קיים", "נזרק"]
}
df = pd.DataFrame(data)

# --- הצגת המלאי ---
st.subheader("📦 מצב המלאי בבית")
st.dataframe(df, use_container_width=True)

# --- טופס דיווח זריקה ---
st.subheader("🚮 דיווח על מוצר שנזרק")
with st.form("throw_form"):
    product = st.selectbox("בחר מוצר", df["מוצר"].unique())
    reason = st.radio("סיבה", ["פג תוקף", "לא השתמשנו", "התקלקל"])
    submit = st.form_submit_button("דווח")

    if submit:
        df.loc[df["מוצר"] == product, "סטטוס במלאי"] = "נזרק"
        st.success(f"עודכן שהמוצר '{product}' נזרק ({reason})")

# --- המלצות קנייה חכמה ---
st.subheader("🤖 רשימת קניות חכמה")
recommendations = df[(df["סטטוס במלאי"] != "קיים") & (df["תדירות רכישה"] >= 3)]
st.write("מוצרים שנרכשו בתדירות גבוהה אך אינם זמינים כעת:")
st.table(recommendations[["מוצר", "קטגוריה", "תדירות רכישה"]])

# --- גרף צריכה לפי קטגוריה ---
st.subheader("📊 צריכה לפי קטגוריה")
chart_data = df.groupby("קטגוריה")["תדירות רכישה"].sum().reset_index()
st.bar_chart(chart_data.set_index("קטגוריה"))
