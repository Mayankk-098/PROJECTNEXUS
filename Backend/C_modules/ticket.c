#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Ticket structure
struct Ticket {
    int ticketID;
    char name[50];
    char destination[50];
    char date[15];
    int seatNumber;
    struct Ticket* next;
};

struct Ticket* front = NULL;
struct Ticket* rear = NULL;

// Enqueue: Book a ticket
void bookTicket() {
    struct Ticket* newTicket = (struct Ticket*)malloc(sizeof(struct Ticket));

    printf("Enter Ticket ID: ");
    scanf("%d", &newTicket->ticketID);
    getchar(); // clear buffer

    printf("Enter Name: ");
    fgets(newTicket->name, sizeof(newTicket->name), stdin);
    newTicket->name[strcspn(newTicket->name, "\n")] = 0;

    printf("Enter Destination: ");
    fgets(newTicket->destination, sizeof(newTicket->destination), stdin);
    newTicket->destination[strcspn(newTicket->destination, "\n")] = 0;

    printf("Enter Date (DD-MM-YYYY): ");
    fgets(newTicket->date, sizeof(newTicket->date), stdin);
    newTicket->date[strcspn(newTicket->date, "\n")] = 0;

    printf("Enter Seat Number: ");
    scanf("%d", &newTicket->seatNumber);

    newTicket->next = NULL;

    if (rear == NULL) {
        front = rear = newTicket;
    } else {
        rear->next = newTicket;
        rear = newTicket;
    }

    printf("\n✅ Ticket booked and added to queue!\n");
}

// Display all tickets
void viewTickets() {
    if (front == NULL) {
        printf("\n❗ No tickets in queue.\n");
        return;
    }

    struct Ticket* temp = front;
    printf("\n🎟️ Tickets in Queue:\n");
    printf("----------------------------------------\n");

    while (temp != NULL) {
        printf("Ticket ID   : %d\n", temp->ticketID);
        printf("Name        : %s\n", temp->name);
        printf("Destination : %s\n", temp->destination);
        printf("Date        : %s\n", temp->date);
        printf("Seat Number : %d\n", temp->seatNumber);
        printf("----------------------------------------\n");
        temp = temp->next;
    }
}

// Cancel a ticket by Ticket ID
void cancelTicket() {
    int id;
    printf("Enter Ticket ID to cancel: ");
    scanf("%d", &id);

    struct Ticket *temp = front, *prev = NULL;
    while (temp != NULL && temp->ticketID != id) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == NULL) {
        printf("❌ Ticket ID %d not found in queue.\n", id);
        return;
    }

    if (temp == front) {
        front = front->next;
        if (front == NULL) rear = NULL;
    } else {
        prev->next = temp->next;
        if (temp == rear) rear = prev;
    }

    free(temp);
    printf("✅ Ticket ID %d cancelled successfully.\n", id);
}

// Main function
int main() {
    int choice;

    do {
        printf("\n===== QUEUE-BASED TICKET SYSTEM =====\n");
        printf("1. Book Ticket\n");
        printf("2. View All Tickets\n");
        printf("3. Cancel Ticket by ID\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        getchar(); // clear buffer

        switch (choice) {
            case 1: bookTicket(); break;
            case 2: viewTickets(); break;
            case 3: cancelTicket(); break;
            case 4: printf("👋 Exiting system.\n"); break;
            default: printf("❗ Invalid choice.\n");
        }
    } while (choice != 4);

    return 0;
}
