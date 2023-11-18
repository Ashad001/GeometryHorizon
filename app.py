import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from jarvisMarch import JarvisMarch

def plot_graph(x, y):
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='blue')
    st.pyplot(fig)

algo = 'Jarvis March'

def main():
    st.title('Point Plotter')
    option = st.selectbox('Choose an option:', ('Enter Points Individually', 'Generate Random Points', 'Add Points from CSV'))

    if 'x_points' not in st.session_state:
        st.session_state.x_points = []
    if 'y_points' not in st.session_state:
        st.session_state.y_points = []

    if option == 'Enter Points Individually':
        
        st.header('Enter Points Individually')
        col1, col2 = st.columns(2)

        with col1:
            x_input = st.text_input('Enter X coordinate:')
            y_input = st.text_input('Enter Y coordinate:')

            if st.button('Add Point'):
                x = float(x_input) if x_input else 0.0
                y = float(y_input) if y_input else 0.0
                st.session_state.x_points.append(x)
                st.session_state.y_points.append(y)
                st.success(f'Point ({x}, {y}) added.')

        with col2:
            st.subheader('Added Points:')
            points_df = pd.DataFrame(list(zip(st.session_state.x_points, st.session_state.y_points)), columns=['X', 'Y'])
            st.table(points_df)

        if st.button(f'Draw {algo}'):
            plot_graph(st.session_state.x_points, st.session_state.y_points)
        
    elif option == 'Generate Random Points':
        st.header('Generate Random Points')
        num_points = st.number_input('Enter the number of points:', min_value=1, value=5, step=1)
        min_range = st.number_input('Enter minimum value:', value=0)
        max_range = st.number_input('Enter maximum value:', value=10)

        if st.button(f'Draw {algo}'):
            random_points_x = np.random.uniform(min_range, max_range, num_points)
            random_points_y = np.random.uniform(min_range, max_range, num_points)
            plot_graph(random_points_x, random_points_y)

    elif option == 'Add Points from CSV':
        st.header('Add Points from CSV')
        uploaded_file = st.file_uploader('Upload a CSV file:', type=['csv'])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            csv_points_x = df.get('x', [])
            csv_points_y = df.get('y', [])

            if st.button(f'Draw {algo}'):
                plot_graph(csv_points_x, csv_points_y)

if __name__ == "__main__":
    main()
