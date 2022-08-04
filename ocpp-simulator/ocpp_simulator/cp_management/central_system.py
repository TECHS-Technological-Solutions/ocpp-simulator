import asyncio
import logging
import websockets
from datetime import datetime

from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result, enums


logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    @on(enums.Action.BootNotification)
    async def on_boot_notification(self, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status='Accepted'
        )

    @on(enums.Action.StatusNotification)
    async def on_send_notification(self, **kwargs):
        return call_result.StatusNotificationPayload()

    @on(enums.Action.Heartbeat)
    async def on_send_heartbeat(self, **kwargs):
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )

    @on(enums.Action.RequestStartTransaction)
    async def on_send_start_transaction(self, **kwargs):
        return call_result.RequestStartTransactionPayload(
            status=enums.RequestStartStopStatusType.accepted
        )

    @on(enums.Action.Authorize)
    async def on_send_authorize(self, **kwargs):
        return call_result.AuthorizePayload(
            id_token_info={'status': enums.AuthorizationStatusType.accepted}
        )

    @on(enums.Action.RequestStopTransaction)
    async def on_send_stop_transaction(self, **kwargs):
        return call_result.RequestStopTransactionPayload(
            status=enums.RequestStartStopStatusType.accepted
        )

    @on(enums.Action.MeterValues)
    async def on_send_meter_value(self, **kwargs):
        return call_result.MeterValuesPayload()


async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    try:
        requested_protocols = websocket.request_headers[
            'Sec-WebSocket-Protocol']
    except KeyError:
        logging.info("Client hasn't requested any Subprotocol. "
                 "Closing Connection")
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning('Protocols Mismatched | Expected Subprotocols: %s,'
                        ' but client supports  %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols)
        return await websocket.close()

    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        "0.0.0.0",
        9000,
        subprotocols=['ocpp2.0.1']
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
