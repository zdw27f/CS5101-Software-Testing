from tile import Tile
from random import choice

global COL_IDENTS
global ROW_IDENTS
global VALID_DIRECTIONS
ROW_IDENTS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
COL_IDENTS = [' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
VALID_DIRECTIONS = ['N', 'E', 'S', 'W']

class Board():

    def __init__(self):
        self.board = {}
        self.ships = {}
        self.rows = 10
        self.cols = 10
        self.num_ship_hits = 0
        self.num_ships_sunk = 0
        self.bonus_shots = 0
        self.aoe_shot = False

        # Member variables used by the computer
        self.tiles_to_attempt = []
        self.ship_found = {
            "tiles_hit": None,
            "direction": None
        }

        for i in range(self.rows):
            self.board[i] = []
            for j in range(self.cols):
                self.board[i].append(Tile(i,j))

    def print_board(self, name):
        print('--- {}\'s ship board ---'.format(name))

        for i in range(len(COL_IDENTS)):
            print('{} '.format(COL_IDENTS[i]), end='')
        print('')

        for i in range(self.rows):
            print('{} '.format(ROW_IDENTS[i]), end='')

            for j in range(self.cols):
                print('{} '.format(self.board[i][j].status_code), end='')

            print('')
        print('')

    def print_shot_board(self):
        print('--- User\'s shot board ---')

        for i in range(len(COL_IDENTS)):
            print('{} '.format(COL_IDENTS[i]), end='')
        print('')

        for i in range(self.rows):
            print('{} '.format(ROW_IDENTS[i]), end='')

            for j in range(self.cols):
                if self.board[i][j].status_code == '!':
                    print('~ ', end='')
                else:
                    print('{} '.format(self.board[i][j].status_code), end='')

            print('')
        print('')

    def check_ship_placement_input(self, ship_placement, ship_length):
        # Strips the user's input of all spaces
        ship_placement = "".join(ship_placement.split())

        # Validates the user input a valid number of characters and that the characters were
        # valid eligible characters
        if len(ship_placement) != 3:
            return (False, ())
        if ship_placement[0] not in ROW_IDENTS:
            return (False, ())
        if ship_placement[1] not in COL_IDENTS:
            return (False, ())
        if ship_placement[2] not in VALID_DIRECTIONS:
            return (False, ())

        # Grabs the individual pieces of data from the stripped user input
        ship_start_row = ord(ship_placement[0]) - 65 # A B C . . .
        ship_start_col = int(ship_placement[1]) # 0 1 2 . . .
        direction = ship_placement[2]

        # Checks if the users input would end up making the ship go off the board
        if direction == 'N':
            if (ship_start_row - (ship_length-1)) < 0:
                return (False, ())

        elif direction == 'S':
            if (ship_start_row + (ship_length-1)) >= self.rows:
                return (False, ())

        elif direction == 'W':
            if (ship_start_col - (ship_length-1)) < 0:
                return (False, ())

        elif direction == 'E':
            if (ship_start_col + (ship_length-1)) >= self.cols:
                return (False, ())

        return (True, (ship_start_row, ship_start_col, direction))

    def check_overlap(self, position, ship_length):
        # Grab initial placement of ship with direction
        x = position[0]
        y = position[1]
        direction = position[2]

        # Add initial tile locations
        locations = []

        # Grab all locations that will be set to a ship
        if direction == 'N':
            for i in range(ship_length):
                locations.append(self.board[x-i][y])

        elif direction == 'E':
            for i in range(ship_length):
                locations.append(self.board[x][y+i])

        elif direction == 'S':
            for i in range(ship_length):
                locations.append(self.board[x+i][y])

        elif direction == 'W':
            for i in range(ship_length):
                locations.append(self.board[x][y-i])

        # Check if ships overlap
        for tiles in self.ships.values():
            for tile in tiles:
                if tile in locations:
                    # Invalid
                    return (False, None)

        # Valid
        return (True, locations)

    def place_ship(self, locations):
        # Add ship to self.ships
        self.ships[len(self.ships)] = locations

        # Sets tile locations to have a "status_code" of !; meaning they're a ship
        for tile in locations:
            self.board[tile.x][tile.y].status_code = '!'

    # Used for generating random input for placing ships
    def generate_random_ship_placement(self):
        return choice(ROW_IDENTS) + choice(COL_IDENTS[1:]) + choice(VALID_DIRECTIONS)

    def generate_computers_random_shots(self):
        # Since the smallest ship is of length 2, the computer will attempt
        # to place shots in a checkerboard pattern. Doing this would mean
        # that every ship would be hit at least once. And if the computer
        # detects a ship has been hit, it will shoot any tile until the ship(s)
        # hit have been sunk.

        counter = 0

        for i in range(self.rows):
            if i % 2 == 0:
                counter = 0
            else:
                counter = 1
            for j in range(self.cols):
                if counter % 2 == 0:
                    self.tiles_to_attempt.append((i,j))
                counter += 1

    def select_random_shot(self):
        random_coordinate = None

        # Loops until a valid shot is found
        while True:
            random_coordinate = choice(self.tiles_to_attempt)
            if self.validate_shot(*random_coordinate):
                break

            # Removes invalid coordinates
            self.tiles_to_attempt.remove(random_coordinate)

        # Removes the to-be-made shot because the coordinate location will
        # no longer be valid after a shot has been made at the specified
        # coordinate location.
        self.tiles_to_attempt.remove(random_coordinate)
        return random_coordinate

    def check_shot_in_specified_direction(self, coordinate, direction):
        row = coordinate[0]
        col = coordinate[1]
        new_coordinate = None

        if direction == 'N':
            if (row-1) >= 0:
                new_coordinate = ((row-1),col)
        if direction == 'E':
            if (col+1) < len(COL_IDENTS)-1:
                new_coordinate = (row,(col+1))
        if direction == 'S':
            if (row+1) < len(ROW_IDENTS):
                new_coordinate = ((row+1),col)
        if direction == 'W':
            if (col-1) >= 0:
                new_coordinate = (row,(col-1))

        return new_coordinate

    # Returns: (False, None) if no ship hits found on board.
    #          (True, coordinate) if ship hit was found; 'coordinate' represents the "smart shot".
    def generate_smart_shot(self):
        new_coordinate = None
        shot_found = False

        # Search the board to see if a ship has been hit
        if not self.ship_found['tiles_hit']:
            self.ship_found['tiles_hit'] = [tile for ship_tiles in self.ships.values() for tile in ship_tiles if tile.status_code == 'X']

        # If no ship hits were found
        if not self.ship_found['tiles_hit']:
            return (False, None)

        # If a direction has already been determined
        if self.ship_found['direction']:
            # If ship tile was hit in the previous shot and you've hit more than one ship tile,
            # continue shotting in whatever direction you've been shooting
            if self.ship_found['tiles_hit'][-1].status_code == 'X':
                row = self.ship_found['tiles_hit'][-1].x
                col = self.ship_found['tiles_hit'][-1].y
                direction = self.ship_found['direction']

                new_coordinate = self.check_shot_in_specified_direction((row,col), direction)
                if new_coordinate and self.validate_shot(*new_coordinate):
                    self.ship_found['tiles_hit'].append(self.board[new_coordinate[0]][new_coordinate[1]])
                    self.ship_found['direction'] = direction
                    return (True, new_coordinate)

            # If the previous shot missed the ship or if the previous shot with the given direction would lead
            # to a shot that went off the board, remove it from the "tiles_hit" list
            del self.ship_found['tiles_hit'][-1]

            # If one or more ships have been hit but the previous shot on the board didn't hit a ship
            # on the board, then try shooting in the oppposite direction of the first tile hit.
            row = self.ship_found['tiles_hit'][0].x
            col = self.ship_found['tiles_hit'][0].y
            direction = None

            # Determine the opposite direction to try
            if self.ship_found['direction'] == 'N':
                direction = 'S'
            elif self.ship_found['direction'] == 'E':
                direction = 'W'
            elif self.ship_found['direction'] == 'S':
                direction = 'N'
            elif self.ship_found['direction'] == 'W':
                direction = 'E'

            # Check if the shot in the opposite direction of the first tile hit works
            new_coordinate = self.check_shot_in_specified_direction((row,col), direction)
            if new_coordinate and self.validate_shot(*new_coordinate):
                self.ship_found['tiles_hit'].append(self.board[new_coordinate[0]][new_coordinate[1]])
                self.ship_found['direction'] = direction
                return (True, new_coordinate)

            self.ship_found['direction'] = None

        # Find and attempt a valid shot around the different hits on the board until
        # a second hit is made. Could also be that multiple tiles have been hit
        # but the direction attempted was not valid so a new direction needs to
        # be attempted.
        if not self.ship_found['direction']:
            tiles_to_be_added = []

            # Loops until a valid shot is found
            while not shot_found:
                for tile in self.ship_found['tiles_hit']:
                    row = tile.x
                    col = tile.y

                    # Checks in all 4 directions for a tile to shoot at
                    for i in range(4):
                        new_coordinate = self.check_shot_in_specified_direction((row,col), VALID_DIRECTIONS[i])
                        if new_coordinate and self.validate_shot(*new_coordinate):
                            self.ship_found['direction'] = VALID_DIRECTIONS[i]
                            shot_found = True
                            break

                    # If it finds a valid tile with a shot around it to take, queue it up to be added and
                    # then break from the for loop
                    if shot_found:
                        tiles_to_be_added = [tile, self.board[new_coordinate[0]][new_coordinate[1]]]
                        break

                self.ship_found['tiles_hit'] = tiles_to_be_added

                # In the rare case the computer can't find a valid location based off of the current tiles given
                if not self.ship_found['tiles_hit']:
                    _, new_coordinate = self.generate_smart_shot()
                    shot_found = True

        return (True, new_coordinate)

    def check_shot_input(self, coordinate_shot):

        # Strips the user's input of all spaces
        coordinate_shot = "".join(coordinate_shot.split())

        # Validates the user input a valid number of characters and that the characters were
        # valid eligible characters
        if len(coordinate_shot) != 2:
            return (False, None)
        if coordinate_shot[0] not in ROW_IDENTS:
            return (False, None)
        if coordinate_shot[1] not in COL_IDENTS:
            return (False, None)

        return (True, coordinate_shot)

    def convert_input(self, coordinate_shot):
        # Grabs the individual pieces of data from the stripped user input
        row = ord(coordinate_shot[0]) - 65 # A B C . . .
        col = int(coordinate_shot[1]) # 0 1 2 . . .

        return (row,col)

    def validate_shot(self, row, col):
        # Gets the status code of the tile being shot at
        tile_status = self.board[row][col].status_code
        valid_locations = ['!', '~']

        # Makes sure the user is shooting a place they've already tried
        if tile_status in valid_locations:
            return True
        else:
            return False

    def validate_bonus_shots(self, num_bonus_shots):
        # Validates input is a number
        try:
            num_bonus_shots = int(num_bonus_shots)
        except:
            return False

        # Checks input against valid range
        if num_bonus_shots >= 0 and num_bonus_shots <= self.bonus_shots:
            self.bonus_shots -= num_bonus_shots
            return True

        return False

    def place_aoe_shot(self, coordinate):
        self.aoe_shot = False

        # Iterate over the 9 possible shots
        for i in range(-1,2):
            for j in range(-1,2):

                # Grab the current row & col
                row = coordinate[0]+i
                col = coordinate[1]+j

                # Validates each of the shots
                if row >= 0 and col >= 0 and row < 10 and col < 10:
                    if self.validate_shot(row,col):
                        if self.place_shot((row,col)):
                            self.update_ships()

        # Clears these variables because the 'generate_smart_shot' doesn't pick
        # up any ship tiles hit during this function. So, essentially, I'm flushing
        # these values so that the board doesn't get possibly stuck looking at an
        # old tile that has no possible shots around it to take.
        self.ship_found['tiles_hit'] = None
        self.ship_found['direction'] = None

    def place_shot(self, coordinate):
        tile_status = self.board[coordinate[0]][coordinate[1]].status_code

        # Hit a ship
        if tile_status == '!':
            self.board[coordinate[0]][coordinate[1]].status_code = 'X'
            self.num_ship_hits += 1
            return True
        # Hit the water
        elif tile_status == '~':
            self.board[coordinate[0]][coordinate[1]].status_code = '*'
            return False

        return False

    def update_ships(self):
        ships_to_be_removed = {}

        # Checks if any of the ships are completely sunk
        for ship_id, ship_tiles in self.ships.items():
            ship_sunk = True

            for tile in ship_tiles:
                if tile.status_code != 'X':
                    ship_sunk = False
                    break

            # If a ship got completely hit, queue it up to be sunk
            if ship_sunk:
                ships_to_be_removed[ship_id] = ship_tiles

        # Removes any sunk ships from the self.ships variable and also updates the board
        # about the sunk ship.
        for ship_id, ship_tiles in ships_to_be_removed.items():
            for tile in ship_tiles:
                self.board[tile.x][tile.y].status_code = 'S'
            self.ships.pop(ship_id)

        # Returns true if a ship sunk
        if ships_to_be_removed:
            # Clear the tiles for a ship being hit (for when using "generate_smart_shot")
            self.ship_found['tiles_hit'] = None
            self.ship_found['direction'] = None

            self.aoe_shot = True
            self.bonus_shots += 1
            self.num_ships_sunk += 1
            return True

        return False

    def compute_game_score(self):
        return self.num_ship_hits + (5 * self.num_ships_sunk)

    def check_win(self):
        if self.ships:
            return False

        return True
