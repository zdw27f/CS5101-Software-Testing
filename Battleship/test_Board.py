from tile import Tile
from board import Board

################################### HOW TO USE THIS FILE #########################################
# Pytest: Used for running unit tests                                                            #
# INSTALL: pytest (for me I installed it via command-line using: "pip3 install pytest")          #
# RUN: Just type "pytest" in the command-line while in the same directory as this file           #
#                                                                                                #
# Pytest-cov: Used for seeing how much code coverage there is                                    #
# INSTALL: pytest-cov (for me I installed it via command-line using: "pip3 install pytest-cov")  #
# RUN: Just type "py.test --cov-report term-missing --cov=./" in the command-line while in       #
#      the same directory as this file                                                           #
##################################################################################################

def test_create_board():
    rows = 10
    cols = 10

    created_board = Board()
    expected_board = {
        0: [ Tile(0,0), Tile(0,1), Tile(0,2), Tile(0,3), Tile(0,4), Tile(0,5), Tile(0,6), Tile(0,7), Tile(0,8), Tile(0,9) ],
        1: [ Tile(1,0), Tile(1,1), Tile(1,2), Tile(1,3), Tile(1,4), Tile(1,5), Tile(1,6), Tile(1,7), Tile(1,8), Tile(1,9) ],
        2: [ Tile(2,0), Tile(2,1), Tile(2,2), Tile(2,3), Tile(2,4), Tile(2,5), Tile(2,6), Tile(2,7), Tile(2,8), Tile(2,9) ],
        3: [ Tile(3,0), Tile(3,1), Tile(3,2), Tile(3,3), Tile(3,4), Tile(3,5), Tile(3,6), Tile(3,7), Tile(3,8), Tile(3,9) ],
        4: [ Tile(4,0), Tile(4,1), Tile(4,2), Tile(4,3), Tile(4,4), Tile(4,5), Tile(4,6), Tile(4,7), Tile(4,8), Tile(4,9) ],
        5: [ Tile(5,0), Tile(5,1), Tile(5,2), Tile(5,3), Tile(5,4), Tile(5,5), Tile(5,6), Tile(5,7), Tile(5,8), Tile(5,9) ],
        6: [ Tile(6,0), Tile(6,1), Tile(6,2), Tile(6,3), Tile(6,4), Tile(6,5), Tile(6,6), Tile(6,7), Tile(6,8), Tile(6,9) ],
        7: [ Tile(7,0), Tile(7,1), Tile(7,2), Tile(7,3), Tile(7,4), Tile(7,5), Tile(7,6), Tile(7,7), Tile(7,8), Tile(7,9) ],
        8: [ Tile(8,0), Tile(8,1), Tile(8,2), Tile(8,3), Tile(8,4), Tile(8,5), Tile(8,6), Tile(8,7), Tile(8,8), Tile(8,9) ],
        9: [ Tile(9,0), Tile(9,1), Tile(9,2), Tile(9,3), Tile(9,4), Tile(9,5), Tile(9,6), Tile(9,7), Tile(9,8), Tile(9,9) ],
    }

    for i in range(rows):
        for j in range(cols):
            assert created_board.board[i][j].status_code == expected_board[i][j].status_code

    assert created_board.board[0][0].x == 0
    assert created_board.board[0][0].y == 0

    assert created_board.board[4][7].x == 4
    assert created_board.board[4][7].y == 7

def test_check_ship_placement_input():
    test_board = Board()

    user_input = "A1     34"
    assert test_board.check_ship_placement_input(user_input, 3) == (False, ())

    user_input = "A9 N"
    assert test_board.check_ship_placement_input(user_input, 3) == (False, ())

    user_input = "A7 S"
    valid, locations = test_board.check_ship_placement_input(user_input, 3)
    assert valid == True
    assert locations[0] == 0
    assert locations[1] == 7
    assert locations[2] == 'S'

def test_check_overlap():
    test_board = Board()
    test_input = "A1 S"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    test_input = "A2 E"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)

    assert valid == True

    test_board.place_ship(locations)
    test_input = "A3 S"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)

    assert valid == False


