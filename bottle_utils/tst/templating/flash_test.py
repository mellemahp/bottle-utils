
import sys
import pytest
from bottle_utils.src.templating.flash import Flash, FlashLvl

TEST_MSG = "test"


def test_when_uses_flash_level_type_then_ok():
    flash = Flash(level=FlashLvl.ERROR, message=TEST_MSG)
    assert(flash.msg == TEST_MSG)
    assert(flash.lvl == "error")


def test_when_not_flashlvl_instance_then_exception():
    with pytest.raises(ValueError):
        Flash(level="Incorrect Type", message=TEST_MSG)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))