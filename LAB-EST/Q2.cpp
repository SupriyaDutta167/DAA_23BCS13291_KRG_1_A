class Solution {
  public:
    int minPlatform(vector<int>& arr, vector<int>& dep) {
        // code here
        
        sort(arr.begin(), arr.end());
        sort(dep.begin(), dep.end());
        
        int i=0;
        int j=0;
        int plat=0;
        int ans=0;
        
        while(i<arr.size()){
            if(arr[i]<=dep[j]){
                i++;
                plat++;
            }
            else{
                plat--;
                j++;
            }
            
            ans= max(ans,plat);
        }
        return ans;
    }
};
