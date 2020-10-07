class Solution:
    def longestCommonPrefix(self, strs) -> str:
        comon_str = ""
        if not strs: return comon_str
        for i, c in enumerate(strs[0]):
            find = 1
            for j in range(len(strs)):
                if i != strs[j].find(c, i):
                    find = 0
                    return comon_str

            if find:
                comon_str += c

        return comon_str

    def longestCommonPrefix(self, strs) -> str:
        ans = ''
        for x in zip(*strs):
            if len(set(x)) == 1:
                ans += x[0]
            else:
                break
        return ans

solut = Solution()
para = ["flower", "flow", "flight"]
print(solut.longestCommonPrefix(para))