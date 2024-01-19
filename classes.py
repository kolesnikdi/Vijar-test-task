from sympy import symbols, Eq, solve
import matplotlib.pyplot as plt


class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def __repr__(self):
        return str([self.x, self.y])


class Segment:
    __slots__ = ('point_a', 'point_b')

    def __init__(self, point_a, point_b):
        if isinstance(point_a, Point):
            self.point_a = point_a
        if isinstance(point_b, Point):
            self.point_b = point_b
        else:
            raise ValueError("Invalid point type. Must be a Point instance.")

    def __repr__(self):
        return str([self.point_a, self.point_b])


class Polygon:
    __slots__ = ('points', 'segments', 'correction', 'index')

    def __init__(self, points_lst):
        self.points = [Point(px, py) for px, py in points_lst[:-1]]
        self.points.append(self.points[0])

        if self.points[0].x != self.points[-1].x and self.points[0].y != self.points[-1].y:
            raise ValueError("Invalid Polygon values. First point must be the same as last.")

        self.segments = self._make_segments()
        self.index = None
        self.correction = 0

    def get_point_data(self):
        # data for draw(). Returns data without last point
        return tuple([p.as_tuple() for p in self.points[:-1]])

    def _make_segments(self):
        count = len(self.points)
        if count < 4:
            raise ValueError("Not enough  Points to make Polygon.")
        segments = []
        for i in range(len(self.points) - 1):
            segments.append(Segment(self.points[i], self.points[i + 1]))
        return segments

    @staticmethod
    def _segment_formula(point_a, point_b):
        x, y = symbols('x y')
        if point_a[0] == point_b[0]:
            eq = Eq(x, point_a[0])
        else:
            eq = Eq(y - point_a[1], (point_b[1] - point_a[1]) / (point_b[0] - point_a[0]) * (x - point_a[0]))
        return eq

    def _get_next_segment_points(self):
        # We don't need here correction because this check is first and index allways will be the same because we
        if self.index == len(self.segments) - 1:
            return self.segments[0]
        else:
            return self.segments[self.index + 1]

    def _get_previous_segment_points(self):
        return self.segments[self.index - 1]

    @staticmethod
    def offset_of_points_along_the_coordinate_axis(new_point_a, new_point_b, offset_value):
        if new_point_a.y == new_point_b.y:
            new_point_a.y += offset_value  # parallel to x
            new_point_b.y += offset_value
        else:
            new_point_a.x += offset_value  # parallel to y
            new_point_b.x += offset_value

    @staticmethod
    def offset_of_points_parallel_to_the_segment(new_point_a, new_point_b, offset_value):
        vector = (new_point_b.x - new_point_a.x, new_point_b.y - new_point_a.y)
        fixed_vector = (
            vector[0] / (vector[0] ** 2 + vector[1] ** 2) ** 0.5, vector[1] / (vector[0] ** 2 + vector[1] ** 2) ** 0.5)
        new_point_a.x, new_point_a.y = new_point_a.x + offset_value * fixed_vector[0], new_point_a.y + offset_value * \
                                       fixed_vector[1]
        new_point_b.x, new_point_b.y = new_point_b.x + offset_value * fixed_vector[0], new_point_b.y + offset_value * \
                                       fixed_vector[1]

    def segment_offset(self, index, offset_value, offset_type):
        self.index = index
        one_time_check = True
        x, y = symbols('x y')
        old_point_a, old_point_b = self.segments[index].point_a, self.segments[index].point_b
        new_point_a, new_point_b = Point(*old_point_a.as_tuple()), Point(*old_point_b.as_tuple())

        if offset_type == 'parallel':
            self.offset_of_points_parallel_to_the_segment(new_point_a, new_point_b, offset_value)
        if offset_type == 'along_axis' or None:
            self.offset_of_points_along_the_coordinate_axis(new_point_a, new_point_b, offset_value)
        else:
            self.offset_of_points_along_the_coordinate_axis(new_point_a, new_point_b, offset_value)

        new_line = self._segment_formula(new_point_a.as_tuple(), new_point_b.as_tuple())
        next_ = self._get_next_segment_points()
        previous = self._get_previous_segment_points()

        while True:
            next_point_a, next_point_b = next_.point_a.as_tuple(), next_.point_b.as_tuple()
            next_line = self._segment_formula(next_point_a, next_point_b)
            if len(self.segments) <= 2:
                intersection_previous = {x: next_.point_a.x, y: next_.point_a.y, }
                intersection_next = {x: next_.point_a.x, y: next_.point_a.y, }
                break
            previous_point_a, previous_point_b = previous.point_a.as_tuple(), previous.point_b.as_tuple()
            previous_line = self._segment_formula(previous_point_a, previous_point_b)

            intersection_previous = solve((new_line, previous_line), (x, y))
            intersection_next = solve((new_line, next_line), (x, y))

            # if new_line is higher than intersection of neighbouring lines our intersection point will be the
            # intersection of neighbours
            if one_time_check:
                if neighbours_cross := solve((previous_line, next_line), (x, y)):
                    one_time_check = False
                    if any([intersection_next[x] <= neighbours_cross[x] <= intersection_previous[x] > previous_point_b[
                        0],
                            intersection_next[x] >= neighbours_cross[x] <= intersection_previous[x] > previous_point_b[
                                0],
                            intersection_previous[x] <= neighbours_cross[x] <= intersection_next[x] < next_point_a[0],
                            intersection_previous[x] >= neighbours_cross[x] <= intersection_next[x] < next_point_a[0],
                            ]):
                        intersection_previous = neighbours_cross
                        intersection_next = neighbours_cross
                        break

            # cut redundant Segment. If there are less than 2 Segments left, we leave only one Segment with one point
            if any([next_point_a[0] < next_point_b[0] <= intersection_next[x],
                    next_point_a[0] > next_point_b[0] >= intersection_next[x],
                    next_point_a[0] == next_point_b[0] and next_point_a[1] > next_point_b[1] >= intersection_next[y],
                    next_point_a[0] == next_point_b[0] and next_point_a[1] < next_point_b[1] <= intersection_next[y],
                    ]):
                self.segments.remove(next_)
                next_ = self._get_next_segment_points()
                continue

            # cut redundant Segment. If there are less than 2 Segments left, we leave only one Segment with one point
            if any([previous_point_b[0] < previous_point_a[0] <= intersection_previous[x],
                    previous_point_b[0] > previous_point_a[0] >= intersection_previous[x],
                    previous_point_b[0] == previous_point_a[0] and
                    previous_point_b[1] > previous_point_a[1] >= intersection_next[y],
                    previous_point_b[0] == previous_point_a[0] and
                    previous_point_b[1] < previous_point_a[1] <= intersection_next[y],
                    ]):
                self.segments.remove(previous)
                if self.index != 0:
                    self.index -= 1
                previous = self._get_previous_segment_points()
                continue

            break
        old_point_a.x, old_point_a.y = round(intersection_previous[x], 3), round(intersection_previous[y], 3)
        old_point_b.x, old_point_b.y = round(intersection_next[x], 3), round(intersection_next[y], 3)

        # Correcting segment data
        self.segments[self.index + 1].point_a = self.segments[self.index].point_b
        self.segments[self.index - 1].point_b = self.segments[self.index].point_a
        self.segments[-1].point_b = self.segments[0].point_a

        # removing duplicates with the ordering of points
        unique_points = set()
        self.points = [point for segment in self.segments for point in [segment.point_a, segment.point_b] if not
        (point.as_tuple() in unique_points or unique_points.add(point.as_tuple()))]
        self.points.append(self.points[0])

    def draw(self):
        x, y = zip(*self.get_point_data())
        plt.plot(x, y, marker='o', linestyle='-', color='b')
        plt.plot([x[-1], x[0]], [y[-1], y[0]], linestyle='-', color='b')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Polygon Plot')
        plt.grid(True)
        plt.show()
