#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>

#define MAX_ATTEMPTS 3
#define TRANSACTION_HISTORY_SIZE 100

struct Transaction {
    time_t timestamp;
    char type[20];  // "DEPOSIT", "WITHDRAW", "CREATE", "DELETE"
    float amount;
    float balance;
};

struct Account {
    char name[50];
    int accountNumber;
    float balance;
    int pin;
    int failedAttempts;
    struct Transaction transactions[TRANSACTION_HISTORY_SIZE];
    int transactionCount;
};

// Function prototypes
void createAccount();
int login(int *index);
void updateAccount(struct Account updated, int index);
void deposit();
void withdraw();
void checkBalance();
void deleteAccount();
void viewTransactionHistory();
int validateInput(const char* input, size_t maxLength);
void addTransaction(struct Account *acc, const char* type, float amount);
void clearInputBuffer();

void createAccount() {
    struct Account acc;
    FILE *fp;
    char name[50];
    int accountNumber;
    int pin;

    printf("Enter your name: ");
    scanf(" %[^\n]", name);
    if (!validateInput(name, (size_t)49)) {
        printf("❌ Invalid name format.\n");
        return;
    }
    strcpy(acc.name, name);

    printf("Set Account Number: ");
    if (scanf("%d", &accountNumber) != 1) {
        printf("❌ Invalid account number.\n");
        clearInputBuffer();
        return;
    }
    acc.accountNumber = accountNumber;

    printf("Set a 4-digit PIN: ");
    if (scanf("%d", &pin) != 1 || pin < 1000 || pin > 9999) {
        printf("❌ PIN must be a 4-digit number.\n");
        clearInputBuffer();
        return;
    }
    acc.pin = pin;
    acc.balance = 0.0;
    acc.failedAttempts = 0;
    acc.transactionCount = 0;

    fp = fopen("bank.txt", "ab");
    if (!fp) {
        printf("❌ Error creating account.\n");
        return;
    }
    fwrite(&acc, sizeof(acc), 1, fp);
    fclose(fp);

    printf("\n✅ Account created successfully!\n");
    addTransaction(&acc, "CREATE", 0.0);
}

int login(int *index) {
    int accNo, pin, i = 0;
    struct Account acc;
    FILE *fp = fopen("bank.txt", "rb");

    if (!fp) {
        printf("❌ Error opening file.\n");
        return -1;
    }

    printf("Enter Account Number: ");
    if (scanf("%d", &accNo) != 1) {
        printf("❌ Invalid account number.\n");
        clearInputBuffer();
        fclose(fp);
        return 0;
    }

    printf("Enter PIN: ");
    if (scanf("%d", &pin) != 1) {
        printf("❌ Invalid PIN.\n");
        clearInputBuffer();
        fclose(fp);
        return 0;
    }

    while (fread(&acc, sizeof(acc), 1, fp)) {
        if (acc.accountNumber == accNo) {
            if (acc.failedAttempts >= MAX_ATTEMPTS) {
                printf("❌ Account locked due to too many failed attempts.\n");
                fclose(fp);
                return 0;
            }
            if (acc.pin == pin) {
                acc.failedAttempts = 0;
                updateAccount(acc, i);
                fclose(fp);
                *index = i;
                return 1;
            } else {
                acc.failedAttempts++;
                updateAccount(acc, i);
                printf("❌ Invalid PIN. %d attempts remaining.\n", MAX_ATTEMPTS - acc.failedAttempts);
                fclose(fp);
                return 0;
            }
        }
        i++;
    }

    fclose(fp);
    printf("❌ Account not found.\n");
    return 0;
}

void updateAccount(struct Account updated, int index) {
    FILE *fp = fopen("bank.txt", "rb+");
    fseek(fp, index * sizeof(struct Account), SEEK_SET);
    fwrite(&updated, sizeof(struct Account), 1, fp);
    fclose(fp);
}

void addTransaction(struct Account *acc, const char* type, float amount) {
    if (acc->transactionCount >= TRANSACTION_HISTORY_SIZE) {
        // Shift all transactions one position back
        for (int i = 0; i < TRANSACTION_HISTORY_SIZE - 1; i++) {
            acc->transactions[i] = acc->transactions[i + 1];
        }
        acc->transactionCount = TRANSACTION_HISTORY_SIZE - 1;
    }

    struct Transaction *t = &acc->transactions[acc->transactionCount++];
    time(&t->timestamp);
    strcpy(t->type, type);
    t->amount = amount;
    t->balance = acc->balance;
}

