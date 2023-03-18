// 23.4.1
let rec format = function
    | (g, s, c) when c > 11 -> format (g, s + (c / 12), c % 12)
    | (g, s, c) when s > 19 -> format (g + (s / 20), s % 20, c)
    | (g, s, c) when c < 0 && s > 0 -> format (g, s - 1, c + 12)
    | (g, s, c) when c < 0 && g > 0 -> format (g - 1, s + 19, c + 12)
    | (g, s, c) when s < 0 && g > 0 -> format (g - 1, s + 20, c)
    | (g, s, c) -> (g, s, c)
    
let (.+.) x y =
    let (g1, s1, c1) = x
    let (g2, s2, c2) = y
    format (g1 + g2, s1 + s2, c1 + c2)

let (.-.) x y =
    let (g1, s1, c1) = x
    let (g2, s2,c2) = y
    format (g1 - g2, s1 - s2, c1 - c1)

// 23.4.2
let (.+) x y =
    let (a, b) = x
    let (c, d) = y
    (a + c, b + d)
    
let (.-) x y =
    let (a, b) = x
    let (c, d) = y
    (a - c, b - d)
    
let (.*) x y =
    let (a, b) = x
    let (c, d) = y
    (a * c - b * d, b * c + a * d)
    
let (./) x y =
    let (a, b) = x
    let (c, d) = y
    (a, b) .* (c / (c * c + d * d) , -d / (c * c + d * d))
