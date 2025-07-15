#include <stdio.h>

char board[3][3];
char currentPlayer = 'X';

// Function to initialize the board
void initializeBoard() {
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            board[i][j] = '1' + i * 3 + j;
}

// Function to print the current board
void printBoard() {
    printf("\n");
    for (int i = 0; i < 3; i++) {
        printf(" %c | %c | %c \n", board[i][0], board[i][1], board[i][2]);
        if (i < 2) printf("---|---|---\n");
    }
    printf("\n");
}

// Function to check if someone has won
char checkWin() {
    // Rows and columns
    for (int i = 0; i < 3; i++) {
        if (board[i][0] == board[i][1] && board[i][1] == board[i][2])
            return board[i][0];
        if (board[0][i] == board[1][i] && board[1][i] == board[2][i])
            return board[0][i];
    }
    // Diagonals
    if (board[0][0] == board[1][1] && board[1][1] == board[2][2])
        return board[0][0];
    if (board[0][2] == board[1][1] && board[1][1] == board[2][0])
        return board[0][2];

    return ' ';  // No winner yet
}

// Function to check for a draw
int checkDraw() {
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (board[i][j] != 'X' && board[i][j] != 'O')
                return 0;  // Still moves left
    return 1;  // It's a draw
}

// Function to handle a player's move
void makeMove() {
    int move;
    printf("Player %c, enter your move (1-9): ", currentPlayer);
    scanf("%d", &move);
    move--;  // Convert to 0-based index

    int row = move / 3;
    int col = move % 3;

    if (move < 0 || move >= 9 || board[row][col] == 'X' || board[row][col] == 'O') {
        printf("Invalid move! Try again.\n");
        makeMove();  // Recursively retry
    } else {
        board[row][col] = currentPlayer;
    }
}

// Switch player turn
void switchPlayer() {
    currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
}

int main() {
    initializeBoard();

    while (1) {
        printBoard();
        makeMove();

        char winner = checkWin();
        if (winner == 'X' || winner == 'O') {
            printBoard();
            printf("🎉 Player %c wins!\n", winner);
            break;
        }

        if (checkDraw()) {
            printBoard();
            printf("🤝 It's a draw!\n");
            break;
        }

        switchPlayer();
    }

    return 0;
}
