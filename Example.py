import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Generate some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Function to plot based on selected range
def plot_selected_range(start, end):
    plt.plot(x, y)
    plt.xlim(start, end)
    plt.xlabel('x')
    plt.ylabel('sin(x)')
    plt.title('Plot of sin(x)')
    st.pyplot()

# Create custom slider for selecting range
st.sidebar.markdown("### Select Range:")
start_value = st.sidebar.slider("Start", min_value=min(x), max_value=max(x), value=min(x))
end_value = st.sidebar.slider("End", min_value=min(x), max_value=max(x), value=max(x))

# Plot based on selected range
plot_selected_range(start_value, end_value)
