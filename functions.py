import re


def input_polygon_data():
    pattern = re.compile(
        r'(\(\s*((\d+(\.\d*)?)|(\.\d+))\s*,\s*((\d+(\.\d*)?)|(\.\d+))\s*\),\s*){3,}\(\s*((\d+(\.\d*)?)|(\.\d+))\s*,\s*'
        r'((\d+(\.\d*)?)|(\.\d+))\s*\)')
    while True:
        user_input = input(
            "Please enter data to draw Polygon. The data must be in format like this: (x,y),(x,y),(x,y). "
            "\nWhere (x,y) is the point and 'x' 'y' is the coordinates of the point. 'x' 'y' can be only"
            " \npositive integers. In your data first point must de the same as last.\n: ")

        if not pattern.fullmatch(user_input):
            print("Invalid input format. Please follow the specified format with at least 4 points. Please re-enter.")
            continue
        break
    points_match = re.findall(r'\(\s*(\d+(\.\d+)?)\s*,\s*(\d+(\.\d+)?)\s*\)', user_input)
    return [tuple(map(float, (point[0], point[2]))) for point in points_match]


def input_segment_index(polygon):
    while True:
        user_input = input("Now if you want to change Polygon segment choose it. Enter the Segment index.\n:")
        try:
            segment_index = int(user_input)
            if 0 <= segment_index < len(polygon.segments):
                return segment_index
            else:
                print("Invalid input. Please enter a valid integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def input_offset_value():
    while True:
        user_input = input("Now enter the value to move segment The value can be only distinctive or positive "
                           "\ninteger. Distinctive integer moves segment to left or down and positive to right or"
                           " up.\n:")
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
