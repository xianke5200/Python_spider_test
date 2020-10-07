class Solution:
    def findMedianSortedArrays(self, nums1, nums2) -> float:
        i = 0
        j = 0
        merge_list = []
        nums1_len = len(nums1)
        nums2_len = len(nums2)

        while(i < nums1_len and j < nums2_len):
            if nums1[i] < nums2[j]:
                merge_list.append(nums1[i])
                i += 1
            else:
                merge_list.append(nums2[j])
                j += 1

        if i == nums1_len:
            merge_list += nums2[j:nums2_len]

        if j == nums2_len:
            merge_list += nums1[i:nums1_len]

        merge_list_len = len(merge_list)

        if merge_list_len % 2 == 1:
            return merge_list[merge_list_len//2]
        else:
            return (merge_list[merge_list_len//2 -1] + merge_list[merge_list_len//2])/2

    def findMedianSortedArray_1(self, nums1, nums2) -> float:
        merge_list = nums1 + nums2

        merge_list = sorted(merge_list)

        merge_list_len = len(merge_list)

        if merge_list_len % 2 == 1:
            return merge_list[merge_list_len//2]
        else:
            return (merge_list[merge_list_len//2 -1] + merge_list[merge_list_len//2])/2

solut = Solution()
para = [1, 2]
para_1 = [3, 4]
print(solut.findMedianSortedArray_1(para, para_1))