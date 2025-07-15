#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define SIZE 4

int score = 0, prev_score = 0, highscore = 0;
int arr[SIZE][SIZE], prev[SIZE][SIZE];
char name[50];

void clear_screen() {
    system("clear || cls");
}

void read_highscore() {
    FILE *fp = fopen("highscore.txt", "r");
    if (fp) {
        fscanf(fp, "%d", &highscore);
        fclose(fp);
    }
}
void write_highscore() {
    if (score > highscore) {
        highscore = score;
        FILE *fp = fopen("highscore.txt", "w");
        if (fp) {
            fprintf(fp, "%d", highscore);
            fclose(fp);
        }
    }
}
void save_prev_state() {
    prev_score = score;
    for (int i = 0; i < SIZE; ++i)
        for (int j = 0; j < SIZE; ++j)
            prev[i][j] = arr[i][j];
}
void restore_prev_state() {
    score = prev_score;
    for (int i = 0; i < SIZE; ++i)
        for (int j = 0; j < SIZE; ++j)
            arr[i][j] = prev[i][j];
}
void generate_tile() {
    int empty[SIZE * SIZE][2];
    int count = 0;

    for (int i = 0; i < SIZE; ++i)
        for (int j = 0; j < SIZE; ++j)
            if (arr[i][j] == 0)
                empty[count][0] = i, empty[count++][1] = j;

    if (count > 0) {
        int index = rand() % count;
        int value = (rand() % 10 == 0) ? 4 : 2; // 10% chance for 4
        arr[empty[index][0]][empty[index][1]] = value;
    }
}
void display() {
    clear_screen();
    printf("\n2048 GAME\n");
    printf("Player: %s | Score: %d | High Score: %d\n", name, score, highscore);
    printf("+------+------+------+------+");

    for (int i = 0; i < SIZE; ++i) {
        printf("\n");
        for (int j = 0; j < SIZE; ++j) {
            if (arr[i][j])
                printf("|%6d", arr[i][j]);
            else
                printf("|      ");
        }
        printf("|\n+------+------+------+------+\n");
    }
}

int can_move() {
    for (int i = 0; i < SIZE; ++i)
        for (int j = 0; j < SIZE; ++j)
            if (arr[i][j] == 0 ||
                (i < SIZE - 1 && arr[i][j] == arr[i + 1][j]) ||
                (j < SIZE - 1 && arr[i][j] == arr[i][j + 1]))
                return 1;
    return 0;
}

void rotate_right() {
    int temp[SIZE][SIZE];
    for (int i = 0; i < SIZE; ++i)
        for (int j = 0; j < SIZE; ++j)
            temp[j][SIZE - i - 1] = arr[i][j];

    memcpy(arr, temp, sizeof(arr));
}

int move_left() {
    int moved = 0;
    for (int i = 0; i < SIZE; ++i) {
        int temp[SIZE] = {0}, idx = 0;
        for (int j = 0; j < SIZE; ++j)
            if (arr[i][j]) temp[idx++] = arr[i][j];

        for (int j = 0; j < idx - 1; ++j) {
            if (temp[j] == temp[j + 1]) {
                temp[j] *= 2;
                score += temp[j];
                temp[j + 1] = 0;
                j++;
            }
        }

        int row[SIZE] = {0};
        idx = 0;
        for (int j = 0; j < SIZE; ++j)
            if (temp[j]) row[idx++] = temp[j];

        for (int j = 0; j < SIZE; ++j) {
            if (arr[i][j] != row[j]) moved = 1;
            arr[i][j] = row[j];
        }
    }
    return moved;
}

int move(char direction) {
    int moved = 0;
    switch (direction) {
        case 'w': rotate_right(); rotate_right(); rotate_right(); moved = move_left(); rotate_right(); break;
        case 'a': moved = move_left(); break;
        case 's': rotate_right(); moved = move_left(); rotate_right(); rotate_right(); rotate_right(); break;
        case 'd': rotate_right(); rotate_right(); moved = move_left(); rotate_right(); rotate_right(); break;
    }
    return moved;
}

int main() {
    srand(time(NULL));
    read_highscore();

    clear_screen();
    printf("Enter your name: ");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = 0;

    memset(arr, 0, sizeof(arr));
    generate_tile();
    generate_tile();

    while (1) {
        display();
        if (!can_move()) {
            printf("\nGame Over!\n");
            write_highscore();
            break;
        }

        printf("\nMove (WASD), U to undo, R to restart, Q to quit: ");
        char ch;
        scanf(" %c", &ch);
        ch = tolower(ch);

        if (ch == 'q') break;
        else if (ch == 'r') {
            score = 0;
            memset(arr, 0, sizeof(arr));
            generate_tile();
            generate_tile();
        } else if (ch == 'u') {
            restore_prev_state();
        } else if (strchr("wasd", ch)) {
            save_prev_state();
            if (move(ch)) generate_tile();
        }
    }

    return 0;
}
