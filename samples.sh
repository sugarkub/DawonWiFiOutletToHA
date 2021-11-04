#!
rm /data/homeassistant/automation/*
rm /data/homeassistant/switch/*
rm /data/homeassistant/sensor/*
rm /data/homeassistant/utility_meter/*
rm /data/homeassistant/customize.yaml

python3 ./dawon_to_ha.py 827d3a1fb962 "로움"
python3 ./dawon_to_ha.py F6CFA2E568F9 "파일서버"
python3 ./dawon_to_ha.py 86f3eb6e7fea "김치냉장고"
python3 ./dawon_to_ha.py F6CFA2E60B61 "세라젬"
python3 ./dawon_to_ha.py E298068148AC "프로젝터"
python3 ./dawon_to_ha.py F6CFA2E5AF1B "전기장판"
python3 ./dawon_to_ha.py E298069CB51D "안방 PC"
python3 ./dawon_to_ha.py 620194603360 "안방 멀티탭"
python3 ./dawon_to_ha.py F6CFA2E54943 "냉장고"
python3 ./dawon_to_ha.py 62019460339d "PC1"
python3 ./dawon_to_ha.py 2ef4322edc38 "PC2"

python3 ./power_off.py F6CFA2E568F9 "파일서버"
python3 ./power_off.py F6CFA2E60B61 "세라젬"
python3 ./power_off.py E298068148AC "프로젝터"
python3 ./power_off.py F6CFA2E5AF1B "전기장판"
python3 ./power_off.py E298069CB51D "안방 PC"
python3 ./power_off.py 620194603360 "안방 멀티탭"
python3 ./power_off.py 62019460339d "PC1"
python3 ./power_off.py 2ef4322edc38 "PC2"
