from dataclasses import dataclass
from hashlib import sha256
from random import choices
from string import digits
from time import time


@dataclass
class State:
    timestamp: float
    digest: str
    phone_number: str


class PhoneVerification(object):

    def __init__(self, secret_key: str,
                 verification_code_length: int = 5,
                 valid_time_in_seconds: int = 300):
        self._secret_key = secret_key
        self._verification_code_length = verification_code_length
        self._valid_time_in_seconds = valid_time_in_seconds

    def _get_now(self) -> float:
        # in unix format
        return time()

    def _hash(self, value: str) -> str:
        return sha256(value.encode('utf-8')).hexdigest()

    def _concatenate(self, phone_number: str,
                     verification_code: str, timestamp: float) -> str:
        return f'{phone_number}{verification_code}{timestamp}{self._secret_key}'

    def _generate_verification_code(self) -> str:
        code = choices(list(digits), k=self._verification_code_length)
        return ''.join(code)

    def generate_verification_state(self, phone_number: str) -> [State, str]:
        verification_code = self._generate_verification_code()
        timestamp = self._get_now()
        concatenated_string = self._concatenate(phone_number,
                                                verification_code,
                                                timestamp)
        digest = self._hash(concatenated_string)
        return State(timestamp, digest, phone_number), verification_code

    def _is_timestamp_valid(self, timestamp: float) -> bool:
        return self._get_now() - timestamp < self._valid_time_in_seconds

    def validate_state(self, state: State, verification_code: str) -> bool:
        concatenated_string = self._concatenate(state.phone_number,
                                                verification_code,
                                                state.timestamp)
        digest = self._hash(concatenated_string)
        is_digest_valid = (digest == state.digest)
        return is_digest_valid and self._is_timestamp_valid(state.timestamp)
