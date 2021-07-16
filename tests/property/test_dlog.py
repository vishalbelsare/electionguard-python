from hypothesis import given
from hypothesis.strategies import integers

from tests.base_test_case import BaseTestCase

from electionguard.constants import (
    get_large_prime,
    get_generator,
)
from electionguard.dlog import discrete_log
from electionguard.group import (
    ElementModP,
    ONE_MOD_P,
    mult_p,
    g_pow_p,
    int_to_q,
    int_to_p_unchecked,
    int_to_q_unchecked,
)
from electionguard.utils import get_optional


# simpler implementation of discrete_log, only meant for comparison testing of the caching version
def _discrete_log_uncached(e: ElementModP) -> int:
    count = 0
    g_inv = int_to_p_unchecked(pow(get_generator(), -1, get_large_prime()))
    while e != ONE_MOD_P:
        e = mult_p(e, g_inv)
        count = count + 1

    return count


class TestDLog(BaseTestCase):
    """Discrete log tests"""

    @given(integers(0, 100))
    def test_uncached(self, exp: int):
        plaintext = get_optional(int_to_q(exp))
        exp_plaintext = g_pow_p(plaintext)
        plaintext_again = _discrete_log_uncached(exp_plaintext)

        self.assertEqual(exp, plaintext_again)

    @given(integers(0, 1000))
    def test_cached(self, exp: int):
        plaintext = get_optional(int_to_q(exp))
        exp_plaintext = g_pow_p(plaintext)
        plaintext_again = discrete_log(exp_plaintext)

        self.assertEqual(exp, plaintext_again)

    def test_cached_one(self):
        plaintext = int_to_q_unchecked(1)
        ciphertext = g_pow_p(plaintext)
        plaintext_again = discrete_log(ciphertext)

        self.assertEqual(1, plaintext_again)
