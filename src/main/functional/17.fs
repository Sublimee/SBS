let try_find key m = 
  let list = Map.toList m
  let rec iterate(list, key) = 
    match list with
      | [] -> None
      | (k, v) :: tail when k = key -> Some(v) 
      | (k, v) :: tail -> iterate(tail, key)
  iterate(list, key)
