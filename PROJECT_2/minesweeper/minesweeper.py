import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        if len(self.cells) == self.count and self.count > 0:
            return self.cells
        return set()
    
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """  
        
        if self.count == 0:
            return self.cells
        return set()
        
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1  

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        if cell in self.cells:
            self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        # self.knowledge => [Sentence1(),Sentence2(),...]
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
########### 1) mark the cell as a move that has been made ###########
        self.moves_made.add(cell)
        
########### 2) mark the cell as safe ###########
        self.mark_safe(cell)
        
########### 3) add a new sentence to the AI's knowledge base ###########
        neighboring_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself and the bounds
                if (i, j) == cell:
                    continue
                
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighboring_cells.add((i, j))
        
        # Newly created sentence having information about the neighbors of (cell)
        main_sentence = Sentence(neighboring_cells, count)
        
        # We check if any of the safe cells haven't been removed from the new sentences
        for already_safe in self.safes:
            if already_safe in main_sentence.cells:
                main_sentence.mark_safe(already_safe)
        
        # We check if any of the safe cells haven't been removed from the new sentences
        for already_mine in self.mines:
            if already_mine in main_sentence.cells:
                main_sentence.mark_mine(already_mine)

        # We append the Sentence to the existing knowledge
        self.knowledge.append(main_sentence)
        
######### 4) mark any additional cells as safe or as mines ###########
        if count == 0:
            for cell_s in neighboring_cells:
                self.mark_safe(cell_s)
        elif count == len(neighboring_cells):
            for cell_m in neighboring_cells:
                self.mark_mine(cell_m)
                
########### 5) add any new sentences if they can be inferred from existing knowledge ###########
        infer_sentences = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 == sentence2 or not sentence1.cells or not sentence2.cells:
                    continue 
                if sentence1.cells.issubset(sentence2.cells):
                    new_infer_count = sentence2.count - sentence1.count
                    new_infer_cells = sentence2.cells - sentence1.cells
                    new_sentence = Sentence(new_infer_cells, new_infer_count)
                    if new_sentence not in self.knowledge and new_sentence not in infer_sentences:
                        infer_sentences.append(new_sentence)
    
        # We extend the existing knowledge
        self.knowledge.extend(infer_sentences)
        
        # We check if any new cells can be marked as safe or mines
        for sentence in self.knowledge:
            if sentence.count == 0:
                for cell_s in sentence.cells.copy():
                    self.mark_safe(cell_s)
            elif sentence.count == len(sentence.cells):
                for cell_m in sentence.cells.copy():
                    self.mark_mine(cell_m)

        # We finally check if any new mines or safes weren't already in self.safes and self.mines
        for sentence in self.knowledge:
            if sentence.known_mines() not in self.mines:
                for cell in sentence.known_mines():
                    self.mines.add(cell)
            elif sentence.known_safes() not in self.safes:
                for cell in sentence.known_safes():
                    self.safes.add(cell)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        random_moves = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    random_moves.append((i, j))
                    
        if random_moves == []:
            return None
        else:            
            return random.choice(random_moves)