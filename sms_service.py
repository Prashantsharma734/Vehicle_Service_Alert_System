from twilio.rest import Client

def send_sms(message, to_number):
    try:
        account_sid = "YOUR_SID"
        auth_token = "YOUR_AUTH_TOKEN"

        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_="+918114128701",   # Your Twilio number
            to=to_number
        )

        return True

    except Exception as e:
        print("SMS Error:", e)
        return False
