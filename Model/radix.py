from .base import ObservableModel

import numpy as np
from numpy.linalg import matrix_power, norm
from smithnormalform import matrix, snfproblem, z
from itertools import product
import math


class RadixSystem(ObservableModel):
    def __init__(self, matrix=None, digits=None, dimension=None):
        super().__init__()
        self.matrix = matrix if matrix is not None else np.array([])
        self.digits = digits if digits is not None else np.array([])
        self.dimension = dimension if dimension is not None else 0


    def set_U_G(self) -> None:
        ''' Set U and G using smithnormalform package '''
        M = self.convert_from_numpy_array(self.matrix)
        prob = snfproblem.SNFProblem(M)
        prob.computeSNF()
        self.U = self.convert_to_numpy_array(prob.S)
        self.G = self.convert_to_numpy_array(prob.J)
        
    def convert_to_numpy_array(self, M):
        ''' Converts smithnormalform matrix to numpy array '''
        # Extract numerical values from original_matrix's elements
        elements = M.elements
        # Convert elements to a 1D numpy array
        flat_array = np.array([element.a for element in elements])
        # Reshape the 1D array into a 2D numpy array
        return flat_array.reshape((M.h, M.w))

    def convert_from_numpy_array(self, M):
        ''' Converts numpy array to smithnormalform matrix '''
        if not isinstance(M, np.ndarray):
            raise ValueError("Input must be a NumPy array.")
        
        rows, cols = M.shape

        # Convert the NumPy array to the smithnormalform format
        elements = [z.Z(int(x)) for x in M.flatten()]
        formatted_matrix = matrix.Matrix(rows, cols, elements)

        return formatted_matrix
    

    def calculate_determinant_abs(self):
        ''' Calculates the system's base's determinant and returns its absolute value '''
        if self.dimension == 1:
            return self.matrix[0][0]
        
        return round(abs(np.linalg.det(self.matrix)))


    def calculate_ui(self, M, digit):
        ''' Calculates Uz coordinates '''
        multiplied_matrix = np.dot(M, digit)

        if isinstance(multiplied_matrix[0], list):
            return np.diag(multiplied_matrix).round().astype(int)
        else:
            return multiplied_matrix


    def h(self, U, z, G):
        ''' Hash function,
        helps to determine the congruent digit for a given element '''
        # ui - k = U * z
        u = self.calculate_ui(U, z)
        g = np.diag(G).round().astype(int)
        sum = 0
        for i in range(G.shape[0]): 
            curr = 0
            if g[i] != 1: 
                curr += (u[i] % g[i]) 
                for j in range(i-1):
                    curr *= g[j]
            sum += curr
        return int(sum)
    

    def check_crs(self):
        ''' Check the hash value for every digits '''
        hash_values = set()
        for d in self.digits:
            if self.h(self.U, d, self.G) in hash_values:
                return False
            hash_values.add(self.h(self.U, d, self.G))

        return True
    

    def phi_n_z(self, z):
        ''' Calculates Phi function '''
        d = z
        for digit in self.digits:
            if self.h(self.U, z, self.G) == self.h(self.U, digit, self.G):
                d = digit
                break
        
        return (np.dot(np.linalg.inv(self.matrix), (z-d)).round()).astype(int)
    

    def phi_n_recursion(self, z) -> None:
        ''' Calculate orbit for z '''
        if not hasattr(self, 'orbit'):
            self.orbit = []

        self.z = z
        # Storing the orbit 
        for o in self.orbit:
            if np.all(o == self.z):
                self.orbit.append(self.z)
                return

        if np.all(self.z == 0):
            self.orbit.append(self.z)
            self.orbit.append(self.z)
            return
        elif np.all(self.z == self.phi_n_z(z)):
            self.orbit.append(self.z)
            self.orbit.append(self.z)
            return
        else:
            self.orbit.append(self.z)
            self.z = self.phi_n_z(z)
            return self.phi_n_recursion(self.z)
        
 
    def mpl(self):
        ''' Setting the value of li and ui '''
        c = 1
        while not norm(matrix_power(self.matrix, -c), np.inf) < 0.01:
            c += 1
        
        gamma = 1/(1 - norm(matrix_power(self.matrix, -c), np.inf))

        dimensions = (self.digits.shape[0], self.dimension) 
        li = np.zeros(self.dimension)
        ui = np.zeros(self.dimension)
        temp = np.zeros(dimensions)
        for i in range(1, c):
            temp = np.zeros(dimensions)
            for j in range(1, dimensions[0]):
                temp[j] = np.dot(matrix_power(self.matrix, -i), self.digits[j])
            li += np.min(temp, axis=0)
            ui += np.max(temp,axis=0)
        
        solution = np.array(np.dot(np.floor(gamma * li), -1)), np.dot(np.ceil(gamma * ui), -1)
        self.li = solution[0].round().astype(int)
        self.ui = solution[1].round().astype(int)

        return solution
    

    def set_H(self, current_digit_index, max_depth) -> None:
        ''' Creating the -H set by setting the H_x and H_y coordinates '''
        if not hasattr(self, 'H_x'):
            self.H_x = []
            self.H_y = []

        self.H_x.clear()
        self.H_y.clear()

        stack = []
        result_stack = []
        current_result = np.zeros(2)
        stack.append((current_digit_index, current_result))

        while stack:
            current_digit_index, current_result = stack.pop()
            
            if current_digit_index == max_depth:
                current_result = np.dot(current_result, -1)
                self.H_x.append(current_result[0])
                self.H_y.append(current_result[1])
            else:
                for d in self.digits:
                    next_matrix_power = matrix_power(self.matrix, -1 * (current_digit_index + 1))
                    next_result = np.dot(next_matrix_power, d) + current_result
                    result_stack.append((current_digit_index + 1, next_result))

            while result_stack:
                stack.append(result_stack.pop())

    
    def count_on_every_lattice_points(self):
        ''' Helper function for finding every lattice points in coverbox '''
        current_ind = 0
        coordinates = []
        while current_ind < len(self.li):
            temp = []
            for x in range(int(self.ui[current_ind]), int(self.li[current_ind]) + 1):
                temp.append(x)
            coordinates.append(temp)
            current_ind += 1
        
        return coordinates


    def get_cycle(self, z, orbit):
        ''' Finding the repeating elements when calculating orbit '''

        # Storing the orbit 
        for i in range(len(orbit)):
            if np.all(orbit[i] == z):
                return orbit[i:len(orbit)]

        if np.all(z == 0):
            orbit.append(z)
            return [np.zeros(self.digits.shape[1], dtype=int) for _ in range(2)]
        elif np.all(z == self.phi_n_z(z)):
            orbit.append(z)
            return [z, z]
        else:
            orbit.append(z)
            z = self.phi_n_z(z)
            return self.get_cycle(z, orbit)


    def find_periodic_points(self) -> None:
        " Finding the periodic points of the system"
        self.mpl()
        periodic_points_set = set()
        coordinates = self.count_on_every_lattice_points()

        # Finding the lattice points within the coverbox
        combinations = list(product(*coordinates))
        self.lattice_points = combinations

        for i in range(len(combinations)):
            z = np.array(combinations[i])
            orbit = []
            temp = self.get_cycle(z, orbit)

            for arr in temp:
                tuple_arr = tuple(arr)
                if tuple_arr not in periodic_points_set:
                    periodic_points_set.add(tuple_arr)

        self.periodic_points = periodic_points_set


    def classify(self) -> None:
        ''' Calculating the classification of the system '''
        periodic_points_set = set()
        classification = []

        for i in range(len(self.lattice_points)):
            z = np.array(self.lattice_points[i])
            orbit = []
            new = False
            temp = self.get_cycle(z, orbit)

            for arr in temp:
                tuple_arr = tuple(arr)
                if tuple_arr not in periodic_points_set:
                    periodic_points_set.add(tuple_arr)
                    new = True
            if new:
                classification.append(temp)

        classified_final = []
        for i in range(len(classification)):
            if tuple(classification[i][0]) in periodic_points_set:
                temp = classification[i]
                if tuple(classification[i][0]) == tuple(classification[i][1]):
                    periodic_points_set.remove(tuple(classification[i][0]))
                    classified_final.append(temp)
                else:
                    for j in range(len(classification[i])):
                        periodic_points_set.remove(tuple(classification[i][j]))
                    temp.append(classification[i][0])
                    classified_final.append(temp)

        self.classification = classified_final


    def canonical_digits(self, num) -> None:
        ''' Setting the system's digit set to canonical '''

        # Create arrays of different dimensions based on the 'dimension' parameter
        if self.dimension == 1:
            result_array = np.arange(num).reshape((num, 1))

        else:
            result_array = np.zeros((num, self.dimension))
            result_array[:, 0] = np.arange(num)
            for i in range(1, self.dimension):
                result_array[:, i] = 0
        
        self.digits = result_array

    
    def canonical_j_digits(self, num, nonzero_index) -> None:
        ''' Setting the system's digit set to j-canonical '''

        # Create arrays of different dimensions based on the 'dimension' parameter
        if self.dimension == 1:
            result_array = np.arange(num).reshape((num, 1))

        else:
            result_array = np.zeros((int(num), self.dimension))
            result_array[:, nonzero_index] = np.arange(num)
            
        self.digits = result_array



    def custom_arange(self, start, stop):
        ''' Helper function of symmetric and j-symmetric '''

        # Calculating the number of elements in the array
        num_elements = max(0, int(stop - start))

        # Creating an empty list to store the generated values
        result = []
        current = start

        # Generating the array values
        for _ in range(num_elements):
            result.append(current)
            current += 1

        return result

    
    def symmetric(self, num) -> None:
        ''' Setting the system's digit set to symmetrical '''
        result_array = np.zeros((num, self.dimension))
        result_array[:, 0] = self.custom_arange(int(math.floor(-0.5*num)+1), int(math.floor(0.5*num)+1))
        for i in range(1, self.dimension):
            result_array[:, i] = int(0)
        
        self.digits = result_array

    def symmetric_j(self, num, nonzero_index) -> None:
        ''' Setting the system's digit set to j-symmetrical '''
        result_array = np.zeros((num, self.dimension))
        result_array[:, nonzero_index] = self.custom_arange(int(math.floor(-0.5*num)+1), int(math.floor(0.5*num)+1))
        
        self.digits = result_array


    def expansive_matrix(self):
        ''' Check if the base matrix is expansive '''
        if self.dimension == 0:
            return False
        
        return np.all(np.abs(np.linalg.eigvals(self.matrix)) > 1)


    def determinant_check(self):
        ''' Check if det (I - M ) ̸ = ±1 '''
        if self.dimension == 1:
            return True

        # Create identity matrix
        identity_matrix = np.identity(self.dimension)

        # Compute determinant of (I - matrix)
        determinant = np.linalg.det(identity_matrix - self.matrix)

        # Check if determinant is not +1 or -1
        return abs(determinant) != 1


    def is_not_GNS(self):
        ''' Check if the given system is number system '''
        if self.check_crs() and self.expansive_matrix() and self.determinant_check():
            if self.dimension == 1:
                if self.matrix[0][0] == len(self.digits):
                    return False
                else:
                    return True

            self.find_periodic_points()

            zeros_tuple = tuple(0 for _ in range(self.dimension))

            if zeros_tuple in self.periodic_points:
                return False
            else:
                return True
        
        else:
            return True

        
    def find_signature(self) -> None:
        ''' Finding the signature of the system '''
        if not hasattr(self, 'lattice_points'):
            self.lattice_points = []

        max_sig = 0
        if len(self.lattice_points) == 0:
            self.find_periodic_points()
            
        self.classify()
        for i in range(len(self.classification)):
            if len(self.classification[i])-1 > max_sig:
                max_sig = len(self.classification[i])-1

        sig = [0] * (max_sig)
        for i in range(len(self.classification)):
            sig[len(self.classification[i])-2] += 1

        self.signature = sig