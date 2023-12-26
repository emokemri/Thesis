import numpy as np
import unittest
from smithnormalform import matrix, z
import sys
import os

def add_subdirectories_to_sys_path(source_directory=os.path.abspath(os.path.join(os.path.dirname(__file__)
, '..', '..'))):
    for root, dirs, files in os.walk(source_directory):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            if "__pycache__" not in directory_path:
                sys.path.append(directory_path)

add_subdirectories_to_sys_path()

from Model.radix import RadixSystem
from Model.model import Model


class Test(unittest.TestCase):
    def test_convert_to_numpy_array(self):
        self.model = Model()
        _matrix = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])
        np.testing.assert_array_equal(self.model.radix.convert_to_numpy_array(_matrix), np.array([[1, 2], [3, 4]]))

        _matrix = matrix.Matrix(2, 2, [z.Z(2), z.Z(-1), z.Z(1), z.Z(2)])
        np.testing.assert_array_equal(self.model.radix.convert_to_numpy_array(_matrix), np.array([[2, -1], [1, 2]]))

        _matrix = matrix.Matrix(2, 2, [z.Z(1), z.Z(-2), z.Z(1), z.Z(1)])
        np.testing.assert_array_equal(self.model.radix.convert_to_numpy_array(_matrix), np.array([[1, -2], [1, 1]]))

        _matrix = matrix.Matrix(1, 1, [z.Z(3)])
        np.testing.assert_array_equal(self.model.radix.convert_to_numpy_array(_matrix), np.array([[3]]))

        _matrix = matrix.Matrix(4, 4, [z.Z(0), z.Z(0), z.Z(0), z.Z(-15), z.Z(1), z.Z(0), z.Z(0), z.Z(-1),
                                       z.Z(0), z.Z(1), z.Z(0), z.Z(-2), z.Z(0), z.Z(0), z.Z(1), z.Z(-3)])
        expected_result = np.array([[0, 0, 0, -15], [1, 0, 0, -1], [0, 1, 0, -2], [0, 0, 1, -3]])
        np.testing.assert_array_equal(self.model.radix.convert_to_numpy_array(_matrix), expected_result)


    def test_convert_from_numpy_array(self):
        self.model = Model()
        _matrix = np.array([[1, -2], [1, 1]])
        np.testing.assert_array_equal(self.model.radix.convert_from_numpy_array(_matrix), matrix.Matrix(2, 2, [z.Z(1), z.Z(-2), z.Z(1), z.Z(1)]))

        _matrix = np.array([[3]])
        np.testing.assert_array_equal(self.model.radix.convert_from_numpy_array(_matrix), matrix.Matrix(1, 1, [z.Z(3)]))

        _matrix = np.array([[0, 0, 0, -15], [1, 0, 0, -1], [0, 1, 0, -2], [0, 0, 1, -3]]) 
        expected_result = matrix.Matrix(4, 4, [z.Z(0), z.Z(0), z.Z(0), z.Z(-15), z.Z(1), z.Z(0), z.Z(0), z.Z(-1),
                                               z.Z(0), z.Z(1), z.Z(0), z.Z(-2), z.Z(0), z.Z(0), z.Z(1), z.Z(-3)])
        np.testing.assert_array_equal(self.model.radix.convert_from_numpy_array(_matrix), expected_result)


    def test_calculate_determinant_abs(self):
        radix1 = RadixSystem()
        radix1.matrix = np.array([[1]])
        self.assertEqual(radix1.calculate_determinant_abs(), 1)

        radix2 = RadixSystem()
        radix2.matrix = np.array([[-1]])
        self.assertEqual(radix2.calculate_determinant_abs(), 1)

        radix3 = RadixSystem()
        radix3.matrix = np.array([[1, 2], [3, 4]])
        self.assertEqual(radix3.calculate_determinant_abs(), 2)


    def test_calculate_ui(self):
        self.model = Model()
        _matrix = np.array([[1, 2], [3, 4]])
        _digit = np.array([1, 2])
        np.testing.assert_array_equal(self.model.radix.calculate_ui(_matrix, _digit), np.array([5, 11]))

        _matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        _digit = np.array([1, 1, 1])
        np.testing.assert_array_equal(self.model.radix.calculate_ui(_matrix, _digit), np.array([6, 15, 24]))


    def test_h(self):
        radix1 = RadixSystem()
        U = np.array([[1, 2], [3, 4]])
        z = np.array([2, 3])
        G = np.array([[1, 0], [0, 1]])
        self.assertEqual(radix1.h(U, z, G), 0)

        radix2 = RadixSystem(np.array([[2, -1], [1, 2]]), np.array([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]]), 2)
        radix2.set_U_G()
        value1 = radix2.h(radix2.U, radix2.digits[0], radix2.G)
        self.assertEqual(radix2.h(radix2.U, radix2.digits[0], radix2.G), 0)

        radix2.matrix = radix2.matrix * 2
        radix2.set_U_G()
        value2 = radix2.h(radix2.U, radix2.digits[0], radix2.G)
        self.assertEqual(value1, value2)

        radix2.matrix = radix2.matrix * 3
        radix2.set_U_G()
        value3 = radix2.h(radix2.U, radix2.digits[0], radix2.G)
        self.assertEqual(value1, value3)


    def test_check_crs(self):
        _matrix = np.array([[2, -1], [1, 2]])
        _digits = np.array([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]])
        self.radix1 = RadixSystem(_matrix, _digits, 2)
        self.radix1.set_U_G()
        self.assertTrue(self.radix1.check_crs())

        _matrix = np.array([[3]])
        _digits = np.array([[-2], [0], [2]])
        self.radix2 = RadixSystem(_matrix, _digits, 1)
        self.radix2.set_U_G()
        self.assertTrue(self.radix2.check_crs())

        _matrix = np.array([[0, 2], [1, 0]])
        _digits = np.array([[0, 1], [0, 1]])
        self.radix3 = RadixSystem(_matrix, _digits, 2)
        self.radix3.set_U_G()
        self.assertFalse(self.radix3.check_crs())


    def test_phi_n_z(self):
        _matrix = np.array([[2, -1], [1, 2]])
        _digits = np.array([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]])
        self.radix1 = RadixSystem(_matrix, _digits, 2)
        self.radix1.set_U_G()

        np.testing.assert_array_equal(self.radix1.phi_n_z(np.array([-6, 5])), np.array([0, 0]))
        np.testing.assert_array_equal(self.radix1.phi_n_z(np.array([-6, 4])), np.array([-2, 3]))
        np.testing.assert_array_equal(self.radix1.phi_n_z(np.array([-6, 3])), np.array([-2, 2]))

        _matrix = np.array([[1, -2], [1, 1]])
        _digits = np.array([[0, 0], [1, 0], [-1, 0]])
        self.radix2 = RadixSystem(_matrix, _digits, 2)
        self.radix2.set_U_G()

        np.testing.assert_array_equal(self.radix2.phi_n_z(np.array([3, 2])), np.array([2, 0]))
        np.testing.assert_array_equal(self.radix2.phi_n_z(np.array([1, 3])), np.array([2, 1]))
        np.testing.assert_array_equal(self.radix2.phi_n_z(np.array([4, 3])), np.array([3, 0]))

        _matrix = np.array([[3]])
        _digits = np.array([[-2], [0], [2]])
        self.radix3 = RadixSystem(_matrix, _digits, 1)
        self.radix3.set_U_G()

        np.testing.assert_array_equal(self.radix3.phi_n_z(np.array([1])), np.array([1]))
        np.testing.assert_array_equal(self.radix3.phi_n_z(np.array([0])), np.array([0]))


    def test_phi_n_recursion(self):
        _matrix = np.array([[2, -1], [1, 2]])
        _digits = np.array([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]])
        self.radix1 = RadixSystem(_matrix, _digits, 2)
        self.radix1.set_U_G()

        self.radix1.phi_n_recursion(np.array([-6, 3]))
        np.testing.assert_array_equal(self.radix1.orbit, [[-6, 3], [-2, 2], [1, -2], [0, -1], [0, 0], [0, 0]])

        self.radix1.orbit.clear()
        self.radix1.phi_n_recursion(np.array([-2, 2]))
        np.testing.assert_array_equal(self.radix1.orbit, [[-2, 2], [1, -2], [0, -1], [0, 0], [0, 0]])

        _matrix = np.array([[3]])
        _digits = np.array([[-2], [0], [2]])
        self.radix2 = RadixSystem(_matrix, _digits, 1)
        self.radix2.set_U_G()

        self.radix2.phi_n_recursion(np.array([3]))
        np.testing.assert_array_equal(self.radix2.orbit, [[3], [1], [1]])

        self.radix2.orbit.clear()
        self.radix2.phi_n_recursion(np.array([7]))
        np.testing.assert_array_equal(self.radix2.orbit, [[7], [3], [1], [1]])


    def test_mpl(self):
        _matrix = np.array([[2, -1], [1, 2]])
        _digits = np.array([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]])
        self.radix1 = RadixSystem(_matrix, _digits, 2)
        self.radix1.set_U_G()
        self.radix1.mpl()

        np.testing.assert_array_equal(self.radix1.ui, [-2, -6])
        np.testing.assert_array_equal(self.radix1.li, [2, 1])

        _matrix = np.array([[1, -2], [1, 1]])
        _digits = np.array([[0, 0], [1, 0], [-1, 0]])
        self.radix2 = RadixSystem(_matrix, _digits, 2)
        self.radix2.set_U_G()
        self.radix2.mpl()

        np.testing.assert_array_equal(self.radix2.ui, [-1, -1])
        np.testing.assert_array_equal(self.radix2.li, [1, 1])

        _matrix = np.array([[1,1,-1,0], [-1, 0, 1, 1], [1, 0, -1, 1], [-1, 0, 0, 0]])
        _digits = np.array([[0, 0, 0, 0], [1, 0, 0, 0]])
        self.radix3 = RadixSystem(_matrix, _digits, 4)
        self.radix3.set_U_G()
        self.radix3.mpl()

        np.testing.assert_array_equal(self.radix3.ui, [-2, -3, -2, -2])
        np.testing.assert_array_equal(self.radix3.li, [2, 2, 2, 2])


    def test_set_H(self):
        _matrix = np.array([[2, 1], [1, 2]]) 
        _digits = np.array([[1, 2], [3, 4]])  
        radix1 = RadixSystem(_matrix, _digits, 2)
        radix1.set_H(0, 3)

        self.assertEqual(len(radix1.H_x), 8)
        self.assertEqual(len(radix1.H_y), 8)

        radix1.set_H(0, 4)
        self.assertEqual(len(radix1.H_x), 16)
        self.assertEqual(len(radix1.H_y), 16)

        radix1.set_H(0, 5)
        self.assertEqual(len(radix1.H_x), 32)
        self.assertEqual(len(radix1.H_y), 32)

        radix1.set_H(0, 6)
        self.assertEqual(len(radix1.H_x), 64)
        self.assertEqual(len(radix1.H_y), 64)

        radix1.set_H(0, 7)
        self.assertEqual(len(radix1.H_x), 128)
        self.assertEqual(len(radix1.H_y), 128)

        radix1.set_H(0, 8)
        self.assertEqual(len(radix1.H_x), 256)
        self.assertEqual(len(radix1.H_y), 256)

        radix1.set_H(0, 9)
        self.assertEqual(len(radix1.H_x), 512)
        self.assertEqual(len(radix1.H_y), 512)

        radix1.set_H(0, 10)
        self.assertEqual(len(radix1.H_x), 1024)
        self.assertEqual(len(radix1.H_y), 1024)

        model = Model()
        _matrix = np.array([[1, 2], [3, 8]]) 
        model.radix.dimension = 2
        model.radix.canonical_digits(10)
        model.radix.matrix = _matrix
        model.radix.set_H(0, 3)

        self.assertEqual(len(model.radix.H_x), 1000)
        self.assertEqual(len(model.radix.H_y), 1000)

        model.radix.set_H(0, 4)
        self.assertEqual(len(model.radix.H_x), 10000)
        self.assertEqual(len(model.radix.H_y), 10000)

        model.radix.set_H(0, 5)
        self.assertEqual(len(model.radix.H_x), 100000)
        self.assertEqual(len(model.radix.H_y), 100000)

        #TOO HIGH!!!
        #model.radix.set_H(0, 6)
        #self.assertEqual(len(model.radix.H_x), 1000000)
        #self.assertEqual(len(model.radix.H_y), 1000000)


    def test_count_on_every_lattice_points(self):
        radix1 = RadixSystem()
        radix1.li = [4, 6]
        radix1.ui = [1, 2]
        self.assertEqual(radix1.count_on_every_lattice_points(), [[1, 2, 3, 4], [2, 3, 4, 5, 6]])

        radix2 = RadixSystem()
        radix2.li = [3, 5]
        radix2.ui = [0, 1]
        self.assertEqual(radix2.count_on_every_lattice_points(), [[0, 1, 2, 3], [1, 2, 3, 4, 5]])

        radix3 = RadixSystem()
        radix3.li = [2, 2, 2, 2]
        radix3.ui = [-2, -3, -2, -2]
        expected_result = [[-2, -1, 0, 1, 2], [-3, -2, -1, 0, 1, 2], [-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2]]
        self.assertEqual(radix3.count_on_every_lattice_points(), expected_result)


    def test_get_cycle(self):
        _matrix = np.array([[2, -1], [1, 2]])
        _digits = np.array([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]])
        radix1 = RadixSystem(_matrix, _digits, 2)
        radix1.set_U_G()

        np.testing.assert_array_equal(radix1.get_cycle([-6, 3], []), [[0, 0], [0, 0]])
        np.testing.assert_array_equal(radix1.get_cycle([-2, 2], []), [[0, 0], [0, 0]])

        radix2 = RadixSystem()
        _matrix = np.array([[0, 2], [1, 0]])
        radix2.dimension = 2
        radix2.canonical_digits(2)
        radix2.matrix = _matrix
        radix2.set_U_G()

        np.testing.assert_array_equal(radix2.get_cycle([-1, 0], []), [[-1, 0], [0, -1]])
        np.testing.assert_array_equal(radix2.get_cycle([0, -1], []), [[0, -1], [-1, 0]])

        _matrix = np.array([[3]])
        _digits = np.array([[-2], [0], [2]])
        radix3 = RadixSystem(_matrix, _digits, 1)
        radix3.set_U_G()

        np.testing.assert_array_equal(radix3.get_cycle([3], []), [[1], [1]])
        np.testing.assert_array_equal(radix3.get_cycle([7], []), [[1], [1]])


    def test_find_periodic_points(self):
        radix1 = RadixSystem()
        _matrix = np.array([[3, 2], [1, 3]])
        radix1.dimension = 2
        radix1.canonical_digits(7)
        radix1.matrix = _matrix
        radix1.set_U_G()
        radix1.find_periodic_points()
        np.testing.assert_array_equal(radix1.periodic_points, {(-6, 3), (-4, 2), (-2, 1), (0, 0)})

        radix2 = RadixSystem()
        _matrix = np.array([[9, 10], [5, 9]])
        radix2.dimension = 2
        radix2.canonical_digits(31)
        radix2.matrix = _matrix
        radix2.set_U_G()
        radix2.find_periodic_points()
        expected_result = {(-16, 10), (-13, 8), (-11, 7), (-10, 6), (-8, 5), (-6, 4), (-5, 3), (-3, 2), (0, 0)}
        np.testing.assert_array_equal(radix2.periodic_points, expected_result)

        _matrix = np.array([[1, 1, -1, 0], [-1, 0, 1, 1], [1, 0, -1, 1], [-1, 0, 0, 0]])
        _digits = np.array([[0, 0, 0, 0], [0, 1, 0, 0]])
        radix3 = RadixSystem(_matrix, _digits, 4)
        radix3.set_U_G()
        radix3.find_periodic_points()
        expected_result = {(0, 0, 0, 0),
                           (0, 1, 0, 1), (-1, 0, -1, 0), (0, -1, 0, -1), (1, -1, 0, -1), (1, 0, 0, -1), (1, 1, 1, 0),
                           (1, 0, 1, 0), (0, 0, -1, 0), (0, 0, 0, -1)}
        
        np.testing.assert_array_equal(radix3.periodic_points, expected_result)


    def test_classify(self):
        radix1 = RadixSystem()
        _matrix = np.array([[9, 10], [5, 9]])
        radix1.dimension = 2
        radix1.canonical_digits(31)
        radix1.matrix = _matrix
        radix1.set_U_G()
        radix1.find_periodic_points()
        radix1.classify()

        # Convert NumPy arrays to tuples and then to a set
        temp = {tuple(map(tuple, sublist)) for sublist in radix1.classification}
        # Create a new set by converting the inner sets into frozensets
        result_set = {frozenset(inner_set) for inner_set in temp}
        expected = [[np.array([0, 0]), np.array([0, 0])],
                    [np.array([-8,  5]), np.array([-8,  5])],
                    [np.array([-6,  4]), np.array([-10,   6]), np.array([-6,  4])],
                    [np.array([-11,   7]), np.array([-13,   8]), np.array([-11,   7])],
                    [np.array([-16,  10]), np.array([-16,  10])],
                    [np.array([-5,  3]), np.array([-3,  2]), np.array([-5,  3])]]
        temp = {tuple(map(tuple, sublist)) for sublist in expected}
        expected_set = {frozenset(inner_set) for inner_set in temp}
        
        np.testing.assert_array_equal(result_set, expected_set)

        radix2 = RadixSystem()
        radix2.matrix = np.array([[1, 1, -1, 0], [-1, 0, 1, 1], [1, 0, -1, 1], [-1, 0, 0, 0]])
        radix2.dimension = 4
        radix2.digits = np.array([[0, 0, 0, 0], [0, 1, 0, 0]])
        radix2.set_U_G()
        radix2.find_periodic_points()
        radix2.classify()
        
        temp = {tuple(map(tuple, sublist)) for sublist in radix2.classification}
        result_set = {frozenset(inner_set) for inner_set in temp}
        expected = [[np.array([0, 0, 0, 0]), np.array([0, 0, 0, 0])],
                    [np.array([1, 1, 1, 0]), np.array([0, 1, 0, 1]), np.array([-1, 0, -1, 0]), np.array([0, -1, 0, -1]), np.array([1, -1, 0, -1]), np.array([1, 0, 0, -1]), np.array([1, 1, 1, 0])],
                    [np.array([0, 0, 0, -1]), np.array([1, 0, 1, 0]), np.array([0, 0, -1, 0]), np.array([0, 0, 0, -1])]]
        temp = {tuple(map(tuple, sublist)) for sublist in expected}
        expected_set = {frozenset(inner_set) for inner_set in temp}
        
        np.testing.assert_array_equal(result_set, expected_set)


    def test_canonical_digits(self):
        radix1 = RadixSystem()
        radix1.dimension = 1
        radix1.canonical_digits(1)
        np.testing.assert_array_equal(radix1.digits, np.array([[0]]))

        radix1.canonical_digits(2)
        np.testing.assert_array_equal(radix1.digits, np.array([[0], [1]]))

        radix2 = RadixSystem()
        radix2.dimension = 2
        radix2.canonical_digits(1)
        np.testing.assert_array_equal(radix2.digits, np.array([[0, 0]]))

        radix2.canonical_digits(2)
        np.testing.assert_array_equal(radix2.digits, np.array([[0, 0], [1, 0]]))

        radix3 = RadixSystem()
        radix3.dimension = 3
        radix3.canonical_digits(1)
        np.testing.assert_array_equal(radix3.digits, np.array([[0, 0, 0]]))

        radix3.canonical_digits(2)
        np.testing.assert_array_equal(radix3.digits, np.array([[0, 0, 0], [1, 0, 0]]))


    def test_canonical_j_digits(self):
        radix1 = RadixSystem()
        radix1.dimension = 1
        radix1.canonical_j_digits(1, 0)
        np.testing.assert_array_equal(radix1.digits, np.array([[0]]))

        radix1.canonical_j_digits(2, 0)
        np.testing.assert_array_equal(radix1.digits, np.array([[0], [1]]))

        radix2 = RadixSystem()
        radix2.dimension = 2
        radix2.canonical_j_digits(1, 1)
        np.testing.assert_array_equal(radix2.digits, np.array([[0, 0]]))

        radix2.canonical_j_digits(2, 1)
        np.testing.assert_array_equal(radix2.digits, np.array([[0, 0], [0, 1]]))

        radix3 = RadixSystem()
        radix3.dimension = 3
        radix3.canonical_j_digits(1, 0)
        np.testing.assert_array_equal(radix3.digits, np.array([[0, 0, 0]]))

        radix3.canonical_j_digits(2, 2)
        np.testing.assert_array_equal(radix3.digits, np.array([[0, 0, 0], [0, 0, 1]]))


    def test_custom_arange(self):
        radix = RadixSystem()
        start = 2
        stop = 5
        expected_result = [2, 3, 4]
        result = radix.custom_arange(start, stop)
        self.assertEqual(result, expected_result)

        start = -3
        stop = 2
        expected_result = [-3, -2, -1, 0, 1]
        result = radix.custom_arange(start, stop)
        self.assertEqual(result, expected_result)

        start = 5
        stop = 2
        expected_result = []
        result = radix.custom_arange(start, stop)
        self.assertEqual(result, expected_result)

    
    def test_symmetric(self):
        radix1 = RadixSystem()
        radix1.dimension = 1
        radix1.symmetric(1)
        np.testing.assert_array_equal(radix1.digits, np.array([[0]]))

        radix1.symmetric(3)
        np.testing.assert_array_equal(radix1.digits, np.array([[-1], [0], [1]]))

        radix2 = RadixSystem()
        radix2.dimension = 2
        radix2.symmetric(1)
        np.testing.assert_array_equal(radix2.digits, np.array([[0, 0]]))

        radix2.symmetric(4)
        np.testing.assert_array_equal(radix2.digits, np.array([[-1, 0], [0, 0], [1, 0], [2, 0]]))

        radix3 = RadixSystem()
        radix3.dimension = 3
        radix3.symmetric(1)
        np.testing.assert_array_equal(radix3.digits, np.array([[0, 0, 0]]))

        radix3.symmetric(2)
        np.testing.assert_array_equal(radix3.digits, np.array([[0, 0, 0], [1, 0, 0]]))


    def test_symmetric_j(self):
        radix1 = RadixSystem()
        radix1.dimension = 1
        radix1.symmetric_j(1, 0)
        np.testing.assert_array_equal(radix1.digits, np.array([[0]]))

        radix1.symmetric_j(3, 0)
        np.testing.assert_array_equal(radix1.digits, np.array([[-1], [0], [1]]))

        radix2 = RadixSystem()
        radix2.dimension = 2
        radix2.symmetric_j(1, 0)
        np.testing.assert_array_equal(radix2.digits, np.array([[0, 0]]))

        radix2.symmetric_j(4, 1)
        np.testing.assert_array_equal(radix2.digits, np.array([[0, -1], [0, 0], [0, 1], [0, 2]]))

        radix3 = RadixSystem()
        radix3.dimension = 3
        radix3.symmetric_j(1, 2)
        np.testing.assert_array_equal(radix3.digits, np.array([[0, 0, 0]]))

        radix3.symmetric_j(2, 2)
        np.testing.assert_array_equal(radix3.digits, np.array([[0, 0, 0], [0, 0, 1]]))


    def test_expansive_matrix(self):
        self.radix1 = RadixSystem()
        self.radix1.dimension = 1
        self.radix1.matrix = np.array([[3]])
        self.assertTrue(self.radix1.expansive_matrix())

        self.radix2 = RadixSystem()
        self.radix2.dimension = 2
        self.radix2.matrix = np.array([[-3, 1], [1, -2]])
        self.assertTrue(self.radix2.expansive_matrix())

        self.radix3 = RadixSystem()
        self.radix3.dimension = 3
        self.radix3.matrix = np.array([[0, 2, 1], [1, 0, 3], [1, 2, 1]])
        self.assertFalse(self.radix3.expansive_matrix())


    def test_determinant_check(self):
        self.radix1 = RadixSystem()
        self.radix1.dimension = 1
        self.radix1.matrix = np.array([[3]])
        self.assertTrue(self.radix1.determinant_check())

        self.radix2 = RadixSystem()
        self.radix2.dimension = 2
        self.radix2.matrix = np.array([[-3, 1], [1, -2]])
        self.assertTrue(self.radix2.determinant_check())

        self.radix3 = RadixSystem()
        self.radix3.dimension = 3
        self.radix3.matrix = np.array([[0, 2, 1], [1, 0, 3], [1, 2, 1]])
        self.assertTrue(self.radix3.determinant_check())


    def test_is_not_GNS(self):
        _matrix = np.array([[3]])
        _digits = np.array([[-2], [0], [2]])
        self.radix1 = RadixSystem(_matrix, _digits, 1)
        self.radix1.set_U_G()
        self.assertFalse(self.radix1.is_not_GNS())

        _matrix = np.array([[0, 2], [1, 0]])
        self.radix2 = RadixSystem()
        self.radix2.matrix = _matrix
        self.radix2.dimension = 2
        self.radix2.canonical_digits(2)
        self.radix2.set_U_G()
        self.assertTrue(self.radix2.is_not_GNS())

        _matrix = np.array([[20, 463], [1, 21]])
        self.radix3 = RadixSystem()
        self.radix3.matrix = _matrix
        self.radix3.dimension = 2
        self.radix3.canonical_digits(2)
        self.radix3.set_U_G()
        self.assertFalse(self.radix3.is_not_GNS())


    def test_find_signature(self):
        _matrix = np.array([[9, 10], [5, 9]])
        radix1 = RadixSystem()
        radix1.matrix = _matrix
        radix1.dimension = 2
        radix1.canonical_digits(31)
        radix1.set_U_G()
        radix1.find_signature()
        np.testing.assert_array_equal(radix1.signature, [3, 3])

        _matrix = np.array([[1, 1, -1, 0], [-1, 0, 1, 1], [1, 0, -1, 1], [-1, 0, 0, 0]])
        _digits = np.array([[0, 0, 0, 0], [0, 1, 0, 0]])
        radix2 = RadixSystem(_matrix, _digits, 4)
        radix2.set_U_G()
        radix2.find_signature()
        np.testing.assert_array_equal(radix2.signature, [1, 0, 1, 0, 0, 1])

        radix3 = RadixSystem()
        _matrix = np.array([[3, 2], [1, 3]])
        radix3.dimension = 2
        radix3.canonical_digits(7)
        radix3.matrix = _matrix
        radix3.set_U_G()
        radix3.find_signature()
        np.testing.assert_array_equal(radix3.signature, [4])


if __name__ == '__main__':
    unittest.main(exit=False)
