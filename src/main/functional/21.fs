let fac_seq =
  seq {
    yield 1
    let mutable acc = 1
    let mutable i = 1
    while true do
      acc <- acc * i
      yield acc
      i <- i + 1
  }

let seq_seq =
  seq {
    yield 0
    let mutable i = 1
    while true do
      yield -i
      yield i
      i <- i + 1
  }