def test_place_ship():
    test_board = Board()
    test_input = "A1 S"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    assert test_board.board[0][0].status_code == '~'
    assert test_board.board[0][1].status_code == '!'
    assert test_board.board[1][1].status_code == '!'
    assert test_board.board[2][1].status_code == '!'
    assert test_board.board[3][1].status_code == '~'

def test_generate_random_ship_placement():
    ROW_IDENTS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    COL_IDENTS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    VALID_DIRECTIONS = ['N', 'E', 'W', 'S']

    test_board = Board()
    test_ship = test_board.generate_random_ship_placement()

    assert len(test_ship) == 3
    assert test_ship[0] in ROW_IDENTS
    assert test_ship[1] in COL_IDENTS
    assert test_ship[2] in VALID_DIRECTIONS

def test_generate_computers_random_shots():
    test_board = Board()
    test_board.generate_computers_random_shots()

    valid_locations = [
        (0,0), (0,2), (0,4), (0,6), (0,8),
        (1,1), (1,3), (1,5), (1,7), (1,9),
        (2,0), (2,2), (2,4), (2,6), (2,8),
        (3,1), (3,3), (3,5), (3,7), (3,9),
        (4,0), (4,2), (4,4), (4,6), (4,8),
        (5,1), (5,3), (5,5), (5,7), (5,9),
        (6,0), (6,2), (6,4), (6,6), (6,8),
        (7,1), (7,3), (7,5), (7,7), (7,9),
        (8,0), (8,2), (8,4), (8,6), (8,8),
        (9,1), (9,3), (9,5), (9,7), (9,9),
    ]

    for coordinate in valid_locations:
        assert coordinate in test_board.tiles_to_attempt
    assert len(valid_locations) == len(test_board.tiles_to_attempt)

def test_select_random_shot():
    test_board = Board()
    test_board.generate_computers_random_shots()

    valid_locations = [
        (0,0), (0,2), (0,4), (0,6), (0,8),
        (1,1), (1,3), (1,5), (1,7), (1,9),
        (2,0), (2,2), (2,4), (2,6), (2,8),
        (3,1), (3,3), (3,5), (3,7), (3,9),
        (4,0), (4,2), (4,4), (4,6), (4,8),
        (5,1), (5,3), (5,5), (5,7), (5,9),
        (6,0), (6,2), (6,4), (6,6), (6,8),
        (7,1), (7,3), (7,5), (7,7), (7,9),
        (8,0), (8,2), (8,4), (8,6), (8,8),
        (9,1), (9,3), (9,5), (9,7), (9,9),
    ]

    for i in range(len(valid_locations)):
        coordinate = test_board.select_random_shot()
        assert coordinate in valid_locations
        assert coordinate not in test_board.tiles_to_attempt

    assert len(test_board.tiles_to_attempt) == 0

def test_check_shot_in_specified_direction():
    test_board = Board()
    coordinate = test_board.check_shot_in_specified_direction((0,0), 'E')
    assert coordinate == (0,1)

    coordinate = test_board.check_shot_in_specified_direction((0,0), 'N')
    assert coordinate == None

