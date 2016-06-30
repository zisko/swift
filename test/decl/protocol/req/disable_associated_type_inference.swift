// RUN: %target-parse-verify-swift -disable-associated-type-witness-inference

protocol P1 {
  associatedtype Assoc1 // expected-note{{protocol requires nested type 'Assoc1'}}
  func p1() -> Assoc1
}

struct X1 : P1 { // expected-error{{type 'X1' does not conform to protocol 'P1'}}
  func p1() -> Int { return 0 }
}
