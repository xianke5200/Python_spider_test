class Solution:
    # def romanToInt(self, s: str) -> int:
    #     data = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD',
    #             100: 'C', 90: 'XC', 50: 'L', 40: 'XL',
    #             10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
    #     int_num = 0
    #     i = 0
    #     for n, sub in data.items():
    #         while True:
    #             if s[i] == sub:
    #                 int_num += n
    #                 i += 1
    #             elif s[i:i+2] == sub:
    #                 int_num += n
    #                 i += 2
    #             else:
    #                 break
    #             if i >= len(s):
    #                 return int_num
    #
    #     return int_num

    def romanToInt(self, s: str) -> int:
        data = {'M': 1000, 'D': 500,
                'C': 100, 'L': 50,
                'X': 10, 'V': 5, 'I': 1}
        int_num = 0
        for i in range(len(s)):
            if i < len(s)-1 and data[s[i]] < data[s[i+1]]:
                int_num -= data[s[i]]
            else:
                int_num += data[s[i]]

        return int_num


solut = Solution()
para = "MCMXCIV"
print(solut.romanToInt(para))