def test_generate_smart_shot():
    test_board = Board()
    valid, position = test_board.check_ship_placement_input('B0 E', 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    smart_shot_found, coordinate = test_board.generate_smart_shot()
    assert smart_shot_found == False

    test_board.place_shot((1,1))
    test_board.update_ships()

    smart_shot_found, coordinate = test_board.generate_smart_shot()
    assert coordinate == (0,1)
    test_board.place_shot((0,1))
    test_board.update_ships()

    smart_shot_found, coordinate = test_board.generate_smart_shot()
    assert coordinate == (2,1)
    test_board.place_shot((2,1))
    test_board.update_ships()

    smart_shot_found, coordinate = test_board.generate_smart_shot()
    assert coordinate == (1,2)
    test_board.place_shot((1,2))
    test_board.update_ships()

    smart_shot_found, coordinate = test_board.generate_smart_shot()
    assert coordinate == (1,3)
    test_board.place_shot((1,3))
    test_board.update_ships()

    smart_shot_found, coordinate = test_board.generate_smart_shot()
    assert coordinate == (1,0)
    test_board.place_shot((1,0))
    test_board.update_ships()

def test_check_shot_input_invalid_input():
    test_board = Board()
    test_shot = 'A 0 4'
    valid, coordinate = test_board.check_shot_input(test_shot)
    assert valid == False
    assert coordinate == None

def test_check_shot_input_valid_input():
    test_board = Board()
    test_shot = '   A    0   '
    valid, coordinate = test_board.check_shot_input(test_shot)
    assert valid == True
    assert coordinate == 'A0'

def test_convert_input():
    test_board = Board()
    user_input = 'A0'
    coordinate = test_board.convert_input(user_input)
    assert coordinate[0] == 0
    assert coordinate[1] == 0

def test_place_shot():
    test_board = Board()
    test_input = "A1 S"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    valid = test_board.place_shot((0, 1))
    assert valid == True
    assert test_board.board[0][1].status_code == 'X'

    valid = test_board.place_shot((4,3))
    assert valid == False
    assert test_board.board[4][3].status_code == '*'

def test_validate_shot():
    test_board = Board()
    test_input = "A1 S"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    test_board.place_shot((0, 1))
    valid = test_board.validate_shot(0, 1)
    assert valid == False

    valid = test_board.validate_shot(0, 2)
    assert valid == True

def test_validate_bonus_shots():
    test_board = Board()
    valid, position = test_board.check_ship_placement_input('A0 S', 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    assert test_board.bonus_shots == 0

    test_board.place_shot((0,0))
    test_board.place_shot((1,0))
    test_board.place_shot((2,0))
    test_board.update_ships()

    assert test_board.bonus_shots == 1

    valid = test_board.validate_bonus_shots('invalid input')
    assert valid == False

    valid = test_board.validate_bonus_shots('0')
    assert valid == True

    valid = test_board.validate_bonus_shots('1')
    assert valid == True

    # False because the bonus shot has just been used.
    valid = test_board.validate_bonus_shots('1')
    assert valid == False

def test_place_aoe_shot():
    test_board = Board()
    test_board = Board()
    valid, position = test_board.check_ship_placement_input('A0 S', 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    test_board.place_aoe_shot((1,1))
    assert test_board.board[0][0].status_code == 'S'
    assert test_board.board[1][0].status_code == 'S'
    assert test_board.board[2][0].status_code == 'S'
    assert test_board.board[0][1].status_code == '*'
    assert test_board.board[1][1].status_code == '*'
    assert test_board.board[2][1].status_code == '*'
    assert test_board.board[0][2].status_code == '*'
    assert test_board.board[1][2].status_code == '*'
    assert test_board.board[2][2].status_code == '*'

def test_update_ships():
    test_board = Board()
    test_input = "A0 S"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    test_input = "A1 S"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    test_input = "A2 S"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    assert test_board.board[0][0].status_code == '!'
    test_board.place_shot((0, 0))
    ship_sunk = test_board.update_ships()
    assert ship_sunk == False
    assert test_board.board[0][0].status_code == 'X'

    test_board.place_shot((1, 0))
    test_board.place_shot((2, 0))
    ship_sunk = test_board.update_ships()
    assert ship_sunk == True
    assert test_board.board[0][0].status_code == 'S'
    assert test_board.board[1][0].status_code == 'S'
    assert test_board.board[2][0].status_code == 'S'

def test_compute_game_score():
    test_board = Board()
    valid, position = test_board.check_ship_placement_input('A0 S', 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    score = test_board.compute_game_score()
    assert score == 0

    test_board.place_shot((0, 0))
    test_board.place_shot((1, 0))
    test_board.update_ships()

    score = test_board.compute_game_score()
    assert score == 2

    test_board.place_shot((2, 0))
    test_board.update_ships()

    score = test_board.compute_game_score()
    assert score == 8

def test_check_win():
    test_board = Board()
    test_input = "A0 S"
    valid, position = test_board.check_ship_placement_input(test_input, 3)
    valid, locations = test_board.check_overlap(position, 3)
    test_board.place_ship(locations)

    winner = test_board.check_win()
    assert winner == False

    test_board.place_shot((0,0))
    test_board.place_shot((1,0))
    test_board.place_shot((2,0))
    test_board.update_ships()

    winner = test_board.check_win()
    assert winner == True
