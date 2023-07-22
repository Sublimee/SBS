let even_seq = Seq.initInfinite (fun i -> 2 * i + 2)

let rec factorial n =
  if n <= 1 then 1
  else n * factorial (n - 1)
  
let fac_seq = Seq.initInfinite factorial

let sequence n =
  match n with
    | n when n % 2 = 0 -> n / 2
    | n -> n / 2 - n

let seq_seq = Seq.initInfinite sequence
