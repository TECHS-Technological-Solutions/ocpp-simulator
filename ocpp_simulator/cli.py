import asyncio
import typer
import questionary
import websockets

from cp_management import cp as Cp  # noqa

app = typer.Typer()


async def connect_cp_to_central_system(url_websocket_address: str, cp_serial_number: str) -> Cp.ChargePoint:
    # Connect to central system
    ws = await websockets.connect(
        f'ws://{url_websocket_address}/{cp_serial_number}',
        subprotocols=['ocpp2.0.1']
    )
    cp = Cp.ChargePoint(cp_serial_number, ws)
    loop = asyncio.get_event_loop()
    loop.create_task(cp.start())

    # Boot notification
    typer.secho('Boot notification', fg=typer.colors.BRIGHT_GREEN, bold=True)
    message = await cp.send_boot_notification()
    typer.echo(message)

    # Status notification
    typer.secho('Status notification', fg=typer.colors.BRIGHT_GREEN, bold=True)
    message = await cp.send_status_notification()
    typer.echo(message)

    return cp


async def send_message(cp, message: str):
    response = await cp.messages[message](cp)
    typer.echo(response)


@app.command()
def start():
    async def _start():
        # Program initialization
        program_continue = typer.confirm("You have just started Charge Point simulator, do you want to continue")
        if not program_continue:
            raise typer.Abort()

        # Central system and charge point information
        cp_serial_number = typer.prompt("Enter charge point serial number")
        central_system_url = typer.prompt("Enter central system URL")

        # Connect to charge point
        cp = await connect_cp_to_central_system(central_system_url, cp_serial_number)

        answer = await questionary.select(
            "What action do you want to perform: ",
            choices=[
                'Send an OCPP message',
                'Quit'
            ]
        ).ask_async()

        if answer == 'Quit':
            raise typer.Abort()

        # Sending messages to particular charge point
        while True:
            message = await questionary.select(
                "What message do you want to send: ",
                choices=list(cp.messages.keys())
            ).ask_async()

            await send_message(cp, message)

            stop_sending_messages = typer.confirm("Do you want to send another message?")
            if not stop_sending_messages:
                break

    # Make Typer command running in async version
    asyncio.run(_start())


if __name__ == '__main__':
    typer.run(start)
