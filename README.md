# blockchain-hw-1

This is an assignment on  EC-Schnorr digital signatures—including how multiple people can combine their signatures into one (a “multi-signature”).

We use a specific elliptic curve called secp256k1 (the same used by Bitcoin), specified in `params.py`. It is a set of points $(x,y)$ that satisfy $y^2 = x^2 + ax+ b (\mod p)$, where $p$ is a large prime and $a=0$, $b=7$. We have a generator point $G$ on this curve with a large order $n$. If you multiply $G$ by any integer $k$ you get another point on this curve. Reaching $n \cdot G$ brings you back to the point at infinity.

A private key is just a random integer $d$ between 1 and $n-1$. Public key is $Q = d \cdot G$. Figuring $d$ by knowing $Q$ is hard as it involves solving a discrete logarithm on the elliptic curve.

To sign a message $m$, you pick a new random number $r$ and compute $R = r \cdot G$. Then you hash together $(Q, R, m)$ to get a challenge $e$. The actual signature is $s = (r + e \cdot d) \mod n$, so the final signature is the pair $(R, s)$. To verify it, you take $(R, s)$, the public key $Q$, and the message $m$, re-hash $(Q, R, m)$ to get the same $e$, and check if $s \cdot G = R + e \cdot Q$. If that holds, the signature checks out.

To see it in action, run `main.py`. It'll generate a key pair, sign a message, and check that the signature is valid. Then it shows how a few people can all sign the same message together and combine their parts into one little signature. At the end, it checks that this combined signature is valid for everyone involved.