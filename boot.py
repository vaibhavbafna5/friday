#!/usr/bin/env python3

import iterm2
import asyncio

perlDir = '~/Documents/SideProjects/perl'
chatDir = '~/Documents/SideProjects/cakechat'

async def main(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_window
    if window is not None:
        await window.async_create_tab()
    else:
        print("No current window")

    # create three splits: left for API, right for frontend, chat for conversation server
    actions = window.current_tab.current_session
    shell = await actions.async_split_pane(vertical=True)
    chat = await actions.async_split_pane(vertical=True)

    # set manual title for what this tab is doing
    await window.current_tab.async_set_title("Running: Perl")

    # Start chat server
    await chat.async_send_text(f"cd {chatDir}\n")
    await chat.async_send_text(f"conda activate cakechat_2\n")
    await chat.async_send_text("python bin/cakechat_server.py\n")

    # Start API by sending text sequences as if we typed them in the terminal
    await actions.async_send_text(f"cd {perlDir}\n")
    await actions.async_send_text(f"conda activate friday\n")
    await actions.async_send_text("rasa run actions\n")

    # Start frontend by sending text sequences as if we typed them in the terminal
    await shell.async_send_text(f"cd {perlDir}\n")
    await shell.async_send_text(f"conda activate friday\n")
    await shell.async_send_text("rasa shell\n")

iterm2.run_until_complete(main)