import requests

url = "http://localhost:9696/predict"

climate = {'aet_mean': 53.616665,
          'def_mean': 68.73333,
          'pdsi_mean': -0.3416663,
          'ppt_mean': 4.051060024240135,
          'soil_mean': 13.175,
          'tmax_mean': 24.96167,
          'tmin_mean': 10.447501,
          'pet_mean': 122.39166666666668,
          'q_mean': 1.3609765531356006,
          'srad_mean': 207.15833333333333,
          'vap_mean': 1.241999972363313,
          'vpd_mean': 0.7143785133043071,
          'ws_mean': 2.884166712562243}

response = requests.post(url, json=climate).json()

print(response)