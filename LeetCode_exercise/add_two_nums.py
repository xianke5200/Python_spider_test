# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        carry= 0
        r = ListNode(0)
        re = r
        while(l1 or l2):
            x = l1.val if l1 else 0
            y = l2.val if l2 else 0
            sum = carry + x + y
            carry = sum // 10
            re.next = ListNode(sum % 10)
            if l1 != None: l1 = l1.next
            if l2 != None: l2 = l2.next
            re = re.next
        if carry: re.next = ListNode(1)
        return r.next