// 17.1
let rec pow = function
  | (s, n) when n <= 0 -> ""
  | (s, 1) -> s
  | (s, n) -> s + pow(s, n - 1)

// 17.2
let rec isIthChar = function
  | (s, n, c) when n < 0 || n >= String.length s -> false
  | (s, n, c) -> s.[n] = c

// 17.3
let boolToInt = function
  | true -> 1
  | false -> 0

let rec occFromIth = function
  | (s, n, c) when n < 0 || n >= String.length s -> 0
  | ("", 0, c) -> 0
  | (s, 0, c) -> boolToInt(s.[0] = c) + occFromIth(s.[1..], 0, c)
  | (s, n, c) -> occFromIth(s.[n..], 0, c)