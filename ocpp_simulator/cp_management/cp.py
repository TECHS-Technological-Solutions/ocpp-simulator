import uuid
import typer
from hashlib import sha256
from datetime import datetime, timedelta
import asyncio
import logging
import websockets
import questionary

import factory
from faker import Faker
from ocpp.routing import on
from ocpp.v201 import ChargePoint as Cp, call, call_result, datatypes, enums

logging.basicConfig(level=logging.INFO)

fake = Faker()


async def ask_question(enum_type, question: str):
    choices = [limit.value for limit in enum_type]
    answer = await questionary.select(
        question,
        choices=[choice for choice in choices]
    ).ask_async()
    return answer


class ChargePoint(Cp):

    async def send_boot_notification(self):
        model = typer.prompt('Enter charge point model', default=fake.pystr(1, 12))
        vendor_name = typer.prompt('Enter charge point vendor name', default=fake.pystr(1, 12))
        reason_type = await ask_question(enums.BootReasonType, "Which reason type:")
        request = call.BootNotificationPayload(
            charging_station={
                'model': model,
                'vendor_name': vendor_name
            },
            reason=reason_type
        )
        response = await self.call(request)
        return response

    async def send_status_notification(self):
        connector_id = int(typer.prompt('Enter connector ID', default=fake.random_int()))
        evse_id = int(typer.prompt('Enter EVSE ID', default=fake.random_int()))
        connector_status = await ask_question(enums.ConnectorStatusType, "Which connector status type:")
        request = call.StatusNotificationPayload(
            connector_id=connector_id,
            connector_status=connector_status,
            timestamp=str(datetime.now()),
            evse_id=evse_id
        )
        response = await self.call(request)
        return response

    async def send_authorize(self):
        id_type = await ask_question(enums.IdTokenType, "Which ID token type:")
        request = call.AuthorizePayload(
            id_token={
                'idToken': str(uuid.uuid4()),
                'type': id_type
            },
        )
        response = await self.call(request)
        return response

    async def send_clear_cache(self):
        request = call.ClearCachePayload()
        response = await self.call(request)
        return response

    async def send_cleared_charging_request(self):
        charging_limit_source = await ask_question(enums.ChargingLimitSourceType, "Which charging limit source:")
        request = call.ClearedChargingLimitPayload(
            charging_limit_source=charging_limit_source
        )
        response = await self.call(request)
        return response

    async def send_firmware_status_notification(self):
        firmware_status = await ask_question(enums.FirmwareStatusType, "Which firmware status notification:")
        request = call.FirmwareStatusNotificationPayload(
            status=firmware_status
        )
        response = await self.call(request)
        return response

    async def send_get_15118ev_certificate(self):
        iso15118_schema_version = typer.prompt('Enter ISO15188 version', default=fake.pystr(1, 12))
        certificate_action_type = await ask_question(enums.CertificateActionType, "Which certificate action type:")
        request = call.Get15118EVCertificatePayload(
            iso15118_schema_version=iso15118_schema_version,
            action=certificate_action_type,
            exi_request=str(uuid.uuid4())
        )
        response = await self.call(request)
        return response

    async def send_get_certificate_status(self):
        issuer_name = typer.prompt('Enter issuer name', default=fake.pystr(1, 128))
        issuer_key = typer.prompt('Enter issuer key', default=fake.pystr(1, 128))
        serial_number = typer.prompt('Enter serial number', default=fake.pystr(1, 40))
        responder_url = typer.prompt('Enter responder URL', default=fake.url())
        request = call.GetCertificateStatusPayload(
            ocsp_request_data=datatypes.OCSPRequestDataType(
                hash_algorithm=enums.HashAlgorithmType.sha256,
                issuer_name_hash=sha256(issuer_name.encode('utf-8')).hexdigest(),
                issuer_key_hash=sha256(issuer_key.encode('utf-8')).hexdigest(),
                responder_url=responder_url,
                serial_number=serial_number
            )
        )
        response = await self.call(request)
        return response

    async def send_get_display_messages(self):
        request_id = typer.prompt('Enter serial number', fake.random_int(min=0, max=10))
        request = call.GetDisplayMessagesPayload(
            request_id=request_id
        )
        response = await self.call(request)
        return response

    async def send_log_status_notification(self):
        log_status = await ask_question(enums.UploadLogStatusType, "Which log status notification:")
        request = call.LogStatusNotificationPayload(
            status=log_status
        )
        response = await self.call(request)
        return response

    async def send_meter_value(self):
        unit = await ask_question(enums.UnitOfMeasureType, "Which measure unit type:")
        evse_id = int(typer.prompt('Enter EVSE ID', default=fake.random_int()))
        value = int(typer.prompt('Enter sample value', default=fake.random_int()))
        value_context = await ask_question(enums.ReadingContextType, "Which value context type:")
        value_measurand = await ask_question(enums.MeasurandType, "Which value measurand type:")
        value_phase = await ask_question(enums.PhaseType, "Which value phase type:")
        request = call.MeterValuesPayload(
            evse_id=evse_id,
            meter_value=[
                datatypes.MeterValueType(
                    timestamp=str(datetime.now()),
                    sampled_value=[
                        datatypes.SampledValueType(
                            value=value,
                            context=value_context,
                            measurand=value_measurand,
                            phase=None,
                            location=None,
                            unit_of_measure=unit
                        ),
                        datatypes.SampledValueType(
                            value=value,
                            context=value_context,
                            measurand=value_measurand,
                            phase=value_phase,
                            location=None,
                            unit_of_measure=unit
                        ),
                    ]
                ),
                datatypes.MeterValueType(
                    timestamp=str(datetime.now() + timedelta(seconds=5)),
                    sampled_value=[
                        datatypes.SampledValueType(
                            value=value,
                            context=value_context,
                            measurand=value_measurand,
                            phase=None,
                            location=None,
                            unit_of_measure=unit
                        ),
                        datatypes.SampledValueType(
                            value=value,
                            context=value_context,
                            measurand=value_measurand,
                            phase=value_phase,
                            location=None,
                            unit_of_measure=unit
                        ),
                    ]
                ),
            ]
        )
        response = await self.call(request)
        return response

    async def send_notify_charging_limit(self):
        charging_limit_source = await ask_question(enums.ChargingLimitSourceType, "Which charging limit source:")
        request = call.NotifyChargingLimitPayload(
            charging_limit={
                'charging_limit_source': charging_limit_source,
                'is_grid_critical': True
            }
        )
        response = await self.call(request)
        return response

    async def send_notify_customer_information(self):
        data = typer.prompt('Enter customer information data', fake.pystr(1, 12))
        seq_no = typer.prompt('Enter sequence number', fake.random_int(min=0, max=10))
        request_id = typer.prompt('Enter request ID', fake.random_int(min=0, max=10))
        request = call.NotifyCustomerInformationPayload(
            data=data,
            seq_no=seq_no,
            generated_at=str(datetime.now()),
            request_id=request_id
        )
        response = await self.call(request)
        return response

    async def send_notify_display_messages(self):
        request_id = typer.prompt('Enter request ID', fake.random_int(min=0, max=10))
        request = call.NotifyDisplayMessagesPayload(
            request_id=request_id
        )
        response = await self.call(request)
        return response

    async def send_notify_ev_charging_needs(self):
        evse_id = typer.prompt('Enter EVSE ID', fake.random_int(min=0, max=100))
        energy_amount = typer.prompt('Enter energy amount', fake.random_int(min=0, max=100))
        ev_min_current = typer.prompt('Enter EV minimum current', fake.random_int(min=0, max=100))
        ev_max_current = typer.prompt('Enter EV maximum current', fake.random_int(min=ev_min_current))
        ev_max_voltage = typer.prompt('Enter EV maximum voltage', fake.random_int(min=0, max=100))
        request_energy_transfer = await ask_question(enums.EnergyTransferModeType, "Which energy transfer:")
        request = call.NotifyEVChargingNeedsPayload(
            evse_id=evse_id,
            charging_needs=datatypes.ChargingNeedsType(
                request_energy_transfer=request_energy_transfer,
                ac_charging_parameters=datatypes.ACChargingParametersType(
                    energy_amount=energy_amount,
                    ev_min_current=ev_min_current,
                    ev_max_current=ev_max_current,
                    ev_max_voltage=ev_max_voltage
                )
            )
        )
        response = await self.call(request)
        return response

    async def send_notify_ev_charging_schedule(self):
        evse_id = typer.prompt('Enter EVSE ID', fake.random_int(min=0, max=100))
        charging_schedule_period_limit = typer.prompt('Enter charging schedule period limit',
                                                      fake.pyfloat(min_value=1, max_value=100, positive=True))
        charging_rate_unit = await ask_question(enums.ChargingRateUnitType, "Which charging rate unit:")
        request = call.NotifyEVChargingSchedulePayload(
            time_base=str(datetime.now()),
            evse_id=evse_id,
            charging_schedule=datatypes.ChargingScheduleType(
                id=fake.random_int(),
                charging_rate_unit=charging_rate_unit,
                charging_schedule_period=[datatypes.ChargingSchedulePeriodType(
                    start_period=datetime.now().day,
                    limit=charging_schedule_period_limit
                )]
            )
        )
        response = await self.call(request)
        return response

    async def send_notify_event(self):
        seq_no = typer.prompt('Enter sequence number', fake.random_int(min=0, max=100))
        event_id = typer.prompt('Enter event ID', fake.random_int(min=0, max=100))
        actual_value = typer.prompt('Enter event data actual value', fake.pystr(1, 50))
        component_name = typer.prompt('Enter event data component name', fake.pystr(1, 50))
        component_instance = typer.prompt('Enter event data component instance', fake.pystr(1, 50))
        variable_name = typer.prompt('Enter event data variable name', fake.pystr(1, 50))
        trigger = await ask_question(enums.EventTriggerType, "Which trigger type:")
        event_notification_type = await ask_question(enums.EventNotificationType, "Which event notification type:")
        request = call.NotifyEventPayload(
            generated_at=str(datetime.now()),
            seq_no=seq_no,
            event_data=[datatypes.EventDataType(
                event_id=event_id,
                timestamp=str(datetime.now()),
                trigger=trigger,
                actual_value=actual_value,
                event_notification_type=event_notification_type,
                component=datatypes.ComponentType(
                    name=component_name,
                    instance=component_instance
                ),
                variable=datatypes.VariableType(
                    name=variable_name
                )
            )]
        )
        response = await self.call(request)
        return response

    async def send_notify_monitoring_report(self):
        request_id = typer.prompt('Enter request ID', fake.random_int(min=0, max=100))
        seq_no = typer.prompt('Enter sequence number', fake.random_int(min=0, max=100))
        request = call.NotifyMonitoringReportPayload(
            request_id=request_id,
            seq_no=seq_no,
            generated_at=str(datetime.now())
        )
        response = await self.call(request)
        return response

    async def send_notify_report(self):
        request_id = typer.prompt('Enter request ID', fake.random_int(min=0, max=100))
        seq_no = typer.prompt('Enter sequence number', fake.random_int(min=0, max=100))
        request = call.NotifyReportPayload(
            request_id=request_id,
            generated_at=str(datetime.now()),
            seq_no=seq_no
        )
        response = await self.call(request)
        return response

    async def send_publish_firmware_status_notification(self):
        status = await ask_question(enums.PublishFirmwareStatusType, "Which publish firmware status:")
        request = call.PublishFirmwareStatusNotificationPayload(
            status=status
        )
        response = await self.call(request)
        return response

    async def send_report_charging_profiles(self):
        evse_id = typer.prompt('Enter EVSE ID', fake.random_int(min=0, max=100))
        request_id = typer.prompt('Enter request ID', fake.random_int(min=0, max=100))
        charging_profile_id = typer.prompt('Enter charging profile ID', fake.random_int(min=0, max=100))
        stack_level = typer.prompt('Enter stack level', fake.random_int(min=0, max=100))
        charging_schedule_id = typer.prompt('Enter charging schedule ID', fake.random_int(min=0, max=100))
        charging_schedule_period_limit = typer.prompt('Enter charging schedule period limit',
                                                      fake.pyfloat(min_value=1, max_value=100, positive=True))
        charging_limit_type = await ask_question(enums.ChargingLimitSourceType, "Which charging limit type:")
        charging_profile_purpose = await ask_question(enums.ChargingProfilePurposeType,
                                                      "Which charging profile purpose:")
        charging_profile_kind = await ask_question(enums.ChargingProfileKindType, "Which charging profile kind:")
        charging_rate_unit = await ask_question(enums.ChargingRateUnitType, "Which charging rate unit:")
        request = call.ReportChargingProfilesPayload(
            request_id=request_id,
            charging_limit_source=charging_limit_type,
            evse_id=evse_id,
            charging_profile=[datatypes.ChargingProfileType(
                id=charging_profile_id,
                stack_level=stack_level,
                charging_profile_purpose=charging_profile_purpose,
                charging_profile_kind=charging_profile_kind,
                charging_schedule=[datatypes.ChargingScheduleType(
                    id=charging_schedule_id,
                    charging_rate_unit=charging_rate_unit,
                    charging_schedule_period=[datatypes.ChargingSchedulePeriodType(
                        start_period=datetime.now().day,
                        limit=charging_schedule_period_limit
                    )]
                )]
            )]
        )
        response = await self.call(request)
        return response

    async def send_heartbeat(self):
        request = call.HeartbeatPayload()
        response = await self.call(request)
        return response

    async def send_start_transaction(self):
        remote_start_id = typer.prompt('Enter remote start', fake.random_int(min=0, max=100))
        id_token_type = await ask_question(enums.IdTokenType, "Which ID token type:")
        request = call.RequestStartTransactionPayload(
            id_token={
                'idToken': str(uuid.uuid4()),
                'type': id_token_type
            },
            remote_start_id=remote_start_id
        )
        response = await self.call(request)
        return response

    async def send_stop_transaction(self):
        transaction_id = typer.prompt('Enter transaction ID', default=fake.pystr(1, 12))
        request = call.RequestStopTransactionPayload(
            transaction_id=transaction_id
        )
        response = await self.call(request)
        return response

    async def send_reservation_status_update(self):
        reservation_id = typer.prompt('Enter reservation ID', default=fake.pyint(1, 100))
        reservation_update_status = await ask_question(enums.ReservationUpdateStatusType,
                                                       "Which reservation update status:")
        request = call.ReservationStatusUpdatePayload(
            reservation_id=reservation_id,
            reservation_update_status=reservation_update_status
        )
        response = await self.call(request)
        return response

    async def send_security_event_notification(self):
        security_event_type = await questionary.select(
            "Which reservation update status: ",
            choices=[
                'FirmwareUpdated',
                'FailedToAuthenticateAtCsms',
                'CsmsFailedToAuthenticate',
                'SettingSystemTime',
                'StartupOfTheDevice',
                'ResetOrReboot',
                'SecurityLogWasCleared',
                'ReconfigurationOfSecurityParameters',
                'MemoryExhaustion',
                'InvalidMessages',
                'AttemptedReplayAttacks',
                'TamperDetectionActivated',
                'InvalidFirmwareSignature',
                'InvalidFirmwareSigningCertificate',
                'InvalidCsmsCertificate',
                'InvalidChargingStationCertificate',
                'InvalidTLSVersion',
                'InvalidTLSCipherSuite'
            ]
        ).ask_async()
        request = call.SecurityEventNotificationPayload(
            type=security_event_type,
            timestamp=str(datetime.now())
        )
        response = await self.call(request)
        return response

    async def send_sign_certificate(self):
        csr = typer.prompt('Enter Certificate Signing Request', fake.pystr(1, 100))
        request = call.SignCertificatePayload(
            csr=csr
        )
        response = await self.call(request)
        return response

    async def send_transaction_event(self):
        transaction_id = typer.prompt('Enter transaction ID', default=fake.pystr(1, 36))
        seq_no = typer.prompt('Enter sequence number', default=fake.pyint(1, 100))
        event_type = await ask_question(enums.TransactionEventType, "Which transaction event type:")
        trigger_reason = await ask_question(enums.TriggerReasonType, "Which trigger reason:")
        request = call.TransactionEventPayload(
            event_type=event_type,
            timestamp=str(datetime.now()),
            trigger_reason=trigger_reason,
            seq_no=seq_no,
            transaction_info=datatypes.TransactionType(
                transaction_id=transaction_id
            )

        )
        response = await self.call(request)
        return response

    @on(enums.Action.CancelReservation)
    async def on_cancel_reservation(self, status=enums.CancelReservationStatusType.accepted):
        return call_result.CancelReservationPayload(status=status)

    @on(enums.Action.CertificateSigned)
    async def on_certificate_signed(self, status=enums.CertificateSignedStatusType.accepted):
        return call_result.CertificateSignedPayload(status=status)

    @on(enums.Action.ChangeAvailability)
    async def on_change_availability(self, status=enums.ChangeAvailabilityStatusType.accepted):
        return call_result.ChangeAvailabilityPayload(status=status)

    @on(enums.Action.ClearChargingProfile)
    async def on_clear_charging_profile(self, status=enums.ClearChargingProfileStatusType.accepted):
        return call_result.ClearChargingProfilePayload(status=status)

    @on(enums.Action.ClearDisplayMessage)
    async def on_clear_display_message(self, status=enums.ClearChargingProfileStatusType.accepted):
        return call_result.ClearDisplayMessagePayload(status=status)

    @on(enums.Action.ClearVariableMonitoring)
    async def on_clear_variable_monitoring(self, monitoring_result_id: int = fake.random_int(1, 100),
                                           status=enums.ClearMonitoringStatusType.accepted):
        return call_result.ClearVariableMonitoringPayload(
            clear_monitoring_result=[{
                'status': status,
                'id': monitoring_result_id,
            }]
        )

    @on(enums.Action.CostUpdate)
    async def on_cost_updated(self):
        return call_result.CostUpdatedPayload()

    @on(enums.Action.CustomerInformation)
    async def on_customer_info(self, status=enums.CustomerInformationStatusType.accepted):
        return call_result.CustomerInformationPayload(status=status)

    @on(enums.Action.DataTransfer)
    async def on_data_transfer(self, status=enums.DataTransferStatusType.accepted):
        return call_result.DataTransferPayload(status=status)

    @on(enums.Action.DeleteCertificate)
    async def on_delete_certificate(self, status=enums.DeleteCertificateStatusType.accepted):
        return call_result.DeleteCertificatePayload(status=status)

    @on(enums.Action.GetBaseReport)
    async def on_get_base_report(self, status=enums.GenericDeviceModelStatusType.accepted):
        return call_result.GetBaseReportPayload(status=status)

    @on(enums.Action.GetChargingProfiles)
    async def on_get_charging_profiles(self, status=enums.GetChargingProfileStatusType.accepted):
        return call_result.GetChargingProfilesPayload(status=status)

    @on(enums.Action.GetCompositeSchedule)
    async def on_get_composite_schedule(self, status=enums.GenericStatusType.accepted):
        return call_result.GetCompositeSchedulePayload(status=status)

    @on(enums.Action.GetDisplayMessages)
    async def on_get_display_messages(self, status=enums.GetDisplayMessagesStatusType.accepted):
        return call_result.GetDisplayMessagesPayload(status=status)

    @on(enums.Action.GetInstalledCertificateIds)
    async def on_get_installed_certificate_ids(self, status=enums.GetInstalledCertificateStatusType.accepted):
        return call_result.GetInstalledCertificateIdsPayload(status=status)

    @on(enums.Action.GetLocalListVersion)
    async def on_get_local_list_version(self, version_number: int = fake.random_int(1, 1000)):
        return call_result.GetLocalListVersionPayload(version_number=version_number)

    @on(enums.Action.GetLog)
    async def on_get_log(self, status=enums.LogStatusType.accepted):
        return call_result.GetLogPayload(status=status)

    @on(enums.Action.GetMonitoringReport)
    async def on_get_monitoring_report(self, status=enums.InstallCertificateStatusType.accepted):
        return call_result.GetMonitoringReportPayload(status=status)

    @on(enums.Action.PublishFirmware)
    async def on_publish_firmware(self, status=enums.GenericStatusType.accepted):
        return call_result.PublishFirmwarePayload(status=status)

    @on(enums.Action.ReserveNow)
    async def on_reserve_now(self, status=enums.ReserveNowStatusType.accepted):
        return call_result.ReserveNowPayload(status=status)

    @on(enums.Action.Reset)
    async def on_reset(self, status=enums.ResetStatusType.accepted):
        return call_result.ResetPayload(status=status)

    @on(enums.Action.SendLocalList)
    async def on_send_local_list(self, status=enums.SendLocalListStatusType.accepted):
        return call_result.SendLocalListPayload(status=status)

    @on(enums.Action.SetChargingProfile)
    async def on_set_charging_profile(self, status=enums.ChargingProfileStatus.accepted):
        return call_result.SetChargingProfilePayload(status=status)

    @on(enums.Action.SetDisplayMessage)
    async def on_set_display_message(self, status=enums.DisplayMessageStatusType.accepted):
        return call_result.SetDisplayMessagePayload(status=status)

    @on(enums.Action.SetMonitoringBase)
    async def on_set_monitoring_base(self, status=enums.GenericDeviceModelStatusType.accepted):
        return call_result.SetMonitoringBasePayload(status=status)

    @on(enums.Action.SetMonitoringLevel)
    async def on_set_monitoring_level(self, status=enums.GenericStatusType.accepted):
        return call_result.SetMonitoringLevelPayload(status=status)

    @on(enums.Action.SetNetworkProfile)
    async def on_set_network_profile(self, status=enums.SetNetworkProfileStatusType.accepted):
        return call_result.SetNetworkProfilePayload(status=status)

    @on(enums.Action.SetVariableMonitoring)
    async def on_set_variable_monitoring(self, status=enums.SetMonitoringStatusType.accepted,
                                         monitor_type=enums.MonitorType.delta, severity: int = fake.random_int(0, 10),
                                         component_name: str = factory.Faker('pystr'),
                                         component_instance: str = factory.Faker('pystr'),
                                         variable_name: str = factory.Faker('pystr')):
        return call_result.SetVariableMonitoringPayload(
            set_monitoring_result=datatypes.SetMonitoringResultType(
                status=status,
                type=monitor_type,
                severity=severity,
                component=datatypes.ComponentType(
                    name=component_name,
                    instance=component_instance
                ),
                variable=datatypes.VariableType(
                    name=variable_name
                )
            )
        )

    @on(enums.Action.SetVariables)
    async def on_set_variables(self, status=enums.SetVariableStatusType.accepted,
                               component_name: str = factory.Faker('pystr'),
                               component_instance: str = factory.Faker('pystr'),
                               variable_name: str = factory.Faker('pystr')):
        return call_result.SetVariablesPayload(
            set_variable_result=datatypes.SetVariableResultType(
                attribute_status=status,
                component=datatypes.ComponentType(
                    name=component_name,
                    instance=component_instance
                ),
                variable=datatypes.VariableType(
                    name=variable_name
                )
            )
        )

    @on(enums.Action.TriggerMessage)
    async def on_trigger_message(self, status=enums.TriggerMessageStatusType.accepted):
        return call_result.TriggerMessagePayload(status=status)

    @on(enums.Action.UnlockConnector)
    async def on_unlock_connector(self, status=enums.UnlockStatusType.unlocked):
        return call_result.UnlockConnectorPayload(status=status)

    @on(enums.Action.UnpublishFirmware)
    async def on_unpublish_firmware(self, status=enums.UnpublishFirmwareStatusType.unpublished):
        return call_result.UnpublishFirmwarePayload(status=status)

    @on(enums.Action.UpdateFirmware)
    async def on_update_firmware(self, status=enums.UpdateFirmwareStatusType.accepted):
        return call_result.UpdateFirmwarePayload(status=status)

    messages = {
        'Authorize': send_authorize,
        'Clear cache': send_clear_cache,
        'Cleared Charging Limit': send_cleared_charging_request,
        'Firmware Status Notification': send_firmware_status_notification,
        'Get 15118 EV Certificate': send_get_15118ev_certificate,
        'Get Certificate Status': send_get_certificate_status,
        'Get Display Messages': send_get_display_messages,
        'Log Status Notification': send_log_status_notification,
        'Meter Value': send_meter_value,
        'Notify Charging Limit': send_notify_charging_limit,
        'Notify Customer Information': send_notify_customer_information,
        'Notify Display Messages': send_notify_display_messages,
        'Notify EV Charging Needs': send_notify_ev_charging_needs,
        'Notify EV Charging Schedule': send_notify_ev_charging_schedule,
        'Notify Event': send_notify_event,
        'Notify Monitoring Report': send_notify_monitoring_report,
        'Notify Report': send_notify_report,
        'Publish Firmware Status': send_publish_firmware_status_notification,
        'Report Charging Profiles': send_report_charging_profiles,
        'Heartbeat': send_heartbeat,
        'Start transaction': send_start_transaction,
        'Stop transaction': send_stop_transaction,
        'Reservation Status Update': send_reservation_status_update,
        'Security Event Notification': send_security_event_notification,
        'Sign Certificate': send_sign_certificate,
        'Transaction Event': send_transaction_event

    }
