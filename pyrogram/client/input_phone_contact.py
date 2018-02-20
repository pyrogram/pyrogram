from pyrogram.api.types import InputPhoneContact as RawInputPhoneContact


class InputPhoneContact:
    def __new__(cls, phone: str, first_name: str, last_name: str = ""):
        return RawInputPhoneContact(
            client_id=0,
            phone="+" + phone.strip("+"),
            first_name=first_name,
            last_name=last_name
        )
