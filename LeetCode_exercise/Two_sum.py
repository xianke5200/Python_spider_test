class Solution:
    def __init__(self, nums, target):
        self.nums = nums
        self.target = target

    def twoSum(self):
        '''
        :param nums: List[int]
        :param target: int
        :return: List[int]
        '''
        hashdict = {}
        for index, num in enumerate(nums):
            another = target - num
            if another in hashdict:
                return [hashdict[another], index]
            hashdict[num] = index

if __name__ == '__main__':
    nums = [2, 7, 11, 15]
    target = 9
    Solut = Solution(nums, target)
    print(Solut.twoSum())