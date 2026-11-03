<p align="center">
  <img src="https://raw.githubusercontent.com/TechSavage1989/network-toolkit/main/assets/Network_Toolkit_Icon.png" width="112" alt="Network Toolkit icon">
</p>

<h1 align="center">Network Toolkit releases (legacy feed)</h1>
<p align="center">The original update feed for Network Toolkit 1.17.x. Current releases are published from the main repository.</p>

<p align="center">
  <a href="https://github.com/TechSavage1989/network-toolkit/releases/latest">Download the current release</a> ·
  <a href="https://github.com/TechSavage1989/network-toolkit">Network Toolkit</a> ·
  <a href="#whats-here">What's here</a> ·
  <a href="#updating-from-117">Updating from 1.17</a>
</p>

## About

This repository distributed compiled Windows updates for **Network Toolkit 1.17.58 to 1.17.63**. It contains no application source code. Newer versions (1.18 and later) are built, released and served as updates from [TechSavage1989/network-toolkit](https://github.com/TechSavage1989/network-toolkit), so new releases no longer appear here.

**For the current version, use [the latest release](https://github.com/TechSavage1989/network-toolkit/releases/latest)** of the main repository.

## What's here

| Path | Contents |
| --- | --- |
| `release.json` | The feed record an installed 1.17.x app reads: version, SHA-256 and the files in the update package (last entry: 1.17.63) |
| `binaries/` | The published 1.17.x update packages |
| `scripts/`, `.github/workflows/` | The automation that published and revised those packages |

Each release on this repository has a binary-only Update ZIP and `SHA256SUMS` for integrity checks. GitHub's automatic "Source code" archives contain only these distribution files and are not update packages. Third-party notices are inside the Update ZIP.

## Updating from 1.17

If you still run a 1.17.x version, download the current release from the main repository's [releases page](https://github.com/TechSavage1989/network-toolkit/releases/latest) and follow its instructions. Downloaded executables may be unsigned; only install downloads you trust, and check them against the published SHA-256 sums.

## Development

This feed is kept unchanged so existing 1.17 installations keep a valid record; don't publish new versions here. The shared repository rules for TechSavage1989 apps are in [network-toolkit's `docs/REPOSITORY_STANDARDS.md`](https://github.com/TechSavage1989/network-toolkit/blob/main/docs/REPOSITORY_STANDARDS.md).
