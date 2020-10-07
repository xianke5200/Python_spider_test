from itertools import product


class Solution:
    def letterCombinations(self, digits):
        if not digits: return []
        num_dict = {"2": ['a', 'b', 'c'], "3": ['d', 'e', 'f'], "4": ['g', 'h', 'i'],
                    "5": ['j', 'k', 'l'], "6": ['m', 'n', 'o'], "7": ['p', 'q', 'r', 's'],
                    "8": ['t', 'u', 'v'], "9": ['w', 'x', 'y', 'z']}
        num_list = []
        res = []
        for c in digits:
            num_list.append(num_dict[c])

        for combin in product(*num_list):
            res.append("".join(combin))

        return res


if __name__ == '__main__':
    solut = Solution()
    para = ""
    print(solut.letterCombinations(para))
