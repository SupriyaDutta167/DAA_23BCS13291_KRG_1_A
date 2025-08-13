class Solution {
public:
    // Function to count the frequency of all elements from 1 to N in the array in O(1) extra space
    vector<int> frequencyCount(vector<int>& arr) {
        int n = arr.size();

        // Step 1: Decrease each element by 1 so elements become in range 0..n-1
        for (int i = 0; i < n; i++) {
            arr[i]--;
        }

        // Step 2: Use elements as index and store counts in the same array
        for (int i = 0; i < n; i++) {
            arr[arr[i] % n] += n;
        }

        // Step 3: Extract frequencies
        for (int i = 0; i < n; i++) {
            arr[i] = arr[i] / n;  // Frequency of (i+1)
        }

        return arr;
    }
};