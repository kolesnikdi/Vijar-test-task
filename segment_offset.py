from classes import Polygon
from functions import input_polygon_data, input_segment_index, input_offset_value

"""
    1. Index - is the numeric name of the "Segment".
    2. offset_of_points_along_the_coordinate_axis() - moves the "Segment" to the right or left along the "X" axis.
        - Exception: if point_a.y == point_b.y we moves the "Segment" to the down or high along the "Y" axis
    3. TODO offset_of_points_parallel_to_the_segment() - moves the "Segment" to a distance that is perpendicular
       TODO to it (as shows on test picture)
    4. Exception: TODO cut redundant Segment:
        - if new points go beyond the coordinates of neighbouring segment,
        - if there are no new intersection points or if the new segments are the same. 
"""


def run_test_task():
    polygon = Polygon(input_polygon_data())
    polygon.draw()
    polygon.segment_offset(input_segment_index(polygon), input_offset_value())
    polygon.draw()
    print(polygon.get_point_data())     # returns data without last point


run_test_task()
"""
TEST DATA:
1.
Polygon = (0, 0),(0, 500),(600, 500),(600, 0),(0, 0)
segment_i = 2
offset = -1.5
Result:
[(0, 0),(0, 500),(598.5, 500),(598.5, 0),(0, 0)]

2.
Polygon = (3, 1),(1, 1),(1, 2),(3, 1)
segment_i = 1
offset = -1
Result:
[(3, 1),(0, 1),(0, 2.5),(3, 1)] 

3.
Polygon = (3, 1),(1, 1),(1, 2),(3, 1)
segment_i = 1
offset = 1
Result:
[(3, 1),(2, 1),(2, 1.5),(3, 1)]

4.
Polygon = (3, 1),(1, 1),(1, 2),(3, 1)
segment_i = 1
offset = 1.5
Result:
[(3, 1),(2.5, 1),(2.5, 1.25),(3, 1)]
"""