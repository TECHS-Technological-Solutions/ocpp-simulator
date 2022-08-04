import uuid
from datetime import datetime, timedelta
import asyncio
import logging
import websockets

from ocpp.v201 import ChargePoint as Cp, call, datatypes, enums
logging.basicConfig(level=logging.INFO)


class ChargePoint(Cp):

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charging_station={
                'model': 'Wallbox XYZ',
                'vendor_name': 'anyone'
            },
            reason="PowerUp"
        )
        response = await self.call(request)
        return response

    async def send_status_notification(self):
        request = call.StatusNotificationPayload(
            connector_id=1,
            connector_status='Available',
            timestamp=str(datetime.now()),
            evse_id=123
        )
        response = await self.call(request)
        return response

    async def send_heartbeat(self):
        request = call.HeartbeatPayload()
        response = await self.call(request)
        return response

    async def send_start_transaction(self):
        request = call.RequestStartTransactionPayload(
            id_token={'idToken': str(uuid.uuid4()), 'type': 'Central'},
            remote_start_id=1
        )
        response = await self.call(request)
        return response

    async def send_stop_transaction(self, transaction_id):
        request = call.RequestStopTransactionPayload(
            transaction_id=transaction_id
        )
        response = await self.call(request)
        return response

    async def send_authorize(self):
        request = call.AuthorizePayload(
            id_token={'idToken': str(uuid.uuid4()), "type": enums.IdTokenType.central},
        )
        response = await self.call(request)
        return response

    async def send_meter_value(self, transaction_id: int):
        unit = datatypes.UnitOfMeasureType(
            unit=enums.UnitOfMeasureType.w
        )
        request = call.MeterValuesPayload(
            evse_id=1,
            meter_value=[
                datatypes.MeterValueType(
                    timestamp=str(datetime.now()),
                    sampled_value=[
                        datatypes.SampledValueType(
                            value=10,
                            context='Sample.Periodic',
                            measurand='Power.Active.Import',
                            phase=None,
                            location=None,
                            unit_of_measure=unit
                        ),
                        datatypes.SampledValueType(
                            value=10,
                            context='Sample.Periodic',
                            measurand='Power.Active.Import',
                            phase='L1',
                            location=None,
                            unit_of_measure=unit
                        ),
                    ]
                ),
                datatypes.MeterValueType(
                    timestamp=str(datetime.now() + timedelta(seconds=5)),
                    sampled_value=[
                        datatypes.SampledValueType(
                            value=10,
                            context='Sample.Periodic',
                            measurand='Power.Active.Import',
                            phase=None,
                            location=None,
                            unit_of_measure=unit
                        ),
                        datatypes.SampledValueType(
                            value=10,
                            context='Sample.Periodic',
                            measurand='Power.Active.Import',
                            phase='L1',
                            location=None,
                            unit_of_measure=unit
                        ),
                    ]
                ),
            ]
        )
        response = await self.call(request)
        return response


async def main():
    async with websockets.connect(
            'ws://localhost:9000/CP_1',
            subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification())


if __name__ == '__main__':
    asyncio.run(main())
