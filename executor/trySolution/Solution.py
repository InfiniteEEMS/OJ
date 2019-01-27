class Solution:

    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        
        buffer_dict = {}
        
        for i in range(0,len(nums)):
            
            if buffer_dict.get(target - nums[i]) is not None:

                return [i,buffer_dict[target-nums[i]]]

            else:     

                buffer_dict[nums[i]] = i
            