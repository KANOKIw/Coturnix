import requests
import base64

def image_to_data_url(image_path):
    with open(image_path, "rb") as img_file:
        binary_data = img_file.read()
        base64_data = base64.b64encode(binary_data).decode('utf-8')
        data_url = f"data:image/jpeg;base64,{base64_data}"
        return data_url
    
const = requests.post("https://kanokiw.com/room/upload", 
    {
    "d": {"me.png": [
        {
            "src": image_to_data_url("./img/Coturnix.jpg")
        }
    ]},
    "r": "rooooo"
    }
)

print(const.json())
