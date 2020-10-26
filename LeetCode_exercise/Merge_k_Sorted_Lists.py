# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists):
        if len(lists) < 1: return []
        res = []
        for lst in lists:
            res.extend(lst)

        res.sort()

        return res


if __name__ == '__main__':
    solut = Solution()
    para = []
    print(solut.mergeKLists(para))
