from typing import Any, Dict, List, Optional, Set, Tuple
from sized_bytes import bytes32
import io
from bech32m import bech32_decode, bech32_encode, convertbits
from puzzle_compression import (
    compress_object_with_puzzles,
    decompress_object_with_puzzles,
    lowest_best_version,
)
import zlib

class Offer:

    def get_requested_amounts(self) -> Dict[Optional[bytes32], int]:
        requested_amounts: Dict[Optional[bytes32], int] = {}
        return requested_amounts

    def get_offered_amounts(self) -> Dict[Optional[bytes32], int]:
        offered_amounts: Dict[Optional[bytes32], int] = {}
        return offered_amounts

    def summary(self) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, Dict[str, Any]]]:
        offered_amounts: Dict[Optional[bytes32], int] = self.get_offered_amounts()
        requested_amounts: Dict[Optional[bytes32], int] = self.get_requested_amounts()

        def keys_to_strings(dic: Dict[Optional[bytes32], Any]) -> Dict[str, Any]:
            new_dic: Dict[str, Any] = {}
            for key in dic:
                if key is None:
                    new_dic["xch"] = dic[key]
                else:
                    new_dic[key.hex()] = dic[key]
            return new_dic

        driver_dict: Dict[str, Any] = {}
        for key, value in self.driver_dict.items():
            driver_dict[key.hex()] = value

        return keys_to_strings(offered_amounts), keys_to_strings(requested_amounts), driver_dict

    @classmethod
    def from_bytess(cls: Any, blob: bytes) -> Any:
        f = io.BytesIO(blob)
        print(f)
        parsed = cls.parse(f)
        assert f.read() == b""
        return parsed

    @classmethod
    def from_bytes(cls, as_bytes: bytes) -> "Offer":
        # Because of the __bytes__ method, we need to parse the dummy CoinSpends as `requested_payments`
        bundle = Offer.from_bytess(as_bytes)
        print(bundle)
        return bundle

    @classmethod
    def from_compressed(cls, compressed_bytes: bytes) -> "Offer":
        return Offer.from_bytes(decompress_object_with_puzzles(compressed_bytes))
        
    @classmethod
    def try_offer_decompression(cls, offer_bytes: bytes) -> "Offer":
        try:
            return cls.from_compressed(offer_bytes)
        except TypeError:
            pass
        return offer_bytes

    @classmethod
    def from_bech32(cls, offer_bech32: str) -> "Offer":
        hrpgot, data = bech32_decode(offer_bech32, max_length=len(offer_bech32))
        if data is None:
            raise ValueError("Invalid Offer")
        decoded = convertbits(list(data), 5, 8, False)
        print(decoded)
        decoded_bytes = bytes(decoded)
        print(decoded_bytes)
        return cls.try_offer_decompression(decoded_bytes)