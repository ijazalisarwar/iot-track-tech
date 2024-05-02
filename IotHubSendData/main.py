import os
import asyncio
import base64
import hmac
import hashlib
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import uuid
provisioning_host = "tracktech.azure-devices-provisioning.net"
id_scope = "0ne0021155F"
symmetric_key = "bY4xQlYyMq/Gfi5HrY02oGovPap48kTrohRyvs4TkArCqGxAHrjMm2rbnd9bbpiLN69JPGyB9tUY4j5VH6DEBA=="

def derive_device_key(device_id):
    """
    The unique device ID and the group master key should be encoded into "utf-8"
    After this the encoded group master key must be used to compute an HMAC-SHA256 of the encoded registration ID.
    Finally the result must be converted into Base64 format.
    The device key is the "utf-8" decoding of the above result.
    """
    message = device_id.encode("utf-8")
    signing_key = base64.b64decode(symmetric_key.encode("utf-8"))
    signed_hmac = hmac.HMAC(signing_key, message, hashlib.sha256)
    device_key_encoded = base64.b64encode(signed_hmac.digest())
    return device_key_encoded.decode("utf-8")


async def register_device(registration_id, derived_device_symmetric_key):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=derived_device_symmetric_key,
    )
    registration_result = await provisioning_device_client.register()
    print(registration_result)

    return registration_result



async def main():
    device_id = str("test_deivce")
    derived_device_id = derive_device_key(device_id)
    print('registring this id...' + str(device_id))
    registration_result = await register_device(device_id, derived_device_id)
    if registration_result.status == "assigned":
        device_id = registration_result.registration_state.device_id
        print(
            "Will send telemetry from the provisioned device with id {id}".format(id=device_id)
        )
        device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=derived_device_id,
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
        )
        # Assign the Id just for print statements
        device_client.id = device_id
        print("device client: " + str(device_client))

        await device_client.connect()
        msg = Message("test wind speed ")
        msg.message_id = uuid.uuid4()
        await device_client.send_message(msg)
        print("done sending message")
    else:
        print("Can not send telemetry from the provisioned device")

if __name__ == "__main__":
    asyncio.run(main())

