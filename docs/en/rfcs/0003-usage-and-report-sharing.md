# Why usage recording and report sharing have separate settings

[Design decisions](README.md) · [简体中文](../../zh/rfcs/0003-usage-and-report-sharing.md)

Producing research requires the methods and the research material. New installations start with usage recording off. An explicit opt-in allows supported hosts to install local event hooks. Existing choices keep their effect.

Report text can contain unpublished material. Sharing it requires separate consent. A one-off choice covers one report. Directory permission covers its chosen scope. Revocation clears pending reports within that scope, while siblings follow their own effective permission.

- [Settings, scope and revocation](../../usage-data.md)
- [Loopback verification](https://github.com/rrrrrredy/research-toolkit/blob/main/scripts/check_usage_sharing.py)
