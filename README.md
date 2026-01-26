# TR-1um_MPW_template

- [Read the documentation for project](docs/info.md)

# TR-1um_MPW actions

The GitHub CI/CD actions will perform the following steps.

**Pre-check**

The pre-check validates that:

- The top cell name matches the entry in info.yaml (top_cell:).

- The top cell name must be unique (not plural).

- The top cell database unit (dbu) must be 0.001um

- The top cell drawing area fits within the range (-1250, -1250) to (1250, 1250).

- The top cell includes one of the OpenSUSI-recommended frame cells OSS_FRAME or OSS_FRAME_TEG.

  
![OpenSUSI MPW](docs/OpenSUSI-MPW.png)

![OpenSUSI MPW](docs/OpenSUSI-MPW-TEG.png)


**DRC**

The DRC stage performs:

- KLayout DRC(Drawing) checks and Antenna checks.

- DRC also check the top cell must preserve open space for corner-reserved areas.

