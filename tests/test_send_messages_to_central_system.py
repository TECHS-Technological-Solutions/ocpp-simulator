import websockets
import pytest
from unittest.mock import patch
import asyncio

from faker import Faker

from .central_system import start_central_system
from ocpp_simulator.cp_management import cp as Cp


fake = Faker()


async def cancel_tasks():
    for task in asyncio.all_tasks():
        task.cancel()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_status_and_boot_notifications(mock_typer, mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.return_value = '123'
        mock_ask_question.return_value = 'PowerUp'
        result = await cp.send_boot_notification()
        assert result.status == 'Accepted'
        assert result.interval == 10

        mock_typer.return_value = 1
        mock_ask_question.return_value = "Available"
        result = await cp.send_status_notification()
        assert str(result) == 'StatusNotificationPayload()'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@pytest.mark.asyncio
async def test_authorize(mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_ask_question.return_value = "MacAddress"
        result = await cp.send_authorize()
        assert result.id_token_info['status'] == 'Accepted'

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_clear_cache():
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_clear_cache()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@pytest.mark.asyncio
async def test_cleared_charging_request(mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_ask_question.return_value = "EMS"
        result = await cp.send_cleared_charging_request()
        assert str(result) == "ClearedChargingLimitPayload()"

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@pytest.mark.asyncio
async def test_firmware_status_notification(mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_ask_question.return_value = "Downloaded"
        result = await cp.send_firmware_status_notification()
        assert str(result) == "FirmwareStatusNotificationPayload()"

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_get_15118ev_certificate(mock_typer, mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.return_value = '1'
        mock_ask_question.return_value = "Install"
        result = await cp.send_get_15118ev_certificate()
        assert result.status == 'Accepted'
        assert result.exi_response == 'Success message'

        await cancel_tasks()
        server.close()


# @patch("ocpp_simulator.cp_management.cp.ask_question")
# @patch("typer.prompt")
# @pytest.mark.asyncio
# async def test_get_certificate_status(mock_typer, mock_ask_question):
#     server = await start_central_system()
#     async with websockets.connect(
#         f'ws://0.0.0.0:9000/123',
#         subprotocols=['ocpp2.0.1']
#     ) as ws:
#         cp = Cp.ChargePoint('123', ws)
#         loop = asyncio.get_running_loop()
#         loop.create_task(cp.start())
#
#         mock_typer.side_effect = [fake.pystr(1, 128), fake.pystr(1, 128), fake.pystr(1, 40), fake.url()]
#         mock_ask_question.return_value = "Central"
#         result = await cp.send_get_certificate_status()
#         assert result.status == 'Accepted'
#
#         await cancel_tasks()
#         server.close()


@patch("typer.prompt")
@pytest.mark.asyncio
async def test_get_display_messages(mock_typer):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.return_value = 1
        result = await cp.send_get_display_messages()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@pytest.mark.asyncio
async def test_log_status_notification(mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_ask_question.return_value = "Uploaded"
        result = await cp.send_log_status_notification()
        assert str(result) == "LogStatusNotificationPayload()"

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_meter_value(mock_typer, mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.side_effect = [fake.random_int(), fake.random_int()]
        mock_ask_question.side_effect = ["Bytes", "Transaction.End", "Current.Export", "L3"]
        await cp.send_meter_value()

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@pytest.mark.asyncio
async def test_notify_charging_limit(mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_ask_question.return_value = "EMS"
        result = await cp.send_notify_charging_limit()
        assert str(result) == "NotifyChargingLimitPayload()"

        await cancel_tasks()
        server.close()


@patch("typer.prompt")
@pytest.mark.asyncio
async def test_notify_customer_information(mock_typer):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.side_effect = [fake.pystr(1, 12), fake.random_int(min=0, max=10), fake.random_int(min=0, max=10)]
        result = await cp.send_notify_customer_information()
        assert str(result) == "NotifyCustomerInformationPayload()"

        await cancel_tasks()
        server.close()


@patch("typer.prompt")
@pytest.mark.asyncio
async def test_notify_display_message(mock_typer):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.return_value = fake.random_int(min=0, max=10)
        result = await cp.send_notify_display_messages()
        assert str(result) == "NotifyDisplayMessagesPayload()"

        await cancel_tasks()
        server.close()


# @patch("ocpp_simulator.cp_management.cp.ask_question")
# @patch("typer.prompt")
# @pytest.mark.asyncio
# async def test_notify_ev_charging_needs(mock_typer, mock_ask_question):
#     server = await start_central_system()
#     async with websockets.connect(
#         f'ws://0.0.0.0:9000/123',
#         subprotocols=['ocpp2.0.1']
#     ) as ws:
#         cp = Cp.ChargePoint('123', ws)
#         loop = asyncio.get_running_loop()
#         loop.create_task(cp.start())
#
#         mock_typer.return_value = fake.random_int(min=0, max=100)
#         mock_ask_question.return_value = "AC_single_phase"
#         result = await cp.send_notify_ev_charging_needs()
#         assert result.status == 'Accepted'
#
#         await cancel_tasks()
#         server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_notify_ev_charging_schedule(mock_typer, mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.return_value = fake.random_int(min=0, max=100)
        mock_ask_question.return_value = "W"
        result = await cp.send_notify_ev_charging_schedule()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_notify_event(mock_typer, mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.side_effect = [
            fake.random_int(min=0, max=100), fake.random_int(min=0, max=100), fake.pystr(1, 50),
            fake.pystr(1, 50), fake.pystr(1, 50), fake.pystr(1, 50)
        ]
        mock_ask_question.side_effect = ["Alerting", "HardWiredNotification"]
        result = await cp.send_notify_event()
        assert str(result) == 'NotifyEventPayload()'

        await cancel_tasks()
        server.close()


@patch("typer.prompt")
@pytest.mark.asyncio
async def test_notify_monitoring_report(mock_typer):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.side_effect = [fake.random_int(min=0, max=100), fake.random_int(min=0, max=100)]
        result = await cp.send_notify_monitoring_report()
        assert str(result) == 'NotifyMonitoringReportPayload()'

        await cancel_tasks()
        server.close()


@patch("typer.prompt")
@pytest.mark.asyncio
async def test_notify_report(mock_typer):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.side_effect = [fake.random_int(min=0, max=100), fake.random_int(min=0, max=100)]
        result = await cp.send_notify_report()
        assert str(result) == 'NotifyReportPayload()'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@pytest.mark.asyncio
async def test_publish_firmware_status_notification(mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_ask_question.return_value = "Downloaded"
        result = await cp.send_publish_firmware_status_notification()
        assert str(result) == 'PublishFirmwareStatusNotificationPayload()'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_report_charging_profiles(mock_typer, mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.side_effect = [
            fake.random_int(min=0, max=100), fake.random_int(min=0, max=100), fake.random_int(min=0, max=100),
            fake.random_int(min=0, max=100), fake.random_int(min=0, max=100), fake.pyfloat(min_value=1, max_value=100)
        ]
        mock_ask_question.side_effect = ["EMS", "ChargingStationExternalConstraints", "Relative", "W"]
        result = await cp.send_report_charging_profiles()
        assert str(result) == "ReportChargingProfilesPayload()"

        await cancel_tasks()
        server.close()


@pytest.mark.asyncio
async def test_heartbeat():
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        result = await cp.send_heartbeat()
        assert result.current_time == '10.10.2010'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_start_and_stop_transaction(mock_typer, mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.return_value = 1
        mock_ask_question.return_value = "Central"
        result = await cp.send_start_transaction()
        assert result.status == 'Accepted'
        result = await cp.send_start_transaction()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_reservation_status_update(mock_typer, mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.return_value = fake.pyint(1, 100)
        mock_ask_question.return_value = "Removed"
        result = await cp.send_reservation_status_update()
        assert str(result) == "ReservationStatusUpdatePayload()"

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@pytest.mark.asyncio
async def test_security_event_notification(mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_ask_question.return_value = "FirmwareUpdated"
        result = await cp.send_security_event_notification()
        assert str(result) == "SecurityEventNotificationPayload()"

        await cancel_tasks()
        server.close()


@patch("typer.prompt")
@pytest.mark.asyncio
async def test_sign_certificate(mock_typer):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.return_value = fake.pystr(1, 100)
        result = await cp.send_sign_certificate()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_transaction_event(mock_typer, mock_ask_question):
    server = await start_central_system()
    async with websockets.connect(
        f'ws://0.0.0.0:9000/123',
        subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = Cp.ChargePoint('123', ws)
        loop = asyncio.get_running_loop()
        loop.create_task(cp.start())

        mock_typer.side_effect = [fake.pystr(1, 36), fake.pyint(1, 100)]
        mock_ask_question.side_effect = ["Started", "Authorized"]
        result = await cp.send_transaction_event()
        assert result.total_cost == 100

        await cancel_tasks()
        server.close()
