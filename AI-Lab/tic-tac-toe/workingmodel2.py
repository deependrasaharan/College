import numpy as np

import matplotlib
matplotlib.use('TkAgg')  # Alternative: 'Qt5Agg' if you have PyQt5 installed

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap



def empty_board():
    """create and empty board"""
    return [' '] * 9


def actions(board):
    """return possible actions as a vector of indices"""
    return np.where(np.array(board) == ' ')[0].tolist()


def result(state, player, action):
    """Add a single symbol to the board."""
    if state[action] != ' ':
        raise Exception(f"Illegal action {action} by player {player}!")
    
    state = state.copy()
    state[action] = player
  
    return state


def terminal(state):
    """is the state terminal?"""
    return check_board(state) != 'n'


def utility(state, player = 'x'):
    """utility of state. None defined for non-terminal states."""
    goal = check_board(state)        
    if goal == player: return +1         # win
    if goal == 'd': return 0             # draw
    if goal == other(player): return -1  # loss
    return None                          # utility is not defined 


def check_board(state):
    """check the board and return one of x, o, d (draw), or n (for next move)"""
    
    state = np.array(state).reshape((3,3))
    
    diagonals = np.array([[state[i][i] for i in range(len(state))], 
                          [state[i][len(state)-i-1] for i in range(len(state))]])
    
    for a_board in [state, np.transpose(state), diagonals]:
        for row in a_board:
            if len(set(row)) == 1 and row[0] != ' ':
                return row[0]
    
    # check for draw
    if(np.sum(state == ' ') < 1):
        return 'd'
    
    return 'n'


def other(player):
    if player == 'x': return 'o'
    else: return 'x'


def show_board_text(board):
    """display the board"""
    b = np.array(board).reshape((3,3))
    print(b)


# def show_board(board, help = True, dpi = 40, colors = {' ': 'white', 'x': 'red', 'o': 'black'}):
#     """Show the tic-tac-toe-board. help adds the array index, dpi changes the size and
#     colors sets the colors"""

#     b = np.array(board).reshape((3,3))

#     with plt.rc_context({'figure.dpi': dpi}):
#         fig = plt.matshow(np.zeros((3, 3)), cmap = ListedColormap(['w']))
#     fig.axes.axis('off')

#     plt.hlines([.5, 1.5], -.5, 2.5)
#     plt.vlines([.5, 1.5], -.5, 2.5)

#     for row in range(3):
#         for col in range(3):
#             plt.text(row, col, b[col, row],
#                  fontsize = 64,
#                  color = colors[b[col, row]],
#                  horizontalalignment = 'center',
#                  verticalalignment = 'center')

#     if help:
#         for row in range(3):
#             for col in range(3):
#                 plt.text(col, row - .35, col + 3 * row,
#                      fontsize = 12,
#                      color = 'gray',
#                      horizontalalignment = 'center',
#                      verticalalignment = 'center')

#     plt.show()

def show_board(board, help = True, dpi = 40, colors = {' ': 'white', 'x': 'red', 'o': 'black'}):
    """Show the tic-tac-toe-board. help adds the array index, dpi changes the size and
    colors sets the colors"""
    
    # Close any existing matplotlib windows to prevent buildup
    plt.close('all')
    
    b = np.array(board).reshape((3,3))

    with plt.rc_context({'figure.dpi': dpi}):
        fig = plt.matshow(np.zeros((3, 3)), cmap = ListedColormap(['w']))
    fig.axes.axis('off')

    plt.hlines([.5, 1.5], -.5, 2.5)
    plt.vlines([.5, 1.5], -.5, 2.5)

    for row in range(3):
        for col in range(3):
            plt.text(row, col, b[col, row],
                 fontsize = 64,
                 color = colors[b[col, row]],
                 horizontalalignment = 'center',
                 verticalalignment = 'center')

    if help:
        for row in range(3):
            for col in range(3):
                plt.text(col, row - .35, col + 3 * row,
                     fontsize = 12,
                     color = 'gray',
                     horizontalalignment = 'center',
                     verticalalignment = 'center')

    # Non-blocking display - allows you to continue entering input
    plt.show(block=False)
    plt.pause(0.001)  # Brief pause to render the window



def random_player(board, player = None):
    """Simple player that chooses a random empty square (equal probability of all permissible actions). 
    player is unused."""
    return np.random.choice(actions(board))


def play(x, o, N = 100, show_final_board = False):
    """Let two agents play each other N times. x starts. x and y are agent functions that 
    get the board as the percept and return their next action."""
    results = {'x': 0, 'o': 0, 'd': 0}
    
    for i in range(N):
        board = empty_board()
        
        while True:
            # x moves
            a = x(board, 'x')
            board = result(board, 'x', a)
            
            win = check_board(board)   # returns the 'n' if the game is not done.
            if win != 'n':
                results[win] += 1
                break
            
            # o moves
            a = o(board, 'o')
            board = result(board, 'o', a)
            
            win = check_board(board)   # returns the 'n' if the game is not done.
            if win != 'n':
                results[win] += 1
                break
    
        if show_final_board:
            show_board(board)   

    return results


# ============================================================================
# NEW FUNCTIONS FOR INTERACTIVE PLAY
# ============================================================================

def heuristic_player(board, player):
    """
    Heuristic-based player (PLACEHOLDER).
    TODO: Implement heuristic logic here.
    For now, this is an empty function that will be implemented later.
    """
    # Placeholder: will implement heuristic logic later
    pass


