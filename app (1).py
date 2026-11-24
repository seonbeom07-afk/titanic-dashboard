
import streamlit as st
import pandas as pd
import plotly.express as px

# [추가] 화면 설정
st.set_page_config(page_title="Titanic 대시보드", layout="wide")


# ===== 필터 함수 =====
def filter_data(df, sexes, classes, age_range):
    lo, hi = age_range
    cond_sex = df["sex"].isin(sexes)
    cond_cls = df["pclass"].isin(classes)
    cond_age = df["age"].between(lo, hi)
    return df[cond_sex & cond_cls & cond_age]


# ===== KPI 함수 =====
def kpi(df):
    if len(df) == 0:
        return 0, 0, 0

    n = len(df)
    rate = round(df["survived"].mean() * 100, 1)
    age = round(df["age"].mean(), 1)

    return n, rate, age


# ===== 객실 등급별 생존율 차트 함수 =====
def class_rate_bar(df):
    r = (
        df.groupby("pclass")["survived"]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
    )

    fig = px.bar(
        r,
        x="pclass",
        y="survived",
        text="survived",
        title="객실 등급별 생존율(%)"
    )
    return fig


# ===== 나이 히스토그램 함수 =====
def age_hist(df):
    fig = px.histogram(
        df,
        x="age",
        color="survived",
        barmode="overlay",
        opacity=0.6,
        title="생존 여부별 나이 분포"
    )
    return fig


# ===== 데이터 읽기 =====
@st.cache_data
def load_data():
    return pd.read_csv("titanic.csv")

df = load_data()


# ===== 제목 =====
st.title("타이타닉, 누가 살아남았나?")


# ===== 사이드바 필터 =====
sexes = st.sidebar.multiselect(
    "성별",
    ["male", "female"],
    ["male", "female"]
)

classes = st.sidebar.multiselect(
    "객실 등급",
    [1, 2, 3],
    [1, 2, 3]
)

ages = st.sidebar.slider(
    "나이",
    0, 80, (0, 80)
)


# ===== 필터 적용 =====
f = filter_data(df, sexes, classes, ages)


# ===== KPI 카드 =====
n, rate, age = kpi(f)

c1, c2, c3 = st.columns(3)

c1.metric("승객 수", f"{n}명")
c2.metric("생존율", f"{rate}%")
c3.metric("평균 나이", f"{age}세")


# ===== [추가] 차트 2개 배치 =====
left, right = st.columns(2)

with left:
    st.plotly_chart(class_rate_bar(f), use_container_width=True)

with right:
    st.plotly_chart(age_hist(f), use_container_width=True)


# ===== [추가] 데이터 보기 =====
with st.expander("데이터 보기"):
    st.dataframe(f)
