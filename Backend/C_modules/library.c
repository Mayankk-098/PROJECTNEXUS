#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Book {
    int id;
    char title[100];
    char author[100];
    int issued; // 0 = not issued, 1 = issued
    struct Book* next; // Stack pointer
};

struct Book* top = NULL; // Top of stack

// Push book onto stack
void pushBook() {
    struct Book* newBook = (struct Book*)malloc(sizeof(struct Book));
    if (!newBook) {
        printf("❌ Memory allocation failed.\n");
        return;
    }

    printf("Enter Book ID: ");
    scanf("%d", &newBook->id);
    getchar(); // Clear newline

    printf("Enter Book Title: ");
    fgets(newBook->title, 100, stdin);
    newBook->title[strcspn(newBook->title, "\n")] = 0;

    printf("Enter Author Name: ");
    fgets(newBook->author, 100, stdin);
    newBook->author[strcspn(newBook->author, "\n")] = 0;

    newBook->issued = 0;
    newBook->next = top;
    top = newBook;

    printf("✅ Book added to the stack (library).\n");
}

// Pop last book (Undo add)
void popBook() {
    if (top == NULL) {
        printf("❗ Stack is empty. Nothing to undo.\n");
        return;
    }

    struct Book* temp = top;
    printf("🗑️ Removing Book: %s by %s\n", temp->title, temp->author);
    top = top->next;
    free(temp);
    printf("✅ Last book entry undone.\n");
}

// Display all books (Traverse stack)
void displayBooks() {
    if (top == NULL) {
        printf("❗ No books in the stack.\n");
        return;
    }

    struct Book* temp = top;
    printf("\n📚 Books in Library (Last Added First):\n");
    printf("--------------------------------------------------------\n");
    while (temp != NULL) {
        printf("📖 ID    : %d\n", temp->id);
        printf("📘 Title : %s\n", temp->title);
        printf("✍️  Author: %s\n", temp->author);
        printf("📦 Issued: %s\n", temp->issued ? "Yes" : "No");
        printf("--------------------------------------------------------\n");
        temp = temp->next;
    }
}

// Search by ID
void searchBook() {
    int id, found = 0;
    printf("🔍 Enter Book ID to search: ");
    scanf("%d", &id);

    struct Book* temp = top;
    while (temp != NULL) {
        if (temp->id == id) {
            printf("✅ Book Found:\n");
            printf("📘 Title : %s\n", temp->title);
            printf("✍️  Author: %s\n", temp->author);
            printf("📦 Issued: %s\n", temp->issued ? "Yes" : "No");
            found = 1;
            break;
        }
        temp = temp->next;
    }

    if (!found)
        printf("❌ Book with ID %d not found.\n", id);
}

// Issue a book
void issueBook() {
    int id, found = 0;
    printf("📤 Enter Book ID to issue: ");
    scanf("%d", &id);

    struct Book* temp = top;
    while (temp != NULL) {
        if (temp->id == id) {
            if (!temp->issued) {
                temp->issued = 1;
                printf("✅ Book issued successfully.\n");
            } else {
                printf("⚠️ Book already issued.\n");
            }
            found = 1;
            break;
        }
        temp = temp->next;
    }

    if (!found)
        printf("❌ Book not found.\n");
}

// Return a book
void returnBook() {
    int id, found = 0;
    printf("📥 Enter Book ID to return: ");
    scanf("%d", &id);

    struct Book* temp = top;
    while (temp != NULL) {
        if (temp->id == id) {
            if (temp->issued) {
                temp->issued = 0;
                printf("✅ Book returned successfully.\n");
            } else {
                printf("⚠️ Book was not issued.\n");
            }
            found = 1;
            break;
        }
        temp = temp->next;
    }

    if (!found)
        printf("❌ Book not found.\n");
}

// Free memory
void freeStack() {
    struct Book* temp;
    while (top != NULL) {
        temp = top;
        top = top->next;
        free(temp);
    }
}

int main() {
    int choice;

    do {
        printf("\n====== 📚 LIBRARY SYSTEM (STACK VERSION) ======\n");
        printf("1. ➕ Add Book (Push)\n");
        printf("2. 📂 Display All Books\n");
        printf("3. 🔍 Search Book by ID\n");
        printf("4. 🔄 Undo Last Add (Pop)\n");
        printf("5. 📤 Issue Book\n");
        printf("6. 📥 Return Book\n");
        printf("7. 🚪 Exit\n");
        printf("👉 Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: pushBook(); break;
            case 2: displayBooks(); break;
            case 3: searchBook(); break;
            case 4: popBook(); break;
            case 5: issueBook(); break;
            case 6: returnBook(); break;
            case 7: freeStack(); printf("👋 Exiting Library System.\n"); break;
            default: printf("❗ Invalid choice. Try again.\n");
        }

    } while (choice != 7);

    return 0;
}
