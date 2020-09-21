from functools import wraps
from cocotb.triggers import Timer

def model_reset(decorated_coro):
    """Function decorator for FUSION test case iteration (model reset)
    use:
    @cocotb.test()
    @model_reset
    async def test_model_reset(dut):
        assert dut.req4_data_in == 0
    """

    @wraps(decorated_coro)
    async def reset_wrapper(dut, *args, **kwargs):
        dut._log.info("Resetting model")
        dut._id('_reset').setimmediatevalue(1)
        await Timer(1)
        dut._log.info("Model reset")
        return await decorated_coro(dut, *args, **kwargs)
    return reset_wrapper
