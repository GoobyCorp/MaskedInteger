class MI:  # MASKED_INTEGER
	value: int = 0
	bits: int = 64

	@property
	def mask(self) -> int:
		return (1 << self.bits) - 1

	def __init__(self, value_or_mi=0, bits: int = 64) -> None:
		assert bits % 8 == 0, "Bits must be divisible by 8!"
		self.reset()
		if isinstance(value_or_mi, int):
			self.value = value_or_mi
		elif isinstance(value_or_mi, MI):
			self.value = value_or_mi.value
		self.bits = bits
		self.value &= self.mask

	def reset(self) -> None:
		self.value = 0
		self.bits = 64

	def __format__(self, fmt: str) -> str:
		return self.value.__format__(fmt)

	def __str__(self) -> str:
		return str(self.value)

	def __int__(self) -> int:
		return self.value

	def __bytes__(self) -> bytes:
		return self.value.to_bytes(self.bits // 8, "little", signed=False)

	#def __bytearray__(self) -> bytearray:
	#	return bytearray(bytes(self))

	def hex(self) -> str:
		return bytes(self).hex().upper()

	def rol(self, count: int):
		t = self.value
		if count > 0:
			count %= self.bits
			high = t >> (self.bits - count)
			high &= self.mask
			if t < 0:  # signed value
				high &= ~((-1 << count))
				high &= self.mask
			t <<= count
			t &= self.mask
			t |= high
			t &= self.mask
		else:
			count = -count % self.bits
			low = t << (self.bits - count)
			low &= self.mask
			t >>= count
			t &= self.mask
			t |= low
			t &= self.mask
		self.value = t
		return self

	def ror(self, count: int):
		return self.rol(-count)

	def perform_compare(self, op: str, other) -> bool:
		if isinstance(other, MI):
			other = other.value
		if op not in ["<", ">", "<=", ">=", "!=", "=="]:
			raise ValueError("Invalid value for \"op\" parameter!")
		return eval(f"{self.value}{op}{other}")

	def perform_math(self, op: str, other, reverse: bool = False) -> None:
		assert isinstance(other, (int, MI)), "Invalid type for \"other\" parameter!"
		if isinstance(other, MI):
			other = other.value
		if op not in ["+", "-", "*", "//", "^", "&", "|", "%", "<<", ">>"]:
			raise ValueError("Invalid value for \"op\" parameter!")
		if reverse:
			self.value = eval(f"{other}{op}{self.value}")
		else:
			self.value = eval(f"{self.value}{op}{other}")

	def __add__(self, other):
		self.perform_math("+", other)
		return self

	def __iadd__(self, other):
		self.perform_math("+", other)
		return self

	def __radd__(self, other):
		self.perform_math("+", other, True)
		return self

	def __sub__(self, other):
		self.perform_math("-", other)
		return self

	def __isub__(self, other):
		self.perform_math("-", other)
		return self

	def __rsub__(self, other):
		self.perform_math("-", other, True)
		return self

	def __mul__(self, other):
		self.perform_math("*", other)
		return self

	def __imul__(self, other):
		self.perform_math("*", other)
		return self

	def __rmul__(self, other):
		self.perform_math("*", other, True)
		return self

	def __truediv__(self, other):
		return NotImplemented()

	def __itruediv__(self, other):
		return NotImplemented()

	def __floordiv__(self, other):
		self.perform_math("//", other)
		return self

	def __ifloordiv__(self, other):
		self.perform_math("//", other)
		return self

	def __rfloordiv__(self, other):
		self.perform_math("//", other, True)
		return self

	def __mod__(self, other):
		self.perform_math("%", other)
		return self

	def __imod__(self, other):
		self.perform_math("%", other)
		return self

	def __rmod__(self, other):
		self.perform_math("%", other, True)
		return self

	def __xor__(self, other):
		self.perform_math("^", other)
		return self

	def __ixor__(self, other):
		self.perform_math("^", other)
		return self

	def __rxor__(self, other):
		self.perform_math("^", other, True)
		return self

	def __or__(self, other):
		self.perform_math("|", other)
		return self

	def __ior__(self, other):
		self.perform_math("|", other)
		return self

	def __ror__(self, other):
		self.perform_math("|", other, True)
		return self

	def __and__(self, other):
		self.perform_math("&", other)
		return self

	def __iand__(self, other):
		self.perform_math("&", other)
		return self

	def __rand__(self, other):
		self.perform_math("&", other, True)
		return self

	def __lshift__(self, other):
		self.perform_math("<<", other)
		return self

	def __ilshift__(self, other):
		self.perform_math("<<", other)
		return self

	def __rlshift__(self, other):
		self.perform_math("<<", other, True)
		return self

	def __rshift__(self, other):
		self.perform_math(">>", other)
		return self

	def __irshift__(self, other):
		self.perform_math(">>", other)
		return self

	def __rrshift__(self, other):
		self.perform_math(">>", other, True)
		return self

	def __pow__(self, other, modulo=None):
		if isinstance(other, MI):
			other = other.value
		if modulo:
			t = pow(self.value, other, modulo)
		else:
			t = pow(self.value, other)
		t &= self.mask
		self.value = t
		return self

	def __ipow__(self, other, modulo=None):
		if isinstance(other, MI):
			other = other.value
		if modulo:
			t = pow(self.value, other, modulo)
		else:
			t = pow(self.value, other)
		t &= self.mask
		self.value = t
		return self

	def __rpow__(self, other, modulo=None):
		if isinstance(other, MI):
			other = other.value
		if modulo:
			t = pow(self.value, other, modulo)
		else:
			t = pow(self.value, other)
		t &= self.mask
		self.value = t
		return self

	def __neg__(self):
		self.value = (-self.value) & self.mask
		return self

	def __invert__(self):
		self.value = (~self.value) & self.mask
		return self

	def __lt__(self, other):
		return self.perform_compare("<", other)

	def __le__(self, other):
		return self.perform_compare("<=", other)

	def __eq__(self, other):
		return self.perform_compare("==", other)

	def __ne__(self, other):
		return self.perform_compare("!=", other)

	def __gt__(self, other):
		return self.perform_compare(">", other)

	def __ge__(self, other):
		return self.perform_compare(">=", other)
