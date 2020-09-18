class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0: return False
        s = str(x)
        return s == s[::-1]

    def isPalindrome_1(self, x: int) -> bool:
        if x < 0: return False
        if x%10 == 0 and x != 0:
            return False

        reversed_num = 0

        while(reversed_num < x):
            print(reversed_num, x)
            reversed_num = reversed_num*10 + x%10
            x = x//10

        return reversed_num==x or reversed_num//10 == x

solut = Solution()
para = 1210
print(solut.isPalindrome_1(para))