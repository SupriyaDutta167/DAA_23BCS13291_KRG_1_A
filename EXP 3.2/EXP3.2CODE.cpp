#include <iostream>
#include <string>
using namespace std;

#define d 256  // Number of characters in input alphabet

void RabinKarpSearch(string text, string pattern, int q) {
    int n = text.length();
    int m = pattern.length();
    int i, j;
    int p = 0; // hash value for pattern
    int t = 0; // hash value for text
    int h = 1;

    // The value of h would be "pow(d, m-1) % q"
    for (i = 0; i < m - 1; i++)
        h = (h * d) % q;

    // Calculate the hash value of pattern and first window of text
    for (i = 0; i < m; i++) {
        p = (d * p + pattern[i]) % q;
        t = (d * t + text[i]) % q;
    }

    // Slide the pattern over text one by one
    for (i = 0; i <= n - m; i++) {
        // Check the hash values of current window of text and pattern
        if (p == t) {
            // Check characters one by one
            for (j = 0; j < m; j++) {
                if (text[i + j] != pattern[j])
                    break;
            }
            if (j == m)
                cout << "Pattern found at index " << i << endl;
        }

        // Calculate hash value for next window of text
        if (i < n - m) {
            t = (d * (t - text[i] * h) + text[i + m]) % q;

            // We might get negative value of t, convert it to positive
            if (t < 0)
                t = (t + q);
        }
    }
}

int main() {
    string text, pattern;
    int q; // A prime number

    cout << "Enter the text: ";
    getline(cin, text);

    cout << "Enter the pattern: ";
    getline(cin, pattern);

    cout << "Enter a prime number for hashing: ";
    cin >> q;

    RabinKarpSearch(text, pattern, q);

    return 0;
}
