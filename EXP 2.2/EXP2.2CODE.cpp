#include <bits/stdc++.h>
using namespace std;

int dp[1001][1001]; // dp[index][target]

// Recursive function with memo (top-down)
bool subsetSum(int index, vector<int>& arr, int target) {

    // Base conditions
    if (target == 0) return true;   // Found subset
    if (index == 0) return (arr[0] == target);

    // Check memo
    if (dp[index][target] != -1) return dp[index][target];

    // Not-pick (skip current element)
    bool notPick = subsetSum(index - 1, arr, target);

    // Pick (include current element if possible)
    bool pick = false;
    if (arr[index] <= target)
        pick = subsetSum(index - 1, arr, target - arr[index]);

    // Store and return result
    return dp[index][target] = (pick || notPick);
}

int main() {
    int n;
    cout << "Enter number of elements: ";
    cin >> n;

    vector<int> arr(n);
    cout << "Enter elements: ";
    for (int i = 0; i < n; i++)
        cin >> arr[i];

    int target;
    cout << "Enter target sum: ";
    cin >> target;

    // Initialize DP with -1 (unknown)
    memset(dp, -1, sizeof(dp));

    if (subsetSum(n - 1, arr, target))
        cout << "YES, subset with sum " << target << " exists.\n";
    else
        cout << "NO, subset with sum " << target << " does not exist.\n";

    return 0;
}
