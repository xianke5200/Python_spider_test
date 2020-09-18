class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows < 2: return s
        conver_list = ["" for _ in range(numRows)]
        flag = -1
        i = 0
        for c in s:
            conver_list[i] += c
            if i == 0 or i == numRows-1:
                flag = -flag
            i += flag

        return "".join(conver_list)

solut = Solution()
str = "Lc"
print(solut.convert(str, 1))
