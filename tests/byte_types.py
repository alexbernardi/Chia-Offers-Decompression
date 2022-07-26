from typing import BinaryIO, Iterable, SupportsBytes, Type, TypeVar, Union


_T_SizedBytes = TypeVar("_T_SizedBytes", bound="SizedBytes")


def hexstr_to_bytes(input_str: str) -> bytes:
    """
    Converts a hex string into bytes, removing the 0x if it's present.
    """
    if input_str.startswith("0x") or input_str.startswith("0X"):
        return bytes.fromhex(input_str[2:])
    return bytes.fromhex(input_str)


class SizedBytes(bytes):
    """A streamable type that subclasses "bytes" but requires instances
    to be a certain, fixed size specified by the `._size` class attribute.
    """

    _size = 0

    @classmethod
    def parse(cls: Type[_T_SizedBytes], f: BinaryIO) -> _T_SizedBytes:
        b = f.read(cls._size)
        return cls(b)

    def stream(self, f: BinaryIO) -> None:
        f.write(self)

    @classmethod
    def from_bytes(cls: Type[_T_SizedBytes], blob: bytes) -> _T_SizedBytes:
        return cls(blob)

    @classmethod
    def from_hexstr(cls: Type[_T_SizedBytes], input_str: str) -> _T_SizedBytes:
        if input_str.startswith("0x") or input_str.startswith("0X"):
            return cls.fromhex(input_str[2:])
        return cls.fromhex(input_str)

    def __str__(self) -> str:
        return self.hex()

    def __repr__(self) -> str:
        return "<%s: %s>" % (self.__class__.__name__, str(self))
