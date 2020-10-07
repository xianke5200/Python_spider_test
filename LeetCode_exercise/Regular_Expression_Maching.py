class Solution:
    def match_recursion(self, s_i, p_j, s, p):
        # print(s_i, p_j, self.s_len, self.p_len)
        if p_j >= self.p_len and s_i >= self.s_len:
            return True
        if p_j >= self.p_len:
            return False
        if s_i >= self.s_len:
            if (self.p_len-p_j) >= 2 and p[p_j+1] == '*':
                return self.match_recursion(s_i, p_j+2, s, p)
            return False

        if p_j+2 <= self.p_len and p[p_j+1] == '*':
            if p[p_j] != s[s_i]:
                if p[p_j] != '.':
                    return self.match_recursion(s_i, p_j+2, s, p)
                return self.match_recursion(s_i, p_j + 2, s, p) or self.match_recursion(s_i + 1, p_j, s, p)
            return self.match_recursion(s_i, p_j + 2, s, p) or self.match_recursion(s_i + 1, p_j, s, p)

        if p[p_j] != s[s_i]:
            if p[p_j] != '.':
                return False

        return self.match_recursion(s_i+1, p_j+1, s, p)

    def isMatch(self, s: str, p: str) -> bool:
        self.p_len = len(p)
        self.s_len = len(s)
        # print("s: \'%s\', p: \'%s\', " % (para[i], para_1[i]))
        return self.match_recursion(0, 0, s, p)

solut = Solution()
para = ["a", 'a', '', '', '', 'aaaaab', 'aaaab', 'aa', 'aa', 'aaa', 'aaab']
para_1 = ["ab*", 'aab', '', '.', '.*', 'aa.*b', 'aa.*bbb', 'a', 'a*', 'a*a', 'aaa.*']
for i in range(len(para)):
    print("s: \'%s\', p: \'%s\', "%(para[i], para_1[i]) , solut.isMatch(para[i], para_1[i]))
