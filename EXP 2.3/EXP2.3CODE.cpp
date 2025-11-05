#include <bits/stdc++.h>
using namespace std;

int dp[1001][1001]; // dp[i][w] = max profit using first i items with capacity w

// Recursive function with memoization
int knapsack(int index, int W, vector<int>& w, vector<int>& v) {
    if (index < 0 || W == 0) return 0;

    if (dp[index][W] != -1) return dp[index][W];

    // Not-pick
    int notPick = knapsack(index - 1, W, w, v);

    // Pick (if weight allows)
    int pick = 0;
    if (w[index] <= W)
        pick = v[index] + knapsack(index - 1, W - w[index], w, v);

    return dp[index][W] = max(pick, notPick);
}

int main() {
    int n, W;
    cout << "Enter number of items: ";
    cin >> n;

    vector<int> w(n), v(n);
    cout << "Enter weights: ";
    for (int i = 0; i < n; i++) cin >> w[i];
    cout << "Enter profits: ";
    for (int i = 0; i < n; i++) cin >> v[i];

    cout << "Enter maximum capacity of knapsack: ";
    cin >> W;

    memset(dp, -1, sizeof(dp));
    int maxProfit = knapsack(n - 1, W, w, v);

    cout << "\nMaximum Profit = " << maxProfit << "\n";

    // Traceback to find items picked
    vector<int> itemsPicked;
    int remainingW = W;
    for (int i = n - 1; i >= 0; i--) {
        if (i == 0) {
            if (dp[i][remainingW] > 0) itemsPicked.push_back(i + 1);
            break;
        }
        if (dp[i][remainingW] != dp[i - 1][remainingW]) {
            itemsPicked.push_back(i + 1); // Item i was picked
            remainingW -= w[i];
        }
    }

    cout << "Items picked (1-based index): ";
    for (auto it = itemsPicked.rbegin(); it != itemsPicked.rend(); ++it)
        cout << *it << " ";
    cout << endl;

    return 0;
}
