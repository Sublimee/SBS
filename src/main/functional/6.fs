let rec pow = function
  | (s, 0) -> ""
  | (s, 1) -> s
  | (s, n) -> s + pow(s, n - 1)

let rec isIthChar(s, n, c) = (string s).[n] = c

let boolToInt = function
    | true -> 1
    | false -> 0

let rec occFromIth = function
  | ("", 0, c) -> 0
  | (s, 0, c) -> boolToInt((string s).[0] = c) + occFromIth(s.[1..], 0, c)
  | (s, n, c) -> occFromIth((string s).[n..], 0, c)