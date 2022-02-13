load harness

@test "self1" {
  check 'x := 2 ; if x > 1 then x := x * x ; else y := x + 10' '⇒ skip; if (x>1) then { x := (x*x) } else { y := (x+10) }, {x → 2}
⇒ if (x>1) then { x := (x*x) } else { y := (x+10) }, {x → 2}
⇒ x := (x*x), {x → 2}
⇒ skip, {x → 4}'
}

@test "self2" {
  check 'x := 4 ; while ( x > 3 ) do { y := 10 + 10 ; x := x - 1 ; }' '⇒ skip; while (x>3) do { y := (10+10); x := (x-1) }, {x → 4}
⇒ while (x>3) do { y := (10+10); x := (x-1) }, {x → 4}
⇒ y := (10+10); x := (x-1); while (x>3) do { y := (10+10); x := (x-1) }, {x → 4}
⇒ skip; x := (x-1); while (x>3) do { y := (10+10); x := (x-1) }, {x → 4, y → 20}
⇒ x := (x-1); while (x>3) do { y := (10+10); x := (x-1) }, {x → 4, y → 20}
⇒ skip; while (x>3) do { y := (10+10); x := (x-1) }, {x → 3, y → 20}
⇒ while (x>3) do { y := (10+10); x := (x-1) }, {x → 3, y → 20}
⇒ skip, {x → 3, y → 20}'
}

@test "self3" {
  check 'while false do { x := x + 1 ; } ; a := a + 5' '⇒ skip; a := (a+5), {}
⇒ a := (a+5), {}
⇒ skip, {a → 5}'
}

@test "self4" {
  check 'a := 10 % 6 ; while ( a > 0 ) do { a := a - 1 ; b := b + a }' '⇒ skip; while (a>0) do { a := (a-1); b := (b+a) }, {a → 4}
⇒ while (a>0) do { a := (a-1); b := (b+a) }, {a → 4}
⇒ a := (a-1); b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 4}
⇒ skip; b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 3}
⇒ b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 3}
⇒ skip; while (a>0) do { a := (a-1); b := (b+a) }, {a → 3, b → 3}
⇒ while (a>0) do { a := (a-1); b := (b+a) }, {a → 3, b → 3}
⇒ a := (a-1); b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 3, b → 3}
⇒ skip; b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 2, b → 3}
⇒ b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 2, b → 3}
⇒ skip; while (a>0) do { a := (a-1); b := (b+a) }, {a → 2, b → 5}
⇒ while (a>0) do { a := (a-1); b := (b+a) }, {a → 2, b → 5}
⇒ a := (a-1); b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 2, b → 5}
⇒ skip; b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 1, b → 5}
⇒ b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 1, b → 5}
⇒ skip; while (a>0) do { a := (a-1); b := (b+a) }, {a → 1, b → 6}
⇒ while (a>0) do { a := (a-1); b := (b+a) }, {a → 1, b → 6}
⇒ a := (a-1); b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 1, b → 6}
⇒ skip; b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 0, b → 6}
⇒ b := (b+a); while (a>0) do { a := (a-1); b := (b+a) }, {a → 0, b → 6}
⇒ skip; while (a>0) do { a := (a-1); b := (b+a) }, {a → 0, b → 6}
⇒ while (a>0) do { a := (a-1); b := (b+a) }, {a → 0, b → 6}
⇒ skip, {a → 0, b → 6}'
}


@test "self5" {
  check 'if true then while ( x < 5 ) do x := x + 2 else y := 10 % 4' '⇒ while (x<5) do { x := (x+2) }, {}
⇒ x := (x+2); while (x<5) do { x := (x+2) }, {}
⇒ skip; while (x<5) do { x := (x+2) }, {x → 2}
⇒ while (x<5) do { x := (x+2) }, {x → 2}
⇒ x := (x+2); while (x<5) do { x := (x+2) }, {x → 2}
⇒ skip; while (x<5) do { x := (x+2) }, {x → 4}
⇒ while (x<5) do { x := (x+2) }, {x → 4}
⇒ x := (x+2); while (x<5) do { x := (x+2) }, {x → 4}
⇒ skip; while (x<5) do { x := (x+2) }, {x → 6}
⇒ while (x<5) do { x := (x+2) }, {x → 6}
⇒ skip, {x → 6}'
}

@test "self6" {
  check 'a := a * 2 ; b := a + 20 ; c := b * 4 ; if ( a < c ) then x := 5 else y := 10' '⇒ skip; b := (a+20); c := (b*4); if (a<c) then { x := 5 } else { y := 10 }, {a → 0}
⇒ b := (a+20); c := (b*4); if (a<c) then { x := 5 } else { y := 10 }, {a → 0}
⇒ skip; c := (b*4); if (a<c) then { x := 5 } else { y := 10 }, {a → 0, b → 20}
⇒ c := (b*4); if (a<c) then { x := 5 } else { y := 10 }, {a → 0, b → 20}
⇒ skip; if (a<c) then { x := 5 } else { y := 10 }, {a → 0, b → 20, c → 80}
⇒ if (a<c) then { x := 5 } else { y := 10 }, {a → 0, b → 20, c → 80}
⇒ x := 5, {a → 0, b → 20, c → 80}
⇒ skip, {a → 0, b → 20, c → 80, x → 5}'
}
