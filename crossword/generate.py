from queue import Queue
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, domain in self.domains.items():
            for x in domain.copy():
                if len(x) != variable.length:
                    self.domains[variable].remove(x)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        for wordX in self.domains[x].copy():
            overlap = self.crossword.overlaps[x, y]
            if overlap is not None:
                # find wordY in Ydomain such that wordX[overlap.Xposition] == wordY[overlap.Yposition]
                found = False
                for wordY in self.domains[y]:
                    if len(wordX) > overlap[0] and len(wordY) > overlap[1] and wordX[overlap[0]] == wordY[overlap[1]]:
                        # print(f"Found {wordY} such that wordX[{overlap[0]}] == wordY[{overlap[1]}], {wordX[overlap[0]]} == {wordY[overlap[1]]}, wordX: {wordX}")
                        found = True
                
                if not found:
                    self.domains[x].remove(wordX)
                    revised = True
        
        return revised
                
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            queue = Queue()
            for v1 in self.crossword.variables:
                for v2 in self.crossword.neighbors(v1):
                    if v1 != v2:
                        queue.put((v1, v2))
        else:
            queue = arcs
        
        while not queue.empty():
            X, Y = queue.get()
            if self.revise(X, Y):
                if len(self.domains[X]) == 0:
                    return False
                for Z in self.crossword.neighbors(X):
                    if Z != Y:
                        queue.put((Z, X))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for word in assignment.values():
            if word is None:
                return False
        return True            

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check if complete
        if not self.assignment_complete(assignment):
            return False
        
        # check for duplicates
        if len(assignment.values()) != len(set(assignment.values())):
            # print(f"duplicate")
            return False

        # check correct length
        for var, word in assignment.items():
            if len(word) != var.length:
                # print(f"len(word) != var.length - len({word}) != {var.length}")
                return False
            
        # check conflicts between neighboring variables
        for var1, word1 in assignment.items():
            for var2, word2 in assignment.items():
                if var1 != var2:
                    overlap = self.crossword.overlaps[var1, var2] 
                    if overlap is not None:
                        if word1[overlap[0]] != word2[overlap[1]]:
                            # print(f"word1[overlap[0]] != word2[overlap[1]] - word1[{overlap[0]} != word2[{overlap[1]}]")
                            return False
        
        return True

    def number_of_values_ruled_out_for_neighboring_variables(self, var, selected_value, already_assigned_vars):
        """
        Calculates the number of values ruled out from neighboring variables given that selected_value was chosen for var.
        """
        count = 0
        for nb_var in self.crossword.neighbors(var):
            if nb_var not in already_assigned_vars:
                overlap = self.crossword.overlaps[nb_var, var] 
                for value in self.domains[nb_var]:
                    if overlap is not None:  # value incompatible with selected_value:
                        if value[overlap[0]] != selected_value[overlap[1]]:
                            count += 1
        return count
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        already_assigned_vars = set()
        for variable, value in assignment.items():
            if value != None:
                already_assigned_vars.add(variable)

        domain_values = list(self.domains[var])
        domain_values.sort(key=lambda x: self.number_of_values_ruled_out_for_neighboring_variables(var, x, already_assigned_vars))
        return domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = list()
        for var, word in assignment.items():
            if word is None:
                unassigned.append(var)

        unassigned.sort(key=lambda v: (len(self.domains[v]), -len(self.crossword.neighbors(v))))
        return unassigned[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if len(assignment) == 0:  # initialize assignment with None
            for v in self.crossword.variables:
                assignment[v] = None

        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        ordered = self.order_domain_values(var, assignment)
        for value in ordered:
            if self.is_value_consistent_with_assignment(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                assignment[var] = None

        return None

    def is_value_consistent_with_assignment(self, var, value, assignment):
        """
        Checks if value for var is consistent with assignment
        """
        aux_assignment = assignment.copy()

        # remove unassigned vars
        for v, w in assignment.items():
            if w == None:
                aux_assignment.pop(v)

        aux_assignment[var] = value

        return self.consistent(aux_assignment)


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
