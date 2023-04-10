let rec split xs =
  match xs with
    | [] -> []
    | head :: tail -> [[head]] @ (split tail)

let rec cartesian = function
 | ([],[]) -> []
 | (xs,[]) -> []
 | ([],ys) -> []
 | (x::xs, ys) -> (List.map(fun y -> x @ y) ys) @ (cartesian (xs,ys))

let rec all = function
 | ([],_,_) -> []
 | (_,[],_) -> []
 | (_,_,0) -> []
 | (xs,ys,1) -> ys
 | (xs,ys,k) -> all(xs, cartesian(xs, ys), k - 1)

let allSubsets n k = 
    let a = Set.ofList (List.filter(fun x -> (Set.count x) = k) (List.map(fun y -> set y) (all(split([1 .. n]), split([1 .. n]), k))))
    if (Set.count a = 0) then set[set[]] else a
