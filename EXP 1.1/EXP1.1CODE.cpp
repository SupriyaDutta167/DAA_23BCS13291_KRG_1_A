#include <iostream>
using namespace std;

template <class T, int SIZE>
class Stack {
private:
    T arr[SIZE];
    int top;

public:
    Stack() : top(-1) {}

    bool isEmpty() {
        return top == -1;
    }

    bool isFull() {
        return top == SIZE - 1;
    }

    void push(T value) {
        if (isFull()) {
            cout << "Stack Overflow! Cannot push " << value << endl;
        } else {
            arr[++top] = value;
            cout << value << " pushed into stack." << endl;
        }
    }

    void pop() {
        if (isEmpty()) {
            cout << "Stack Underflow! Cannot pop." << endl;
        } else {
            cout << arr[top--] << " popped from stack." << endl;
        }
    }

    T peek() {
        if (isEmpty()) {
            cout << "Stack is empty. No top element." << endl;
            return T(); // return default value
        } else {
            return arr[top];
        }
    }
};

int main() {
    Stack<int, 5> s;  // Stack of int type, size 5

    s.push(10);
    s.push(20);
    s.push(30);
    s.push(40);
    s.push(50);

    cout << "Top element: " << s.peek() << endl;

    s.pop();
    cout << "Top element after pop: " << s.peek() << endl;

    s.push(60); // Will show overflow if already full

    while (!s.isEmpty()) {
        s.pop();
    }

    s.pop(); // Underflow example

    return 0;
}
