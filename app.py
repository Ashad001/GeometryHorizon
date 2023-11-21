import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ConvexHull.jarvisMarch import JarvisMarch
from ConvexHull.grhamScan import GrahamScan
from ConvexHull.quickHull import QuickHull
from ConvexHull.bruteForce import BruteForce

from LineIntersection.lineIntersection import LineIntersection


def plot_graph(x, y):
    fig, ax = plt.subplots()
    ax.scatter(x, y, color="blue")
    st.pyplot(fig)


algo = "Jarvis March"


def convex_hull_page():
    st.empty()
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
            st.subheader("Min/Max Point")
            num_points = st.number_input(
                "Enter the number of points:", min_value=1, value=5, step=1
            )
            min_range = st.number_input("Enter minimum value:", value=0)
            max_range = st.number_input("Enter maximum value:", value=10)
            if st.button("Generate Points"):
                st.session_state.x_points = np.random.uniform(
                    min_range, max_range, num_points
                )
                st.session_state.y_points = np.random.uniform(
                    min_range, max_range, num_points
                )

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
        # fig = jm.plot_step_by_step()
        fig = jm.create_animation()
        st.plotly_chart(fig, use_container_width=True)

    elif algo == "Graham Scan":
        gs = GrahamScan(points=points)
        hull_points = gs()
        fig = gs.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)
    elif algo == "QuickHull":
        qh = QuickHull(points=points)
        hull_points = qh()
        fig = qh.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)
    elif algo == "Brute Force":
        bf = BruteForce(points=points)
        hull_points = bf()
        fig = bf.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)
        pass
    else:
        pass


def line_intersection_page():
    st.empty()
    st.title("Line Intersection Visualizer")
    option = st.selectbox(
        "Choose an option:",
        ("Enter Points Individually", "Generate Random Points", "Add Points from CSV"),
    )

    if "line_1" not in st.session_state:
        st.session_state.line_1 = []
    if "line_2" not in st.session_state:
        st.session_state.line_2 = []

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
                        st.session_state.line_1.append(x)
                        st.session_state.line_2.append(y)
                        st.success(f"Point ({x}, {y}) added.")
                    except ValueError:
                        st.error(
                            "Invalid input. Please enter valid numerical values for X and Y coordinates."
                        )

            with clear_col:
                if st.button("Clear Points"):
                    st.session_state.line_1 = []
                    st.session_state.line_2 = []
                    st.success("Points cleared.")

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.line_1, st.session_state.line_2)),
                columns=["X", "Y"],
            )
            st.subheader("Added Points:")
            st.table(points_df)

    elif option == "Generate Random Points":
        st.header("Generate Random Points")
        point_col, table_col = st.columns(2)
        with point_col:
            st.subheader("Min/Max Point")
            min_range = st.number_input("Enter minimum value:", value=0)
            max_range = st.number_input("Enter maximum value:", value=10)
            if st.button("Generate Points"):
                st.session_state.line_1 = np.random.uniform(min_range, max_range, 4)
                st.session_state.line_2 = np.random.uniform(min_range, max_range, 4)

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.line_1, st.session_state.line_2)),
                columns=["X", "Y"],
            )

            st.subheader("Added Points:")
            st.table(points_df)

    elif option == "Add Points from CSV":
        point_col, table_col = st.columns(2)
        with point_col:
            st.subheader("Upload CSV file")
            uploaded_file = st.file_uploader("CSV", type=["csv"])
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                if len(df.columns) != 2 or len(df.index) < 4:
                    st.error("Invalid CSV file. Please upload a valid CSV file.")
                if len(df.index) > 4:
                    df = df.head(4)
                    st.info("Size too large, only first 4 rows are considered.")
                st.session_state.line_1 = df.get("x", [])
                st.session_state.line_2 = df.get("y", [])

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.line_1, st.session_state.line_1)),
                columns=["X", "Y"],
            )

            st.subheader("Added Points:")
            st.table(points_df)

    st.header("Intersection Points")
    if st.button("Check Intersection"):
        if len(st.session_state.line_1) != 4 or len(st.session_state.line_2) != 4:
            st.error("Add atleast 4 points")
        else:
            draw_intersection_points()


def draw_intersection_points():
    algo = st.selectbox(
        "Choose an algorithm:",
        ("Brute Force", "Sweep Line"),
    )
    lines = [
        item
        for pair in zip(st.session_state.line_1, st.session_state.line_2)
        for item in pair
    ]
    line1 = lines[: len(lines) // 2]
    line2 = lines[len(lines) // 2 :]
    if algo == "Brute Force":
        bf = LineIntersection(line1=line1, line2=line2)
        intersect_points = bf()
        fig = bf.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)

    elif algo == "Sweep Line":
        bf = LineIntersection(line1=line1, line2=line2)
        intersect_points = bf()
        fig = bf.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)
    else:
        pass


def report_page():
    st.empty()
    header_text = "Design and Analysis of Geometric Algorithms"
    st.markdown(
        f"""
        <h1 style='text-align: center;'>{header_text}</h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <h5 style='text-align: center;'>Ashad Abdullah Qureshi November 20, 2023</h5>
        """,
        unsafe_allow_html=True,
    )

    with open("./templates/index.html", "r") as f:
        html_string = f.read()
    st.markdown(html_string, unsafe_allow_html=True)
    st.subheader("All rights reserved by Ashad (and only Ashad).")


def main():
    st.sidebar.title("Geometry Overpowerred")
    choice = st.sidebar.radio(
        "Menu:",
        ("report", "Convex Hull Algorithms", "Line Intersection Algorithms"),
    )

    if choice == "report":
        report_page()
    elif choice == "Convex Hull Algorithms":
        convex_hull_page()
    elif choice == "Line Intersection Algorithms":
        line_intersection_page()


if __name__ == "__main__":
    main()
