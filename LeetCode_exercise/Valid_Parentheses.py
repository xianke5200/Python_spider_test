class Solution:
    def isValid(self, s: str) -> bool:
        paren_dict = {'(': ')', '{': '}', '[': ']'}
        paren_list = []
        count = 0
        for c in s:
            if c in paren_dict.keys():
                paren_list.append(c)
                count += 1
            else:
                # print(c, paren_list[-1], paren_dict[paren_list[-1]])
                if len(paren_list) > 0 and c == paren_dict[paren_list[-1]]:
                    count -= 1
                    paren_list.pop(-1)
                else:
                    return False
        if count == 0:
            return True
        return False


if __name__ == '__main__':
    solut = Solution()
    para = "]"
    print(solut.isValid(para))
