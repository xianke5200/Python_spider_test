class Solution:
    def threeSumClosest(self, nums, target: int) -> int:
        nums_length = len(nums)
        # if nums_length < 4:
        #     return
        min_gap = 10000
        closest_sum = 0
        nums.sort()

        for i in range(nums_length):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            left = i + 1
            right = nums_length - 1
            while left < right:
                three_sum = nums[i] + nums[left] + nums[right]

                if three_sum == target:
                    return three_sum
                elif three_sum > target:
                    right -= 1
                else:
                    left += 1

                if min_gap > abs(three_sum - target):
                    min_gap = abs(three_sum - target)
                    closest_sum = three_sum

        return closest_sum


if __name__ == '__main__':
    solut = Solution()
    para = [1,1,1,1]
    print(solut.threeSumClosest(para, 0))
