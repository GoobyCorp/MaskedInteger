#!/usr/bin/env python3

from MaskedInteger import MI

GM = lambda bits: (1 << bits) - 1

def main() -> int:
	m = GM(64)

	# compute normally
	t0 = (0x8877665544332211 + 0x1122334455667788)
	t0 += 0x7777777777777777
	t0 += 1
	t0 += 0x99999999
	t0 &= m

	# compute using class
	m0 = MI(0x8877665544332211)
	m0 += 0x1122334455667788
	m0 += 0x7777777777777777
	m0 += 1
	m0 += 0x99999999

	print(f"{t0:X}")
	print(m0.hex())

	print(m0 == t0)

	return 0

if __name__ == "__main__":
	exit(main())