import difflib
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Football Cards Prediction",
    page_icon="⚽",
    layout="centered",
)

st.title("⚽ Football Cards Prediction")
st.write("توقع عدد الكروت الصفراء والحمراء للاعب في الموسم القادم")

BASE = Path(__file__).parent

# نفس الـ features اللي الموديل اتدرب عليها (وبنفس الترتيب)
FEATURES = ["appearances", "yellow_cards", "red_cards"]


@st.cache_resource
def load_models():
    rf_yellow = joblib.load(BASE / "rf_yellow_model.pkl")
    rf_red = joblib.load(BASE / "rf_red_model.pkl")
    return rf_yellow, rf_red


@st.cache_data
def load_data():
    return pd.read_csv(BASE / "player_season.csv")


try:
    rf_yellow, rf_red = load_models()
    df = load_data()
except Exception as e:
    st.error(f"مشكلة في تحميل الموديلات أو الداتا: {e}")
    st.stop()


def predict(appearances, yellow, red):
    X_new = pd.DataFrame([[appearances, yellow, red]], columns=FEATURES)
    pred_yellow = max(0, round(float(rf_yellow.predict(X_new)[0]), 2))
    pred_red = max(0, round(float(rf_red.predict(X_new)[0]), 2))
    st.success("Prediction Results (الموسم القادم)")
    st.write(f"🟨 المتوقع من الكروت الصفراء: **{pred_yellow}**")
    st.write(f"🟥 المتوقع من الكروت الحمراء: **{pred_red}**")


mode = st.radio(
    "طريقة الإدخال",
    ["🔎 البحث عن لاعب في الداتا", "✍️ إدخال إحصائيات لاعب (أي لاعب)"],
)

# ---------------------------------------------------------------
# الوضع 1: البحث في الداتا
# ---------------------------------------------------------------
if mode.startswith("🔎"):
    player_name = st.text_input("Enter football player name")

    if player_name.strip():
        matches = df[
            df["player_name"].str.contains(
                player_name.strip(), case=False, na=False, regex=False
            )
        ]

        if matches.empty:
            st.warning(
                "اللاعب مش موجود في الداتا. "
                "جرّب وضع «إدخال إحصائيات لاعب» لتوقع أي لاعب."
            )
            # اقتراحات لأسماء قريبة (لو الاسم متكتب غلط)
            all_names = df["player_name"].dropna().unique().tolist()
            close = difflib.get_close_matches(
                player_name.strip(), all_names, n=5, cutoff=0.5
            )
            if close:
                st.info("هل تقصد: " + " | ".join(close))
        else:
            latest = (
                matches.sort_values("season")
                .groupby("player_id")
                .tail(1)
                .reset_index(drop=True)
            )
            labels = [
                f"{r.player_name} (آخر موسم: {int(r.season)})"
                for r in latest.itertuples()
            ]
            choice = st.selectbox("اختار اللاعب", labels)
            row = latest.iloc[[labels.index(choice)]]

            if st.button("Predict"):
                r = row.iloc[0]
                predict(r["appearances"], r["yellow_cards"], r["red_cards"])
                with st.expander("البيانات المستخدمة في التوقع"):
                    st.dataframe(row[["player_name", "season"] + FEATURES])

# ---------------------------------------------------------------
# الوضع 2: إدخال يدوي لأي لاعب
# ---------------------------------------------------------------
else:
    st.caption("اكتب إحصائيات اللاعب في آخر موسم له، وهيتوقع الموسم اللي بعده.")
    name = st.text_input("اسم اللاعب (اختياري)")
    c1, c2, c3 = st.columns(3)
    appearances = c1.number_input("عدد المباريات", min_value=0, max_value=80, value=30, step=1)
    yellow = c2.number_input("الكروت الصفراء", min_value=0, max_value=30, value=3, step=1)
    red = c3.number_input("الكروت الحمراء", min_value=0, max_value=10, value=0, step=1)

    if st.button("Predict", key="manual"):
        if name.strip():
            st.write(f"**{name.strip()}**")
        predict(appearances, yellow, red)