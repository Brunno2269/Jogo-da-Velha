# Jogo da Velha (Tic-Tac-Toe)

Este é um projeto simples de um **Jogo da Velha** desenvolvido com **Python** (usando Flask) para o backend e **HTML, CSS e JavaScript** para o frontend. O jogo oferece três níveis de dificuldade para o jogador competir contra o computador: **Fácil**, **Médio** e **Difícil**.

## Funcionalidades

- **Modo de Jogo**: O jogador compete contra um **robô inteligente**.
- **Níveis de Dificuldade**:
  - **Fácil**: O robô faz movimentos aleatórios, sem qualquer estratégia.
  - **Médio**: O robô tenta bloquear o jogador caso ele tenha uma oportunidade de vitória.
  - **Difícil**: O robô usa um algoritmo **Minimax** para calcular a melhor jogada e jogar de forma estratégica.
- **Primeira Jogada Aleatória**: A primeira jogada do robô é sempre aleatória, independentemente da dificuldade escolhida.
- **Animações e Feedback**: Ao vencer, o jogo mostra uma animação de confetes e marca a linha vencedora.

## Tecnologias Utilizadas

- **Backend**:
  - **Python** com **Flask** para construir o servidor e gerenciar o estado do jogo.
  - Lógica do jogo implementada em Python, com a função **Minimax** usada para calcular os melhores movimentos no nível difícil.
  
- **Frontend**:
  - **HTML** para a estrutura da página.
  - **CSS** para o estilo e layout do tabuleiro do jogo.
  - **JavaScript** para interatividade, incluindo a escolha de dificuldade e envio de jogadas para o backend.
  
## Como Jogar

1. **Escolha o Nível de Dificuldade**: Ao abrir o jogo, você pode escolher entre três níveis de dificuldade: **Fácil**, **Médio** ou **Difícil**.
   - No nível **Fácil**, o robô faz jogadas aleatórias.
   - No nível **Médio**, o robô tenta bloquear as jogadas do jogador.
   - No nível **Difícil**, o robô usa a lógica de **Minimax** para fazer as melhores jogadas possíveis.
   
2. **Jogada do Jogador**: O jogador faz a sua jogada clicando em uma célula do tabuleiro.
   
3. **Jogada do Robô**: Após a jogada do jogador, o robô faz a sua jogada de acordo com o nível de dificuldade.
   
4. **Vitória ou Empate**: O jogo verifica se há um vencedor ou se o jogo terminou em empate, e exibe o resultado. Se o jogador ou o robô ganhar, uma linha azul clara marcará a combinação vencedora. Após isso, o jogo exibirá uma animação de confetes para celebrar a vitória.

5. **Reiniciar Jogo**: Ao final de cada partida, você pode reiniciar o jogo clicando no botão "Reiniciar Jogo".

## Estrutura do Projeto

