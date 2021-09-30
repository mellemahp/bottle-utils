from redislite import Redis

TEST_REDIS_FILENAME = "test_redis.db"


def get_test_redis():
    return Redis(TEST_REDIS_FILENAME)
