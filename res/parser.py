from pandas import read_csv, concat
from os import path, listdir

ROOT = path.normpath(path.dirname(__file__))


def _parse_data(*args: str, sort=None, fn=None):

    # Initialise data to store pandas object
    data = list()

    # Iterate over each path specified and load the data
    for file_name in args:
        data.append(read_csv(file_name))

    # Exit if there is no data available
    if not data:
        print("No data available. Exiting...")
        exit(0)

    # Concatenate all values
    data = concat(data)

    # If the sort argument and function are specified, sort the data
    if sort and fn:

        # Create a temporary data column to put the calculated values in
        data["temp"] = data[sort].apply(fn)

        # Sort the values by timestamp and reset indexes
        data = data.sort_values("temp").drop("temp", axis=1).reset_index(drop=True)

    # Return parsed data
    return data


def _parse_timestamp(stamp: str):

    # Unpack date and time
    date, time = stamp.split()

    # Unpack values within date
    day, month, year = date.split("/")

    # Unpack values within time
    hour, minute, second = time.split(":")

    # Build and return new string with the spaces of values changed
    return " ".join(x for x in (year, month, day, hour, minute, second))


# TODO: A lot of hardcoded values, could use a decorator to register new data (kinda like single-dispatch)
def get_formatted_data():

    # Parse the data
    data = get_raw_data()

    # Declare a function to normalise the values
    normalize = lambda _min, _max, v: (v - _min) / (_max - _min) * 255

    # Cast each series to list
    red, green, blue, humidity, temperature, battery, noise = \
              list(data["Carbon Monoxide"]),\
              list(data["Nitric Oxide"]),\
              list(data["Nitrogen Dioxide"]),\
              list(data["Relative Humidity"]),\
              list(data["Temperature"]),\
              list(data["Battery"]),\
              list(data["Noise"])

    # Find out maximums and minimums
    max_red, min_red = max(red), min(red)
    max_green, min_green = max(green), min(green)
    max_blue, min_blue = max(blue), min(blue)
    max_humidity, min_humidity = max(humidity), min(humidity)
    avg_temperature = sum(temperature)/len(temperature)
    max_battery, min_battery = max(battery), min(battery)
    avg_noise = sum(noise)/len(noise)

    # Apply either the default or custom normalisation functions
    red = [normalize(max_red, min_red, x) for x in red]
    green = [normalize(max_green, min_green, x) for x in green]
    blue = [normalize(max_blue, min_blue, x) for x in blue]
    humidity = [int(50 + ((x - min_humidity)*(70-50)/(max_humidity - min_humidity))) for x in humidity]
    temperature = [0 if x > avg_temperature else 10 for x in temperature]
    battery = [normalize(max_battery, min_battery, x) for x in battery]
    noise = [1 if x > avg_noise else 0 for x in noise]

    # Initialise a list of strings to return
    strings = list()

    # Iterate over each row
    for i in range(len(data)):

        # Write to the file
        strings.append(",".join(str(int(x))for x in
                                (red[i], green[i], blue[i], humidity[i], temperature[i], battery[i], noise[i])))

    # Return the strings
    return strings


def get_raw_data():

    # Automatically load the data from csv folder and parse it
    data = _parse_data(*[path.join(ROOT, "csv", file) for file in listdir(path.join(ROOT, "csv"))],
                       sort="Timestamp", fn=_parse_timestamp)

    return data


if __name__ == "__main__":
    print(get_formatted_data())
