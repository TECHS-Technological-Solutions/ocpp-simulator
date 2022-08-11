import websockets
import pytest
from unittest.mock import patch
import asyncio

from .central_system import connect_to_central_system
from ocpp_simulator.cp_management import cp as Cp


async def cancel_tasks():
    for task in asyncio.all_tasks():
        task.cancel()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_status_and_boot_notifications(mock_typer, mock_ask_question):
    server = await connect_to_central_system()
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
        mock_ask_question.return_value = "Central"
        result = await cp.send_start_transaction()
        assert result.status == 'Accepted'

        await cancel_tasks()
        server.close()


@patch("ocpp_simulator.cp_management.cp.ask_question")
@pytest.mark.asyncio
async def test_authorize(mock_ask_question):
    server = await connect_to_central_system()
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
    server = await connect_to_central_system()
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
@patch("typer.prompt")
@pytest.mark.asyncio
async def test_start_and_stop_transaction(mock_typer, mock_ask_question):
    server = await connect_to_central_system()
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
