import re

def find_suggestions(inputStr, outputStr):

    def lcs_matrix(a, b):
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp


    def traceback_lcs(dp, a, b):
        i, j = len(a), len(b)
        lcs_indices = []
        while i > 0 and j > 0:
            if a[i - 1] == b[j - 1]:
                lcs_indices.append((i - 1, j - 1))
                i -= 1
                j -= 1
            elif dp[i - 1][j] >= dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        return lcs_indices[::-1]


    def split_with_indices(s):
        tokens = []
        indices = []
        for match in re.finditer(r'\S+|\s+', s):
            tokens.append(match.group())
            indices.append((match.start(), match.end()))
        return tokens, indices

    input_tokens, input_indices = split_with_indices(inputStr)
    output_tokens, output_indices = split_with_indices(outputStr)


    dp = lcs_matrix(input_tokens, output_tokens)
    lcs_indices = traceback_lcs(dp, input_tokens, output_tokens)

    suggestions = []
    input_idx = 0
    output_idx = 0
    lcs_pos = 0

    while input_idx < len(input_tokens) or output_idx < len(output_tokens):
        if (lcs_pos < len(lcs_indices) and
            input_idx < len(input_tokens) and
            output_idx < len(output_tokens) and
            input_idx == lcs_indices[lcs_pos][0] and
            output_idx == lcs_indices[lcs_pos][1]):
            
            input_idx += 1
            output_idx += 1
            lcs_pos += 1
        else:
            
            if input_idx < len(input_tokens):
                start_input, end_input = input_indices[input_idx]
            else:
                start_input, end_input = len(inputStr), len(inputStr)
            if output_idx < len(output_tokens):
                suggest = output_tokens[output_idx]
                output_idx += 1
            else:
                suggest = ''
            suggestions.append({
                "start": start_input,
                "end": end_input - 1,
                "suggest": suggest
            })
            if input_idx < len(input_tokens):
                input_idx += 1

    print("Input:", inputStr)
    print("Output:", outputStr)
    print("Suggestions:", suggestions)
    return suggestions


