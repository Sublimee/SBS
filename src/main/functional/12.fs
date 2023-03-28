let rec upto = function
    | 1 -> [1]
    | n -> upto(n - 1) @ [n]
 
let rec dnto = function
    | 1 -> [1]
    | n -> n :: dnto(n - 1)
 
let rec evenn = function
    | n when n < 1 -> []
    | n -> evenn(n - 1) @ [2 * (n - 1)]
