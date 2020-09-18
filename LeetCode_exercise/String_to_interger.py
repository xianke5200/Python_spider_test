import re

class Solution:
    def myAtoi(self, str: str) -> int:
        if not str: return 0
        find = 0
        sign = -1
        start = len(str)
        end = len(str)
        for i in range(len(str)):
            if str[i] in "-":
                if find == 0:
                    if sign == -1:
                        sign = 1
                    else:
                        return 0
                else:
                    end = i
                    break
                continue
            if str[i] in "+":
                if find == 0:
                    if sign == -1:
                        sign = 0
                    else:
                        return 0
                else:
                    end = i
                    break
                continue

            if str[i] in " " and find == 0:
                if sign != -1:
                    return 0
                continue

            if str[i] in "1234567890":
                if find == 0:
                    find = 1
                    start = i
            else:
                end = i
                break

        print(i, start, end, str[i])
        if start < end:
            x = int(str[start:end])
        else:
            return 0
        if sign>0:
            x = -x

        return min(max(x, -2147483648), 2147483648-1)

    def myAtoi_1(self, str: str) -> int:
        patern = re.compile('([ ]*[\-\+]?[0-9]+)', re.S)
        res = re.match(patern, str)
        try:
            x = int(res.group())
        except:
            x = 0
        return min(max(x, -2147483648), 2147483648-1)

solut = Solution()
s = "+1241"
print(solut.myAtoi_1(s))