class Solution:
    # def generateParenthesis(self, n: int):
    #     def generate(A):
    #         if len(A) == 2*n:
    #             if valid(A):
    #                 res.append(''.join(A))
    #         else:
    #             A.append('(')
    #             generate(A)
    #             A.pop()
    #             A.append(')')
    #             generate(A)
    #             A.pop()
    #
    #     def valid(A):
    #         count = 0
    #         for c in A:
    #             if c == '(':
    #                 count += 1
    #             else:
    #                 count -= 1
    #             if count < 0: return False
    #         return count == 0
    #
    #     res = []
    #     generate([])
    #     return res

    def generateParenthesis(self, n: int):
        def backtrack(s=[], left=n, right=n):
            if not right:
                res.append(''.join(s))
            if left:
                backtrack(s + ['('], left-1, right)
            if left < right:
                backtrack(s + [')'], left, right-1)

        res = []
        backtrack()
        return res


if __name__ == '__main__':
    solut = Solution()
    para = 3
    print(solut.generateParenthesis(para))
