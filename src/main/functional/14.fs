let rec sum (p, xs) = 
  match xs with
    | [] -> 0
    | head :: tail when p(head) -> head + sum(p, tail)
    | head :: tail -> sum(p, tail)

let rec count (xs, n) =
  match xs with
    | [] -> 0
    | head :: tail when head < n -> 0 + count(tail, n)
    | head :: tail when head = n -> 1 + count(tail, n)
    | head :: tail when head > n -> 0

let rec insert (xs, n) =
  match xs with
    | [] -> [n]
    | head :: tail when head < n -> head :: insert(tail, n)
    | head :: tail when head >= n -> n :: xs

let rec intersect (xs1, xs2) =
  match xs1, xs2 with
    | [], _ -> []
    | _, [] -> []
    | head1 :: tail1, head2 :: tail2 when head1 < head2 -> intersect(tail1, xs2)
    | head1 :: tail1, head2 :: tail2 when head1 = head2 -> head1 :: intersect(tail1, tail2)
    | head1 :: tail1, head2 :: tail2 when head1 > head2 -> intersect(xs1, tail2)

let rec plus (xs1, xs2) =
  match xs1, xs2 with
    | [], xs2 -> xs2
    | xs1, [] -> xs1
    | head1 :: tail1, head2 :: tail2 when head1 < head2 -> head1 :: plus(tail1, xs2)
    | head1 :: tail1, head2 :: tail2 when head1 = head2 -> head1 :: (head1 :: plus(tail1, tail2))
    | head1 :: tail1, head2 :: tail2 when head1 > head2 -> head2 :: plus(xs1, tail2)

let rec minus (xs1, xs2) =
  match xs1, xs2 with
    | [], xs2 -> []
    | xs1, [] -> xs1
    | head1 :: tail1, head2 :: tail2 when head1 < head2 -> head1 :: minus(tail1, xs2)
    | head1 :: tail1, head2 :: tail2 when head1 = head2 -> minus(tail1, tail2)
    | head1 :: tail1, head2 :: tail2 when head1 > head2 -> minus(xs1, tail2)

let rec smallest (xs : int list) =
  match xs with
    | [] -> None
    | [x] -> Some x
    | candidate :: tail -> let last_smallest = Option.get(smallest tail)
                           if (candidate < last_smallest) then Some(candidate) else Some(last_smallest)

let rec delete (n, xs) =
  match xs with
    | [] -> []
    | head :: tail when head = n -> tail
    | head :: tail -> head :: delete(n, tail)

let rec sort = function
  | [] -> []
  | xs -> let smaller = Option.get(smallest xs)
          smaller :: sort(delete(smaller, xs))

let rec revrev = function
  | [] -> []
  | [x] -> [List.rev x]
  | x :: xs -> (revrev xs) @ [List.rev x]
