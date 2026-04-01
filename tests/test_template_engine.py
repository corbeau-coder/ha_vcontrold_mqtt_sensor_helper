draft from https://github.com/Alexandre-io/homeassistant-vcontrol/blob/main/vcontrold/DOCS.md

mqtt:
  binary_sensor:
    - name: "Status Zirklulationspumpe"
      unique_id: "vcontroldgetPumpeStatusZirku"
      state_topic: "openv/getPumpeStatusZirku"
      device_class: running
      value_template: "{% if(value|int == '0') %}OFF{% else %}ON{% endif %}"
      device:
        identifiers: vcontrold
        manufacturer: Viessmann
  sensor:
    - name: "Aussentemperatur"
      unique_id: "vcontroldgetTempA"
      device_class: temperature
      state_topic: "openv/getTempA"
      unit_of_measurement: "°C"
      value_template: |-
        {{ value | round(2) }}
      device:
        identifiers: vcontrold
        manufacturer: Viessmann

  switch:
    - name: "Betriebsart Party"
      unique_id: "vcontroldgetBetriebPartyM1"
      state_topic: "openv/getBetriebPartyM1"
      command_topic: "openv/setBetriebPartyM1"
      device:
        identifiers: vcontrold
        manufacturer: Viessmann
      value_template: | 
        {{ value|round(0) }}
      payload_on: 1
      payload_off: 0
      state_on: 1
      state_off: 0