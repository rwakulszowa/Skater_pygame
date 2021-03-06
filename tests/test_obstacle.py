import pygame
from unittest import TestCase

from skater.obstacles import Obstacle
from skater import image, image_paths
from skater.rendering.point import Point
from skater.rendering.shape import Polygon

class TestObstacle(TestCase):
    """
    Base TestCase class -> all tests will share the same setup logic
    """
    def setUp(self):
        """
        This is the code that will get executed before every test.
   
        Resets the state for each test case, which in turn decouples
        tests from each other.
        """
        size = width, height = (1280, 720)
        screen = pygame.display.set_mode(size)  # FIXME: decouple Obstacle from pygame.display
        img = image.Image.load(image_paths.PLAYER_MAIN)  # some image is needed to construct an Obstacle
        self.obstacle = Obstacle(img)
        self.base_rect = self.obstacle.rect

        # Non-overlapping rectangles
        x_offset = self.obstacle.rect.width
        y_offset = self.obstacle.rect.height
        self.rect_above = self.base_rect.shifted(y_shift=-(10 + y_offset))
        self.rect_below = self.base_rect.shifted(y_shift=10 + y_offset)
        self.rect_left = self.base_rect.shifted(x_shift=-(10 + x_offset))
        self.rect_right = self.base_rect.shifted(x_shift=10 + x_offset)

class TestIsUnder(TestObstacle):
    def test_is_under_is_true_for_rect_above(self):
        self.assertTrue(
            self.obstacle.is_under(self.rect_above))

    def test_is_under_is_false_for_rect_below(self):
        self.assertFalse(
            self.obstacle.is_under(self.rect_below))

    def test_is_under_is_false_for_rect_on_the_side(self):
        self.assertFalse(
            self.obstacle.is_under(self.rect_left))

class TestIsOver(TestObstacle):
    def test_is_true_for_rect_below(self):
        self.assertTrue(
            self.obstacle.is_over(self.rect_below))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.obstacle.is_over(self.rect_above))

    def test_is_false_for_rect_on_the_side(self):
        self.assertFalse(
            self.obstacle.is_over(self.rect_left))

class TestIsToTheRight(TestObstacle):
    def test_is_true_for_rect_on_the_left(self):
        self.assertTrue(
            self.obstacle.is_to_the_right(self.rect_left))

    def test_is_false_for_rect_on_the_right(self):
        self.assertFalse(
            self.obstacle.is_to_the_right(self.rect_right))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.obstacle.is_to_the_right(self.rect_above))

    def test_is_false_for_line_in_the_bottom_left_corner(self):
        corner = Point(
            self.obstacle.rect.left,
            self.obstacle.rect.bottom)
        
        # Build a line so that the player is on its edge
        line = Polygon([
            corner + Point(-10, -10),
            corner + Point(10, 10)])

        self.assertFalse(
            self.obstacle.is_to_the_right(line))

class TestIsToTheLeft(TestObstacle):
    def test_is_true_for_rect_on_the_right(self):
        self.assertTrue(
            self.obstacle.is_to_the_left(self.rect_right))

    def test_is_false_for_rect_on_the_left(self):
        self.assertFalse(
            self.obstacle.is_to_the_left(self.rect_left))

    def test_is_false_for_rect_above(self):
        self.assertFalse(
            self.obstacle.is_to_the_left(self.rect_above))