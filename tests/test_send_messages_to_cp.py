import websockets
import pytest
import asyncio

from faker import Faker

from .central_system import ChargePoint as central_system
from ocpp_simulator.cp_management import cp as Cp


fake = Faker()


async def cancel_tasks():
    for task in asyncio.all_tasks():
        task.cancel()


@pytest.mark.asyncio
async def test_cancel_reservation():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_cancel_reservation()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_certificate_signed():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_certificate_signed()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_change_availability():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_change_availability()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_clear_charging_profile():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_clear_charging_profile()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_clear_display_message():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_clear_display_message()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_clear_variable_monitoring():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_clear_variable_monitoring()
        assert result.clear_monitoring_result[0]['status'] == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_cost_updated():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_cost_updated()
        assert str(result) == 'CostUpdatedPayload()'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_customer_info():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_customer_info()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_data_transfer():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_data_transfer()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_delete_certificate():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_delete_certificate()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_get_base_report():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_get_base_report()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_get_charging_profiles():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_get_charging_profiles()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_get_composite_schedule():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_get_composite_schedule()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_get_display_messages():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_get_display_messages()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_get_installed_certificate_ids():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_get_installed_certificate_ids()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_get_local_list_version():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_get_local_list_version()
        assert 'GetLocalListVersionPayload' in str(result)

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_get_log():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_get_log()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_get_monitoring_report():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_get_monitoring_report()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_publish_firmware():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_publish_firmware()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_reserve_now():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_reserve_now()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_reset():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_reset()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_send_local_list():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_send_local_list()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_set_charging_profile():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_set_charging_profile()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_set_display_message():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_set_display_message()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_set_monitoring_base():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_set_monitoring_base()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_set_monitoring_level():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_set_monitoring_level()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_set_network_profile():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_set_network_profile()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_set_variable_monitoring():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_set_variable_monitoring()
        assert result.set_monitoring_result[0]['status'] == 'Accepted'
        assert result.set_monitoring_result[0]['type'] == 'Delta'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_set_variables():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_set_variables()
        assert result.set_variable_result[0]['attribute_status'] == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_trigger_message():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_trigger_message()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_unlock_connector():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_unlock_connector()
        assert result.status == 'Unlocked'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_unpublish_firmware():
    server = await Cp.start_cp()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = central_system('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_unpublish_firmware()
        assert result.status == 'Unpublished'

        await cancel_tasks()
        server.close()


# @pytest.mark.asyncio
# async def test_update_firmware():
#     server = await Cp.start_cp()
#     async with websockets.connect(
#         f'ws://0.0.0.0:9000/123',
#         subprotocols=['ocpp2.0.1']
#     ) as ws:
#         cp = central_system('123', ws)
#         loop = asyncio.get_running_loop()
#         loop.create_task(cp.start())
#
#         result = await cp.send_update_firmware()
#         assert result.status == 'Accepted'
#
#         await cancel_tasks()
#         server.close()
