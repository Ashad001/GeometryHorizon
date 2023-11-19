import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from jarvisMarch import JarvisMarch
from grhamScan import GrahamScan

def plot_graph(x, y):
    fig, ax = plt.subplots()
    ax.scatter(x, y, color="blue")
    st.pyplot(fig)

algo = "Jarvis March"

def main():
    st.title("Convex Hull Visualizer")
    option = st.selectbox(
        "Choose an option:",
        ("Enter Points Individually", "Generate Random Points", "Add Points from CSV"),
    )

    if "x_points" not in st.session_state:
        st.session_state.x_points = []
    if "y_points" not in st.session_state:
        st.session_state.y_points = []

    if option == "Enter Points Individually":
        st.header("Enter Points Individually")
        input_col, table_col = st.columns(2)

        with input_col:
            st.subheader("Enter Coordinates")
            x_input = st.text_input("Enter X coordinate:")
            y_input = st.text_input("Enter Y coordinate:")

            point_col, clear_col = st.columns(2)
            with point_col:
                if st.button("Add Point"):
                    try:
                        x = float(x_input) if x_input else 0.0
                        y = float(y_input) if y_input else 0.0
                        st.session_state.x_points.append(x)
                        st.session_state.y_points.append(y)
                        st.success(f"Point ({x}, {y}) added.")
                    except ValueError:
                        st.error(
                            "Invalid input. Please enter valid numerical values for X and Y coordinates."
                        )

            with clear_col:
                if st.button("Clear Points"):
                    st.session_state.x_points = []
                    st.session_state.y_points = []
                    st.success("Points cleared.")

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.x_points, st.session_state.y_points)),
                columns=["X", "Y"],
            )
            st.subheader("Added Points:")
            st.dataframe(points_df, height=200, width=800)
            


    elif option == "Generate Random Points":
        st.header("Generate Random Points")
        point_col, table_col = st.columns(2)
        with point_col:
            num_points = st.number_input(
                "Enter the number of points:", min_value=1, value=5, step=1
            )
            min_range = st.number_input("Enter minimum value:", value=0)
            max_range = st.number_input("Enter maximum value:", value=10)
            if st.button("Generate Points"):
                st.session_state.x_points = np.random.uniform(min_range, max_range, num_points)
                st.session_state.y_points = np.random.uniform(min_range, max_range, num_points)
            
        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.x_points, st.session_state.y_points)),
                columns=["X", "Y"],
            )

            st.subheader("Added Points:")
            st.dataframe(points_df, height=200, width=800)

            
    elif option == "Add Points from CSV":
        st.header("Add Points from CSV")
        point_col, table_col = st.columns(2)
        
        with point_col:
            st.subheader("Upload CSV file")
            uploaded_file = st.file_uploader("CSV", type=["csv"])
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                st.session_state.x_points = df.get("x", [])
                st.session_state.y_points = df.get("y", [])

        with table_col: 
            points_df = pd.DataFrame(
                list(zip(st.session_state.x_points, st.session_state.y_points)),
                columns=["X", "Y"],
            )

            st.subheader("Added Points:")
            st.dataframe(points_df, height=200, width=800)
            
    st.header("Create Convex Hull")    
    draw_convex_hull()


def draw_convex_hull():
    points = np.column_stack((st.session_state.x_points, st.session_state.y_points))
    algo = st.selectbox(
        "Choose an algorithm:",
        ("Jarvis March", "Graham Scan", "QuickHull", "Brute Force"),
    )

    if algo == "Jarvis March":
        jm = JarvisMarch(points=points)
        hull_points = jm()
        fig = jm.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)
        
    elif algo == "Graham Scan":
        gs = GrahamScan(points=points)
        hull_points = gs()
        fig = gs.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)
        pass
    elif algo == "QuickHull":
        pass
    elif algo == "Brute Force":
        pass
    else:
        pass


if __name__ == "__main__":
    main()
