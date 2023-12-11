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
    __slots__ = ('points', 'segments', 'neighbor_correction', 'neighbor_correction2')

    def __init__(self, points_lst):
        self.points = [Point(px, py) for px, py in points_lst]

        if self.points[0].x != self.points[-1].x and self.points[0].y != self.points[-1].y:
            raise ValueError("Invalid Polygon values. First point must be the same as last.")
        else:
            self.points[-1] = self.points[0]

        self.segments = self._make_segments()
        self.neighbor_correction = 0
        self.neighbor_correction2 = 0

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

    @staticmethod
    def _check_if_broken(previous_position, current_position, border_position):
        if any([previous_position[1] > current_position[1] < border_position[1],
                previous_position[0] > current_position[0] < border_position[0]]):
            return True

    def _get_next_segment_points(self, index):
        if index == 0:
            next = self.segments[1 + self.neighbor_correction]
        elif index == len(self.segments) - 1:
            next = self.segments[0 + self.neighbor_correction]
        else:
            next = self.segments[index + 1 + self.neighbor_correction]
        return next.point_a.as_tuple(), next.point_b.as_tuple()

    def _get_previous_segment_points(self, index):
        if index == 0:
            previous = self.segments[len(self.segments) - 1 - self.neighbor_correction2]
        elif index == len(self.segments) - 1:
            previous = self.segments[index - 1 - self.neighbor_correction2]
        else:
            previous = self.segments[index - 1 - self.neighbor_correction2]
        return previous.point_a.as_tuple(), previous.point_b.as_tuple()

    @staticmethod
    def offset_of_points_along_the_coordinate_axis(new_point_a, new_point_b, offset_value):
        if new_point_a.y == new_point_b.y:
            new_point_a.y += offset_value  # parallel to x
            new_point_b.y += offset_value
        else:
            new_point_a.x += offset_value  # parallel to y
            new_point_b.x += offset_value

    def segment_offset(self, index, offset_value):

        old_point_a, old_point_b = self.segments[index].point_a, self.segments[index].point_b

        next_point_a, next_point_b = self._get_next_segment_points(index)
        previous_point_a, previous_point_b = self._get_previous_segment_points(index)

        new_point_a, new_point_b = Point(*old_point_a.as_tuple()), Point(*old_point_b.as_tuple())
        self.offset_of_points_along_the_coordinate_axis(new_point_a, new_point_b, offset_value)

        # TODO self.offset_of_points_parallel_to_the_segment(new_point_a, new_point_b, offset_value)

        new_line = self._segment_formula(new_point_a.as_tuple(), new_point_b.as_tuple())

        x, y = symbols('x y')
        intersection_previous = solve((new_line, self._segment_formula(previous_point_a, previous_point_b)), (x, y))
        intersection_next = solve((new_line, self._segment_formula(next_point_a, next_point_b)), (x, y))

        # TODO cut redundant Segment for previous
        # TODO cut redundant Segment for next
        # TODO cut redundant Segment if intersection_next == intersection_previous

        old_point_a.x, old_point_a.y = intersection_previous[x], intersection_previous[y]
        old_point_b.x, old_point_b.y = intersection_next[x], intersection_next[y]
        self.get_point_data()

    def draw(self):
        x, y = zip(*self.get_point_data())
        plt.plot(x, y, marker='o', linestyle='-', color='b')
        plt.plot([x[-1], x[0]], [y[-1], y[0]], linestyle='-', color='b')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Polygon Plot')
        plt.grid(True)
        plt.show()


