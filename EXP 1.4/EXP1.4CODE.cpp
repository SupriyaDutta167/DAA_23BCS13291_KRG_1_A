#include <iostream>
using namespace std;

// ---------------- Doubly Linked List ----------------
struct DNode {
    int data;
    DNode* prev;
    DNode* next;
};

class DoublyLinkedList {
    DNode* head;
public:
    DoublyLinkedList() : head(NULL) {}

    // Insert at beginning
    void insertAtBegin(int val) {
        DNode* newNode = new DNode{val, NULL, head};
        if (head != NULL)
            head->prev = newNode;
        head = newNode;
    }

    // Insert at end
    void insertAtEnd(int val) {
        DNode* newNode = new DNode{val, NULL, NULL};
        if (head == NULL) {
            head = newNode;
            return;
        }
        DNode* temp = head;
        while (temp->next) temp = temp->next;
        temp->next = newNode;
        newNode->prev = temp;
    }

    // Delete from beginning
    void deleteAtBegin() {
        if (head == NULL) return;
        DNode* temp = head;
        head = head->next;
        if (head) head->prev = NULL;
        delete temp;
    }

    // Delete from end
    void deleteAtEnd() {
        if (head == NULL) return;
        if (head->next == NULL) {
            delete head;
            head = NULL;
            return;
        }
        DNode* temp = head;
        while (temp->next) temp = temp->next;
        temp->prev->next = NULL;
        delete temp;
    }

    // Display list
    void display() {
        DNode* temp = head;
        cout << "Doubly List: ";
        while (temp) {
            cout << temp->data << " ";
            temp = temp->next;
        }
        cout << "\n";
    }
};

// ---------------- Circular Linked List ----------------
struct CNode {
    int data;
    CNode* next;
};

class CircularLinkedList {
    CNode* tail;  // tail pointer (helps for both begin and end ops)
public:
    CircularLinkedList() : tail(NULL) {}

    // Insert at beginning
    void insertAtBegin(int val) {
        CNode* newNode = new CNode{val, NULL};
        if (tail == NULL) {
            tail = newNode;
            tail->next = tail;
        } else {
            newNode->next = tail->next;
            tail->next = newNode;
        }
    }

    // Insert at end
    void insertAtEnd(int val) {
        CNode* newNode = new CNode{val, NULL};
        if (tail == NULL) {
            tail = newNode;
            tail->next = tail;
        } else {
            newNode->next = tail->next;
            tail->next = newNode;
            tail = newNode;
        }
    }

    // Delete at beginning
    void deleteAtBegin() {
        if (tail == NULL) return;
        CNode* head = tail->next;
        if (head == tail) { // only one node
            delete head;
            tail = NULL;
        } else {
            tail->next = head->next;
            delete head;
        }
    }

    // Delete at end
    void deleteAtEnd() {
        if (tail == NULL) return;
        CNode* head = tail->next;
        if (head == tail) { // only one node
            delete tail;
            tail = NULL;
        } else {
            CNode* temp = head;
            while (temp->next != tail) temp = temp->next;
            temp->next = tail->next;
            delete tail;
            tail = temp;
        }
    }

    // Display
    void display() {
        if (tail == NULL) {
            cout << "Circular List is empty\n";
            return;
        }
        CNode* temp = tail->next;
        cout << "Circular List: ";
        do {
            cout << temp->data << " ";
            temp = temp->next;
        } while (temp != tail->next);
        cout << "\n";
    }
};

// ---------------- Main ----------------
int main() {
    DoublyLinkedList dll;
    CircularLinkedList cll;

    // Demo Doubly Linked List
    cout << "=== Doubly Linked List Operations ===\n";
    dll.insertAtBegin(10);
    dll.insertAtEnd(20);
    dll.insertAtBegin(5);
    dll.display();
    dll.deleteAtBegin();
    dll.display();
    dll.deleteAtEnd();
    dll.display();

    // Demo Circular Linked List
    cout << "\n=== Circular Linked List Operations ===\n";
    cll.insertAtBegin(10);
    cll.insertAtEnd(20);
    cll.insertAtBegin(5);
    cll.display();
    cll.deleteAtBegin();
    cll.display();
    cll.deleteAtEnd();
    cll.display();

    return 0;
}
