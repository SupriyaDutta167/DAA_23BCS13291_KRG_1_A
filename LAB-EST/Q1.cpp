// Online C++ compiler to run C++ program online
#include <bits/stdc++.h>
using namespace std;

int subarraySumClosestToK(vector<int>& nums, int k) {
    int n = nums.size();
    int closest = INT_MAX;  // minimum absolute difference

    for(int i = 0; i < n; i++) {
        int sum = 0;

        // try all subarrays starting from i
        for(int j = i; j < n; j++) {
            sum += nums[j];

            // update closest difference
            closest = min(closest, abs(sum - k));
        }
    }

    return closest;
}

int main() {
    vector<int> nums = {2, -1, 3, 5};
    int k = 12;

    cout << "Minimum difference = "
         << subarraySumClosestToK(nums, k);

    return 0;
}
