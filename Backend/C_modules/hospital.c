#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 100

struct Patient {
    int id;
    char name[50];
    int age;
    char gender[10];
    char disease[100];
};

// Queue for waiting patients
struct PatientQueue {
    struct Patient queue[MAX];
    int front, rear;
};

// Stack for served patients
struct PatientStack {
    struct Patient stack[MAX];
    int top;
};

// Initialize Queue
void initQueue(struct PatientQueue *q) {
    q->front = q->rear = -1;
}

// Check if queue is full
int isQueueFull(struct PatientQueue *q) {
    return q->rear == MAX - 1;
}

// Check if queue is empty
int isQueueEmpty(struct PatientQueue *q) {
    return q->front == -1 || q->front > q->rear;
}

// Add patient to queue
void enqueue(struct PatientQueue *q, struct Patient p) {
    if (isQueueFull(q)) {
        printf("❌ Waiting queue is full!\n");
        return;
    }
    if (q->front == -1) q->front = 0;
    q->queue[++q->rear] = p;
    printf("✅ Patient added to waiting list.\n");
}

// Display queue
void displayQueue(struct PatientQueue *q) {
    if (isQueueEmpty(q)) {
        printf("❌ No patients in the waiting queue.\n");
        return;
    }
    printf("\n--- Waiting Queue ---\n");
    for (int i = q->front; i <= q->rear; i++) {
        struct Patient p = q->queue[i];
        printf("ID: %d | Name: %s | Age: %d | Gender: %s | Disease: %s\n", p.id, p.name, p.age, p.gender, p.disease);
    }
}

// Remove from queue and return patient
struct Patient dequeue(struct PatientQueue *q) {
    struct Patient empty = {0};
    if (isQueueEmpty(q)) {
        printf("❌ No patients to serve.\n");
        return empty;
    }
    return q->queue[q->front++];
}

// Initialize Stack
void initStack(struct PatientStack *s) {
    s->top = -1;
}

// Check if stack is full
int isStackFull(struct PatientStack *s) {
    return s->top == MAX - 1;
}

// Check if stack is empty
int isStackEmpty(struct PatientStack *s) {
    return s->top == -1;
}

// Push to stack
void push(struct PatientStack *s, struct Patient p) {
    if (isStackFull(s)) {
        printf("❌ Attended patient stack is full!\n");
        return;
    }
    s->stack[++s->top] = p;
}

// Display stack
void displayStack(struct PatientStack *s) {
    if (isStackEmpty(s)) {
        printf("❌ No patients have been attended yet.\n");
        return;
    }
    printf("\n--- Recently Attended Patients (LIFO) ---\n");
    for (int i = s->top; i >= 0; i--) {
        struct Patient p = s->stack[i];
        printf("ID: %d | Name: %s | Age: %d | Gender: %s | Disease: %s\n", p.id, p.name, p.age, p.gender, p.disease);
    }
}

// Input patient details
struct Patient inputPatient() {
    struct Patient p;
    printf("Enter Patient ID: ");
    scanf("%d", &p.id);
    printf("Enter Name: ");
    scanf(" %[^\n]", p.name);
    printf("Enter Age: ");
    scanf("%d", &p.age);
    printf("Enter Gender: ");
    scanf(" %s", p.gender);
    printf("Enter Disease: ");
    scanf(" %[^\n]", p.disease);
    return p;
}

int main() {
    struct PatientQueue waitingList;
    struct PatientStack servedList;
    initQueue(&waitingList);
    initStack(&servedList);

    int choice;

    do {
        printf("\n--- Hospital Management ---\n");
        printf("1. Add Patient to Waiting Queue\n");
        printf("2. View Waiting Queue\n");
        printf("3. Serve Next Patient (Move to Stack)\n");
        printf("4. View Recently Attended Patients\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        struct Patient temp;
        switch (choice) {
            case 1:
                temp = inputPatient();
                enqueue(&waitingList, temp);
                break;
            case 2:
                displayQueue(&waitingList);
                break;
            case 3:
                temp = dequeue(&waitingList);
                if (temp.id != 0) {
                    printf("✅ Serving Patient: %s\n", temp.name);
                    push(&servedList, temp);
                }
                break;
            case 4:
                displayStack(&servedList);
                break;
            case 5:
                printf("Exiting program...\n");
                break;
            default:
                printf("❌ Invalid choice!\n");
        }
    } while (choice != 5);

    return 0;
}
