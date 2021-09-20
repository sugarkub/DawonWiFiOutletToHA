# 다원DNS WiFi 플러그 로컬화하여 HA에 등록하기

## HA에 MQTT 설치하기

저는 도커를 이용하여 MQTT 서버를 설치하였습니다. 이 때 사용한 docker-compose의 설정 정보는 다음과 같습니다.

```yaml
# docker-compose.yml

version: '3'
services:

  mosquitto:
    container_name: mosquitto
    image: eclipse-mosquitto
    volumes:
      - /data/mosquitto/config:/mosquitto/config
      - /data/mosquitto/data:/mosquitto/data
      - /data/mosquitto/log:/mosquitto/log
    restart: always
    network_mode: host

```

HA 설정에서도 MQTT를 추가해줍니다.

```yaml
# HA configuration.yaml

mqtt:
  broker: {서버 주소}
```


## 플러그 초기화하기

아래 링크를 참고하여 플러그를 MQTT 서버에 등록시켜줍니다. 참고로 AIPM 앱에서 플러그를 삭제하면 자동으로 초기화되고, 등록모드로 진입합니다.

- https://cafe.naver.com/koreassistant/1977
- https://cafe.naver.com/koreassistant/4600

## HA에 등록하기

HA의 설정 파일 경로가 /data/homeassistant 라고 가정했을때 다음과 같이 폴더 구조를 만들어줍니다.

- /data/homeassistant/switch
- /data/homeassistant/sensor
- /data/homeassistant/automation
- /data/homeassistant/utility_meter

HA의 설정파일인 configuration.yaml 파일을 플러그를 추가/삭제할때마다 수정하는게 좀 번거로울 수 있으므로, 각 플러그별 설정 파일을 별도로 생성하여 사용할 수 있도록 configuration.yaml 파일을 다음과 같이 수정합니다. 해당 항목이 없으면 새로 추가합니다.

```yaml
# HA configuration.yaml

homeassistant:
  customize: !include customize.yaml

automation: !include_dir_list automation/
switch: !include_dir_list switch/
sensor: !include_dir_list sensor/
utility_meter: !include_dir_merge_named utility_meter/
```

### 스위치, 내부온도 센서, 전력 측정 센서, 센서 정보 갱신 자동화, 유틸리티 센서 등록

```bash
python3 dawon_to_ha.py {mac_address} {friendly_name} {model_name}[optional]
```

### 자동 전원 끄기 자동화 등록

```bash
python3 power_off.py {mac_address} {friendly_name}
```

## 동작 확인

이 스크립트 및 아래 플러그 등록 코드를 사용하여 동작을 확인한 제품 리스트는 다음과 같습니다.

- PM-B530-W
- PM-B540-W
- PM-M130-WE

## 특이사항

- 사용법은 samples.sh 파일을 참고하면 됩니다.
- 멀티탭의 경우에는 내부 온도 값이 올라오지 않고 있습니다.