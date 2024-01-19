from classes import Polygon
from functions import input_polygon_data, input_segment_index, input_offset_value

"""
    1. Index - is the numeric name of the "Segment". Numeration begins from 0.
    2. If offset_type == 'along_axis' or else we use offset_of_points_along_the_coordinate_axis() - moves the "Segment"
     to the right or left along the "X" axis. Exception: if point_a.y == point_b.y we moves the "Segment" to the down
     or high along the "Y" axis.
    3. If offset_type == 'parallel' we use offset_of_points_parallel_to_the_segment() - moves the "Segment" to a
     distance that is parallel to it (as shows on test picture)
    4. Handled exceptions:
        - If new intersection is higher or equal than intersection of neighbouring lines our intersection point will
         be the intersection of neighbours
        - If there are less than 2 Segments left, we cut redundant Segments and leave only one Segment with one point 
        - If new intersection goes beyond the Segment we cut this redundant Segments and search to the new intersection
         wit next / previous Segment. 
"""


def run_test_task():
    polygon = Polygon(input_polygon_data())
    polygon.draw()
    polygon.segment_offset(input_segment_index(polygon), input_offset_value(), 'parallel')
    polygon.draw()
    print(polygon.points)  # returns data without last point


run_test_task()
"""
TEST DATA:
exception_1. If new_line is higher than intersection of neighbouring lines our intersection point will be the
intersection of neighbours.
Polygon = (100, 100),(150, 400),(300, 550),(640, 500),(600, 0),(100, 100)
segment_i = 1
offset = -100
Result:
[[100.0, 100.0], [177.990, 567.943], [640.0, 500.0], [600.0, 0.0], [100.0, 100.0]]

exception_2. Cut redundant Segment if the offset goes beyond it.
Polygon = (100, 100),(150, 400),(300, 550),(640, 500),(600, 0),(100, 100)
segment_i = 1
offset = 400
Result:
[(225.000000000000, 75.0000000000000), (639.130, 489.130), (600.0, 0.0), (225.000000000000, 75.0000000000000)]

exception_3. Collapse to one point.
Polygon = (100, 100),(150, 400),(300, 550),(640, 500),(600, 0),(100, 100)
segment_i = 1
offset = 1000
Result:
[(600.0, 0.0), (600.0, 0.0)]

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
(3, 1),(0, 1)
(0, 1),(0, 2.5)
(0, 2.5),(3, 1)
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
