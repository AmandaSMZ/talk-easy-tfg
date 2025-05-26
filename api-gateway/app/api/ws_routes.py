
'''
@app.websocket("/talk")
async def talk_to_talkeasy(
    client_ws: WebSocket,
    user = Depends(get_current_user)
):
    await client_ws.accept()
    user_id = str(user["id"])
    talkeasy_url = (
      f"ws://talk_easy:8000/ws"
      f"?token={INTERNAL_SECRET}"
      f"&user_id={user_id}"
    )
    try:
        async with ws_connect(talkeasy_url) as srv_ws:
            # Bucle único: del microservicio → al cliente
            while True:
                msg = await srv_ws.recv()         # recibe de TalkEasy
                await client_ws.send_text(msg)    # envía al cliente
    except WebSocketDisconnect:
        pass
    finally:
        await client_ws.close()

'''