from typing import Literal

class MI:  # MASKED_INTEGER
	# value: int = 0
	# _value: int = 0
	bits: int = 64
	signed: bool = False
	endian: Literal["little", "big"] = "little"

	@property
	def value(self) -> int:
		return self._value & self.mask

	@value.setter
	def value(self, value: int) -> None:
		self._value = value & self.mask

	@property
	def mask(self) -> int:
		return (1 << self.bits) - 1

	def __init__(self, value_or_mi = 0, bits: int = 64, signed: bool = False, endian: Literal["little", "big"] = "little") -> None:
		assert bits % 8 == 0, "Bits must be divisible by 8!"
		self.reset()
		self.bits = bits
		self.signed = signed
		self.endian = endian
		if isinstance(value_or_mi, int):
			self.value = value_or_mi
		elif isinstance(value_or_mi, MI):
			self.value = value_or_mi.value

	def reset(self) -> None:
		self.bits = 64
		self.value = 0
		self.signed = False
		self.endian = "little"

	def __format__(self, fmt: str) -> str:
		return self.value.__format__(fmt)

	def __str__(self) -> str:
		return str(self.value)

	def __int__(self) -> int:
		return self.value

	def __bytes__(self) -> bytes:
		return self.value.to_bytes(self.bits // 8, self.endian, signed=self.signed)

	def hex(self) -> str:
		return bytes(self).hex().upper()

	def rol(self, count: int):
		t = self.value
		if count > 0:
			count %= self.bits
			high = t >> (self.bits - count)
			high &= self.mask
			if t < 0:  # signed value
				high &= ~(-1 << count)
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

	def perform_compare(self, op: Literal["<", ">", "<=", ">=", "!=", "=="], other) -> bool:
		if isinstance(other, MI):
			other = other.value
		if op not in ["<", ">", "<=", ">=", "!=", "=="]:
			raise ValueError("Invalid value for \"op\" parameter!")
		return eval(f"{self.value}{op}{other}")

	def perform_math(self, op: Literal["+", "-", "*", "//", "^", "&", "|", "%", "<<", ">>"], other, reverse: bool = False, copy: bool = False):
		assert isinstance(other, (int, MI)), "Invalid type for \"other\" parameter!"
		if isinstance(other, MI):
			other = other.value
		if op not in ["+", "-", "*", "//", "^", "&", "|", "%", "<<", ">>"]:
			raise ValueError("Invalid value for \"op\" parameter!")
		if reverse:
			r = eval(f"{other}{op}{self.value}")
		else:
			r = eval(f"{self.value}{op}{other}")
		if copy:
			return MI(r, self.bits, self.signed, self.endian)
		self.value = r
		return self

	def __add__(self, other):
		return self.perform_math("+", other, copy=True)

	def __iadd__(self, other):
		return self.perform_math("+", other)

	def __radd__(self, other):
		return self.perform_math("+", other, True, True)

	def __sub__(self, other):
		return self.perform_math("-", other, copy=True)

	def __isub__(self, other):
		return self.perform_math("-", other)

	def __rsub__(self, other):
		return self.perform_math("-", other, True, True)

	def __mul__(self, other):
		return self.perform_math("*", other, copy=True)

	def __imul__(self, other):
		return self.perform_math("*", other)

	def __rmul__(self, other):
		return self.perform_math("*", other, True, True)

	def __truediv__(self, other):
		return NotImplemented()

	def __itruediv__(self, other):
		return NotImplemented()

	def __rtruediv__(self, other):
		return NotImplemented()

	def __floordiv__(self, other):
		return self.perform_math("//", other, copy=True)

	def __ifloordiv__(self, other):
		return self.perform_math("//", other)

	def __rfloordiv__(self, other):
		return self.perform_math("//", other, True, True)

	def __mod__(self, other):
		return self.perform_math("%", other, copy=True)

	def __imod__(self, other):
		return self.perform_math("%", other)

	def __rmod__(self, other):
		return self.perform_math("%", other, True, True)

	def __xor__(self, other):
		return self.perform_math("^", other, copy=True)

	def __ixor__(self, other):
		return self.perform_math("^", other)

	def __rxor__(self, other):
		return self.perform_math("^", other, True, True)

	def __or__(self, other):
		return self.perform_math("|", other, copy=True)

	def __ior__(self, other):
		return self.perform_math("|", other)

	def __ror__(self, other):
		return self.perform_math("|", other, True, True)

	def __and__(self, other):
		return self.perform_math("&", other, copy=True)

	def __iand__(self, other):
		return self.perform_math("&", other)

	def __rand__(self, other):
		return self.perform_math("&", other, True, True)

	def __lshift__(self, other):
		return self.perform_math("<<", other, copy=True)

	def __ilshift__(self, other):
		return self.perform_math("<<", other)

	def __rlshift__(self, other):
		return self.perform_math("<<", other, True, True)

	def __rshift__(self, other):
		return self.perform_math(">>", other, copy=True)

	def __irshift__(self, other):
		return self.perform_math(">>", other)

	def __rrshift__(self, other):
		return self.perform_math(">>", other, True, True)

	def __pow__(self, other, modulo=None):
		if isinstance(other, MI):
			other = other.value
		if modulo:
			t = pow(self.value, other, modulo)
		else:
			t = pow(self.value, other)
		return MI(t, self.bits, self.signed, self.endian)

	def __ipow__(self, other, modulo=None):
		if isinstance(other, MI):
			other = other.value
		if modulo:
			t = pow(self.value, other, modulo)
		else:
			t = pow(self.value, other)
		self.value = t
		return self

	def __rpow__(self, other, modulo=None):
		if isinstance(other, MI):
			other = other.value
		if modulo:
			t = pow(self.value, other, modulo)
		else:
			t = pow(self.value, other)
		return MI(t, self.bits, self.signed, self.endian)

	def __neg__(self):
		return MI(-self.value, self.bits, self.signed, self.endian)

	def __invert__(self):
		return MI(~self.value, self.bits, self.signed, self.endian)

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

__all__ = [
	"MI"
]