def human_player(board, player):
    """
    Human player - prompts user for move input.
    Returns the chosen action (index 0-8).
    """
    valid_actions = actions(board)
    
    while True:
        try:
            move = input(f"\n{player.upper()}'s turn. Enter your move (0-8): ").strip()
            move = int(move)
            
            if move not in range(9):
                print("❌ Invalid input! Please enter a number between 0 and 8.")
                continue
            
            if move not in valid_actions:
                print(f"❌ Square {move} is already occupied! Choose from: {valid_actions}")
                continue
            
            return move
            
        except ValueError:
            print("❌ Invalid input! Please enter a number between 0 and 8.")
        except KeyboardInterrupt:
            print("\n\nGame interrupted by user.")
            exit()


def play_interactive(human_symbol, human_goes_first, ai_mode):
    """
    Interactive game where human plays against AI.
    
    Args:
        human_symbol: 'x' or 'o' - the symbol the human player chose
        human_goes_first: bool - True if human moves first, False if AI moves first
        ai_mode: str - 'random' or 'heuristic' - the AI strategy to use
    """
    # Setup players
    ai_symbol = other(human_symbol)
    
    # Select AI player function based on mode
    if ai_mode == 'random':
        ai_player = random_player
    elif ai_mode == 'heuristic':
        ai_player = heuristic_player
    else:
        raise ValueError(f"Unknown AI mode: {ai_mode}")
    
    # Determine turn order
    if human_goes_first:
        if human_symbol == 'x':
            x_player, o_player = human_player, ai_player
        else:
            x_player, o_player = ai_player, human_player
    else:
        if human_symbol == 'x':
            x_player, o_player = ai_player, human_player
        else:
            x_player, o_player = human_player, ai_player
    
    # Game setup
    board = empty_board()
    print("\n" + "="*50)
    print(f"🎮 GAME START!")
    print(f"   You are: {human_symbol.upper()}")
    print(f"   AI is: {ai_symbol.upper()}")
    print(f"   AI Mode: {ai_mode.upper()}")
    print(f"   {'You' if human_goes_first else 'AI'} go first")
    print("="*50)
    
    # Show initial empty board
    print("\nInitial board:")
    show_board(board)
    
    # Game loop
    current_player_symbol = 'x'  # X always starts in tic-tac-toe
    
    while True:
        # Determine which player function to use
        if current_player_symbol == 'x':
            current_player_func = x_player
        else:
            current_player_func = o_player
        
        # Make move
        if current_player_func == human_player:
            print(f"\n{'='*50}")
            action = current_player_func(board, current_player_symbol)
        else:
            print(f"\n{'='*50}")
            print(f"🤖 AI ({current_player_symbol.upper()}) is thinking...")
            action = current_player_func(board, current_player_symbol)
            print(f"🤖 AI chose square {action}")
        
        # Apply move
        board = result(board, current_player_symbol, action)
        
        # Show updated board
        print(f"\nBoard after {current_player_symbol.upper()}'s move:")
        show_board(board)
        
        # Check for game end
        game_status = check_board(board)
        if game_status != 'n':
            print("\n" + "="*50)
            if game_status == 'd':
                print("🤝 GAME OVER - It's a DRAW!")
            elif game_status == human_symbol:
                print("🎉 CONGRATULATIONS! You WON! 🎉")
            else:
                print("😞 AI WINS! Better luck next time!")
            print("="*50 + "\n")
            break
        
        # Switch player
        current_player_symbol = other(current_player_symbol)


def get_user_input():
    """
    Get game configuration from user.
    Returns: (human_symbol, human_goes_first, ai_mode)
    """
    print("\n" + "="*50)
    print("🎮 WELCOME TO TIC-TAC-TOE!")
    print("="*50)
    
    # Choose symbol
    while True:
        symbol = input("\nDo you want to play as X or O? ").strip().lower()
        if symbol in ['x', 'o']:
            human_symbol = symbol
            break
        print("❌ Invalid choice! Please enter 'X' or 'O'.")
    
    # Choose turn order
    while True:
        turn = input("\nDo you want to move FIRST or SECOND? ").strip().lower()
        if turn in ['first', 'second', '1st', '2nd', '1', '2']:
            human_goes_first = turn in ['first', '1st', '1']
            break
        print("❌ Invalid choice! Please enter 'FIRST' or 'SECOND'.")
    
    # Choose AI mode
    print("\n" + "-"*50)
    print("SELECT AI MODE:")
    print("  1. Random  - AI makes random moves")
    print("  2. Heuristic - AI uses heuristic strategy (TODO)")
    print("-"*50)
    
    while True:
        mode = input("\nEnter mode (1 or 2): ").strip()
        if mode == '1':
            ai_mode = 'random'
            break
        elif mode == '2':
            ai_mode = 'heuristic'
            print("\n⚠️  WARNING: Heuristic mode not yet implemented!")
            print("   The AI will not make any moves in this mode.")
            confirm = input("   Continue anyway? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                break
            else:
                continue
        else:
            print("❌ Invalid choice! Please enter '1' or '2'.")
    
    return human_symbol, human_goes_first, ai_mode


# ============================================================================
# MAIN PROGRAM
# ============================================================================

if __name__ == "__main__":
    # Get user preferences
    human_symbol, human_goes_first, ai_mode = get_user_input()
    
    # Start interactive game
    play_interactive(human_symbol, human_goes_first, ai_mode)
