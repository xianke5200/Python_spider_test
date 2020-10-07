class Solution:
    # def intToRoman(self, num: int) -> str:
    #     thousand_bit = num//1000
    #     hundred_bit = num%1000//100
    #     ten_bit = num%100//10
    #     single_bit = num%10
    #     roman = ""+'M'*thousand_bit
    #     if hundred_bit < 4:
    #         roman += 'C'*hundred_bit
    #     elif hundred_bit >= 5 and hundred_bit < 9:
    #         roman += 'D' + 'C'*(hundred_bit-5)
    #     elif hundred_bit == 4:
    #         roman += 'CD'
    #     elif hundred_bit == 9:
    #         roman += 'CM'
    #
    #     if ten_bit < 4:
    #         roman += 'X'*ten_bit
    #     elif ten_bit >= 5 and ten_bit < 9:
    #         roman += 'L' + 'X'*(ten_bit-5)
    #     elif ten_bit == 4:
    #         roman += 'XL'
    #     elif ten_bit == 9:
    #         roman += 'XC'
    #
    #     if single_bit < 4:
    #         roman += 'I'*single_bit
    #     elif single_bit >= 5 and single_bit < 9:
    #         roman += 'V' + 'I'*(single_bit-5)
    #     elif single_bit == 4:
    #         roman += 'IV'
    #     elif single_bit == 9:
    #         roman += 'IX'
    #
    #     return roman

    def intToRoman(self, num: int) -> str:
        data = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD',
                100: 'C', 90: 'XC', 50: 'L', 40: 'XL',
                10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
        roman = ''
        for n, s in data.items():
            a = num//n
            if a > 0:
                roman += s*a
                num -= a*n
        return roman


solut = Solution()
para = 3999
print(solut.intToRoman(para))