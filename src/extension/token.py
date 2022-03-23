import random

from extension.redis_client import redis_client


def generate_token() -> str:
    _string = 'ABCDEFGHIJKLMNOPQUVWXYZ' \
              'abcdefghijklmnopquvwxyz' \
              '0123456789'
    return "".join([random.choice(_string) for _ in range(20)])


class Token:
    """
    用户 token
    """
    USER_TOKEN_KEY = "spending:token:{name}"

    def get(self, name: str) -> str:
        """ 得到token
        """
        _token = redis_client.get(self.USER_TOKEN_KEY.format(name=name))

        # 如果没有新建一个
        if not _token:
            _token = generate_token()
            redis_client.set(
                self.USER_TOKEN_KEY.format(name=name), _token
            )
        return _token

    def check(self, name: str, token: str) -> bool:
        _token = redis_client.get(self.USER_TOKEN_KEY.format(name=name))
        if not _token:
            return False

        return _token.decode() == token
