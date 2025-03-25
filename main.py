from keys import generate_keys
from signer import sign, multi_sign
from verify import verify

print("=== Single Schnorr (EC) Signature ===")
d, Q = generate_keys()
print("d (private key) =", d)
print("Q (public key) =", Q)

message = "Hello, this is the message to be signed!"
R, s = sign(message, d, Q)
print(f"\nSignature for the message '{message}':")
print(" R =", R)
print(" s =", s)

valid = verify(message, R, s, Q)
print("Validity:", valid)

tampered_message = message + " (hehe)"
valid2 = verify(tampered_message, R, s, Q)
print("Validity of changed message:", valid2)

print("\n=== Multisignature ===")
# 2 participants
d1, Q1 = generate_keys()
d2, Q2 = generate_keys()

m = "Two people signed this!"
(R_agg, s_agg, X_agg) = multi_sign([m], [d1, d2], [Q1, Q2])
print("Aggregated R =", R_agg)
print("Aggregated s =", s_agg)
print("Aggregated public key X =", X_agg)

multi_valid = verify(m, R_agg, s_agg, X_agg)
print("Validity:", multi_valid)

multi_valid2 = verify(m + " (hehe)", R_agg, s_agg, X_agg)
print("Validity of changed message:", multi_valid2)
