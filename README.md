# BedsteLectio integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]

_Integration to integrate with [BedsteLectio][bedste_lectio]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Shows your next room.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `bedste_lectio`.
1. Download _all_ the files from the `custom_components/bedste_lectio/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "BedsteLectio"

## Configuration

Configuration is done in the UI. You need to provide your username, password and school for BedsteLectio.

You can find your school by logging into Lectio and looking at the URL. It should look something like this:
`https://www.lectio.dk/lectio/<school_id>/forside.aspx`

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[bedste_lectio]: https://bedstelectio.dk
[commits-shield]: https://img.shields.io/github/commit-activity/y/JohnnyJTH/BedsteLectioHA.svg?style=for-the-badge
[commits]: https://github.com/JohnnyJTH/BedsteLectioHA/commits/main
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/JohnnyJTH/BedsteLectioHA.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-JohnnyJTH-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/JohnnyJTH/BedsteLectioHA.svg?style=for-the-badge
[releases]: https://github.com/JohnnyJTH/BedsteLectioHA/releases
