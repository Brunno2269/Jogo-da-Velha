import random
from flask import Flask, render_template, jsonify, request
import webbrowser
import threading
import os
import signal

app = Flask(__name__)

# Inicializando o estado do jogo
game_state = {
    'board': [' ' for _ in range(9)],
    'current_player': 'X',
    'winner': None,
    'winning_combo': None,  # Para destacar as células vencedoras
}

# Função para verificar se há um vencedor
def check_winner():
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]  # Diagonais
    ]
    
    for combo in winning_combinations:
        if game_state['board'][combo[0]] == game_state['board'][combo[1]] == game_state['board'][combo[2]] != ' ':
            game_state['winner'] = game_state['board'][combo[0]]
            game_state['winning_combo'] = combo
            return True
    return False

# Função para a jogada automática do círculo
def make_robot_move():
    available_positions = [i for i, cell in enumerate(game_state['board']) if cell == ' ']
    if available_positions:
        robot_position = random.choice(available_positions)
        game_state['board'][robot_position] = 'O'
        check_winner()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state')
def get_game_state():
    return jsonify(game_state)

import random

@app.route('/make_move/<int:position>', methods=['POST'])
def make_move(position):
    global game_state

    if game_state['board'][position] != ' ' or game_state['winner']:
        return jsonify(game_state)  # Movimento inválido

    # Movimento do jogador X
    game_state['board'][position] = 'X'

    # Verificar vitória ou empate após o movimento do jogador
    if check_winner(game_state['board'], 'X'):
        game_state['winner'] = 'X'
        game_state['winning_combo'] = get_winning_combo(game_state['board'], 'X')
        return jsonify(game_state)
    if is_draw(game_state['board']):
        game_state['winner'] = 'Draw'
        return jsonify(game_state)

    # O primeiro movimento do robô é sempre aleatório
    if game_state.get('first_robot_move', True):
        make_random_move('O')
        game_state['first_robot_move'] = False  # Garantir que só será aleatório uma vez
    else:
        # Movimento do robô com base no nível de dificuldade
        difficulty = game_state.get('difficulty', 'easy')
        if difficulty == 'easy':
            make_random_move('O')
        elif difficulty == 'medium':
            make_blocking_move('O')
        elif difficulty == 'hard':
            make_best_move('O')

    # Verificar vitória ou empate após o movimento do robô
    if check_winner(game_state['board'], 'O'):
        game_state['winner'] = 'O'
        game_state['winning_combo'] = get_winning_combo(game_state['board'], 'O')
    elif is_draw(game_state['board']):
        game_state['winner'] = 'Draw'

    return jsonify(game_state)

def make_random_move(player):
    """Faz um movimento aleatório."""
    empty_positions = [i for i, cell in enumerate(game_state['board']) if cell == ' ']
    if empty_positions:
        position = random.choice(empty_positions)
        game_state['board'][position] = player

def make_blocking_move(player):
    """Tenta bloquear o adversário ou joga aleatoriamente."""
    opponent = 'X' if player == 'O' else 'O'
    for i in range(9):
        if game_state['board'][i] == ' ':
            # Simula o movimento do oponente
            game_state['board'][i] = opponent
            if check_winner(game_state['board'], opponent):
                game_state['board'][i] = player  # Bloqueia a jogada
                return
            game_state['board'][i] = ' '
    # Se não precisar bloquear, faz um movimento aleatório
    make_random_move(player)

def make_best_move(player):
    """Usa o algoritmo Minimax para encontrar o melhor movimento."""
    def minimax(board, depth, is_maximizing):
        opponent = 'X' if player == 'O' else 'O'
        if check_winner(board, player):
            return 10 - depth
        if check_winner(board, opponent):
            return depth - 10
        if is_draw(board):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = player
                    score = minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = opponent
                    score = minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    best_score = float('-inf')
    best_move = None
    for i in range(9):
        if game_state['board'][i] == ' ':
            game_state['board'][i] = player
            score = minimax(game_state['board'], 0, False)
            game_state['board'][i] = ' '
            if score > best_score:
                best_score = score
                best_move = i

    if best_move is not None:
        game_state['board'][best_move] = player

def check_winner(board, player):
    """Verifica se há um vencedor."""
    return get_winning_combo(board, player) is not None

def is_draw(board):
    """Verifica se o jogo é um empate."""
    return ' ' not in board


@app.route('/reset_game', methods=['POST'])
def reset_game():
    global game_state
    game_state = {
        'board': [' ' for _ in range(9)],
        'current_player': 'X',
        'winner': None,
        'winning_combo': None,
    }
    return jsonify(game_state)

def get_winning_combo(board, player):
    # Combinações vencedoras possíveis (linhas, colunas e diagonais)
    winning_combos = [
        [0, 1, 2],  # Linha superior
        [3, 4, 5],  # Linha do meio
        [6, 7, 8],  # Linha inferior
        [0, 3, 6],  # Coluna esquerda
        [1, 4, 7],  # Coluna do meio
        [2, 5, 8],  # Coluna direita
        [0, 4, 8],  # Diagonal principal
        [2, 4, 6]   # Diagonal secundária
    ]
    
    # Verifica se alguma combinação vencedora contém 3 peças do jogador
    for combo in winning_combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return combo
    return None


# Função para abrir o navegador automaticamente
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Função para encerrar o servidor quando a página for fechada
@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)  # Enviar sinal de interrupção
    return 'Server shutting down...'

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=False)

@app.route('/start_game/<difficulty>', methods=['POST'])
def start_game(difficulty):
    global game_state
    game_state = {
        'board': [' ' for _ in range(9)],
        'current_player': 'X',
        'winner': None,
        'winning_combo': None,
    }
    game_state['difficulty'] = difficulty
    return jsonify(game_state)

def make_robot_move():
    available_positions = [i for i, cell in enumerate(game_state['board']) if cell == ' ']
    if available_positions:
        if game_state['difficulty'] == 'easy':
            # Jogada aleatória
            robot_position = random.choice(available_positions)
        elif game_state['difficulty'] == 'medium':
            # Tentar bloquear vitória do adversário, caso possível
            robot_position = find_best_move('X') or random.choice(available_positions)
        elif game_state['difficulty'] == 'hard':
            # Melhor jogada possível para o robô
            robot_position = find_best_move('O') or find_best_move('X') or random.choice(available_positions)
        game_state['board'][robot_position] = 'O'
        check_winner()

def find_best_move(player):
    """Procura a melhor jogada para o jogador fornecido."""
    for i in range(9):
        if game_state['board'][i] == ' ':
            game_state['board'][i] = player
            if check_winner():
                game_state['board'][i] = ' '  # Reverter movimento
                return i
            game_state['board'][i] = ' '  # Reverter movimento
    return None

