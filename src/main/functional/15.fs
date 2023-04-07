let list_filter f xs = List.foldBack (fun head tail -> if f head then (head::tail) else tail) xs []

let sum (p, xs) = List.fold (+) 0 (List.filter p xs)

let revrev = fun xs -> List.fold (fun head tail -> (List.rev tail) :: head) [] xs
