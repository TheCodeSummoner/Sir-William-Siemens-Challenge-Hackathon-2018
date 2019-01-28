from res.parser import get_raw_data
import matplotlib.pyplot as plt

# Collect all data
data = get_raw_data()

# Define the number of elements to display in the graph
NO_ELEMENTS = 200

# Define y-axis boundaries
Y_BOUNDARY_MAX = 100
Y_BOUNDARY_MIN = 0

# Define the delay
DELAY = 0.01


def get_next_data(index: int):

    # Check if there are enough elements to display
    if index + NO_ELEMENTS >= len(data):

        # Set the axis
        plt.gca().set_xlim([len(data) - NO_ELEMENTS, len(data)])

        # Return everything possible if less than n elements left
        return data[index:]

    else:
        # Return n elements starting from the element at a given index
        return data[index:index + NO_ELEMENTS]


def display_animated_graph():

    # Initialise the index
    index = 0

    # Make sure the window is updated properly (turn interactive mode on)
    plt.ion()

    # Set the style
    plt.style.use("fivethirtyeight")

    # Retrieve and store the initial graph's axis
    axis = data.plot(visible=False)

    # Declare graph boundaries
    y_min = Y_BOUNDARY_MIN
    y_max = Y_BOUNDARY_MAX

    # Set the axis
    plt.gca().set_ylim([y_min, y_max])

    # Animate the graph
    while True:

        # Retrieve current points
        current_data = get_next_data(index)

        # Plot the points and set the labels
        current_data.plot(ax=axis, title="MindSphere data")

        # Apply a pause each time to correctly display the change
        plt.pause(DELAY)

        # Clear the graph
        plt.cla()

        # Set the axis
        plt.gca().set_ylim([y_min, y_max])

        # Set the index
        index += 1
        if index == len(data):
            index = 0


if __name__ == "__main__":
    display_animated_graph()