import random

# init variables for final score
user_wins = 0
bot_wins = 0
draws = 0

# get rounds number from user
rounds = input('rounds:')

for round_number in range(1, int(rounds) + 1):
    # divide rounds by round number header
    print(f'\n--- round {round_number} ---')

    # get move from user
    user_move = input('user move:')

    # get random bot move
    bot_move = random.choice(['rock', 'paper', 'scissors'])
    print(f'bot move:{bot_move}')

    # get the winner
    if user_move == bot_move:
        draws += 1
    elif user_move == 'rock':
        if bot_move == 'paper':
            bot_wins += 1
        else:
            user_wins += 1
    elif user_move == 'paper':
        if bot_move == 'scissors':
            bot_wins += 1
        else:
            user_wins += 1
    elif user_move == 'scissors':
        if bot_move == 'rock':
            bot_wins += 1
        else:
            user_wins += 1

# print results
print('\n--------------')
if user_wins > bot_wins:
    print('   user won')
elif user_wins < bot_wins:
    print('    bot won')
else:
    print('     draw')
print('--------------')
print(f'user wins: {user_wins}')
print(f'bot wins: {bot_wins}')
print(f'draws: {draws}')
