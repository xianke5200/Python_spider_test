class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        s_len = len(s)
        p_len = len(p)
        print(p_len, s_len)

        i = 0
        j = 0
        j_temp = 0

        while p[i]:
            if p[i] == '.':
                if (i+1) < p_len and  p[i+1] == '*':
                    return True
                else:
                    i += 1
                    j += 1
                    if i >= p_len and j >= s_len:
                        print('true 2')
                        return True
                    elif i < p_len and j < s_len:
                        pass
                    elif i < p_len and j >= s_len:
                         try:
                            if p[i+1] == '*' and (i+2) == p_len:
                                return True
                         except:
                            return False
                         return False
                    else:
                        print('false 2')
                        return False
            elif p[i] == s[j]:
                if (i+1) < p_len and p[i+1] == '*':
                    j_temp += 1
                    if (j+j_temp) < s_len and p[i] != s[j+j_temp]:
                        j = j+j_temp
                        j_temp = 0
                        i += 2
                    elif (j+j_temp) == s_len:
                        print('true 3')
                        return True
                elif (i+1) >= p_len and (j+1) >= s_len:
                    if p[i] == s[j]:
                        print('true 4')
                        return True
                    else:
                        print('false 3: ', i, j)
                        return False
                else:
                    i += 1
                    j += 1
                    if i >= p_len and j >= s_len:
                        print('true 5')
                        return True
                    elif i < p_len and j < s_len:
                        pass
                    elif i < p_len and j >= s_len:
                        try:
                            if p[i+1] == '*' and (i+2) == p_len:
                                return True
                        except:
                            return False
                        return False
                    else:
                        print('false 4')
                        return False
            else:
                if (i+1) < p_len and p[i+1] == '*':
                    i += 2
                elif (i+1) >= p_len:
                    print('error 5')
                    return False

                if i >= p_len:
                    return False

        return True



solut = Solution()
para = "a"
para_1 = "ab*"
print(solut.isMatch(para, para_1))