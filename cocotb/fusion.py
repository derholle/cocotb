import cocotb
from functools import wraps
from cocotb.triggers import Timer

def model_reset(decorated_coro):
    """Function decorator for FUSION test case iteration
    this will lead to a model (and RTX) reset
    use:
    @cocotb.test()
    @model_reset
    async def test_model_reset(dut):
        assert dut.req4_data_in == 0
    """
    if not cocotb.SIM_NAME.lower().startswith("fusion"):
        raise Exception("model_reset can only be used with FUSION")

    @wraps(decorated_coro)
    async def reset_wrapper(dut, *args, **kwargs):
        dut._log.info("Resetting model")
        dut._id('_reset').setimmediatevalue(1)
        await Timer(1)
        dut._log.info("Model reset")
        cocotb.regression_manager._test_start_sim_time = 0
        return await decorated_coro(dut, *args, **kwargs)
    return reset_wrapper
