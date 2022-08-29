import logging
import websockets
from datetime import datetime
import uuid
from hashlib import sha256

from faker import Faker

from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result, enums, call, datatypes


logging.basicConfig(level=logging.INFO)


fake = Faker()


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

    @on(enums.Action.ClearCache)
    async def on_clear_cache(self, **kwargs):
        return call_result.ClearCachePayload(
            status=enums.ClearCacheStatusType.accepted
        )

    @on(enums.Action.ClearedChargingLimit)
    async def on_cleared_charging_limit(self, **kwargs):
        return call_result.ClearedChargingLimitPayload()

    @on(enums.Action.FirmwareStatusNotification)
    async def on_firmware_status_notification(self, **kwargs):
        return call_result.FirmwareStatusNotificationPayload()

    @on(enums.Action.Get15118EVCertificate)
    async def on_get_15118ev_certificate(self, **kwargs):
        return call_result.Get15118EVCertificatePayload(
            status=enums.Iso15118EVCertificateStatusType.accepted,
            exi_response='Success message'
        )

    @on(enums.Action.GetCertificateStatus)
    async def on_get_certificate_status(self, **kwargs):
        return call_result.GetCertificateStatusPayload(
            status=enums.GetCertificateStatusType.accepted
        )

    @on(enums.Action.GetDisplayMessages)
    async def on_get_display_messages(self, **kwargs):
        return call_result.GetDisplayMessagesPayload(
            status=enums.GetDisplayMessagesStatusType.accepted
        )

    @on(enums.Action.LogStatusNotification)
    async def on_log_status_notification(self, **kwargs):
        return call_result.LogStatusNotificationPayload()

    @on(enums.Action.MeterValues)
    async def on_meter_value(self, **kwargs):
        return call_result.MeterValuesPayload()

    @on(enums.Action.NotifyChargingLimit)
    async def on_notify_charging_limit(self, **kwargs):
        return call_result.NotifyChargingLimitPayload()

    @on(enums.Action.NotifyCustomerInformation)
    async def on_notify_customer_information(self, **kwargs):
        return call_result.NotifyCustomerInformationPayload()

    @on(enums.Action.NotifyDisplayMessages)
    async def on_notify_display_message(self, **kwargs):
        return call_result.NotifyDisplayMessagesPayload()

    @on(enums.Action.NotifyEVChargingNeeds)
    async def on_notify_ev_charging_needs(self, **kwargs):
        return call_result.NotifyEVChargingNeedsPayload(
            status=enums.NotifyEVChargingNeedsStatusType.accepted
        )

    @on(enums.Action.NotifyEVChargingSchedule)
    async def on_notify_ev_charging_schedule(self, **kwargs):
        return call_result.NotifyEVChargingSchedulePayload(
            status=enums.GenericStatusType.accepted
        )

    @on(enums.Action.NotifyEvent)
    async def on_notify_event(self, **kwargs):
        return call_result.NotifyEventPayload()

    @on(enums.Action.NotifyMonitoringReport)
    async def on_notify_monitoring_report(self, **kwargs):
        return call_result.NotifyMonitoringReportPayload()

    @on(enums.Action.NotifyReport)
    async def on_notify_report(self, **kwargs):
        return call_result.NotifyReportPayload()

    @on(enums.Action.PublishFirmwareStatusNotification)
    async def on_publish_firmware_status_notification(self, **kwargs):
        return call_result.PublishFirmwareStatusNotificationPayload()

    @on(enums.Action.ReportChargingProfiles)
    async def on_report_charging_profiles(self, **kwargs):
        return call_result.ReportChargingProfilesPayload()

    @on(enums.Action.Heartbeat)
    async def on_heartbeat(self, **kwargs):
        return call_result.HeartbeatPayload(
            current_time='10.10.2010'
        )

    @on(enums.Action.ReservationStatusUpdate)
    async def on_reservation_status_update(self, **kwargs):
        return call_result.ReservationStatusUpdatePayload()

    @on(enums.Action.SecurityEventNotification)
    async def on_security_event_notification(self, **kwargs):
        return call_result.SecurityEventNotificationPayload()

    @on(enums.Action.SignCertificate)
    async def on_sign_certificate(self, **kwargs):
        return call_result.SignCertificatePayload(
            status=enums.GenericStatusType.accepted
        )

    @on(enums.Action.TransactionEvent)
    async def on_transaction_event(self, **kwargs):
        return call_result.TransactionEventPayload(
            total_cost=100
        )

    async def send_cancel_reservation(self):
        request = call.CancelReservationPayload(
            reservation_id=12
        )
        response = await self.call(request)
        return response

    async def send_certificate_signed(self):
        request = call.CertificateSignedPayload(
            certificate_chain=fake.pystr(1, 12)
        )
        response = await self.call(request)
        return response

    async def send_change_availability(self):
        request = call.ChangeAvailabilityPayload(
            operational_status=enums.OperationalStatusType.operative
        )
        response = await self.call(request)
        return response

    async def send_clear_charging_profile(self):
        request = call.ClearChargingProfilePayload()
        response = await self.call(request)
        return response

    async def send_clear_display_message(self):
        request = call.ClearDisplayMessagePayload(
            id=fake.random_int(1, 100)
        )
        response = await self.call(request)
        return response

    async def send_clear_variable_monitoring(self):
        request = call.ClearVariableMonitoringPayload(
            id=[fake.random_int(1, 100)]
        )
        response = await self.call(request)
        return response

    async def send_cost_updated(self):
        request = call.CostUpdatedPayload(
            total_cost=fake.random_int(1, 100),
            transaction_id=str(uuid.uuid4())
        )
        response = await self.call(request)
        return response

    async def send_customer_info(self):
        request = call.CustomerInformationPayload(
            request_id=fake.random_int(1, 100),
            report=True,
            clear=True
        )
        response = await self.call(request)
        return response

    async def send_data_transfer(self):
        request = call.DataTransferPayload(
            vendor_id=str(uuid.uuid4())
        )
        response = await self.call(request)
        return response

    async def send_delete_certificate(self):
        request = call.DeleteCertificatePayload(
            certificate_hash_data=datatypes.CertificateHashDataType(
                hash_algorithm=enums.HashAlgorithmType.sha256,
                issuer_name_hash=sha256(fake.pystr(1, 128).encode('utf-8')).hexdigest(),
                issuer_key_hash=sha256(fake.pystr(1, 128).encode('utf-8')).hexdigest(),
                serial_number=fake.pystr(1, 40)
            )
        )
        response = await self.call(request)
        return response

    async def send_get_base_report(self):
        request = call.GetBaseReportPayload(
            request_id=fake.random_int(1, 100),
            report_base=enums.ReportBaseType.configuration_inventory
        )
        response = await self.call(request)
        return response

    async def send_get_charging_profiles(self):
        request = call.GetChargingProfilesPayload(
            request_id=fake.random_int(1, 100),
            charging_profile=datatypes.ChargingProfileCriterionType(
                stack_level=fake.random_int(min=0, max=100),
                charging_profile_purpose=enums.ChargingProfilePurposeType.tx_profile
                )
            )
        response = await self.call(request)
        return response

    async def send_get_composite_schedule(self):
        request = call.GetCompositeSchedulePayload(
            duration=fake.random_int(min=0, max=100),
            evse_id=fake.random_int(min=0, max=100)
            )
        response = await self.call(request)
        return response

    async def send_get_display_messages(self):
        request = call.GetDisplayMessagesPayload(
            request_id=fake.random_int(min=0, max=100)
            )
        response = await self.call(request)
        return response

    async def send_get_installed_certificate_ids(self):
        request = call.GetInstalledCertificateIdsPayload()
        response = await self.call(request)
        return response

    async def send_get_local_list_version(self):
        request = call.GetLocalListVersionPayload()
        response = await self.call(request)
        return response

    async def send_get_log(self):
        request = call.GetLogPayload(
            log_type=enums.LogType.security_log,
            request_id=fake.random_int(min=0, max=100),
            log=datatypes.LogParametersType(
                remote_location=fake.pystr(1, 128)
            )
        )
        response = await self.call(request)
        return response

    async def send_get_monitoring_report(self):
        request = call.GetMonitoringReportPayload(
            request_id=fake.random_int(min=0, max=100)
            )
        response = await self.call(request)
        return response

    async def send_publish_firmware(self):
        request = call.PublishFirmwarePayload(
            location=fake.pystr(1, 512),
            checksum=fake.pystr(1, 20),
            request_id=fake.random_int(min=0, max=100)
            )
        response = await self.call(request)
        return response

    async def send_reserve_now(self):
        request = call.ReserveNowPayload(
            id=fake.random_int(min=0, max=100),
            expiry_date_time=str(datetime.now()),
            id_token={
                'idToken': str(uuid.uuid4()),
                'type': enums.IdTokenType.central
            }
        )
        response = await self.call(request)
        return response

    async def send_reset(self):
        request = call.ResetPayload(
            type=enums.ResetType.immediate
        )
        response = await self.call(request)
        return response

    async def send_send_local_list(self):
        request = call.SendLocalListPayload(
            version_number=fake.random_int(min=0, max=100),
            update_type=enums.UpdateType.full
        )
        response = await self.call(request)
        return response

    async def send_set_charging_profile(self):
        request = call.SetChargingProfilePayload(
            evse_id=fake.random_int(min=0, max=100),
            charging_profile=datatypes.ChargingProfileType(
                id=fake.random_int(min=0, max=100),
                stack_level=fake.random_int(min=0, max=100),
                charging_profile_purpose=enums.ChargingProfilePurposeType.charging_station_max_profile,
                charging_profile_kind=enums.ChargingProfileKindType.absolute,
                charging_schedule=[datatypes.ChargingScheduleType(
                    id=fake.random_int(min=0, max=100),
                    charging_rate_unit=enums.ChargingRateUnitType.amps,
                    charging_schedule_period=[datatypes.ChargingSchedulePeriodType(
                        start_period=datetime.now().day,
                        limit=fake.pyfloat(min_value=1, max_value=100)
                    )]
                )]
            )
        )
        response = await self.call(request)
        return response

    async def send_set_display_message(self):
        request = call.SetDisplayMessagePayload(
            message=datatypes.MessageInfoType(
                id=fake.random_int(min=0, max=100),
                priority=enums.MessagePriorityType.normal_cycle,
                message=datatypes.MessageContentType(
                    format=enums.MessageFormatType.ascii,
                    content=fake.pystr(1, 512),
                    language=fake.pystr(1, 8)
                )
            )
        )
        response = await self.call(request)
        return response

    async def send_set_monitoring_base(self):
        request = call.SetMonitoringBasePayload(
            monitoring_base=enums.MonitorBaseType.all
        )
        response = await self.call(request)
        return response

    async def send_set_monitoring_level(self):
        request = call.SetMonitoringLevelPayload(
            severity=fake.random_int(min=0, max=9)
        )
        response = await self.call(request)
        return response

    async def send_set_network_profile(self):
        request = call.SetNetworkProfilePayload(
            configuration_slot=fake.random_int(min=0, max=100),
            connection_data=datatypes.NetworkConnectionProfileType(
                ocpp_version=enums.OCPPVersionType.ocpp20,
                ocpp_transport=enums.OCPPTransportType.json,
                ocpp_csms_url=fake.url(),
                message_timeout=fake.random_int(min=0, max=100),
                security_profile=fake.random_int(min=0, max=9),
                ocpp_interface=enums.OCPPInterfaceType.wired0
            )
        )
        response = await self.call(request)
        return response

    async def send_set_variable_monitoring(self):
        request = call.SetVariableMonitoringPayload(
            set_monitoring_data=[datatypes.SetMonitoringDataType(
                id=fake.random_int(min=0, max=100),
                value=fake.pyfloat(min_value=1, max_value=100),
                type=enums.MonitorType.periodic,
                severity=fake.random_int(min=0, max=9),
                component=datatypes.ComponentType(
                    name=str(uuid.uuid4()),
                ),
                variable=datatypes.VariableType(
                    name=str(uuid.uuid4())
                )
            )]
        )
        response = await self.call(request)
        return response

    async def send_set_variables(self):
        request = call.SetVariablesPayload(
            set_variable_data=[datatypes.SetVariableDataType(
                attribute_type=enums.AttributeType.maxSet,
                attribute_value=fake.pystr(1, 1000),
                component=datatypes.ComponentType(
                    name=str(uuid.uuid4()),
                ),
                variable=datatypes.VariableType(
                    name=str(uuid.uuid4())
                )
            )]
        )
        response = await self.call(request)
        return response

    async def send_trigger_message(self):
        request = call.TriggerMessagePayload(
            requested_message=enums.MessageTriggerType.log_status_notification
        )
        response = await self.call(request)
        return response

    async def send_unlock_connector(self):
        request = call.UnlockConnectorPayload(
            evse_id=fake.random_int(min=0, max=100),
            connector_id=fake.random_int(min=0, max=100)
        )
        response = await self.call(request)
        return response

    async def send_unpublish_firmware(self):
        request = call.UnpublishFirmwarePayload(
            checksum=fake.pystr(1, 32)
        )
        response = await self.call(request)
        return response

    async def send_update_firmware(self):
        request = call.UpdateFirmwarePayload(
            request_id=fake.random_int(min=0, max=100),
            firmware=datatypes.FirmwareType(
                location=fake.pystr(1, 512),
                retrieval_date_time=str(datetime.now())
            )
        )
        response = await self.call(request)
        return response


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


async def start_central_system():
    server = await websockets.serve(
        on_connect,
        "0.0.0.0",
        9000,
        subprotocols=['ocpp2.0.1']
    )
    logging.info("WebSocket Server Started")
    return server