void deposit() {
    int index;
    if (login(&index)) {
        FILE *fp = fopen("bank.txt", "rb");
        struct Account acc;

        fseek(fp, index * sizeof(acc), SEEK_SET);
        fread(&acc, sizeof(acc), 1, fp);
        fclose(fp);

        float amount;
        printf("Enter amount to deposit: ₹");
        if (scanf("%f", &amount) != 1 || amount <= 0) {
            printf("❌ Invalid amount.\n");
            clearInputBuffer();
            return;
        }

        acc.balance += amount;
        addTransaction(&acc, "DEPOSIT", amount);
        updateAccount(acc, index);
        printf("✅ ₹%.2f deposited. New Balance: ₹%.2f\n", amount, acc.balance);
    }
}

void withdraw() {
    int index;
    if (login(&index)) {
        FILE *fp = fopen("bank.txt", "rb");
        struct Account acc;

        fseek(fp, index * sizeof(acc), SEEK_SET);
        fread(&acc, sizeof(acc), 1, fp);
        fclose(fp);

        float amount;
        printf("Enter amount to withdraw: ₹");
        if (scanf("%f", &amount) != 1 || amount <= 0) {
            printf("❌ Invalid amount.\n");
            clearInputBuffer();
            return;
        }

        if (amount > acc.balance) {
            printf("❌ Insufficient balance.\n");
            return;
        }

        acc.balance -= amount;
        addTransaction(&acc, "WITHDRAW", amount);
        updateAccount(acc, index);
        printf("✅ ₹%.2f withdrawn. New Balance: ₹%.2f\n", amount, acc.balance);
    }
}

void checkBalance() {
    int index;
    if (login(&index)) {
        FILE *fp = fopen("bank.txt", "rb");
        struct Account acc;

        fseek(fp, index * sizeof(acc), SEEK_SET);
        fread(&acc, sizeof(acc), 1, fp);
        fclose(fp);

        printf("👤 Name: %s\n💳 Account Number: %d\n💰 Balance: ₹%.2f\n", acc.name, acc.accountNumber, acc.balance);
    } else {
        printf("❌ Login failed. Invalid credentials.\n");
    }
}

void viewTransactionHistory() {
    int index;
    if (login(&index)) {
        FILE *fp = fopen("bank.txt", "rb");
        struct Account acc;

        fseek(fp, index * sizeof(acc), SEEK_SET);
        fread(&acc, sizeof(acc), 1, fp);
        fclose(fp);

        printf("\n📜 Transaction History for Account: %d\n", acc.accountNumber);
        printf("========================================\n");
        
        for (int i = 0; i < acc.transactionCount; i++) {
            struct Transaction *t = &acc.transactions[i];
            char timeStr[20];
            strftime(timeStr, sizeof(timeStr), "%Y-%m-%d %H:%M:%S", localtime(&t->timestamp));
            printf("Time: %s\n", timeStr);
            printf("Type: %s\n", t->type);
            printf("Amount: ₹%.2f\n", t->amount);
            printf("Balance: ₹%.2f\n", t->balance);
            printf("----------------------------------------\n");
        }
    }
}

void deleteAccount() {
    int index;
    if (login(&index)) {
        FILE *fp = fopen("bank.txt", "rb");
        FILE *temp = fopen("temp.txt", "wb");
        struct Account acc;
        int i = 0;

        while (fread(&acc, sizeof(acc), 1, fp)) {
            if (i != index) {
                fwrite(&acc, sizeof(acc), 1, temp);
            }
            i++;
        }

        fclose(fp);
        fclose(temp);

        remove("bank.txt");
        rename("temp.txt", "bank.txt");
        printf("✅ Account deleted successfully.\n");
    }
}

int validateInput(const char* input, size_t maxLength) {
    if (strlen(input) == (size_t)0 || strlen(input) > maxLength) {
        return 0;
    }
    for (int i = 0; input[i]; i++) {
        if (!isprint(input[i])) {
            return 0;
        }
    }
    return 1;
}

void clearInputBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

int main() {
    int choice;

    do {
        printf("\n==== BANKING SYSTEM ====\n");
        printf("1. Create Account\n");
        printf("2. Deposit Money\n");
        printf("3. Withdraw Money\n");
        printf("4. Check Balance\n");
        printf("5. View Transaction History\n");
        printf("6. Delete Account\n");
        printf("7. Exit\n");
        printf("Enter your choice: ");
        
        if (scanf("%d", &choice) != 1) {
            printf("❌ Invalid input.\n");
            clearInputBuffer();
            continue;
        }

        switch (choice) {
            case 1: createAccount(); break;
            case 2: deposit(); break;
            case 3: withdraw(); break;
            case 4: checkBalance(); break;
            case 5: viewTransactionHistory(); break;
            case 6: deleteAccount(); break;
            case 7: printf("👋 Exiting Banking System.\n"); break;
            default: printf("❗ Invalid choice.\n");
        }
    } while (choice != 7);

    return 0;
}
