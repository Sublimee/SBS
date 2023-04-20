let rec fibo1 n n1 n2 =
  match n with
    | 0 -> n2
    | 1 -> n1
    | n -> fibo1 (n - 1) (n1 + n2) n1

let rec fibo2 n c = 
  let f = fun x -> c x
  match n with
    | 0 -> c 0
    | 1 -> c 1
    | n -> fibo2 (n - 1) f + fibo2 (n - 2) f

let rec bigList n k =
  let rec f counter list =
    match counter with
      | 0 -> k list
      | counter -> f (counter - 1) (1 :: (k list))
  f n []
