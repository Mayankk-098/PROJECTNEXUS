#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Student {
    char name[50];
    int roomNumber;
    int rollNumber;
    char phone[15];
    struct Student* next;  // Pointer for queue (linked list)
};

// Queue front and rear
struct Student *front = NULL, *rear = NULL;

// Enqueue student (Add to queue)
void enqueueStudent() {
    struct Student* temp = (struct Student*)malloc(sizeof(struct Student));
    if (!temp) {
        printf("❌ Memory allocation failed.\n");
        return;
    }

    printf("👤 Enter name: ");
    scanf(" %[^\n]", temp->name);
    printf("🏢 Enter room number: ");
    scanf("%d", &temp->roomNumber);
    printf("🎓 Enter roll number: ");
    scanf("%d", &temp->rollNumber);
    printf("📞 Enter phone number: ");
    scanf(" %[^\n]", temp->phone);

    temp->next = NULL;

    if (rear == NULL) {
        front = rear = temp;
    } else {
        rear->next = temp;
        rear = temp;
    }

    printf("\n✅ Student added to the queue (hostel).\n");
}

// View all students (Traverse queue)
void viewAllStudents() {
    if (front == NULL) {
        printf("❗ Hostel is empty. No students found.\n");
        return;
    }

    struct Student* temp = front;
    printf("\n📋 List of Hostel Students (Queue Order):\n");
    printf("-------------------------------------------\n");

    while (temp != NULL) {
        printf("👤 Name       : %s\n", temp->name);
        printf("🏢 Room No.   : %d\n", temp->roomNumber);
        printf("🎓 Roll No.   : %d\n", temp->rollNumber);
        printf("📞 Phone      : %s\n", temp->phone);
        printf("-------------------------------------------\n");
        temp = temp->next;
    }
}

// Search student by room number
void searchByRoom() {
    if (front == NULL) {
        printf("❗ Hostel is empty.\n");
        return;
    }

    int room;
    printf("🔍 Enter room number to search: ");
    scanf("%d", &room);

    struct Student* temp = front;
    int found = 0;

    while (temp != NULL) {
        if (temp->roomNumber == room) {
            printf("\n✅ Found student in Room %d:\n", room);
            printf("👤 Name : %s\n", temp->name);
            printf("🎓 Roll: %d\n", temp->rollNumber);
            printf("📞 Phone: %s\n", temp->phone);
            found = 1;
        }
        temp = temp->next;
    }

    if (!found) {
        printf("❌ No student found in room %d.\n", room);
    }
}

// Delete student by roll number (from queue)
void deleteByRoll() {
    if (front == NULL) {
        printf("❗ Hostel is empty.\n");
        return;
    }

    int roll;
    printf("🗑️ Enter roll number to delete: ");
    scanf("%d", &roll);

    struct Student *temp = front, *prev = NULL;
    int found = 0;

    while (temp != NULL) {
        if (temp->rollNumber == roll) {
            if (temp == front) {
                front = front->next;
                if (rear == temp) rear = NULL; // only one element
            } else {
                prev->next = temp->next;
                if (rear == temp) rear = prev;
            }

            free(temp);
            found = 1;
            printf("✅ Student with roll %d deleted.\n", roll);
            break;
        }
        prev = temp;
        temp = temp->next;
    }

    if (!found) {
        printf("❌ No student found with roll number %d.\n", roll);
    }
}

// Free all memory on exit
void freeQueue() {
    struct Student* temp;
    while (front != NULL) {
        temp = front;
        front = front->next;
        free(temp);
    }
}

// Main menu
int main() {
    int choice;

    do {
        printf("\n========= 🏨 HOSTEL MANAGEMENT (QUEUE) =========\n");
        printf("1. ➕ Add Student (Enqueue)\n");
        printf("2. 📂 View All Students\n");
        printf("3. 🔍 Search by Room Number\n");
        printf("4. 🗑️  Delete by Roll Number\n");
        printf("5. 🚪 Exit\n");
        printf("👉 Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: enqueueStudent(); break;
            case 2: viewAllStudents(); break;
            case 3: searchByRoom(); break;
            case 4: deleteByRoll(); break;
            case 5: freeQueue(); printf("👋 Exiting Queue-based Hostel System.\n"); break;
            default: printf("❗ Invalid choice. Try again.\n");
        }
    } while (choice != 5);

    return 0;
}
