class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) <= 1 : return s

        left = 0
        right = 0
        sub_len = 0
        pre_len = 0
        lookup_i = []
        lookup_j = []
        for i in range(len(s)):
            left = i -1
            right = i + 1
            if left < 0 or right >= len(s):
                sub_len = right - left - 1
                if sub_len > pre_len:
                    lookup_i = s[left+1:right]
                    pre_len = sub_len
                continue

            print(left, right)

            while s[left] == s[right]:
                sub_len = right - left + 1
                if sub_len > pre_len:
                    lookup_i = s[left:right + 1]
                    pre_len = sub_len

                left -= 1
                right += 1
                if left < 0 or right >= len(s):
                    break

        for i in range(len(s)):
            left = i
            right = i + 1
            if left < 0 or right >= len(s):
                continue

            print(left, right)

            while s[left] == s[right]:
                sub_len = right - left + 1
                if sub_len > pre_len:
                    lookup_j = s[left:right + 1]
                    pre_len = sub_len

                left -= 1
                right += 1
                if left < 0 or right >= len(s):
                    break

        return lookup_i if len(lookup_i) > len(lookup_j) else lookup_j

    def longestPalindrome_1(self, s: str) -> str:
        if not s : return ""
        if len(s) < 2 or s == s[::-1]:
            return s

        max_len = 1
        start = 0
        for i in range(1, len(s)):
            evens = s[i-max_len:i+1]
            odds = s[i-max_len-1:i+1]

            if i-max_len >= 0 and evens == evens[::-1]:
                start = i-max_len
                max_len += 1
                continue

            if i-max_len-1 >= 0 and odds == odds[::-1]:
                start = i-max_len-1
                max_len += 2
                continue

        return s[start:start+max_len]

str = 'abadd'
solut = Solution()
print(solut.longestPalindrome(str))
print(solut.longestPalindrome_1(str))