class Solution:
    def reverse(self, x: int) -> int:
        s = str(x)
        if x > 0:
            s = s[::-1]
        else:
            s =s[0]+s[1:][::-1]
        return int(s)

solut = Solution()
x = 1534236469
print(solut.reverse(x))