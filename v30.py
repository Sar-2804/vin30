import streamlit as st
import random
import time

# Initialize session state
if "ball_x" not in st.session_state:
    st.session_state.ball_x = 300
    st.session_state.ball_y = 350
    st.session_state.ball_radius = 20
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.frame_count = 0

WIDTH, HEIGHT = 600, 400
ball_speed = 15
obstacle_width = 50
obstacle_height = 20
obstacle_speed = 10
spawn_rate = 10

st.title("🎮 Ball Avoidance Game (Streamlit)")

# Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Left"):
        st.session_state.ball_x -= ball_speed
with col2:
    if st.button("➡️ Right"):
        st.session_state.ball_x += ball_speed
with col3:
    if st.button("🔄 Restart"):
        st.session_state.ball_x = 300
        st.session_state.ball_y = 350
        st.session_state.obstacles = []
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.frame_count = 0

# Game logic
if not st.session_state.game_over:
    st.session_state.frame_count += 1

    # Spawn obstacles
    if st.session_state.frame_count % spawn_rate == 0:
        obs_x = random.randint(0, WIDTH - obstacle_width)
        st.session_state.obstacles.append([obs_x, 0])

    # Move obstacles
    new_obstacles = []
    for obs in st.session_state.obstacles:
        obs[1] += obstacle_speed
        if obs[1] < HEIGHT:
            new_obstacles.append(obs)
    st.session_state.obstacles = new_obstacles

    # Collision detection
    for obs in st.session_state.obstacles:
        if (
            st.session_state.ball_x + st.session_state.ball_radius > obs[0]
            and st.session_state.ball_x - st.session_state.ball_radius < obs[0] + obstacle_width
            and st.session_state.ball_y + st.session_state.ball_radius > obs[1]
            and st.session_state.ball_y - st.session_state.ball_radius < obs[1] + obstacle_height
        ):
            st.session_state.game_over = True

    st.session_state.score += 1

# Draw (simple text-based visualization)
st.write(f"**Score:** {st.session_state.score}")

canvas = [[" " for _ in range(30)] for _ in range(20)]

# Draw ball
bx = int(st.session_state.ball_x / 20)
by = int(st.session_state.ball_y / 20)
if 0 <= by < 20 and 0 <= bx < 30:
    canvas[by][bx] = "O"

# Draw obstacles
for obs in st.session_state.obstacles:
    ox = int(obs[0] / 20)
    oy = int(obs[1] / 20)
    if 0 <= oy < 20 and 0 <= ox < 30:
        canvas[oy][ox] = "X"

# Render grid
for row in canvas:
    st.text("".join(row))

# Game over
if st.session_state.game_over:
    st.error("💀 GAME OVER")

# Auto refresh
time.sleep(0.1)
st.rerun()
