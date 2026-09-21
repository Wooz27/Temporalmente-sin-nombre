import io
import base64
import qrcode

def generate_qr_base64 (data_to_code):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
        )
    qr.add_data(data_to_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    byte_data = buffer.getvalue()
    base64_bytes = base64.b64encode(byte_data)
    
    return base64_bytes.decode("utf-8")