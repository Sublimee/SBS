type TimeOfDay = { hours: int; minutes: int; f: string }

let evaluate x = function
    | x when x > 0 -> true
    | x -> false
    
let format = function
    | (hours, minutes, f) when f = "PM" -> (hours + 12) * 60 + minutes
    | (hours, minutes, f) -> (hours * 60) + minutes
    
let (.>.) x y = evaluate (format(x) - format(y))
