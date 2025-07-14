import streamlit as st
from goal import Goal
from agent import AIAgent
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from io import BytesIO

st.set_page_config(page_title="Мотивационный ИИ-Агент", layout="centered")
st.title("🤖 Мотивационный ИИ-Агент")

SAVE_LOG = "log.json"
SAVE_GOALS = "goals.json"

if 'agent' not in st.session_state:
    agent = AIAgent()
    agent.goals.add_goal(Goal("Изучить Python", priority=1.0))
    agent.goals.add_goal(Goal("Построить ИИ", priority=1.5))
    agent.goals.add_goal(Goal("Написать статью", priority=0.8))
    st.session_state.agent = agent

agent = st.session_state.agent

st.sidebar.header("🛠 Настройки")
mood = st.sidebar.slider("Настроение агента", 0.5, 1.5, agent.motivation.mood, step=0.01)
agent.motivation.mood = mood

st.sidebar.subheader("➕ Добавить цель")
with st.sidebar.form("goal_form"):
    goal_name = st.text_input("Название цели")
    goal_priority = st.slider("Приоритет", 0.1, 2.0, 1.0)
    goal_submit = st.form_submit_button("Добавить")
    if goal_submit and goal_name:
        agent.goals.add_goal(Goal(goal_name, goal_priority))
        st.success(f"Добавлена цель: {goal_name}")

st.sidebar.subheader("💾 Сохранение / Загрузка")
col1, col2 = st.sidebar.columns(2)
if col1.button("💾 Сохранить лог"):
    agent.memory.save_to_file(SAVE_LOG)
    with open(SAVE_GOALS, "w", encoding="utf-8") as f:
        json.dump([{"name": g.name, "priority": g.priority, "progress": g.progress} for g in agent.goals.goals], f)
    st.sidebar.success("Лог и цели сохранены")

if col2.button("📂 Загрузить лог"):
    if os.path.exists(SAVE_LOG):
        with open(SAVE_LOG, "r", encoding="utf-8") as f:
            agent.memory.log = json.load(f)
        st.sidebar.success("Лог загружен!")
    else:
        st.sidebar.warning("Файл log.json не найден.")
    if os.path.exists(SAVE_GOALS):
        with open(SAVE_GOALS, "r", encoding="utf-8") as f:
            agent.goals.goals = [Goal(**g) for g in json.load(f)]
        st.sidebar.success("Цели загружены!")
    else:
        st.sidebar.warning("Файл goals.json не найден.")

if st.sidebar.button("🧹 Очистить всё"):
    agent.goals.goals.clear()
    agent.memory.log.clear()
    st.sidebar.success("Все данные очищены")

# Кнопка скачивания лога
if agent.memory.log:
    log_bytes = BytesIO()
    log_bytes.write(json.dumps(agent.memory.log, indent=2, ensure_ascii=False).encode('utf-8'))
    log_bytes.seek(0)
    st.sidebar.download_button(
        label="📥 Скачать лог",
        data=log_bytes,
        file_name="log.json",
        mime="application/json"
    )

# Кнопка скачивания целей
if agent.goals.goals:
    goals_bytes = BytesIO()
    goals_bytes.write(json.dumps([
        {"name": g.name, "priority": g.priority, "progress": g.progress} for g in agent.goals.goals
    ], indent=2, ensure_ascii=False).encode('utf-8'))
    goals_bytes.seek(0)
    st.sidebar.download_button(
        label="📥 Скачать цели",
        data=goals_bytes,
        file_name="goals.json",
        mime="application/json"
    )

with st.form("run_form"):
    steps = st.slider("Сколько шагов выполнить?", 1, 50, 5)
    submitted = st.form_submit_button("▶️ Запустить")
    if submitted:
        for _ in range(steps):
            agent.run_step()

st.subheader("🎯 Активные цели")
active_goals = agent.goals.get_active_goals()
for g in active_goals:
    st.write(f"{g.name}: {g.progress:.2f} / 1.0 (приоритет: {g.priority:.2f})")

st.subheader("📈 Прогресс по целям")
data = agent.memory.log
if data:
    df = pd.DataFrame(data)
    fig, ax = plt.subplots()
    for goal in df['goal'].unique():
        goal_df = df[df['goal'] == goal]
        cumulative = goal_df['progress_delta'].cumsum()
        ax.plot(goal_df['step'], cumulative, label=goal)
    ax.set_xlabel("Шаг")
    ax.set_ylabel("Прогресс")
    ax.set_title("Динамика прогресса")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("Лог пока пуст. Запусти шаги выше.")

# 🧠 Просмотр памяти агента
st.subheader("🧠 Что знает агент?")
if data:
    st.dataframe(df)
else:
    st.info("Агент пока ничего не знает.")
