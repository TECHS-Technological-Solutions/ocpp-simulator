import typer
import questionary
import websockets
import asyncio

from cp_management import central_system, cp as Cp

app = typer.Typer()


async def connect_to_central_system(address: str, port: int) -> websockets.WebSocketServer:
    server = await websockets.serve(
        central_system.on_connect,
        address,
        port,
        subprotocols=['ocpp2.0.1']
    )
    typer.echo("WebSocket Server Started")
    return server


async def connect_to_cp(address: str, port: int, cp_serial_number: str) -> Cp.ChargePoint:
    ws = await websockets.connect(
        f'ws://{address}:{port}/{cp_serial_number}',
        subprotocols=['ocpp2.0.1']
    )
    cp = Cp.ChargePoint(cp_serial_number, ws)
    loop = asyncio.get_event_loop()
    loop.create_task(cp.start())
    typer.secho('Boot notification', fg=typer.colors.BRIGHT_GREEN, bold=True)
    await cp.send_boot_notification()
    typer.secho('Status notification', fg=typer.colors.BRIGHT_GREEN, bold=True)
    await cp.send_status_notification()
    return cp


async def send_message(cp, message: str):
    if message == 'Heartbeat':
        await cp.send_heartbeat()
    if message == 'Authorize':
        await cp.send_authorize()
    if message == 'Start transaction':
        await cp.send_start_transaction()
    if message == 'Stop transaction':
        await cp.send_stop_transaction('1')
    if message == 'Meter Value':
        await cp.send_meter_value(1)


@app.command()
def start():
    async def _start():
        # Program initialization
        program_continue = typer.confirm("You have just started Charge Point simulator, do you want to continue")
        if not program_continue:
            raise typer.Abort()

        # Central system and charge point information
        cp_serial_number = typer.prompt("Enter charge point serial number")
        try:
            central_system_url = typer.prompt("Enter central system URL")
            url = central_system_url.split(":")
            address = url[0]
            port = int(url[1])
        except ValueError:
            typer.echo('You have entered wrong central system URL.')
            raise typer.Abort()

        # Connect to central system and charge point
        server = await connect_to_central_system(address, int(port))
        cp = await connect_to_cp(address, int(port), cp_serial_number)

        answer = await questionary.select(
            "What action do you want to perform: ",
            choices=[
                'Quit',
                'Send an OCPP message'
            ]
        ).ask_async()

        if answer == 'Quit':
            server.close()
            raise typer.Abort()

        # Sending messages to particular charge point
        while True:
            message = await questionary.select(
                "What message do you want to send: ",
                choices=[
                    'Heartbeat',
                    'Start transaction',
                    'Stop transaction',
                    'Authorize',
                    'Meter Value'
                ]
            ).ask_async()

            await send_message(cp, message)

            stop_sending_messages = typer.confirm("Do you want to send another message?")
            if not stop_sending_messages:
                server.close()
                break

    # Make Typer command running in async version
    asyncio.run(_start())


if __name__ == '__main__':
    typer.run(start)
