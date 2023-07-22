let rec rmodd = function
  | head :: (tail_head :: tail) -> tail_head :: rmodd tail
  | [x] -> []
  | []  -> []

let rec del_even = function
  | [] -> []
  | head :: tail when head % 2 = 0 -> del_even tail 
  | head :: tail -> head :: (del_even tail)  

let rec multiplicity x xs =
  match x, xs with
  | x, [] -> 0
  | x, head :: tail when head = x -> 1 + (multiplicity x tail)
  | x, head :: tail -> multiplicity x tail

let rec rmeven = function 
  | head :: (head2 :: tail) -> head :: rmeven tail 
  | [head] -> [head] 
  | _ -> []

let rec split = fun list -> (rmeven list, rmodd list)

let rec zip (xs1,xs2) =
  match xs1, xs2 with
  | [], [] -> []
  | xs1, xs2 when (xs1.Length <> xs2.Length) -> failwith "exception"
  | head1 :: tail1, head2 :: tail2 -> [(head1, head2)] @ zip (tail1, tail2)
